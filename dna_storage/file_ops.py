from .binary_to_dna import bytes_to_binary, binary_to_dna_sequence, dna_sequence_to_binary, binary_to_bytes
from .ecc import ECC
from .metadata import MetadataManager

class DNAStorage:
    def __init__(self, ecc_method='rs', nsym=10):
        self.ecc_method = ecc_method
        self.nsym = nsym
        
    def _encode_body(self, data_bytes):
        """Internal method to encode data body."""
        # Error Correction
        if self.ecc_method == 'rs':
            encoded_bytes = ECC.rs_encode(data_bytes, self.nsym)
            # Convert to DNA
            binary = bytes_to_binary(encoded_bytes)
            return binary_to_dna_sequence(binary)
        elif self.ecc_method == 'hamming':
            binary = bytes_to_binary(data_bytes)
            encoded_bits = ECC.hamming_encode(binary)
            return binary_to_dna_sequence(encoded_bits)
        else:
            # No ECC
            binary = bytes_to_binary(data_bytes)
            return binary_to_dna_sequence(binary)

    def _decode_body(self, dna_sequence):
        """Internal method to decode data body."""
        binary = dna_sequence_to_binary(dna_sequence)
        
        if self.ecc_method == 'rs':
            data_bytes = binary_to_bytes(binary)
            return ECC.rs_decode(data_bytes, self.nsym)
        elif self.ecc_method == 'hamming':
            decoded_bits = ECC.hamming_decode(binary)
            return binary_to_bytes(decoded_bits)
        else:
            return binary_to_bytes(binary)

    def encode(self, data_bytes):
        """
        Encodes data with a metadata header.
        Structure: [LengthPrefix(16 bases)][HeaderDNA][BodyDNA]
        """
        # 1. Encode Body
        body_dna = self._encode_body(data_bytes)
        
        # 2. Create Header
        ecc_params = {"nsym": self.nsym} if self.ecc_method == 'rs' else {}
        header_dna = MetadataManager.create_header_dna(self.ecc_method, ecc_params)
        
        # 3. Create Prefix
        prefix_dna = MetadataManager.encode_length_prefix(len(header_dna))
        
        return prefix_dna + header_dna + body_dna

    def decode(self, dna_sequence):
        """
        Decodes data, parsing the metadata header to determine settings.
        """
        # 1. Parse Prefix
        prefix_len = 16 # 4 bytes * 4 bases/byte
        if len(dna_sequence) < prefix_len:
            raise ValueError("Data too short to contain header prefix")
            
        prefix_dna = dna_sequence[:prefix_len]
        header_len = MetadataManager.decode_length_prefix(prefix_dna)
        
        # 2. Parse Header
        total_header_end = prefix_len + header_len
        if len(dna_sequence) < total_header_end:
             raise ValueError("Data too short to contain header")
             
        header_dna = dna_sequence[prefix_len:total_header_end]
        metadata = MetadataManager.parse_header_dna(header_dna)
        
        # 3. Configure from Metadata
        # Update instance state to match the file's settings
        self.ecc_method = metadata.get('ecc', 'rs')
        params = metadata.get('ecc_params', {})
        if self.ecc_method == 'rs':
            self.nsym = params.get('nsym', 10)
            
        # 4. Decode Body
        body_dna = dna_sequence[total_header_end:]
        return self._decode_body(body_dna)
