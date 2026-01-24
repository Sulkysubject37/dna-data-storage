# Python Performance Profiling Results

## Methodology
Profiling was performed using `cProfile` on two files:
1. `init_reslik.sh` (5 KB) - Small file baseline.
2. `NL.pdf` (5.8 MB) - Large binary to stress throughput.

## Key Findings

### 1. ECC Overhead (Dominant)
The Reed-Solomon implementation (`reedsolo.py`) is the primary bottleneck, consuming **>70% of total runtime**.
- **Issue**: `reedsolo.RSCodec` is re-initialized for *every chunk*.
- **Impact**: `init_tables` is called hundreds of thousands of times (once per 128-byte chunk).
- **Core Cost**: Galois Field arithmetic (`gf_mul`, `gf_mult_noLUT`) is pure Python and extremely slow for millions of operations.

### 2. String Manipulation
String operations (`str.join`, slicing) consume **~15-20% of runtime**.
- **Issue**: Converting bytes to binary strings (`'010101...'`) and then to DNA (`'AGCT...'`) creates massive temporary objects.
- **Impact**: Heavy memory churn and CPU usage for copying buffers.

### 3. Function Call Overhead
The chunk-based architecture results in millions of function calls (600 million calls for 5.8 MB file).
- **Issue**: Python function call overhead is significant in tight loops (chunk processing).

## Conclusion
To achieve high throughput, the following must be moved to a native C++ core:
1. **ECC Backend**: A C++ Reed-Solomon implementation (or optimized library) to eliminate Python GF arithmetic and initialization overhead.
2. **Binary ↔ DNA Mapping**: Byte-level lookups to replace string-based mapping.
3. **Chunking Loop**: The inner loop processing chunks should ideally happen in C++ to avoid Python interpreter overhead per chunk.

## Profiling Data (NL.pdf)
- Total Time: 162.78s
- `rs_decode` + `rs_encode`: ~125s
- `str.join`: ~20s
- `init_tables`: ~41s (Part of ECC)
