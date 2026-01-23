from ..chunking import ChunkManager

class AddressIndexer:
    def __init__(self, chunk_size, ecc_method, ecc_params):
        self.chunk_size = chunk_size
        self.ecc_method = ecc_method
        self.ecc_params = ecc_params
        
    def calculate_chunk_dna_length(self):
        packet_size = ChunkManager.HEADER_SIZE + self.chunk_size
        
        if self.ecc_method == 'rs':
             nsym = self.ecc_params.get('nsym', 10)
             return (packet_size + nsym) * 4
        elif self.ecc_method == 'hamming':
             return packet_size * 7
        else:
             return packet_size * 4

    def get_chunk_range(self, chunk_index, header_offset):
        """
        Returns (start, end) in DNA sequence for the given chunk index.
        header_offset: End of the file header (where body starts).
        """
        chunk_len = self.calculate_chunk_dna_length()
        start = header_offset + (chunk_index * chunk_len)
        end = start + chunk_len
        return start, end
