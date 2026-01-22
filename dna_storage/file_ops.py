from .binary_to_dna import bytes_to_binary, binary_to_dna_sequence, dna_sequence_to_binary, binary_to_bytes
from .ecc import ECC
from .metadata import MetadataManager
from .chunking import ChunkManager

class DNAStorage:
    def __init__(self, ecc_method='rs', nsym=10, chunk_size=128):
        self.ecc_method = ecc_method
        self.nsym = nsym
        self.chunk_size = chunk_size
        
    def _encode_body(self, data_bytes):
        """Internal method to encode a single data packet."""
        # Error Correction
        if self.ecc_method == 'rs':
            encoded_bytes = ECC.rs_encode(data_bytes, self.nsym)
            binary = bytes_to_binary(encoded_bytes)
            return binary_to_dna_sequence(binary)
        elif self.ecc_method == 'hamming':
            binary = bytes_to_binary(data_bytes)
            encoded_bits = ECC.hamming_encode(binary)
            return binary_to_dna_sequence(encoded_bits)
        else:
            binary = bytes_to_binary(data_bytes)
            return binary_to_dna_sequence(binary)

    def _decode_body(self, dna_sequence):
        """Internal method to decode a single data packet."""
        binary = dna_sequence_to_binary(dna_sequence)
        
        if self.ecc_method == 'rs':
            data_bytes = binary_to_bytes(binary)
            return ECC.rs_decode(data_bytes, self.nsym)
        elif self.ecc_method == 'hamming':
            decoded_bits = ECC.hamming_decode(binary)
            return binary_to_bytes(decoded_bits)
        else:
            return binary_to_bytes(binary)

    def _calculate_dna_chunk_length(self, packet_size_bytes):
        if self.ecc_method == 'rs':
             return (packet_size_bytes + self.nsym) * 4
        elif self.ecc_method == 'hamming':
             # 1 byte -> 14 bits -> 7 bases
             return packet_size_bytes * 7
        else:
             return packet_size_bytes * 4

    def encode(self, data_bytes):
        """
        Encodes data with chunking and metadata header.
        Structure: [LengthPrefix][HeaderDNA][Chunk1DNA][Chunk2DNA]...
        """
        # 1. Chunk Data
        chunks = ChunkManager.chunk_data(data_bytes, self.chunk_size)
        
        # 2. Encode Chunks
        encoded_chunks = [self._encode_body(chunk) for chunk in chunks]
        body_dna = "".join(encoded_chunks)
        
        # 3. Create Header
        ecc_params = {"nsym": self.nsym} if self.ecc_method == 'rs' else {}
        header_dna = MetadataManager.create_header_dna(
            self.ecc_method, ecc_params, self.chunk_size, len(chunks)
        )
        
        # 4. Create Prefix
        prefix_dna = MetadataManager.encode_length_prefix(len(header_dna))
        
        return prefix_dna + header_dna + body_dna

    def decode(self, dna_sequence):
        """
        Decodes data, parsing header and reassembling chunks.
        """
        # 1. Parse Prefix
        prefix_len = 16 
        if len(dna_sequence) < prefix_len:
            raise ValueError("Data too short to contain header prefix")
            
        prefix_dna = dna_sequence[:prefix_len]
        header_len = MetadataManager.decode_length_prefix(prefix_dna)
        
        # 2. Parse Header
        total_header_end = prefix_len + header_len
        if len(dna_sequence) < total_header_end:
             raise ValueError("Data too short to contain header")
             
        header_dna = dna_sequence[prefix_len:total_header_end]
        metadata = MetadataManager.parse_header_dna(header_dna)
        
        # 3. Configure from Metadata
        self.ecc_method = metadata.get('ecc', 'rs')
        params = metadata.get('ecc_params', {})
        if self.ecc_method == 'rs':
            self.nsym = params.get('nsym', 10)
        self.chunk_size = metadata.get('chunk_size', 128)
        total_chunks = metadata.get('total_chunks', 0)
        
        # 4. Decode Chunks
        body_dna = dna_sequence[total_header_end:]
        
        # Packet size = Header(12) + chunk_size (padded)
        packet_size = 12 + self.chunk_size
        chunk_dna_len = self._calculate_dna_chunk_length(packet_size)
        
        chunks_data = []
        for i in range(total_chunks):
            start = i * chunk_dna_len
            end = start + chunk_dna_len
            
            if end > len(body_dna):
                raise ValueError("Unexpected end of stream (missing chunks)")
            
            chunk_segment = body_dna[start:end]
            packet_bytes = self._decode_body(chunk_segment)
            
            idx, data = ChunkManager.parse_chunk(packet_bytes)
            
            if idx != i:
                raise ValueError(f"Chunk index mismatch. Expected {i}, got {idx}")
                
            chunks_data.append(data)
            
        return b"".join(chunks_data)