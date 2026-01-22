from typing import List, Tuple

def hamming_encode_block(data_bits: List[int]) -> List[int]:
    """
    Encodes 4 data bits into 7 bits using Hamming(7,4) code.
    Parity bits are at positions 1, 2, 4 (1-based index).
    
    Layout: p1 p2 d1 p3 d2 d3 d4
    Indices: 0  1  2  3  4  5  6
    """
    if len(data_bits) != 4:
        raise ValueError("Block size must be 4 bits")

    d1, d2, d3, d4 = data_bits

    # Calculate parity bits
    # p1 covers positions 1, 3, 5, 7 -> indices 0, 2, 4, 6
    # p1 + d1 + d2 + d4 = 0 (mod 2)
    p1 = d1 ^ d2 ^ d4

    # p2 covers positions 2, 3, 6, 7 -> indices 1, 2, 5, 6
    # p2 + d1 + d3 + d4 = 0 (mod 2)
    p2 = d1 ^ d3 ^ d4

    # p3 covers positions 4, 5, 6, 7 -> indices 3, 4, 5, 6
    # p3 + d2 + d3 + d4 = 0 (mod 2)
    p3 = d2 ^ d3 ^ d4

    return [p1, p2, d1, p3, d2, d3, d4]

def hamming_decode_block(bits: List[int]) -> Tuple[List[int], bool]:
    """
    Decodes 7 bits into 4 data bits using Hamming(7,4).
    Returns (data_bits, error_corrected).
    
    Note: Hamming(7,4) can correct exactly one bit error.
    It cannot detect double bit errors (they will be miscorrected).
    It cannot handle insertions or deletions (bit slips).
    """
    if len(bits) != 7:
        raise ValueError("Block size must be 7 bits")

    p1, p2, d1, p3, d2, d3, d4 = bits

    # Calculate syndrome
    # s1 checks p1, d1, d2, d4 (indices 0, 2, 4, 6)
    s1 = p1 ^ d1 ^ d2 ^ d4
    
    # s2 checks p2, d1, d3, d4 (indices 1, 2, 5, 6)
    s2 = p2 ^ d1 ^ d3 ^ d4
    
    # s3 checks p3, d2, d3, d4 (indices 3, 4, 5, 6)
    s3 = p3 ^ d2 ^ d3 ^ d4

    syndrome = (s3 << 2) | (s2 << 1) | s1
    error_corrected = False

    if syndrome != 0:
        error_corrected = True
        # Flip the bit at index 'syndrome - 1'
        idx = syndrome - 1
        bits[idx] ^= 1
        
        # Re-extract data bits after correction
        p1, p2, d1, p3, d2, d3, d4 = bits

    return [d1, d2, d3, d4], error_corrected

def hamming_encode(bits: List[int]) -> List[int]:
    """
    Encodes a stream of bits using Hamming(7,4).
    Pads with zeros if input length is not divisible by 4.
    
    LIMITATIONS:
    - Only corrects single-bit errors per 7-bit block.
    - Two bit errors in a block will result in incorrect decoding (aliasing).
    - Does NOT handle insertions or deletions (synchronization errors).
    """
    encoded = []
    # Pad input to multiple of 4
    padding = (4 - (len(bits) % 4)) % 4
    padded_bits = bits + [0] * padding
    
    for i in range(0, len(padded_bits), 4):
        block = padded_bits[i:i+4]
        encoded.extend(hamming_encode_block(block))
        
    return encoded

def hamming_decode(bits: List[int]) -> Tuple[List[int], bool]:
    """
    Decodes a stream of bits using Hamming(7,4).
    
    Returns:
        (decoded_bits, any_error_corrected)
        
    Note: Returns all decoded bits including padding. 
    (Padding removal is the responsibility of the caller/layer above).
    """
    decoded = []
    any_corrected = False
    
    # Check alignment
    if len(bits) % 7 != 0:
        # In a real system we might raise error, but here we process what we can
        # or truncate. Let's raise for now as per "Correctness > performance".
        raise ValueError("Input length must be multiple of 7 for Hamming(7,4)")

    for i in range(0, len(bits), 7):
        block = list(bits[i:i+7]) # Make a copy to mutate
        data, corrected = hamming_decode_block(block)
        decoded.extend(data)
        if corrected:
            any_corrected = True
            
    return decoded, any_corrected
