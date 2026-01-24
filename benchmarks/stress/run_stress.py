import os
import time
import argparse
import sys

# Add root to path
sys.path.append(os.getcwd())

from dna_storage.file_ops import DNAStorage

def generate_file(filename, size_mb):
    with open(filename, 'wb') as f:
        # Write in chunks to avoid memory spike during generation
        chunk = os.urandom(1024 * 1024)
        for _ in range(size_mb):
            f.write(chunk)

def run_stress(size_mb, backend, ecc):
    filename = f"stress_{size_mb}mb.bin"
    print(f"Generating {size_mb} MB file: {filename}")
    generate_file(filename, size_mb)
    
    print(f"Encoding (Backend={backend}, ECC={ecc})...")
    # Use larger chunk size for throughput
    storage = DNAStorage(ecc_method=ecc, chunk_size=4096, backend=backend)
    
    # Read full file into memory to stress memory usage of the encoder
    # Ideally use streaming, but stress test can test memory limits too.
    with open(filename, 'rb') as f:
        data = f.read()
        
    start = time.perf_counter()
    encoded = storage.encode(data)
    end = time.perf_counter()
    encode_time = end - start
    print(f"Encode Time: {encode_time:.2f}s ({size_mb / encode_time:.2f} MB/s)")
    
    print(f"Encoded Length: {len(encoded)} bases")
    
    print("Decoding...")
    start = time.perf_counter()
    decoded = storage.decode(encoded)
    end = time.perf_counter()
    decode_time = end - start
    print(f"Decode Time: {decode_time:.2f}s ({size_mb / decode_time:.2f} MB/s)")
    
    if data != decoded:
        print("FAILURE: Content mismatch")
    else:
        print("SUCCESS: Bit-exact match")
        
    os.remove(filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=10, help='Size in MB') # Default 10MB for quick check
    parser.add_argument('--backend', default='cpp')
    parser.add_argument('--ecc', default='hamming')
    args = parser.parse_args()
    
    run_stress(args.size, args.backend, args.ecc)
