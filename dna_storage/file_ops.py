from .binary_to_dna import bytes_to_binary, binary_to_dna_sequence, dna_sequence_to_binary, binary_to_bytes
from .ecc import ECC

class DNAStorage:
    def __init__(self, ecc_method='rs', nsym=10):
        self.ecc_method = ecc_method
        self.nsym = nsym
        
    def encode(self, data_bytes):
        # Error Correction
        if self.ecc_method == 'rs':
            encoded_bytes = ECC.rs_encode(data_bytes, self.nsym)
        elif self.ecc_method == 'hamming':
            binary = bytes_to_binary(data_bytes)
            encoded_bits = ECC.hamming_encode(binary)
            return binary_to_dna_sequence(encoded_bits)
        else:
            encoded_bytes = data_bytes
        
        # Convert to DNA
        binary = bytes_to_binary(encoded_bytes)
        return binary_to_dna_sequence(binary)

    def decode(self, dna_sequence):
        binary = dna_sequence_to_binary(dna_sequence)
        data_bytes = binary_to_bytes(binary)
        
        # Error Correction
        if self.ecc_method == 'rs':
            return ECC.rs_decode(data_bytes, self.nsym)
        elif self.ecc_method == 'hamming':
            decoded_bits = ECC.hamming_decode(binary)
            return binary_to_bytes(decoded_bits)
        return data_bytes