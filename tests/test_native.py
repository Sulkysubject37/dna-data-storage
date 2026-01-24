import unittest
from dna_storage.file_ops import DNAStorage, CPP_AVAILABLE

@unittest.skipUnless(CPP_AVAILABLE, "C++ extension not available")
class TestNativeCore(unittest.TestCase):
    def test_hamming_native(self):
        data = b'Native Test'
        storage = DNAStorage(ecc_method='hamming', backend='cpp')
        encoded = storage.encode(data)
        decoded = storage.decode(encoded)
        self.assertEqual(decoded, data)
        self.assertEqual(storage.backend, 'cpp')
        
    def test_baseline_native(self):
        # RS uses C++ mapping if backend=cpp
        data = b'Native RS'
        storage = DNAStorage(ecc_method='rs', backend='cpp')
        encoded = storage.encode(data)
        decoded = storage.decode(encoded)
        self.assertEqual(decoded, data)
        self.assertEqual(storage.backend, 'cpp')

if __name__ == '__main__':
    unittest.main()
