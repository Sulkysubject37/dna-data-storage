# Phase 4: Scaling & Robustness

## Memory Efficiency
- **Packed Representation**: Introduced a 2-bit-per-base representation in C++ core (`pack_dna`/`unpack_dna`), reducing memory footprint for DNA strings by 4x.
- **Streaming Pipeline**: Implemented `StreamPipeline` to encode/decode data block-by-block, enabling processing of files larger than available RAM.

## Parallelism
- **Chunk-Level Parallelism**: Added `hamming_encode_batch` and `hamming_decode_batch` in C++, utilizing `std::async` and releasing the Python GIL.
- **Speedup**: Batch processing allows scaling with CPU cores for high-throughput workloads.

## Robustness
- **Missing Chunk Detection**: The logical addressing system allows the decoder to identify missing chunks based on index mismatches.
- **Rejection-and-Remap**: The encoding loop automatically retries chunks (with different nonces) if they violate biological constraints (GC/Homopolymer).

## Operational Features
- **CLI**: `encode_file.py` and `decode_file.py` now support:
  - `--backend cpp`: Use native core.
  - `--stream`: Use streaming pipeline.
  - `--chunk-size`: Configurable chunking.

## Limits
- **RS Overhead**: Reed-Solomon encoding is still single-threaded Python (bottleneck for RS mode). Hamming mode is fully accelerated.
- **Streaming Header**: Requires known file size upfront or seekable stream.
