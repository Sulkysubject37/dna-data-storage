import os
import sys
import time
import resource
import csv
import matplotlib.pyplot as plt

# Add root to path
sys.path.append(os.getcwd())

from dna_storage.file_ops import DNAStorage
from scripts.plotting_utils import setup_plot, save_plot

def get_peak_memory_mb():
    # macOS returns bytes, Linux returns KB
    if sys.platform == 'darwin':
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)
    else:
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024

def run_limit_test():
    # Test range: 1MB to 50MB (scaled down for interactive session, but logic holds for larger)
    sizes_mb = [1, 5, 10, 25, 50] 
    results = []
    
    print("Starting Operational Envelope Discovery...")
    
    for size in sizes_mb:
        print(f"Testing {size} MB...")
        filename = f"limit_test_{size}mb.bin"
        
        # Generate file
        with open(filename, 'wb') as f:
            f.write(os.urandom(size * 1024 * 1024))
            
        try:
            # Use C++ backend for performance limits
            storage = DNAStorage(ecc_method='hamming', backend='cpp', chunk_size=4096)
            
            # Read to memory to stress RAM limits directly
            with open(filename, 'rb') as f:
                data = f.read()
            
            # Encode
            start = time.perf_counter()
            encoded = storage.encode(data)
            end = time.perf_counter()
            encode_time = end - start
            encode_mem = get_peak_memory_mb()
            
            # Decode
            start = time.perf_counter()
            decoded = storage.decode(encoded)
            end = time.perf_counter()
            decode_time = end - start
            
            if decoded != data:
                raise RuntimeError("Mismatch")
                
            throughput = size / encode_time
            results.append({
                "size_mb": size,
                "encode_time": encode_time,
                "throughput_mb_s": throughput,
                "peak_mem_mb": encode_mem
            })
            
        except Exception as e:
            print(f"Failed at {size} MB: {e}")
            break
        finally:
            if os.path.exists(filename):
                os.remove(filename)
                
    if not results:
        print("No results collected.")
        return

    # Save CSV
    with open("benchmarks/limits/results.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        
    # Plot Throughput
    sizes = [r['size_mb'] for r in results]
    throughputs = [r['throughput_mb_s'] for r in results]
    mems = [r['peak_mem_mb'] for r in results]
    
    fig, ax = setup_plot("Throughput vs File Size", "File Size (MB)", "Throughput (MB/s)")
    ax.plot(sizes, throughputs, marker='o')
    save_plot(fig, "benchmarks/limits/throughput_vs_size.png")
    
    # Plot Memory
    fig, ax = setup_plot("Peak Memory vs File Size", "File Size (MB)", "Peak Memory (MB)")
    ax.plot(sizes, mems, marker='o', color='orange')
    save_plot(fig, "benchmarks/limits/memory_vs_size.png")

if __name__ == '__main__':
    run_limit_test()
