#!/bin/bash
set -e
cd "$(dirname "$0")/.."

echo "Cleaning C++ build artifacts..."
rm -f dna_storage/native/*.so

echo "Clean complete."
