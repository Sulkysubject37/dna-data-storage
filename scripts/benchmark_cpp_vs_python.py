import time
import os
import sys

# Add root to path
sys.path.append(os.getcwd())

from dna_storage.file_ops import DNAStorage

def benchmark(filename, backend, iterations=3):
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Test Hamming for maximum native throughput
    print(f"Benchmarking {filename} with backend={backend} (Hamming)...")
    storage = DNAStorage(ecc_method='hamming', nsym=10, chunk_size=128, backend=backend)
    
    start = time.perf_counter()
    for _ in range(iterations):
        encoded = storage.encode(data)
        decoded = storage.decode(encoded)
        if decoded != data:
            raise RuntimeError("Mismatch!")
    end = time.perf_counter()
    
    avg_time = (end - start) / iterations
    return avg_time

if __name__ == '__main__':
    # Prefer a medium/large file
    targets = ["f_test/NL.pdf", "f_test/init_reslik.sh"]
    target = next((f for f in targets if os.path.exists(f)), None)
    
    if not target:
        print("No test file found.")
        sys.exit(1)
        
    t_py = benchmark(target, 'python', iterations=3)
    t_cpp = benchmark(target, 'cpp', iterations=3)
    
    print(f"\nResults for {target}:")
    print(f"Python: {t_py:.4f}s")
    print(f"C++:    {t_cpp:.4f}s")
    print(f"Speedup: {t_py / t_cpp:.2f}x")
    
    # Save result
    os.makedirs("dna_storage/benchmarks/results", exist_ok=True)
    with open("dna_storage/benchmarks/results/cpp_vs_python.txt", "w") as f:
        f.write(f"File: {target}\n")
        f.write(f"Python: {t_py:.4f}s\n")
        f.write(f"C++:    {t_cpp:.4f}s\n")
        f.write(f"Speedup: {t_py / t_cpp:.2f}x\n")
