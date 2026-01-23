class EncodingStrategy:
    def encode(self, binary_data: str) -> str:
        raise NotImplementedError
    def decode(self, dna_sequence: str) -> str:
        raise NotImplementedError
    def bits_per_base(self) -> float:
        raise NotImplementedError
