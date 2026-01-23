from ..chunking import ChunkManager
import math

class AddressIndexer:
    def __init__(self, chunk_size, ecc_method, ecc_params, bits_per_base=2.0):
        self.chunk_size = chunk_size
        self.ecc_method = ecc_method
        self.ecc_params = ecc_params
        self.bits_per_base = bits_per_base
        
    def calculate_chunk_dna_length(self):
        packet_size = ChunkManager.HEADER_SIZE + self.chunk_size
        
        # Calculate BITS of encoded packet
        if self.ecc_method == 'rs':
             nsym = self.ecc_params.get('nsym', 10)
             bytes_len = packet_size + nsym
             bits = bytes_len * 8
        elif self.ecc_method == 'hamming':
             # 1 byte input -> 14 bits output
             bits = packet_size * 14
        else:
             bits = packet_size * 8
             
        # Bits -> DNA bases
        return math.ceil(bits / self.bits_per_base)

    def get_chunk_range(self, chunk_index, header_offset):
        """
        Returns (start, end) in DNA sequence for the given chunk index.
        header_offset: End of the file header (where body starts).
        """
        chunk_len = self.calculate_chunk_dna_length()
        start = header_offset + (chunk_index * chunk_len)
        end = start + chunk_len
        return start, end