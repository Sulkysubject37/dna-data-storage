# Encoding & Decoding

## Binary to DNA Mapping
The system uses a simple 2-bit mapping:
- `00` -> `A`
- `01` -> `T`
- `10` -> `C`
- `11` -> `G`

## File Format Structure
The encoded DNA file has the following structure:

1.  **Length Prefix**: Fixed 16 bases (32 bits) encoding the length of the Header.
2.  **Header**: Variable length DNA segment containing metadata (JSON).
3.  **Body**: Concatenation of encoded chunks.

### Header
The header is encoded using Reed-Solomon (nsym=10) for robustness. It contains:
- `version`: Format version.
- `ecc`: ECC method ('rs' or 'hamming').
- `ecc_params`: Parameters for the ECC.
- `chunk_size`: Size of data chunks (before encoding).
- `total_chunks`: Number of chunks.

### Chunking
The input file is split into chunks of `chunk_size` (default 128 bytes).
Each chunk is wrapped in a packet:
`[Index (4 bytes)][Length (4 bytes)][Checksum (4 bytes)][Payload]`

This packet is then ECC-encoded and converted to DNA.

## Decoding Flow
1.  Read the first 16 bases to determine Header Length.
2.  Read and decode the Header.
3.  Configure the decoder based on Header metadata.
4.  Read the Body stream.
5.  Split Body into segments corresponding to chunks.
6.  Decode each segment, verify checksum and index.
7.  Reassemble the original file.
