import json
import struct
from ..binary_to_dna import bytes_to_binary, binary_to_dna_sequence, dna_sequence_to_binary, binary_to_bytes
from ..ecc import ECC

# Fixed constants for Header encoding (Self-describing format requires a bootstrap)
HEADER_ECC_METHOD = 'rs'
HEADER_ECC_NSYM = 10
HEADER_LENGTH_BYTES = 4 # 32-bit integer for header length

class MetadataManager:
    @staticmethod
    def create_header_dna(ecc_method, ecc_params):
        """
        Creates the DNA sequence for the header.
        """
        metadata = {
            "version": "1.0",
            "encoding": "binary_map_2bit",
            "ecc": ecc_method,
            "ecc_params": ecc_params
        }
        json_bytes = json.dumps(metadata, sort_keys=True).encode('utf-8')
        
        # Protect Header with fixed ECC
        try:
            encoded_bytes = ECC.rs_encode(json_bytes, HEADER_ECC_NSYM)
        except Exception as e:
            # Fallback or re-raise? 
            # If header encoding fails (e.g. too small for RS?), we might need padding?
            # RS works on small data too usually.
            raise RuntimeError(f"Failed to encode header: {e}")

        binary = bytes_to_binary(encoded_bytes)
        dna = binary_to_dna_sequence(binary)
        return dna

    @staticmethod
    def parse_header_dna(dna_segment):
        """
        Decodes the header DNA segment into a dictionary.
        """
        try:
            binary = dna_sequence_to_binary(dna_segment)
            data_bytes = binary_to_bytes(binary)
            decoded_bytes = ECC.rs_decode(data_bytes, HEADER_ECC_NSYM)
            return json.loads(decoded_bytes.decode('utf-8'))
        except Exception as e:
            raise ValueError(f"Corrupt or invalid header: {e}")

    @staticmethod
    def encode_length_prefix(length):
        """
        Encodes an integer length into a fixed-width DNA sequence (16 bases for 32-bit int).
        """
        length_bytes = length.to_bytes(HEADER_LENGTH_BYTES, byteorder='big')
        binary = bytes_to_binary(length_bytes)
        return binary_to_dna_sequence(binary)

    @staticmethod
    def decode_length_prefix(dna_prefix):
        """
        Decodes the fixed-width DNA sequence into an integer length.
        """
        if len(dna_prefix) != HEADER_LENGTH_BYTES * 4: # 4 bases per byte ? No, 4 bases = 8 bits? No.
            # 1 byte = 8 bits = 4 bases (00 00 00 00).
            # 4 bytes = 16 bases.
            raise ValueError("Invalid length prefix size")
            
        binary = dna_sequence_to_binary(dna_prefix)
        length_bytes = binary_to_bytes(binary)
        return int.from_bytes(length_bytes, byteorder='big')
