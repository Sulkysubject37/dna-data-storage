from .base import EncodingStrategy

class RotatingStrategy(EncodingStrategy):
    BASES = ['A', 'C', 'G', 'T']
    
    def encode(self, binary_data):
        if not binary_data:
            return ""
        
        # Preserve length by prepending '1'
        val = int('1' + binary_data, 2)
        
        trits = []
        while val > 0:
            trits.append(val % 3)
            val //= 3
        trits.reverse()
        
        dna = []
        prev_idx = 0 # Assume previous was A (index 0) implied
        
        for t in trits:
            # t is 0, 1, 2.
            # 0 -> +1 offset (A->C)
            # 1 -> +2 offset (A->G)
            # 2 -> +3 offset (A->T)
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
