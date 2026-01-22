import unittest
from dna_storage.file_ops import DNAStorage

class TestFullRoundtrip(unittest.TestCase):
    def test_rs_roundtrip_with_header(self):
        storage = DNAStorage(ecc_method='rs', nsym=10)
        data = b"Hello DNA Storage!"
        encoded_dna = storage.encode(data)
        
        # Create a fresh storage to simulate decoding without prior knowledge
        decoder = DNAStorage() 
        decoded_data = decoder.decode(encoded_dna)
        
        self.assertEqual(decoded_data, data)
        # Verify decoder picked up the right settings
        self.assertEqual(decoder.ecc_method, 'rs')
        self.assertEqual(decoder.nsym, 10)

    def test_hamming_roundtrip_with_header(self):
        storage = DNAStorage(ecc_method='hamming')
        data = b"Hamming Test"
        encoded_dna = storage.encode(data)
        
        decoder = DNAStorage()
        decoded_data = decoder.decode(encoded_dna)
        
        self.assertEqual(decoded_data, data)
        self.assertEqual(decoder.ecc_method, 'hamming')

if __name__ == '__main__':
    unittest.main()
