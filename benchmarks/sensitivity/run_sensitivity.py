import sys
import time
import os
import matplotlib.pyplot as plt
import csv

# Add root to path
sys.path.append(os.getcwd())

from dna_storage.file_ops import DNAStorage
try:
    from dna_storage.native import dna_native
except ImportError:
    print("C++ backend required for sensitivity analysis")
    sys.exit(1)

from scripts.plotting_utils import setup_plot, save_plot

def run_chunk_sensitivity():
    sizes = [32, 64, 128, 256, 512, 1024, 2048, 4096]
    results = []
    data_size_mb = 5
    data = b'A' * 1024 * 1024 * data_size_mb
    
    print("Running Chunk Size Sensitivity...")
    for size in sizes:
        # Use C++ backend
        storage = DNAStorage(chunk_size=size, backend='cpp', ecc_method='hamming')
        start = time.perf_counter()
        storage.encode(data)
        end = time.perf_counter()
        tput = data_size_mb / (end - start)
        results.append({"chunk_size": size, "throughput": tput})
        print(f"Size {size}: {tput:.2f} MB/s")
        
    # Plot
    sizes = [r['chunk_size'] for r in results]
    tputs = [r['throughput'] for r in results]
    fig, ax = setup_plot("Throughput vs Chunk Size", "Chunk Size (Bytes)", "Throughput (MB/s)")
    ax.plot(sizes, tputs, marker='o')
    ax.set_xscale('log', base=2)
    save_plot(fig, "benchmarks/sensitivity/throughput_vs_chunk_size.png")

def run_thread_sensitivity():
    threads = [1, 2, 4, 8, 16]
    data_size_mb = 20 # Larger data to see parallel gain
    chunk_size = 256
    num_chunks = (data_size_mb * 1024 * 1024) // chunk_size
    
    # Create batch of bytes
    chunk_data = b'A' * chunk_size
    batch = [chunk_data] * num_chunks
    
    print(f"Running Thread Sensitivity (C++ Core, {data_size_mb} MB)...")
    results = []
    for t in threads:
        start = time.perf_counter()
        # Direct call to native batch API which releases GIL
        dna_native.hamming_encode_batch(batch, t)
        end = time.perf_counter()
        
        tput = data_size_mb / (end - start)
        results.append({"threads": t, "throughput": tput})
        print(f"Threads {t}: {tput:.2f} MB/s")
        
    # Plot
    ts = [r['threads'] for r in results]
    tputs = [r['throughput'] for r in results]
    fig, ax = setup_plot("Throughput vs Threads (C++ Core)", "Threads", "Throughput (MB/s)")
    ax.plot(ts, tputs, marker='o')
    save_plot(fig, "benchmarks/sensitivity/throughput_vs_threads.png")

if __name__ == '__main__':
    run_chunk_sensitivity()
    print("-" * 40)
    run_thread_sensitivity()
