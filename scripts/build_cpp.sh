#!/bin/bash
set -e

# Ensure we are in project root
cd "$(dirname "$0")/.."

# Use python from env or fallback to python3
PYTHON=${PYTHON:-python}

echo "Using Python: $PYTHON"

INCLUDES=$($PYTHON -m pybind11 --includes)
SUFFIX=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX') or '.so')")

OUTPUT="dna_storage/native/dna_native$SUFFIX"

if [ "$(uname)" == "Darwin" ]; then
    LINK_FLAGS="-undefined dynamic_lookup"
else
    LINK_FLAGS=""
fi

echo "Building C++ core..."
c++ -O3 -Wall -shared -std=c++17 -fPIC \
    $INCLUDES \
    -I cpp_core/include \
    cpp_core/src/dna_core.cpp \
    dna_storage/native/bindings.cpp \
    -o "$OUTPUT" \
    $LINK_FLAGS

echo "Build complete: $OUTPUT"
