import os
import time
import glob
import argparse
import sys

# Ensure we can import from the package
sys.path.append(os.getcwd())
try:
    from dna_storage.file_ops import DNAStorage
except ImportError:
    # If running from scripts/, we might need to adjust path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from dna_storage.file_ops import DNAStorage

def run_pipeline(input_dir, output_dir, backend):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Initialize report
    report_lines = []
    report_lines.append("| File | Size (MB) | Encode Time (s) | Decode Time (s) | Throughput (MB/s) | Backend | Status |")
    report_lines.append("|---|---|---|---|---|---|---|")
    
    files = [f for f in glob.glob(os.path.join(input_dir, "*")) if os.path.isfile(f)]
    files.sort()
    
    if not files:
        print(f"No files found in {input_dir}")
        sys.exit(1)

    print(f"Found {len(files)} files to process in {input_dir}")

    # Initialize storage
    # using RS (Reed-Solomon) as it is the robust default
    try:
        storage = DNAStorage(ecc_method='rs', backend=backend)
        print(f"Initialized DNAStorage with backend={backend}")
    except Exception as e:
        print(f"Failed to initialize DNAStorage: {e}")
        # If backend is strictly required, we might want to fail
        # But for the report, we can just log it
        sys.exit(1)
    
    for file_path in files:
        filename = os.path.basename(file_path)
        # Check size
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        print(f"\nProcessing {filename} ({file_size_mb:.2f} MB)...")
        
        try:
            # Read
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Encode
            start_enc = time.time()
            encoded_dna = storage.encode(data)
            enc_time = time.time() - start_enc
            
            # Save Encoded
            encoded_path = os.path.join(output_dir, f"{filename}.dna")
            with open(encoded_path, 'w') as f:
                f.write(encoded_dna)
            
            print(f"  Encoded in {enc_time:.4f}s. Saved to {encoded_path}")

            # Decode
            start_dec = time.time()
            decoded_data = storage.decode(encoded_dna)
            dec_time = time.time() - start_dec
            
            print(f"  Decoded in {dec_time:.4f}s.")

            # Verify
            if data == decoded_data:
                status = "PASS"
                print("  Verification: SUCCESS")
            else:
                status = "FAIL (Mismatch)"
                print("  Verification: FAILED")
            
            # Calculate throughput (MB processed / Total Time)
            # "Throughput" usually refers to the speed of the system.
            # Here we can report the effective throughput for the round trip or just encode.
            # Let's report Round-Trip Throughput.
            total_time = enc_time + dec_time
            throughput = file_size_mb / total_time if total_time > 0 else 0
            
            report_lines.append(f"| {filename} | {file_size_mb:.4f} | {enc_time:.4f} | {dec_time:.4f} | {throughput:.2f} | {backend} | {status} |")
            
        except Exception as e:
            print(f"  Error: {e}")
            report_lines.append(f"| {filename} | {file_size_mb:.4f} | N/A | N/A | N/A | {backend} | FAIL ({e}) |")

    # Write Report
    report_path = os.path.join(output_dir, "throughput_report.md")
    with open(report_path, "w") as f:
        f.write("# DNA Storage Throughput Report\n\n")
        f.write("\n".join(report_lines))
    
    print(f"\nReport generated at {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True, help="Directory containing files to encode")
    parser.add_argument("--output-dir", required=True, help="Directory to save output artifacts")
    parser.add_argument("--backend", default="python", choices=["python", "cpp"], help="Backend to use")
    args = parser.parse_args()
    
    run_pipeline(args.input_dir, args.output_dir, args.backend)
