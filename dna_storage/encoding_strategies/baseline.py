from .base import EncodingStrategy
from ..binary_to_dna import binary_to_dna_sequence, dna_sequence_to_binary

class BaselineStrategy(EncodingStrategy):
    def encode(self, binary_data):
        return binary_to_dna_sequence(binary_data)
    
    def decode(self, dna_sequence):
        return dna_sequence_to_binary(dna_sequence)
        
    def bits_per_base(self):
        return 2.0
