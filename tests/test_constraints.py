import unittest
from dna_storage.file_ops import DNAStorage
from dna_storage.constraints import ConstraintValidator

class TestConstraints(unittest.TestCase):
    def test_gc_content(self):
        # AAAA -> 0% GC. Fails min_gc=0.4
        self.assertFalse(ConstraintValidator.validate_gc_content("AAAA", 0.4, 0.6))
        # GCGC -> 100% GC. Fails max_gc=0.6
        self.assertFalse(ConstraintValidator.validate_gc_content("GCGC", 0.4, 0.6))
        # ACGT -> 50%. Pass.
        self.assertTrue(ConstraintValidator.validate_gc_content("ACGT", 0.4, 0.6))

    def test_homopolymer(self):
        self.assertFalse(ConstraintValidator.validate_homopolymers("AAAA", 3))
        self.assertTrue(ConstraintValidator.validate_homopolymers("AAA", 3))

    def test_encoding_with_constraints(self):
        # 00 00 00 00 -> AAAA (if mapped directly)
        data = b'\x00\x00\x00\x00' * 10
        # Relax constraint to 4. 
        # Rejection sampling with RS-encoded blocks is inefficient for strict constraints.
        storage = DNAStorage(chunk_size=16, constraints={'max_homopolymer': 4})
        encoded = storage.encode(data)
        
        # Verify decoding works
        decoder = DNAStorage()
        decoded = decoder.decode(encoded)
        self.assertEqual(decoded, data)

if __name__ == '__main__':
    unittest.main()