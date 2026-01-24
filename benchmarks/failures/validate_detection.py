import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
from dna_storage.file_ops import DNAStorage
from dna_storage.addressing import AddressIndexer
from scripts.plotting_utils import setup_plot, save_plot

def run_failure_validation():
    data = b'A' * 128 * 2 # 2 chunks
    storage = DNAStorage(chunk_size=128) # RS default
    encoded = storage.encode(data)
    
    offset, _ = storage._parse_header_and_configure(encoded)
    
    results = []

    # 1. Minor Flip
    mutated = list(encoded)
    mutated[offset + 80] = 'T' if mutated[offset + 80] == 'A' else 'A'
    bad_payload = "".join(mutated)
    try:
        decoded = storage.decode(bad_payload)
        if decoded == data: results.append(('Minor Flip', 'Corrected'))
    except Exception: results.append(('Minor Flip', 'Detected'))

    # 2. Massive
    mutated = list(encoded)
    for i in range(80):
        if offset + 80 + i < len(mutated): mutated[offset+80+i] = 'C'
    try:
        storage.decode("".join(mutated))
        results.append(('Massive', 'Silent'))
    except Exception: results.append(('Massive', 'Detected'))

    # 3. Missing
    indexer = AddressIndexer(128, 'rs', {'nsym': 10})
    chunk_len = indexer.calculate_chunk_dna_length()
    missing_chunk = encoded[0:offset] + encoded[offset + chunk_len:]
    try:
        storage.decode(missing_chunk)
        results.append(('Missing Chunk', 'Silent'))
    except Exception: results.append(('Missing Chunk', 'Detected'))

    print(f"Validation Results: {results}")
    
    # Plot
    labels = [r[0] for r in results]
    outcomes = [r[1] for r in results]
    
    fig, ax = setup_plot("Failure Detection Matrix", "Scenario", "Outcome")
    colors = {'Corrected': 'green', 'Detected': 'blue', 'Silent': 'red'}
    ax.bar(labels, [1]*3, color=[colors[o] for r,o in results])
    
    for i, o in enumerate(outcomes):
        ax.text(i, 0.5, o, ha='center', va='center', color='white', fontweight='bold')
        
    ax.set_yticks([])
    save_plot(fig, "benchmarks/failures/detection_status.png")

if __name__ == '__main__':
    run_failure_validation()
