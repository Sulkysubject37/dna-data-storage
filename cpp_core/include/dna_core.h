#pragma once
#include <cstdint>
#include <vector>
#include <string>

namespace dna_core {

    std::string binary_to_dna(const std::vector<uint8_t>& data);
    std::vector<uint8_t> dna_to_binary(const std::string& dna);

    // Hamming ECC (7,4)
    std::string hamming_encode_dna(const std::vector<uint8_t>& data);

    struct HammingDecodeResult {
        std::vector<uint8_t> data;
        bool corrected;
    };

    HammingDecodeResult hamming_decode_dna(const std::string& dna);

    // Packed DNA (2-bit per base)
    std::vector<uint8_t> pack_dna(const std::string& dna);
    std::string unpack_dna(const std::vector<uint8_t>& packed, size_t length);

    // Parallel Batch APIs
    std::vector<std::string> hamming_encode_batch(const std::vector<std::vector<uint8_t>>& batch, int threads=0);
    std::vector<HammingDecodeResult> hamming_decode_batch(const std::vector<std::string>& batch, int threads=0);

}