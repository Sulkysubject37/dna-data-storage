import struct
import zlib
import random
from ..failures import DNAStorageError, FailureType

class ChunkManager:
    HEADER_FORMAT = "!IIII" # Index (4), Length (4), Checksum (4), Nonce (4)
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    
    # Fixed mask to whiten header (break homopolymers in Index/Length)
    HEADER_MASK = b'd\x1d\x8c\xd9\x8f\x00\xb2\x04\xe9\x80\t\x98\xec\xf8B~'

    @staticmethod
    def _apply_scramble(data, nonce):
        if nonce == 0:
            return data
        rng = random.Random(nonce)
        mask = rng.randbytes(len(data))
        return bytes(a ^ b for a, b in zip(data, mask))

    @staticmethod
    def _apply_header_mask(header):
        return bytes(a ^ b for a, b in zip(header, ChunkManager.HEADER_MASK))

    @staticmethod
    def pack_chunk(index, payload, actual_len, nonce=0):
        """
        Packs a chunk into a packet with header.
        payload: The raw data (potentially padded).
        actual_len: The length of valid data in payload.
        """
        scrambled_payload = ChunkManager._apply_scramble(payload, nonce)
        checksum = zlib.crc32(scrambled_payload)
        header = struct.pack(ChunkManager.HEADER_FORMAT, index, actual_len, checksum, nonce)
        
        # Whiten header
        masked_header = ChunkManager._apply_header_mask(header)
        
        return masked_header + scrambled_payload

    @staticmethod
    def unpack_chunk_components(packet_bytes):
        """
        Extracts components from a packet for inspection or repacking.
        Returns: (index, raw_payload, actual_len, nonce)
        """
        if len(packet_bytes) < ChunkManager.HEADER_SIZE:
             raise ValueError("Packet too small")
             
        masked_header = packet_bytes[:ChunkManager.HEADER_SIZE]
        header_bytes = ChunkManager._apply_header_mask(masked_header)
        
        index, length, checksum, nonce = struct.unpack(ChunkManager.HEADER_FORMAT, header_bytes)
        payload = packet_bytes[ChunkManager.HEADER_SIZE:]
        
        unscrambled = ChunkManager._apply_scramble(payload, nonce)
        return index, unscrambled, length, nonce

    @staticmethod
    def chunk_data(data, chunk_size=128):
        """
        Splits data into packets.
        Each packet is: [Index][Length][Checksum][Nonce][Data + Padding]
        """
        chunks = []
        total_len = len(data)
        
        for i, offset in enumerate(range(0, total_len, chunk_size)):
            chunk_data = data[offset:offset + chunk_size]
            actual_len = len(chunk_data)
            
            # Pad if necessary
            if actual_len < chunk_size:
                padding = b'\x00' * (chunk_size - actual_len)
                payload = chunk_data + padding
            else:
                payload = chunk_data
                
            packet = ChunkManager.pack_chunk(i, payload, actual_len, nonce=0)
            chunks.append(packet)
            
        return chunks

    @staticmethod
    def parse_chunk(packet_bytes):
        """
        Parses a packet bytes into (index, data, nonce).
        Validates checksum.
        """
        if len(packet_bytes) < ChunkManager.HEADER_SIZE:
             raise ValueError("Packet too small")
             
        masked_header = packet_bytes[:ChunkManager.HEADER_SIZE]
        header_bytes = ChunkManager._apply_header_mask(masked_header)
        
        index, length, checksum, nonce = struct.unpack(ChunkManager.HEADER_FORMAT, header_bytes)
        
        payload = packet_bytes[ChunkManager.HEADER_SIZE:]
        
        if zlib.crc32(payload) != checksum:
            raise DNAStorageError(f"Checksum mismatch in chunk {index}", FailureType.CORRUPTION_DETECTED)
            
        unscrambled = ChunkManager._apply_scramble(payload, nonce)
        return index, unscrambled[:length], nonce
