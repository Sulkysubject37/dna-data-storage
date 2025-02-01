import reedsolo

class ECC:
    @staticmethod
    def hamming_encode(data_bits):
        # Hamming code implementation from previous answer
        return encoded_bits

    @staticmethod
    def hamming_decode(encoded_bits):
        # Hamming decode implementation from previous answer
        return decoded_bits

    @staticmethod
    def rs_encode(data_bytes, nsym=10):
        rs = reedsolo.RSCodec(nsym)
        return rs.encode(data_bytes)

    @staticmethod
    def rs_decode(encoded_bytes, nsym=10):
        rs = reedsolo.RSCodec(nsym)
        return rs.decode(encoded_bytes)[0]