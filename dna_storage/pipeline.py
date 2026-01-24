from .file_ops import DNAStorage
from .chunking import ChunkManager
from .metadata import MetadataManager
from .addressing import AddressIndexer
from .encoding_strategies import get_strategy
import math

class StreamPipeline:
    def __init__(self, storage):
        self.storage = storage

    def encode_stream(self, in_stream, out_stream, file_size=None):
        chunk_size = self.storage.chunk_size
        
        if file_size is None:
            try:
                pos = in_stream.tell()
                in_stream.seek(0, 2)
                file_size = in_stream.tell()
                in_stream.seek(pos)
            except:
                raise ValueError("file_size must be provided for non-seekable streams")

        total_chunks = math.ceil(file_size / chunk_size) if file_size > 0 else 0
        
        # 1. Write Prefix + Header
        ecc_params = {"nsym": self.storage.nsym} if self.storage.ecc_method == 'rs' else {}
        header_dna = MetadataManager.create_header_dna(
            self.storage.ecc_method, ecc_params, chunk_size, total_chunks,
            self.storage.constraints, self.storage.encoding_name
        )
        prefix_dna = MetadataManager.encode_length_prefix(len(header_dna))
        
        out_stream.write(prefix_dna)
        out_stream.write(header_dna)
        
        # 2. Stream Chunks
        idx = 0
        while True:
            data = in_stream.read(chunk_size)
            if not data:
                break
            
            actual_len = len(data)
            if actual_len < chunk_size:
                padding = b'\x00' * (chunk_size - actual_len)
                payload = data + padding
            else:
                payload = data
            
            chunk = ChunkManager.pack_chunk(idx, payload, actual_len, nonce=0)
            
            # Encode with constraints
            dna = self.storage.encode_packet_with_constraints(chunk)
            
            out_stream.write(dna)
            idx += 1
            
    def decode_stream(self, in_stream, out_stream):
        # 1. Read Prefix
        prefix_len = 16
        prefix_dna = in_stream.read(prefix_len)
        if len(prefix_dna) < prefix_len:
            raise ValueError("Stream too short for prefix")
            
        header_len = MetadataManager.decode_length_prefix(prefix_dna)
        
        # 2. Read Header
        header_dna = in_stream.read(header_len)
        if len(header_dna) < header_len:
            raise ValueError("Stream too short for header")
            
        metadata = MetadataManager.parse_header_dna(header_dna)
        
        # Configure storage
        self.storage.ecc_method = metadata.get('ecc', 'rs')
        params = metadata.get('ecc_params', {})
        if self.storage.ecc_method == 'rs':
            self.storage.nsym = params.get('nsym', 10)
        self.storage.chunk_size = metadata.get('chunk_size', 128)
        self.storage.constraints = metadata.get('constraints', {})
        self.storage.encoding_name = metadata.get('encoding', 'baseline')
        self.storage.strategy = get_strategy(self.storage.encoding_name)
        
        total_chunks = metadata.get('total_chunks', 0)
        
        indexer = AddressIndexer(
            self.storage.chunk_size, self.storage.ecc_method, 
            {"nsym": self.storage.nsym}, self.storage.strategy.bits_per_base()
        )
        chunk_len = indexer.calculate_chunk_dna_length()
        
        # 3. Stream Chunks
        for i in range(total_chunks):
            chunk_dna = in_stream.read(chunk_len)
            if len(chunk_dna) < chunk_len:
                raise ValueError(f"Stream truncated at chunk {i}")
            
            packet_bytes = self.storage.decode_packet(chunk_dna)
            idx, data, nonce = ChunkManager.parse_chunk(packet_bytes)
            
            if idx != i:
                raise ValueError(f"Index mismatch: {idx} != {i}")
                
            out_stream.write(data)
