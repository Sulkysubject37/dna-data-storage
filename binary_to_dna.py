binary_to_dna = {
    '00': 'A',
    '01': 'T',
    '10': 'C',
    '11': 'G'
}

dna_to_binary = {v: k for k, v in binary_to_dna.items()}

def bytes_to_binary(data):
    return ''.join(format(byte, '08b') for byte in data)

def binary_to_dna_sequence(binary_data):
    if len(binary_data) % 2 != 0:
        raise ValueError("Binary data length must be even")
    return ''.join(binary_to_dna[binary_data[i:i+2]] for i in range(0, len(binary_data), 2))

def dna_sequence_to_binary(dna_sequence):
    binary = []
    for base in dna_sequence:
        if base not in dna_to_binary:
            raise ValueError(f"Invalid DNA base '{base}' detected")
        binary.append(dna_to_binary[base])
    return ''.join(binary)

def binary_to_bytes(binary_data):
    if len(binary_data) % 8 != 0:
        raise ValueError("Binary data length must be multiple of 8")
    return bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))