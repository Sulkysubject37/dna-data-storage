import os
import time
import statistics
import json
import csv
import argparse
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
        for i in range(3):
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
                print(f"CRITICAL FAILURE: {filename} - Content mismatch on run {i+1}. Decoded len {len(decoded_data)} vs Original {len(data)}")
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

    def run_all(self, tier='small'):
        if not os.path.exists(self.test_dir):
            print(f"Test directory {self.test_dir} not found.")
            return

        files = []
        for f in os.listdir(self.test_dir):
            path = os.path.join(self.test_dir, f)
            if not os.path.isfile(path) or f == 'README.md' or f.endswith('.mp4'):
                continue
            
            size = os.path.getsize(path)
            is_large = size > 1024 * 1024 # 1MB cutoff
            
            if tier == 'small' and is_large:
                continue
            if tier == 'large' and not is_large:
                continue
                
            files.append(f)
            
        files.sort()
        print(f"Found {len(files)} files in {self.test_dir} (Tier: {tier})")
        
        for f in files:
            print(f"Benchmarking {f}...")
            try:
                res = self.run_file(f)
                self.results.append(res)
            except Exception as e:
                print(f"ERROR on {f}: {e}")
                self.results.append({"filename": f, "success": False, "error": str(e)})

    def save_results(self):
        output_dir = os.path.join(os.path.dirname(__file__), 'results')
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(output_dir, f'baseline_results_{timestamp}.json')
        csv_path = os.path.join(output_dir, f'baseline_results_{timestamp}.csv')
        
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=2)
            
        if self.results:
            keys = set()
            for r in self.results:
                keys.update(r.keys())
            keys = sorted(list(keys))
            
            with open(csv_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.results)
        
        print(f"Results saved to {json_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tier', choices=['small', 'large', 'all'], default='small', help='Baseline tier: small (<=1MB), large (>1MB), or all')
    args = parser.parse_args()
    
    runner = BenchmarkRunner()
    runner.run_all(args.tier)
    runner.save_results()
    print(f"Completed {len(runner.results)} benchmarks.")