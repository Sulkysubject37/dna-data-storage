import random

class ErrorInjector:
    @staticmethod
    def inject_bit_flip(data_bytes, error_rate=0.01):
        """
        Flips bits in data_bytes with probability error_rate per bit.
        RETURNS new bytes.
        """
        if error_rate <= 0:
            return data_bytes
            
        data = bytearray(data_bytes)
        # Iterate over bytes for efficiency, then bits?
        # Or iterate all bits? For simulation, we can be slow.
        # Let's iterate bytes and check if we need to flip anything.
        
        # Optimization: geometric distribution for next error?
        # For simplicity, just iterate bytes.
        
        for i in range(len(data)):
            byte = data[i]
            for bit in range(8):
                if random.random() < error_rate:
                    byte ^= (1 << bit)
            data[i] = byte
            
        return bytes(data)

    @staticmethod
    def inject_dna_substitution(dna_sequence, error_rate=0.01):
        """
        Substitutes bases in DNA sequence with probability error_rate per base.
        RETURNS new string.
        """
        if error_rate <= 0:
            return dna_sequence
            
        bases = list(dna_sequence)
        options = ['A', 'C', 'G', 'T']
        
        for i in range(len(bases)):
            if random.random() < error_rate:
                current = bases[i]
                # Pick a different base
                possible = [b for b in options if b != current]
                bases[i] = random.choice(possible)
                
        return "".join(bases)
