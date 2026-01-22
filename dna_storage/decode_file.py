import argparse
from dna_storage.file_ops import DNAStorage

def main():
    parser = argparse.ArgumentParser(description='Decode DNA sequence to file')
    parser.add_argument('dna_file', help='File containing DNA sequence')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('-e', '--ecc', choices=['rs', 'hamming'], default='rs',
                       help='Error correction method used for encoding')
    args = parser.parse_args()

    with open(args.dna_file, 'r') as f:
        dna = f.read().strip()
    
    storage = DNAStorage(ecc_method=args.ecc)
    decoded = storage.decode(dna)
    
    with open(args.output, 'wb') as f:
        f.write(decoded)

if __name__ == '__main__':
    main()