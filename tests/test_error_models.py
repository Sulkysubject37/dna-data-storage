import unittest
from dna_storage.error_models import SubstitutionModel, IndelModel, BurstErrorModel

class TestErrorModels(unittest.TestCase):
    def test_substitution(self):
        dna = "A" * 100
        model = SubstitutionModel(rate=0.5)
        corrupted = model.apply(dna)
        self.assertEqual(len(corrupted), 100)
        # It's statistically nearly impossible to match exactly with rate 0.5
        self.assertNotEqual(corrupted, dna)

    def test_indel(self):
        dna = "A" * 100
        # High delete rate, low insert
        model = IndelModel(insert_rate=0.0, delete_rate=0.5)
        corrupted = model.apply(dna)
        self.assertLess(len(corrupted), 100)
        
        # High insert rate
        model2 = IndelModel(insert_rate=0.5, delete_rate=0.0)
        corrupted2 = model2.apply(dna)
        self.assertGreater(len(corrupted2), 100)

    def test_burst(self):
        dna = "A" * 100
        model = BurstErrorModel(burst_prob=1.0, min_len=5, max_len=5)
        corrupted = model.apply(dna)
        self.assertEqual(len(corrupted), 100)
        self.assertNotEqual(corrupted, dna)
        
if __name__ == '__main__':
    unittest.main()
