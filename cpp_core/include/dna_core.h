#pragma once
#include <cstdint>
#include <vector>
#include <string>

namespace dna_core {

    /**
     * @brief Encodes binary bytes to DNA string using standard 2-bit mapping.
     * 00->A, 01->T, 10->C, 11->G
     * 
     * @param data Input binary data
     * @return std::string DNA sequence (4 chars per input byte)
     */
    std::string binary_to_dna(const std::vector<uint8_t>& data);

    /**
     * @brief Decodes DNA string to binary bytes.
     * 
     * @param dna Input DNA sequence (length must be multiple of 4)
     * @return std::vector<uint8_t> Decoded binary data
     */
    std::vector<uint8_t> dna_to_binary(const std::string& dna);

    /**
     * @brief Hamming(7,4) Encode.
     * Takes packed bytes, expands to Hamming codewords.
     * 
     * @param data Input data
     * @return std::vector<uint8_t> Encoded data (packed)
     */
    std::vector<uint8_t> hamming_encode(const std::vector<uint8_t>& data);

    struct HammingDecodeResult {
        std::vector<uint8_t> data;
        bool corrected;
    };

    /**
     * @brief Hamming(7,4) Decode with single-bit correction.
     * 
     * @param encoded Encoded data (packed)
     * @return HammingDecodeResult Decoded data and correction status
     */
    HammingDecodeResult hamming_decode(const std::vector<uint8_t>& encoded);

}
