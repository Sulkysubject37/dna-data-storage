from .binary_to_dna import bytes_to_binary, binary_to_dna_sequence, dna_sequence_to_binary, binary_to_bytes
from .ecc import ECC
from .metadata import MetadataManager
from .chunking import ChunkManager
from .constraints import ConstraintValidator
from .addressing import AddressIndexer
from .encoding_strategies import get_strategy

try:
    from .native import dna_native
    CPP_AVAILABLE = True
except ImportError:
    CPP_AVAILABLE = False

class DNAStorage:
    def __init__(self, ecc_method='rs', nsym=10, chunk_size=128, constraints=None, encoding='baseline', backend='python'):
        self.ecc_method = ecc_method
        self.nsym = nsym
        self.chunk_size = chunk_size
        self.constraints = constraints or {}
        self.encoding_name = encoding
        self.strategy = get_strategy(encoding)
        self.backend = backend
        
        if backend == 'cpp' and not CPP_AVAILABLE:
            print("Warning: C++ backend requested but not available. Falling back to Python.")
            self.backend = 'python'
        
    def _encode_body(self, data_bytes):
        """Internal method to encode a single data packet."""
        # C++ Fast Path
        if self.backend == 'cpp' and self.encoding_name == 'baseline':
            if self.ecc_method == 'hamming':
                return dna_native.hamming_encode_dna(data_bytes)
            elif self.ecc_method == 'rs':
                encoded_bytes = ECC.rs_encode(data_bytes, self.nsym)
                # reedsolo returns bytearray
                if isinstance(encoded_bytes, bytearray):
                    encoded_bytes = bytes(encoded_bytes)
                return dna_native.binary_to_dna(encoded_bytes)
            else:
                return dna_native.binary_to_dna(data_bytes)
        
        # Python Path
        if self.ecc_method == 'rs':
            encoded_bytes = ECC.rs_encode(data_bytes, self.nsym)
            binary = bytes_to_binary(encoded_bytes)
        elif self.ecc_method == 'hamming':
            binary = bytes_to_binary(data_bytes)
            encoded_bits = ECC.hamming_encode(binary)
            binary = encoded_bits
        else:
            binary = bytes_to_binary(data_bytes)
            
        return self.strategy.encode(binary)

    def _decode_body(self, dna_sequence):
        """Internal method to decode a single data packet."""
        # C++ Fast Path
        if self.backend == 'cpp' and self.encoding_name == 'baseline':
            if self.ecc_method == 'hamming':
                res = dna_native.hamming_decode_dna(dna_sequence)
                return res.data
            elif self.ecc_method == 'rs':
                data_bytes = dna_native.dna_to_binary(dna_sequence)
                return ECC.rs_decode(data_bytes, self.nsym)
            else:
                return dna_native.dna_to_binary(dna_sequence)

        # Python Path
        binary = self.strategy.decode(dna_sequence)
        
        if self.ecc_method == 'rs':
            data_bytes = binary_to_bytes(binary)
            return ECC.rs_decode(data_bytes, self.nsym)
        elif self.ecc_method == 'hamming':
            decoded_bits = ECC.hamming_decode(binary)
            return binary_to_bytes(decoded_bits)
        else:
            return binary_to_bytes(binary)

    def _parse_header_and_configure(self, dna_sequence):
        prefix_len = 16 
        if len(dna_sequence) < prefix_len:
            raise ValueError("Data too short to contain header prefix")
        prefix_dna = dna_sequence[:prefix_len]
        header_len = MetadataManager.decode_length_prefix(prefix_dna)
        
        total_header_end = prefix_len + header_len
        if len(dna_sequence) < total_header_end:
             raise ValueError("Data too short to contain header")
             
        header_dna = dna_sequence[prefix_len:total_header_end]
        metadata = MetadataManager.parse_header_dna(header_dna)
        
        self.ecc_method = metadata.get('ecc', 'rs')
        params = metadata.get('ecc_params', {})
        if self.ecc_method == 'rs':
            self.nsym = params.get('nsym', 10)
        self.chunk_size = metadata.get('chunk_size', 128)
        self.constraints = metadata.get('constraints', {})
        self.encoding_name = metadata.get('encoding', 'baseline')
        self.strategy = get_strategy(self.encoding_name)
        
        return total_header_end, metadata

    def encode(self, data_bytes):
        # 1. Chunk Data
        chunks = ChunkManager.chunk_data(data_bytes, self.chunk_size)
        
        encoded_chunks_dna = []
        for chunk in chunks:
            nonce = 0
            while True:
                if nonce > 0:
                    idx, payload, length, _ = ChunkManager.unpack_chunk_components(chunk)
                    chunk = ChunkManager.pack_chunk(idx, payload, length, nonce)
                
                dna = self._encode_body(chunk)
                
                # Check Constraints
                valid = True
                if self.constraints:
                    if 'min_gc' in self.constraints:
                        min_gc = self.constraints.get('min_gc')
                        max_gc = self.constraints.get('max_gc', 0.6)
                        if not ConstraintValidator.validate_gc_content(dna, min_gc, max_gc):
                            valid = False
                    if valid and 'max_homopolymer' in self.constraints:
                        max_hp = self.constraints.get('max_homopolymer', 3)
                        if not ConstraintValidator.validate_homopolymers(dna, max_hp):
                            valid = False
                
                if valid:
                    encoded_chunks_dna.append(dna)
                    break
                
                nonce += 1
                if nonce > 1000:
                    raise RuntimeError("Failed to satisfy constraints after 1000 attempts")
        
        body_dna = "".join(encoded_chunks_dna)
        
        # 3. Create Header
        ecc_params = {"nsym": self.nsym} if self.ecc_method == 'rs' else {}
        header_dna = MetadataManager.create_header_dna(
            self.ecc_method, ecc_params, self.chunk_size, len(chunks), 
            self.constraints, self.encoding_name
        )
        
        # 4. Create Prefix
        prefix_dna = MetadataManager.encode_length_prefix(len(header_dna))
        
        return prefix_dna + header_dna + body_dna

    def decode(self, dna_sequence):
        total_header_end, metadata = self._parse_header_and_configure(dna_sequence)
        total_chunks = metadata.get('total_chunks', 0)
        
        indexer = AddressIndexer(self.chunk_size, self.ecc_method, {"nsym": self.nsym}, self.strategy.bits_per_base())
        
        chunks_data = []
        for i in range(total_chunks):
            start, end = indexer.get_chunk_range(i, total_header_end)
            if end > len(dna_sequence):
                raise ValueError("Unexpected end of stream (missing chunks)")
            
            chunk_segment = dna_sequence[start:end]
            packet_bytes = self._decode_body(chunk_segment)
            
            idx, data, nonce = ChunkManager.parse_chunk(packet_bytes)
            
            if idx != i:
                raise ValueError(f"Chunk index mismatch. Expected {i}, got {idx}")
                
            chunks_data.append(data)
            
        return b"".join(chunks_data)

    def decode_chunk(self, dna_sequence, chunk_index):
        total_header_end, metadata = self._parse_header_and_configure(dna_sequence)
        total_chunks = metadata.get('total_chunks', 0)
        
        if chunk_index < 0 or chunk_index >= total_chunks:
            raise IndexError("Chunk index out of bounds")
            
        indexer = AddressIndexer(self.chunk_size, self.ecc_method, {"nsym": self.nsym}, self.strategy.bits_per_base())
        start, end = indexer.get_chunk_range(chunk_index, total_header_end)
        
        if end > len(dna_sequence):
            raise ValueError("Chunk data incomplete or missing")
            
        chunk_segment = dna_sequence[start:end]
        packet_bytes = self._decode_body(chunk_segment)
        idx, data, nonce = ChunkManager.parse_chunk(packet_bytes)
        
        if idx != chunk_index:
             raise ValueError("Index mismatch in random access")
             
        return data
