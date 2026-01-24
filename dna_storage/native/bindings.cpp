#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../../cpp_core/include/dna_core.h"

namespace py = pybind11;

// Helper to convert string (from py::bytes) to vector
std::vector<uint8_t> bytes_to_vector(const std::string& s) {
    return std::vector<uint8_t>(s.begin(), s.end());
}

// Helper to convert vector to bytes
py::bytes vector_to_bytes(const std::vector<uint8_t>& v) {
    return py::bytes(reinterpret_cast<const char*>(v.data()), v.size());
}

PYBIND11_MODULE(dna_native, m) {
    m.doc() = "Native C++ core for DNA Storage";

    m.def("binary_to_dna", [](py::bytes input) {
        return dna_core::binary_to_dna(bytes_to_vector(input));
    }, "Convert binary bytes to DNA string");

    m.def("dna_to_binary", [](std::string dna) {
        return vector_to_bytes(dna_core::dna_to_binary(dna));
    }, "Convert DNA string to binary bytes");
    
    m.def("hamming_encode_dna", [](py::bytes input) {
        return dna_core::hamming_encode_dna(bytes_to_vector(input));
    }, "Hamming Encode (7,4) bytes to DNA");
    
    py::class_<dna_core::HammingDecodeResult>(m, "HammingDecodeResult")
        .def_readonly("corrected", &dna_core::HammingDecodeResult::corrected)
        .def_property_readonly("data", [](const dna_core::HammingDecodeResult& r) {
            return vector_to_bytes(r.data);
        });
        
    m.def("hamming_decode_dna", [](std::string dna) {
        return dna_core::hamming_decode_dna(dna);
    }, "Hamming Decode (7,4) DNA to bytes");
}