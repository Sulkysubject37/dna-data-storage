# Phase 2: Biological Realism & Evaluation

## Biological Constraints
To ensure DNA sequences are compatible with synthesis constraints, we introduced:
- **GC Content Enforcement**: Rejects chunks outside the target range (e.g., 40-60%).
- **Homopolymer Control**: Rejects runs of identical bases (e.g., >3).
- **Mechanism**: A "Rejection-and-Remap" strategy using a nonce-based scrambler. If a chunk violates constraints, it is re-scrambled with a new nonce until compliant. To handle Header constraints, we implemented a fixed "Whitening" mask.

## Error Models
We moved beyond simple random errors to structured channels:
- **Substitution**: Standard point mutations.
- **Indel**: Insertion and deletion events (simulating synthesis/sequencing drift).
- **Burst**: Localized clusters of errors.

## Addressing & Random Access
The system now supports **Logical Chunk Addressing**.
- **Indexer**: Calculates byte offsets in the DNA stream based on ECC parameters and strategy.
- **Random Access**: `decode_chunk(index)` allows retrieving specific data blocks without decoding the entire file.

## Encoding Strategies
- **Baseline**: Direct 2-bit mapping (A=00, etc.). High density (2 bits/base) but poor biological properties.
- **Rotating**: Base-3 encoding ensuring no adjacent identical bases. Lower density (~1.58 bits/base) but guaranteed homopolymer avoidance (run length=1).

## Evaluation
A new evaluation toolkit (`dna_storage.evaluation`) provides metrics:
- **Overhead**: Additional bases required vs theoretical minimum.
- **Success Rate**: Binary integrity check after error injection.
- **GC/Homopolymer Stats**: Verification of sequence properties.
