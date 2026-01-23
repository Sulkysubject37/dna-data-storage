class ConstraintValidator:
    @staticmethod
    def validate_gc_content(dna_sequence, min_gc=0.4, max_gc=0.6):
        """
        Checks if GC content is within [min_gc, max_gc].
        """
        if not dna_sequence:
            return True
        gc_count = dna_sequence.count('G') + dna_sequence.count('C')
        gc_ratio = gc_count / len(dna_sequence)
        return min_gc <= gc_ratio <= max_gc

    @staticmethod
    def validate_homopolymers(dna_sequence, max_run=3):
        """
        Checks if no homopolymer run exceeds max_run.
        """
        if not dna_sequence:
            return True
        current_run = 1
        for i in range(1, len(dna_sequence)):
            if dna_sequence[i] == dna_sequence[i-1]:
                current_run += 1
                if current_run > max_run:
                    return False
            else:
                current_run = 1
        return True
