import argparse
from dna_storage.file_ops import DNAStorage

def main():
    parser = argparse.ArgumentParser(description='Encode file to DNA sequence')
    parser.add_argument('input', help='Input file path')
    parser.add_argument('-e', '--ecc', choices=['rs', 'hamming'], default='rs',
                       help='Error correction method')
    args = parser.parse_args()

    with open(args.input, 'rb') as f:
        data = f.read()
    
    storage = DNAStorage(ecc_method=args.ecc)
    dna = storage.encode(data)
    print(dna)

if __name__ == '__main__':
    main()