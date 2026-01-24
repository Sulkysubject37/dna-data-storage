# Phase 5: Operational Robustness

## Stability & Checkpointing
- **Long-Run Stability**: Verified via `benchmarks/stability/run_stability.py` (memory/throughput monitoring).
- **Checkpointing**: `StreamPipeline` supports `checkpoint_path`. Saves state (`processed_chunks`) periodically to allow resumption.

## Reproducibility
- **Manifests**: Every experiment using `RunManifest` stores configuration, stats, and unique ID in `runs/{ID}/manifest.json`.
- **Seeding**: Error models accept explicit seeds for deterministic failure simulation.

## Failure Handling
- **Classification**: `dna_storage.failures.FailureType` classifies errors (CORRUPTION, MISSING, etc.).
- **Silent Failure Prevention**: Checksums detect silent corruption (collisions). Indexing detects missing chunks.

## Longevity
See `docs/longevity_assumptions.md` for physical storage assumptions.

## Known Limitations
- **Resume**: Only supported for Encoding (chunk-based). Decoding resume not fully implemented (requires seeking output stream safely).
- **Stream Header**: Streaming requires file size upfront to write Header. Pipe input requires buffering or size estimation.
