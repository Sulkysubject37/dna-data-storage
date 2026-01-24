import cProfile
import pstats
import sys
import os

# Add root to path
sys.path.append(os.getcwd())

from dna_storage.benchmarks.run_baseline import BenchmarkRunner

def profile_file(filename):
    runner = BenchmarkRunner()
    print(f"Profiling {filename}...")
    profiler = cProfile.Profile()
    profiler.enable()
    runner.run_file(filename)
    profiler.disable()
    
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(20)

if __name__ == '__main__':
    profile_file("init_reslik.sh")
    print("-" * 40)
    # NL.pdf is 5.8MB, might take a while but good for data
    if os.path.exists("f_test/NL.pdf"):
        profile_file("NL.pdf")
