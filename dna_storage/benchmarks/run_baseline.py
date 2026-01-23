import os
import time
import statistics
import json
import csv
from dna_storage.file_ops import DNAStorage

class BenchmarkRunner:
    def __init__(self, test_dir="f_test"):
        self.test_dir = test_dir
        self.results = []
        
    def run_file(self, filename):
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'rb') as f:
            data = f.read()
            
        file_size = len(data)
        ext = os.path.splitext(filename)[1]
        
        # Configure storage: RS, chunking ON (default), errors OFF, constraints OFF, encoding baseline
        storage = DNAStorage(ecc_method='rs', nsym=10, chunk_size=128, constraints=None, encoding='baseline')
        
        encode_times = []
        decode_times = []
        dna_length = 0
        success = False
        
        # Run 3 times
        for _ in range(3):
            # Encode
            start = time.perf_counter()
            encoded_dna = storage.encode(data)
            end = time.perf_counter()
            encode_times.append(end - start)
            
            dna_length = len(encoded_dna)
            
            # Decode
            start = time.perf_counter()
            decoded_data = storage.decode(encoded_dna)
            end = time.perf_counter()
            decode_times.append(end - start)
            
            if decoded_data != data:
                print(f"FAILURE: {filename} - Content mismatch")
                success = False
                break
            else:
                success = True
                
        if not success:
            return {
                "filename": filename,
                "success": False,
                "error": "Content mismatch"
            }
            
        return {
            "filename": filename,
            "extension": ext,
            "size_bytes": file_size,
            "dna_length": dna_length,
            "encode_time_median": statistics.median(encode_times),
            "decode_time_median": statistics.median(decode_times),
            "success": True
        }

    def run_all(self):
        if not os.path.exists(self.test_dir):
            print(f"Test directory {self.test_dir} not found.")
            return

        # Skip README and large MP4s for baseline speed
        files = [f for f in os.listdir(self.test_dir) 
                 if os.path.isfile(os.path.join(self.test_dir, f)) 
                 and f != 'README.md' 
                 and not f.endswith('.mp4')]
        files.sort()
        print(f"Found {len(files)} files in {self.test_dir}")
        
        for f in files:
            print(f"Benchmarking {f}...")
            try:
                res = self.run_file(f)
                self.results.append(res)
            except Exception as e:
                print(f"ERROR on {f}: {e}")
                self.results.append({"filename": f, "success": False, "error": str(e)})

if __name__ == '__main__':
    runner = BenchmarkRunner()
    runner.run_all()
    print(f"Completed {len(runner.results)} benchmarks.")