import time
import os
import resource
import argparse
import sys

# Add root to path
sys.path.append(os.getcwd())

from dna_storage.file_ops import DNAStorage

def get_memory_usage_mb():
    rusage = resource.getrusage(resource.RUSAGE_SELF)
    if sys.platform == 'darwin':
        return rusage.ru_maxrss / (1024 * 1024) # bytes -> MB
    else:
        return rusage.ru_maxrss / 1024 # KB -> MB

def run_stability(iterations, backend):
    print(f"Starting stability test ({iterations} chunks, Backend: {backend})...")
    
    # Use Hamming for speed/throughput stress
    storage = DNAStorage(backend=backend, chunk_size=4096, ecc_method='hamming')
    data = b'A' * 4096
    
    start_time = time.time()
    last_log = start_time
    bytes_processed = 0
    
    for i in range(iterations):
        # Full encode flow (Chunking -> ECC -> Mapping -> Header)
        # Note: storage.encode() creates a NEW header each time.
        # This stresses the full stack allocation/deallocation.
        encoded = storage.encode(data)
        
        bytes_processed += 4096
        
        now = time.time()
        if now - last_log > 1.0: # Log every second
            mem = get_memory_usage_mb()
            elapsed = now - start_time
            throughput = (bytes_processed / elapsed) / (1024 * 1024) # MB/s
            print(f"Iter {i}: Mem {mem:.2f} MB (Peak), Throughput {throughput:.2f} MB/s")
            last_log = now

    end_time = time.time()
    print(f"Finished. Total time: {end_time - start_time:.2f}s")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations', type=int, default=10000)
    parser.add_argument('--backend', default='cpp')
    args = parser.parse_args()
    
    run_stability(args.iterations, args.backend)
