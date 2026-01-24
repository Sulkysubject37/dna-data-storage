import unittest
from dna_storage.file_ops import DNAStorage
from dna_storage.addressing import AddressIndexer

class TestRobustness(unittest.TestCase):
    def test_missing_chunk_detection(self):
        # 3 chunks
        data = b'A' * 128 * 3 
        storage = DNAStorage(chunk_size=128, ecc_method='rs', nsym=10)
        encoded = storage.encode(data)
        
        # Get header offset
        offset, _ = storage._parse_header_and_configure(encoded)
        
        indexer = AddressIndexer(128, 'rs', {'nsym': 10})
        chunk_len = indexer.calculate_chunk_dna_length()
        
        # Remove 2nd chunk (index 1)
        # Sequence: [Header] [Chunk 0] [Chunk 1] [Chunk 2]
        # New:      [Header] [Chunk 0] [Chunk 2]
        corrupted = encoded[:offset + chunk_len] + encoded[offset + 2*chunk_len:]
        
        # Decode expects Chunk 1 at position 1, but finds Chunk 2 (Index 2).
        with self.assertRaisesRegex(ValueError, "Chunk index mismatch"):
            storage.decode(corrupted)

    def test_bit_flip_recovery(self):
        data = b'Test' * 10
        storage = DNAStorage(ecc_method='hamming', backend='python') # Use python backend to ensure we can flip easily?
        # Backend doesn't matter for logic.
        encoded = storage.encode(data)
        
        # Flip a base in the middle of the body
        # Need to find body start
        offset, _ = storage._parse_header_and_configure(encoded)
        body = list(encoded)
        
        # Flip base at offset + 10
        orig = body[offset + 10]
        body[offset + 10] = 'A' if orig != 'A' else 'T'
        corrupted = "".join(body)
        
        # Hamming should correct single error
        decoded = storage.decode(corrupted)
        self.assertEqual(decoded, data)

if __name__ == '__main__':
    unittest.main()
