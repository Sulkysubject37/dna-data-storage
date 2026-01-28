# CI/CD Workflows

This project utilizes GitHub Actions to ensure cross-platform compatibility and performance regression testing.

## Overview
We maintain two parallel workflows to validate the DNA data storage pipeline on different operating systems:
1.  **Ubuntu Pipeline** (`ubuntu_pipeline.yml`): Runs on `ubuntu-latest`.
2.  **macOS Pipeline** (`macos_pipeline.yml`): Runs on `macos-latest`.

## Workflow Logic
Both workflows execute the following identical steps to ensure consistency:

### 1. Environment Setup
- Checkout the repository.
- Set up Python 3.10.
- Install dependencies from `requirements.txt`.
- Compile the C++ backend (`scripts/build_cpp.sh`) to enable high-performance encoding.

### 2. Data Fetching
- The pipeline utilizes existing test artifacts in `f_test/`.
- It also fetches an external sample file (e.g., from Project Gutenberg) to verify the system's ability to handle arbitrary external data streams.

### 3. Pipeline Execution
A custom script (`scripts/run_ci_pipeline.py`) orchestrates the test:
- **Encoding**: Converts input files to DNA sequences (`.dna`).
- **Decoding**: Restores original files from the DNA sequences.
- **Verification**: Performs a bitwise comparison (`diff`) to ensure 100% data integrity.
- **Benchmarking**: Measures execution time for both phases.

### 4. Artifacts & Reporting
- **Intermediate Files**: The encoded `.dna` files are archived and available for download.
- **Throughput Report**: A Markdown summary (`throughput_report.md`) is generated, detailing the processing speed (MB/s) for each file.

## Triggering
These workflows are triggered automatically on:
- `push` to the `main` branch.
- `pull_request` targeting the `main` branch.
