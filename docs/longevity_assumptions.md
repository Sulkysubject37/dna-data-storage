# DNA Storage Longevity & Degradation Assumptions

## Digital vs. Physical
- **Digital DNA (Simulated)**: Exact information. Lossless.
- **Physical DNA (Wet-lab)**: Subject to entropy, hydrolysis, oxidation.

## Degradation Models
We map physical degradation to our error models:

1. **Substitutions (Point Mutations)**
   - Cause: PCR errors, UV damage (C->T).
   - Modeled by: `SubstitutionModel`.
   - Mitigation: Reed-Solomon / Hamming.

2. **Strand Breaks (Deletions/Loss)**
   - Cause: Hydrolysis, shear force.
   - Modeled by: `IndelModel` (Deletion), `Missing Chunk` simulation.
   - Mitigation: Indexing + Erasure Coding (e.g. Fountain codes - not yet implemented).

3. **Pool Bias (Dropout)**
   - Cause: Uneven amplification.
   - Modeled by: Chunk loss simulation.

## Assumptions
- **Lifetime**: We assume "cold storage" (dried/frozen) preserves sequences with <1% error rate per century.
- **Readout**: Sequencing introduces specific error profiles (e.g. homopolymer errors in Nanopore) which we model via constraints.

## Out of Scope
- Chemical kinetics simulation.
- Environmental factors (temperature/humidity logic).
