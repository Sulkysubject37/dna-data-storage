import time
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
from dna_storage.file_ops import DNAStorage
from scripts.plotting_utils import setup_plot, save_plot

def measure(storage_func, data):
    start = time.perf_counter()
    storage_func(data)
    end = time.perf_counter()
    return end - start

def run_comparison():
    data_size_mb = 2 # Small enough for Python RS not to take forever
    data = b'A' * 1024 * 1024 * data_size_mb
    
    modes = ['Py(Ham)', 'Cpp(Ham)', 'Py(RS)', 'Cpp(RS)']
    times = []
    
    print(f"Comparing Backends/ECC ({data_size_mb} MB)...")
    
    # 1. Python Hamming
    s = DNAStorage(ecc_method='hamming', backend='python')
    times.append(measure(s.encode, data))
    
    # 2. C++ Hamming
    s = DNAStorage(ecc_method='hamming', backend='cpp')
    times.append(measure(s.encode, data))
    
    # 3. Python RS
    s = DNAStorage(ecc_method='rs', backend='python')
    times.append(measure(s.encode, data))
    
    # 4. C++ RS (Mapping only accelerated)
    s = DNAStorage(ecc_method='rs', backend='cpp')
    times.append(measure(s.encode, data))
    
    throughputs = [data_size_mb / t for t in times]
    
    # Plot
    fig, ax = setup_plot("Throughput Comparison", "Configuration", "Throughput (MB/s)")
    bars = ax.bar(modes, throughputs, color=['gray', 'green', 'gray', 'lightgreen'])
    
    # Add values
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    save_plot(fig, "benchmarks/comparison/backend_comparison.png")
    
    for m, t in zip(modes, throughputs):
        print(f"{m}: {t:.2f} MB/s")

if __name__ == '__main__':
    run_comparison()
