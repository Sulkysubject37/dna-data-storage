import unittest
from dna_storage.ecc.hamming import hamming_encode, hamming_decode

class TestHammingFailure(unittest.TestCase):
    def test_double_bit_error_aliasing(self):
        # 4 bits: 1010
        data = [1, 0, 1, 0]
        encoded = hamming_encode(data)
        
        # Introduce 2 bit errors
        # Hamming distance is 3. 
        # 2 errors will result in a state that is distance 1 from another codeword.
        # The decoder will "correct" it to that other codeword.
        if len(encoded) >= 4:
            encoded[2] ^= 1
            encoded[3] ^= 1
        
        decoded, corrected = hamming_decode(encoded)
        
        # The decoded data should NOT match original
        self.assertNotEqual(decoded, data)
        
        # The decoder might report "corrected" (True) because it found a syndrome != 0
        # and flipped a bit to reach a valid codeword.
        # This confirms the limitation: it mis-corrects.

if __name__ == '__main__':
    unittest.main()
