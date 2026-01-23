import unittest
from dna_storage.file_ops import DNAStorage

class TestAddressing(unittest.TestCase):
    def test_random_access(self):
        # 3 chunks (chunk_size=10). Total 30 bytes.
        data = b'0123456789' * 3
        storage = DNAStorage(chunk_size=10)
        encoded = storage.encode(data)
        
        # Access chunk 1 (middle)
        chunk1 = storage.decode_chunk(encoded, 1)
        self.assertEqual(chunk1, b'0123456789')
        
        # Access chunk 2 (last)
        chunk2 = storage.decode_chunk(encoded, 2)
        self.assertEqual(chunk2, b'0123456789')
        
        # Access chunk 0 (first)
        chunk0 = storage.decode_chunk(encoded, 0)
        self.assertEqual(chunk0, b'0123456789')
        
        # Out of bounds
        with self.assertRaises(IndexError):
            storage.decode_chunk(encoded, 3)

if __name__ == '__main__':
    unittest.main()
