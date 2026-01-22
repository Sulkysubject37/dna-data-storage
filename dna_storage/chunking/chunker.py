import struct
import zlib

class ChunkManager:
    HEADER_FORMAT = "!III" # Index (4), Length (4), Checksum (4)
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    
    @staticmethod
    def chunk_data(data, chunk_size=128):
        """
        Splits data into packets.
        Each packet is: [Index][Length][Checksum][Data + Padding]
        Total packet size = 12 + chunk_size
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
                
            checksum = zlib.crc32(payload)
            # Pack header
            header = struct.pack(ChunkManager.HEADER_FORMAT, i, actual_len, checksum)
            
            chunks.append(header + payload)
            
        return chunks

    @staticmethod
    def parse_chunk(packet_bytes):
        """
        Parses a packet bytes into (index, data).
        Validates checksum.
        """
        if len(packet_bytes) < ChunkManager.HEADER_SIZE:
             raise ValueError("Packet too small")
             
        header_bytes = packet_bytes[:ChunkManager.HEADER_SIZE]
        index, length, checksum = struct.unpack(ChunkManager.HEADER_FORMAT, header_bytes)
        
        payload = packet_bytes[ChunkManager.HEADER_SIZE:]
        
        if zlib.crc32(payload) != checksum:
            raise ValueError(f"Checksum mismatch in chunk {index}")
            
        return index, payload[:length]
