#include "dna_core.h"
#include <stdexcept>
#include <array>

namespace dna_core {

    static const char BIN_TO_DNA[] = {'A', 'T', 'C', 'G'};
    
    static const std::array<uint8_t, 256> create_dna_map() {
        std::array<uint8_t, 256> map;
        map.fill(0xFF);
        map['A'] = 0b00;
        map['T'] = 0b01;
        map['C'] = 0b10;
        map['G'] = 0b11;
        return map;
    }
    static const auto DNA_TO_BIN = create_dna_map();

    std::string binary_to_dna(const std::vector<uint8_t>& data) {
        std::string dna;
        dna.reserve(data.size() * 4);
        
        for (uint8_t b : data) {
            dna.push_back(BIN_TO_DNA[(b >> 6) & 0x03]);
            dna.push_back(BIN_TO_DNA[(b >> 4) & 0x03]);
            dna.push_back(BIN_TO_DNA[(b >> 2) & 0x03]);
            dna.push_back(BIN_TO_DNA[b & 0x03]);
        }
        return dna;
    }

    std::vector<uint8_t> dna_to_binary(const std::string& dna) {
        if (dna.size() % 4 != 0) {
            throw std::invalid_argument("DNA length must be multiple of 4");
        }
        
        std::vector<uint8_t> data;
        data.reserve(dna.size() / 4);
        
        for (size_t i = 0; i < dna.size(); i += 4) {
            uint8_t b = 0;
            for (int j = 0; j < 4; ++j) {
                uint8_t val = DNA_TO_BIN[static_cast<uint8_t>(dna[i+j])];
                if (val == 0xFF) {
                    throw std::invalid_argument("Invalid DNA character");
                }
                b = (b << 2) | val;
            }
            data.push_back(b);
        }
        return data;
    }

    std::vector<uint8_t> hamming_encode(const std::vector<uint8_t>& data) {
        // Placeholder
        return {};
    }

    HammingDecodeResult hamming_decode(const std::vector<uint8_t>& encoded) {
        // Placeholder
        return {{}, false};
    }

}