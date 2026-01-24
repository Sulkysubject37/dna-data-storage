#pragma once
#include <cstdint>
#include <vector>
#include <string>

namespace dna_core {

    std::string binary_to_dna(const std::vector<uint8_t>& data);
    std::vector<uint8_t> dna_to_binary(const std::string& dna);

    // Hamming ECC (7,4)
    // Encodes data bytes -> Hamming Bits -> DNA string.
    // 1 byte -> 2 nibbles -> 14 bits -> 7 bases.
    std::string hamming_encode_dna(const std::vector<uint8_t>& data);

    struct HammingDecodeResult {
        std::vector<uint8_t> data;
        bool corrected;
    };

    // Decodes DNA -> Hamming Bits -> Data bytes.
    HammingDecodeResult hamming_decode_dna(const std::string& dna);

    // Packed DNA (2-bit per base)
    // 1 byte stores 4 bases.
    std::vector<uint8_t> pack_dna(const std::string& dna);
    std::string unpack_dna(const std::vector<uint8_t>& packed, size_t length);

}
