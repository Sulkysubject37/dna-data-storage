# Threats to Validity

## Internal Validity (Benchmarking)
- **Representativeness**: The `f_test/` dataset and synthetic URANDOM files may not reflect the compressibility or entropy of real-world genomic or archival data.
- **Hardware Dependence**: Throughput and parallelism scaling results are highly dependent on the host CPU architecture (e.g., Apple M1 Max vs Intel Xeon). Results may not generalize to low-power ARM or high-density server environments without re-characterization.

## External Validity (Biological Assumptions)
- **Simplified Error Models**: The `Substitution`, `Indel`, and `Burst` models are statistical approximations. Real DNA synthesis and sequencing (e.g., Illumina vs. Oxford Nanopore) exhibit complex, motif-dependent error profiles (e.g., homopolymer bias) that are not fully captured by uniform random distributions.
- **Longevity Extrapolation**: Longevity assumptions (centuries of stability) are based on literature for specific storage conditions (e.g., encapsulated, dry, cold). Environmental drift (temperature spikes, humidity) is not modeled.

## Construct Validity (Measurement)
- **Memory Monitoring**: Peak RSS (`ru_maxrss`) measures the high-water mark of memory allocation. It does not account for temporary spikes or fragmented heaps between measurement intervals.
- **Throughput Boundary**: Measured throughput includes Python orchestration overhead. For very small chunks, Python overhead dominates, making C++ speedups appear lower than the theoretical core potential.
