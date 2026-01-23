# Baseline Benchmark Methodology

## Overview
This document describes the methodology for establishing performance baselines for the DNA Data Storage system. The goal is to measure correctness and timing before any optimization scaling.

## Test Data
The `f_test/` directory contains a heterogeneous set of files:
- **Small Tier (≤1MB)**: Text files, scripts, small images. Used for fast regression testing.
- **Large Tier (>1MB)**: Audio, Video, PDF. Used for throughput measurement.

## Methodology
The benchmark script (`dna_storage/benchmarks/run_baseline.py`) performs the following for each file:
1. **Read**: Loads file into memory.
2. **Encode**: Converts binary to DNA using Reed-Solomon (nsym=10), Baseline Strategy (2-bit), Default Chunking (128 bytes). Timing excludes I/O.
3. **Decode**: Converts DNA back to binary. Timing excludes I/O.
4. **Verify**: Compares decoded bytes with original bytes bit-for-bit.
5. **Repeat**: Runs 3 iterations and reports median time.

## Metrics
- **Encode Time**: CPU time for encoding logic.
- **Decode Time**: CPU time for decoding logic.
- **Overhead**: Implicitly measured by DNA length vs Original size.
- **Correctness**: Boolean success flag.

## Usage
Run the benchmark:
```bash
# Small files only (default)
python -m dna_storage.benchmarks.run_baseline --tier small

# Large files
python -m dna_storage.benchmarks.run_baseline --tier large

# All
python -m dna_storage.benchmarks.run_baseline --tier all
```

Results are saved to `dna_storage/benchmarks/results/` in JSON and CSV formats.

## Limitations
- This is a single-threaded Python implementation.
- String concatenation performance dominates for large files.
- No parallelization or optimizations applied yet.
