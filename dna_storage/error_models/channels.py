import random
from .base import ErrorModel

class SubstitutionModel(ErrorModel):
    def __init__(self, rate=0.01):
        self.rate = rate
    
    def apply(self, dna_sequence):
        if self.rate <= 0:
            return dna_sequence
        bases = list(dna_sequence)
        options = ['A', 'C', 'G', 'T']
        for i in range(len(bases)):
            if random.random() < self.rate:
                current = bases[i]
                possible = [b for b in options if b != current]
                bases[i] = random.choice(possible)
        return "".join(bases)

class IndelModel(ErrorModel):
    def __init__(self, insert_rate=0.005, delete_rate=0.005):
        self.insert_rate = insert_rate
        self.delete_rate = delete_rate

    def apply(self, dna_sequence):
        if self.insert_rate <= 0 and self.delete_rate <= 0:
            return dna_sequence
            
        result = []
        bases = ['A', 'C', 'G', 'T']
        for base in dna_sequence:
            r = random.random()
            if r < self.delete_rate:
                continue # Skip (Deletion)
            elif r < self.delete_rate + self.insert_rate:
                result.append(base)
                # Insertion (random base)
                result.append(random.choice(bases))
            else:
                result.append(base)
        return "".join(result)

class BurstErrorModel(ErrorModel):
    def __init__(self, burst_prob=0.001, min_len=2, max_len=5):
        self.burst_prob = burst_prob
        self.min_len = min_len
        self.max_len = max_len

    def apply(self, dna_sequence):
        # Apply bursts of substitutions
        bases = list(dna_sequence)
        options = ['A', 'C', 'G', 'T']
        i = 0
        while i < len(bases):
            if random.random() < self.burst_prob:
                burst_len = random.randint(self.min_len, self.max_len)
                for j in range(burst_len):
                    if i + j < len(bases):
                        current = bases[i+j]
                        possible = [b for b in options if b != current]
                        bases[i+j] = random.choice(possible)
                i += burst_len
            else:
                i += 1
        return "".join(bases)
