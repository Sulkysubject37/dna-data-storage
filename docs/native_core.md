# Native C++ Core

## Motivation
Profiling revealed that >90% of runtime was spent in:
1. Reed-Solomon GF arithmetic (Python).
2. Binary-to-DNA string concatenation.
3. Hamming bitwise operations.

Phase 3 introduces a C++ core (`dna_native`) to handle these throughput-critical paths.

## Architecture
- **Language**: C++17
- **Binding**: pybind11
- **Module**: `dna_storage.native.dna_native`

### Features Ported
1. **Binary ↔ DNA Mapping**:
   - `binary_to_dna`: Byte-level lookup table (256 entries).
   - `dna_to_binary`: Reverse lookup.
2. **Hamming ECC**:
   - Full Encode/Decode cycle in C++.
   - Fused mapping: `Bytes -> Hamming -> DNA` avoids intermediate bit-packing overhead.

## Performance
Benchmarking on a 5.8 MB PDF file (Hamming ECC):
- **Python**: ~45.9s
- **C++**: ~0.42s
- **Speedup**: **~109x**

## Build System
- `scripts/build_cpp.sh`: Compiles the shared object using system C++ compiler and `pybind11` includes.
- `scripts/clean_cpp.sh`: Removes artifacts.

## Usage
The `DNAStorage` class now accepts a `backend` parameter:
```python
storage = DNAStorage(ecc_method='hamming', backend='cpp')
```
If `cpp` backend is unavailable, it gracefully falls back to `python` with a warning.
