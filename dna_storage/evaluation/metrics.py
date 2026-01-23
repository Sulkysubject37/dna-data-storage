def calculate_overhead(data_size, dna_bases):
    """
    Calculates encoding overhead relative to theoretical maximum (2 bits/base).
    1 byte = 8 bits = 4 bases (Theoretical Min).
    """
    if data_size == 0:
        return 0.0
    theoretical_bases = data_size * 4
    return (dna_bases - theoretical_bases) / theoretical_bases

def sequence_stats(dna):
    if not dna:
        return {"gc": 0.0, "max_homopolymer": 0}
        
    gc = (dna.count('G') + dna.count('C')) / len(dna)
    
    max_run = 0
    curr = 1
    for i in range(1, len(dna)):
        if dna[i] == dna[i-1]:
            curr += 1
        else:
            max_run = max(max_run, curr)
            curr = 1
    max_run = max(max_run, curr)
    
    return {"gc": gc, "max_homopolymer": max_run}
