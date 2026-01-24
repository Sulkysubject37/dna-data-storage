import argparse
import sys
from dna_storage.file_ops import DNAStorage
from dna_storage.pipeline import StreamPipeline

def main():
    parser = argparse.ArgumentParser(description='Decode DNA sequence to file')
    parser.add_argument('dna_file', help='File containing DNA sequence')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('-e', '--ecc', choices=['rs', 'hamming'], default='rs', help='Error correction method (overridden by header)')
    parser.add_argument('--backend', choices=['python', 'cpp'], default='python', help='Processing backend')
    parser.add_argument('--stream', action='store_true', help='Use streaming mode')
    
    args = parser.parse_args()

    storage = DNAStorage(ecc_method=args.ecc, backend=args.backend)

    if args.stream:
        with open(args.dna_file, 'r') as f_in, open(args.output, 'wb') as f_out:
            pipeline = StreamPipeline(storage)
            pipeline.decode_stream(f_in, f_out)
            print(f"Decoded stream to {args.output}")
    else:
        with open(args.dna_file, 'r') as f:
            dna = f.read().strip()
        
        decoded = storage.decode(dna)
        
        with open(args.output, 'wb') as f:
            f.write(decoded)
        print(f"Decoded to {args.output}")

if __name__ == '__main__':
    main()
