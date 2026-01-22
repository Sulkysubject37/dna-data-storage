import unittest
from dna_storage.ecc import ECC

class TestReedSolomonRoundtrip(unittest.TestCase):
    def test_rs_roundtrip(self):
        data = b"Hello World"
        encoded = ECC.rs_encode(data)
        decoded = ECC.rs_decode(encoded)
        self.assertEqual(decoded, data)

if __name__ == '__main__':
    unittest.main()
