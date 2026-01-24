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

    // Hamming Internals
    static uint8_t encode_nibble(uint8_t d) {
        uint8_t d1 = (d >> 3) & 1;
        uint8_t d2 = (d >> 2) & 1;
        uint8_t d3 = (d >> 1) & 1;
        uint8_t d4 = (d >> 0) & 1;
        
        uint8_t p1 = d1 ^ d2 ^ d4;
        uint8_t p2 = d1 ^ d3 ^ d4;
        uint8_t p3 = d2 ^ d3 ^ d4;
        
        return (p1 << 6) | (p2 << 5) | (d1 << 4) | (p3 << 3) | (d2 << 2) | (d3 << 1) | d4;
    }

    static uint8_t decode_nibble(uint8_t v, bool& corrected) {
        uint8_t p1 = (v >> 6) & 1;
        uint8_t p2 = (v >> 5) & 1;
        uint8_t d1 = (v >> 4) & 1;
        uint8_t p3 = (v >> 3) & 1;
        uint8_t d2 = (v >> 2) & 1;
        uint8_t d3 = (v >> 1) & 1;
        uint8_t d4 = (v >> 0) & 1;
        
        uint8_t s1 = p1 ^ d1 ^ d2 ^ d4;
        uint8_t s2 = p2 ^ d1 ^ d3 ^ d4;
        uint8_t s3 = p3 ^ d2 ^ d3 ^ d4;
        
        uint8_t syndrome = (s3 << 2) | (s2 << 1) | s1;
        
        if (syndrome != 0) {
            corrected = true;
            // bit_pos to flip. 7 - syndrome.
            // syndrome=1 -> pos=6 (p1).
            // syndrome=7 -> pos=0 (d4).
            int bit_pos = 7 - syndrome;
            v ^= (1 << bit_pos);
            
            d1 = (v >> 4) & 1;
            d2 = (v >> 2) & 1;
            d3 = (v >> 1) & 1;
            d4 = (v >> 0) & 1;
        }
        
        return (d1 << 3) | (d2 << 2) | (d3 << 1) | d4;
    }

    std::string hamming_encode_dna(const std::vector<uint8_t>& data) {
        std::string dna;
        dna.reserve(data.size() * 7);
        for (uint8_t b : data) {
            uint8_t h = encode_nibble((b >> 4) & 0xF);
            uint8_t l = encode_nibble(b & 0xF);
            
            // H6 H5
            dna.push_back(BIN_TO_DNA[(h >> 5) & 0x3]);
            // H4 H3
            dna.push_back(BIN_TO_DNA[(h >> 3) & 0x3]);
            // H2 H1
            dna.push_back(BIN_TO_DNA[(h >> 1) & 0x3]);
            // H0 L6
            dna.push_back(BIN_TO_DNA[((h & 1) << 1) | ((l >> 6) & 1)]);
            // L5 L4
            dna.push_back(BIN_TO_DNA[(l >> 4) & 0x3]);
            // L3 L2
            dna.push_back(BIN_TO_DNA[(l >> 2) & 0x3]);
            // L1 L0
            dna.push_back(BIN_TO_DNA[l & 0x3]);
        }
        return dna;
    }

    HammingDecodeResult hamming_decode_dna(const std::string& dna) {
        if (dna.size() % 7 != 0) {
            throw std::invalid_argument("DNA length must be multiple of 7");
        }
        
        std::vector<uint8_t> data;
        data.reserve(dna.size() / 7);
        bool any_corrected = false;
        
        for (size_t i = 0; i < dna.size(); i += 7) {
            // Read 7 bases -> 14 bits
            // B0: H6 H5
            uint8_t b0 = DNA_TO_BIN[static_cast<uint8_t>(dna[i])];
            uint8_t b1 = DNA_TO_BIN[static_cast<uint8_t>(dna[i+1])];
            uint8_t b2 = DNA_TO_BIN[static_cast<uint8_t>(dna[i+2])];
            uint8_t b3 = DNA_TO_BIN[static_cast<uint8_t>(dna[i+3])];
            uint8_t b4 = DNA_TO_BIN[static_cast<uint8_t>(dna[i+4])];
            uint8_t b5 = DNA_TO_BIN[static_cast<uint8_t>(dna[i+5])];
            uint8_t b6 = DNA_TO_BIN[static_cast<uint8_t>(dna[i+6])];
            
            // Reconstruct H (7 bits)
            // H: b0(2) b1(2) b2(2) b3_high(1)
            uint8_t h = (b0 << 5) | (b1 << 3) | (b2 << 1) | ((b3 >> 1) & 1);
            
            // Reconstruct L (7 bits)
            // L: b3_low(1) b4(2) b5(2) b6(2)
            uint8_t l = ((b3 & 1) << 6) | (b4 << 4) | (b5 << 2) | b6;
            
            uint8_t nib_h = decode_nibble(h, any_corrected);
            uint8_t nib_l = decode_nibble(l, any_corrected);
            
            data.push_back((nib_h << 4) | nib_l);
        }
        
        return {data, any_corrected};
    }

}
