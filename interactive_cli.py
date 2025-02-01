from dna_storage import DNAStorage, visualize_mapping
import argparse

def display_banner():
    print("""
    ██████╗ ███╗   ██╗ █████╗     ██████╗  █████╗ ████████╗ █████╗ 
    ██╔══██╗████╗  ██║██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
    ██║  ██║██╔██╗ ██║███████║    ██║  ██║███████║   ██║   ███████║
    ██║  ██║██║╚██╗██║██╔══██║    ██║  ██║██╔══██║   ██║   ██╔══██║
    ██████╔╝██║ ╚████║██║  ██║    ██████╔╝██║  ██║   ██║   ██║  ██║
    ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
    """)

def interactive_cli():
    storage = DNAStorage()
    
    while True:
        print("\nDNA Data Storage Toolkit")
        print("1. Encode Text to DNA")
        print("2. Decode DNA to Text")
        print("3. Encode File to DNA File")
        print("4. Decode DNA File to File")
        print("5. Visualize DNA Mapping")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        try:
            if choice == '1':
                text = input("Enter text to encode: ")
                ecc = input("Choose ECC [rs/hamming] (default=rs): ") or 'rs'
                storage.ecc_method = ecc.lower()
                dna = storage.encode(text.encode('utf-8'))
                print(f"\nEncoded DNA:\n{dna}")
                
            elif choice == '2':
                dna = input("Enter DNA sequence: ").strip().upper()
                ecc = input("Choose ECC used [rs/hamming] (default=rs): ") or 'rs'
                storage.ecc_method = ecc.lower()
                decoded = storage.decode(dna).decode('utf-8', errors='replace')
                print(f"\nDecoded Text:\n{decoded}")
                
            elif choice == '3':
                in_file = input("Input file path: ")
                out_file = input("Output DNA file path: ")
                ecc = input("Choose ECC [rs/hamming] (default=rs): ") or 'rs'
                storage.ecc_method = ecc.lower()
                
                with open(in_file, 'rb') as f:
                    data = f.read()
                
                dna = storage.encode(data)
                with open(out_file, 'w') as f:
                    f.write(dna)
                print(f"File encoded to {out_file}")
                
            elif choice == '4':
                dna_file = input("DNA file path: ")
                out_file = input("Output file path: ")
                ecc = input("Choose ECC used [rs/hamming] (default=rs): ") or 'rs'
                storage.ecc_method = ecc.lower()
                
                with open(dna_file, 'r') as f:
                    dna = f.read().strip()
                
                decoded = storage.decode(dna)
                with open(out_file, 'wb') as f:
                    f.write(decoded)
                print(f"File decoded to {out_file}")
                
            elif choice == '5':
                visualize_mapping()
                print("Visualization window opened!")
                
            elif choice == '6':
                print("Exiting...")
                break
                
            else:
                print("Invalid choice. Please try again.")
                
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please check your input and try again.")

if __name__ == '__main__':
    display_banner()
    interactive_cli()