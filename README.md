# DNA Data Storage System

A Python implementation of DNA-based data storage with error correction.
**Research Prototype - Not for Production Use.**

## Scope
This project demonstrates the principles of encoding digital data into DNA sequences. It includes:
- **Binary-to-DNA Mapping**: 2-bit mapping (A, T, C, G).
- **Error Correction**: Reed-Solomon (robust) and Hamming (educational).
- **Format**: Structured file format with metadata header and chunking.
- **Simulation**: Tools to inject errors for testing robustness.

## Setup

1.  **Clone:**
    ```bash
    git clone https://github.com/Sulkysubject37/dna-data-storage.git
    cd dna-data-storage
    ```

2.  **Environment:**
    ```bash
    python3.10 -m venv dna-storage
    source dna-storage/bin/activate
    pip install -r requirements.txt
    ```

3.  **Build C++ Core (Optional):**
    ```bash
    ./scripts/build_cpp.sh
    ```

## Usage

### Interactive CLI
```bash
python -m dna_storage.interactive_cli
```

### Library
```python
from dna_storage.file_ops import DNAStorage

# Use C++ backend for performance (requires build)
storage = DNAStorage(ecc_method='hamming', backend='cpp')
encoded_dna = storage.encode(b"Hello World")
decoded_data = storage.decode(encoded_dna)
```

### Scripts
Encode a file:
```bash
python -m dna_storage.encode_file input.txt -e rs
```

Decode a file:
```bash
python -m dna_storage.decode_file input.dna output.txt
```

## Benchmarking

This project includes a benchmarking harness to establish performance baselines.

### Running Benchmarks
Establishing a baseline for small files:
```bash
python -m dna_storage.benchmarks.run_baseline --tier small
```

### Baseline vs. Scaling
- **Baseline Benchmarking**: Focuses on correctness and single-threaded performance using fixed parameters. These results are recorded in `dna_storage/benchmarks/results/` and serve as a pre-optimization reference.
- **Scaling Experiments**: (Planned) Will focus on throughput, parallelization, and large-scale data handling.

## Performance
A native C++ backend is available for high-performance encoding/decoding.
See `docs/native_core.md` for details.

## License
This project is licensed under the **PolyForm Noncommercial License 1.0.0**. 

**Noncommercial use only.** For commercial inquiries, quotes, or royalty agreements, please contact the copyright holder.

## Testing
Run unit tests:
```bash
python -m unittest discover tests
```

## Limitations
- **No Wet-Lab Support**: This is a computational simulation. It does not interface with synthesizers or sequencers.
- **ECC Constraints**: Hamming code handles single-bit errors only. RS handles burst errors but has limits.
- **Performance**: Optimized for correctness and clarity, not speed (unless C++ backend is used).