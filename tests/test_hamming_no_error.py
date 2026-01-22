import unittest
from dna_storage.ecc.hamming import hamming_encode, hamming_decode

class TestHammingNoError(unittest.TestCase):
    def test_basic_roundtrip(self):
        # Data: 0000, 1111, 1010, 0101
        data = [0,0,0,0, 1,1,1,1, 1,0,1,0, 0,1,0,1]
        encoded = hamming_encode(data)
        decoded, corrected = hamming_decode(encoded)
        
        self.assertEqual(decoded, data)
        self.assertFalse(corrected)

if __name__ == '__main__':
    unittest.main()
