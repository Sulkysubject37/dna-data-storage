import unittest
import os
import shutil
from dna_storage.pipeline import StreamPipeline
from dna_storage.file_ops import DNAStorage
from dna_storage.checkpoint import CheckpointManager

class TestCheckpoint(unittest.TestCase):
    def test_resume(self):
        data = b'A' * 128 * 200 # 200 chunks
        filename = "test_resume.bin"
        ckpt = "test.ckpt"
        out_dna = "test_resume.dna"
        
        with open(filename, 'wb') as f:
            f.write(data)
            
        storage = DNAStorage(chunk_size=128)
        pipeline = StreamPipeline(storage)
        
        cm = CheckpointManager(ckpt)
        cm.save({"processed_chunks": 100})
        
        with open(filename, 'rb') as f_in, open(out_dna, 'w') as f_out:
            pipeline.encode_stream(f_in, f_out, len(data), ckpt)
            
        with open(out_dna, 'r') as f:
            content = f.read()
            
        # 100 chunks * 616 bases = 61600
        self.assertEqual(len(content), 61600)
        
        os.remove(filename)
        os.remove(ckpt)
        os.remove(out_dna)

if __name__ == '__main__':
    unittest.main()