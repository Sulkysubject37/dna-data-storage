import argparse
import sys
from dna_storage.file_ops import DNAStorage
from dna_storage.pipeline import StreamPipeline

def main():
    parser = argparse.ArgumentParser(description='Encode file to DNA sequence')
    parser.add_argument('input', help='Input file path')
    parser.add_argument('output', nargs='?', help='Output file path (default: stdout)')
    parser.add_argument('-e', '--ecc', choices=['rs', 'hamming'], default='rs', help='Error correction method')
    parser.add_argument('--backend', choices=['python', 'cpp'], default='python', help='Processing backend')
    parser.add_argument('--chunk-size', type=int, default=128, help='Chunk size in bytes')
    parser.add_argument('--stream', action='store_true', help='Use streaming mode')
    
    args = parser.parse_args()

    storage = DNAStorage(ecc_method=args.ecc, chunk_size=args.chunk_size, backend=args.backend)

    if args.stream:
        if not args.output:
            print("Error: Streaming mode requires an output file.")
            sys.exit(1)
            
        with open(args.input, 'rb') as f_in, open(args.output, 'w') as f_out:
            pipeline = StreamPipeline(storage)
            # File size needed for streaming header?
            # Pipeline can deduce from seek/tell if file-like.
            pipeline.encode_stream(f_in, f_out)
            print(f"Encoded stream to {args.output}")
    else:
        with open(args.input, 'rb') as f:
            data = f.read()
        
        dna = storage.encode(data)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(dna)
            print(f"Encoded to {args.output}")
        else:
            print(dna)

if __name__ == '__main__':
    main()
