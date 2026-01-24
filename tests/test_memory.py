import unittest
try:
    from dna_storage.native import dna_native
    CPP_AVAILABLE = True
except ImportError:
    CPP_AVAILABLE = False

@unittest.skipUnless(CPP_AVAILABLE, "C++ extension not available")
class TestMemory(unittest.TestCase):
    def test_packed_dna(self):
        dna = "ACGT" * 10
        packed = dna_native.pack_dna(dna)
        self.assertEqual(len(packed), 10) # 40 bases / 4 = 10 bytes
        
        unpacked = dna_native.unpack_dna(packed, len(dna))
        self.assertEqual(unpacked, dna)

    def test_packed_dna_partial(self):
        dna = "ACGTA" # 5 bases
        packed = dna_native.pack_dna(dna)
        self.assertEqual(len(packed), 2) # ceil(5/4) = 2 bytes
        
        unpacked = dna_native.unpack_dna(packed, len(dna))
        self.assertEqual(unpacked, dna)

if __name__ == '__main__':
    unittest.main()
