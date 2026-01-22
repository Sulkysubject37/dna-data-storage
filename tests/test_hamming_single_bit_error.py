import unittest
from dna_storage.ecc.hamming import hamming_encode, hamming_decode

class TestHammingSingleBitError(unittest.TestCase):
    def test_single_bit_correction(self):
        # 4 bits: 1010
        data = [1, 0, 1, 0]
        encoded = hamming_encode(data)
        # Hamming(7,4) block length is 7
        self.assertEqual(len(encoded), 7)
        
        # Introduce error at index 2 (arbitrary)
        encoded[2] ^= 1 
        
        decoded, corrected = hamming_decode(encoded)
        
        self.assertEqual(decoded, data)
        self.assertTrue(corrected)

if __name__ == '__main__':
    unittest.main()
