# Error Correction Codes (ECC)

## Reed-Solomon (RS)
- **Overview**: A block-based error correction code widely used in storage systems (CD/DVD, QR codes).
- **Implementation**: Uses the `reedsolo` Python library.
- **Parameters**: `nsym` (number of symbol errors correctable). Default is 10 bytes overhead per block.
- **Capabilities**: Can correct up to `nsym/2` byte errors per block. Handles burst errors well.

## Hamming Code
- **Overview**: A simple linear error-correcting code.
- **Implementation**: Custom Hamming(7,4).
- **Capabilities**: Corrects single-bit errors. Detects (but cannot correct) two-bit errors.
- **Limitations**: 
  - Cannot handle insertions or deletions.
  - Efficient only for sparse random errors.
  - Less robust than RS for large data.

## Design Decisions
- **RS** is the default for reliability.
- **Hamming** is provided for educational purposes and low-overhead requirements where only single-bit flips are expected.
- **Header Protection**: The file header is always protected with RS to ensure metadata can be recovered even if the body is corrupted.

## Limitations
- Neither method handles major insertions/deletions (DNA synthesis errors) without external synchronization markers.
- Large burst errors exceeding RS capacity will corrupt the chunk.
