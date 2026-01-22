import reedsolo
import math
from .hamming import hamming_encode as h_encode, hamming_decode as h_decode

class ECC:
    @staticmethod
    def hamming_encode(data_bits_str):
        """
        Adapter for Hamming(7,4) encoding.
        Input: Binary string '0101...'
        Output: Encoded binary string '0101...'
        """
        # Convert string '01' to list [0, 1]
        bits = [int(c) for c in data_bits_str]
        encoded_bits = h_encode(bits)
        # Convert list [0, 1] back to string '01'
        return ''.join(str(b) for b in encoded_bits)

    @staticmethod
    def hamming_decode(encoded_bits_str):
        """
        Adapter for Hamming(7,4) decoding.
        Input: Binary string '0101...'
        Output: Decoded binary string '0101...'
        """
        bits = [int(c) for c in encoded_bits_str]
        decoded_bits, corrected = h_decode(bits)
        return ''.join(str(b) for b in decoded_bits)

    @staticmethod
    def rs_encode(data_bytes, nsym=10):
        rs = reedsolo.RSCodec(nsym)
        return rs.encode(data_bytes)

    @staticmethod
    def rs_decode(encoded_bytes, nsym=10):
        rs = reedsolo.RSCodec(nsym)
        return rs.decode(encoded_bytes)[0]

    @staticmethod
    def calculate_encoded_length(data_bytes_len, method, params):
        if method == 'rs':
            nsym = params.get('nsym', 10)
            return data_bytes_len + nsym
        elif method == 'hamming':
            # Input bits
            bits = data_bytes_len * 8
            # Blocks (4 bits per block)
            blocks = math.ceil(bits / 4)
            # Output bits (7 bits per block)
            out_bits = blocks * 7
            # Output bytes (ceil(out_bits / 8))
            return math.ceil(out_bits / 8)
        else:
            return data_bytes_len