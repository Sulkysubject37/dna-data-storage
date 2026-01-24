#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../../cpp_core/include/dna_core.h"

namespace py = pybind11;

PYBIND11_MODULE(dna_native, m) {
    m.doc() = "Native C++ core for DNA Storage";

    m.def("binary_to_dna", &dna_core::binary_to_dna, "Convert binary bytes to DNA string");
    m.def("dna_to_binary", &dna_core::dna_to_binary, "Convert DNA string to binary bytes");
    
    m.def("hamming_encode_dna", &dna_core::hamming_encode_dna, "Hamming Encode (7,4) bytes to DNA");
    
    py::class_<dna_core::HammingDecodeResult>(m, "HammingDecodeResult")
        .def_readonly("data", &dna_core::HammingDecodeResult::data)
        .def_readonly("corrected", &dna_core::HammingDecodeResult::corrected);
        
    m.def("hamming_decode_dna", &dna_core::hamming_decode_dna, "Hamming Decode (7,4) DNA to bytes");
}
