import math
from .base import EncodingStrategy

class RotatingStrategy(EncodingStrategy):
    BASES = ['A', 'C', 'G', 'T']
    
    def encode(self, binary_data):
        if not binary_data:
            return ""
        
        # Calculate fixed length to ensure random access works
        L = len(binary_data)
        # We encode '1' + binary. Total bits = L + 1.
        # Max value < 2^(L+1).
        # Trits needed = ceil((L + 1) * log(2) / log(3))
        num_trits = math.ceil((L + 1) * math.log(2) / math.log(3))
        
        val = int('1' + binary_data, 2)
        
        trits = []
        while val > 0:
            trits.append(val % 3)
            val //= 3
            
        # Pad with leading zeros to meet fixed length
        while len(trits) < num_trits:
            trits.append(0)
            
        trits.reverse()
        
        dna = []
        prev_idx = 0 # Assume previous was A (index 0) implied
        
        for t in trits:
            idx = (prev_idx + 1 + t) % 4
            dna.append(self.BASES[idx])
            prev_idx = idx
            
        return "".join(dna)

    def decode(self, dna_sequence):
        if not dna_sequence:
            return ""
            
        trits = []
        prev_idx = 0
        base_map = {b: i for i, b in enumerate(self.BASES)}
        
        for base in dna_sequence:
            curr_idx = base_map[base]
            # Reverse: t = (curr - prev - 1) % 4
            t = (curr_idx - prev_idx - 1) % 4
            trits.append(t)
            prev_idx = curr_idx
            
        val = 0
        for t in trits:
            val = val * 3 + t
            
        bin_str = bin(val)[2:]
        return bin_str[1:] # Remove leading '1'

    def bits_per_base(self):
        return 1.58496