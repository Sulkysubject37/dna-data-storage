import unittest
import io
from dna_storage.file_ops import DNAStorage
from dna_storage.pipeline import StreamPipeline

class TestStreaming(unittest.TestCase):
    def test_streaming_roundtrip(self):
        data = b"Stream me!" * 100
        input_stream = io.BytesIO(data)
        encoded_stream = io.StringIO()
        
        storage = DNAStorage(chunk_size=32)
        pipeline = StreamPipeline(storage)
        
        pipeline.encode_stream(input_stream, encoded_stream, len(data))
        
        encoded_data = encoded_stream.getvalue()
        
        # Decode
        decode_input = io.StringIO(encoded_data)
        decoded_output = io.BytesIO()
        
        pipeline.decode_stream(decode_input, decoded_output)
        
        self.assertEqual(decoded_output.getvalue(), data)

if __name__ == '__main__':
    unittest.main()
