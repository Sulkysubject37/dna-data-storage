import unittest
from dna_storage.file_ops import DNAStorage
from dna_storage.encoding_strategies import RotatingStrategy

class TestStrategies(unittest.TestCase):
    def test_rotating_strategy_logic(self):
        strategy = RotatingStrategy()
        data = "010101" 
        # Manual calc verified in reasoning: GTAGA
        encoded = strategy.encode(data)
        self.assertEqual(encoded, "GTAGA")
        
        decoded = strategy.decode(encoded)
        self.assertEqual(decoded, data)
        
    def test_rotating_integration(self):
        storage = DNAStorage(encoding='rotating')
        data = b'Hello Rotating World'
        encoded = storage.encode(data)
        decoded = storage.decode(encoded)
        self.assertEqual(decoded, data)
        self.assertEqual(storage.encoding_name, 'rotating')

if __name__ == '__main__':
    unittest.main()
