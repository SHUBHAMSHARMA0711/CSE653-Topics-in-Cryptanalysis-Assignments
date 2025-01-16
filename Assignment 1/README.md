# AES-128 Encryption Implementation

This project involves the implementation of the AES-128 encryption algorithm in Python. AES-128 (Advanced Encryption Standard) is a symmetric block cipher widely used for secure data encryption.

## Overview

This code implements the following features:

1. **Key Expansion:** Expands the given 16-byte encryption key into round keys used during encryption.
2. **Byte Substitution (SubBytes):** Substitutes bytes in the block using the AES S-Box.
3. **Shift Rows:** Shifts rows of the state matrix to the left by varying offsets.
4. **Mix Columns:** Applies a linear transformation to mix the columns of the state matrix.
5. **Add Round Key:** XORs the current block with a round key.
6. **Padding:** Implements PKCS#7 padding for plaintext messages shorter than the block size (16 bytes).
7. **Encryption:** Combines all the steps into a full AES-128 encryption process.


## How It Works

1. **Key Input:** The user provides a 16-byte encryption key. If the key length is not 16 bytes, an error is raised.
2. **Rounds Configuration:** The user specifies the number of encryption rounds (default is 10 for AES-128).
3. **Plaintext Input:** The user enters the plaintext message to encrypt.
4. **Encryption Process:**
   - If the plaintext length is not a multiple of 16 bytes, it is padded using PKCS#7.
   - The AES encryption process is applied block-by-block.
   - The encrypted ciphertext is output as a hexadecimal string.

## Usage

1. Run the script using Python 3.x:

   ```bash
   python AES.py
   ```

2. Follow the prompts:
   - Enter a 16-character encryption key.
   - Specify the number of rounds (default for AES-128 is 10).
   - Enter the plaintext message to encrypt.

3. The script will output the ciphertext as a hexadecimal string.

### Example

```bash
--------------------AES-128 Encryption--------------------

Enter Encryption Key: mysecretkey12345
Enter number of rounds: 10
Enter Plain Text to Encrypt: Hello, AES-128!!

CipherText: 91fc3164f284dae2c0c9edeb987e1485
```

## Implementation Details

### Constants
- **S-Box:** A predefined substitution box for byte substitution.
- **Mix Columns Matrix:** The fixed matrix used in the Mix Columns transformation.
- **RCON:** Round constants for the key schedule.

### Key Functions

1. **`keyExpansion`:** Generates the round keys based on the initial key.
2. **`substituteBlock`:** Substitutes bytes in the block using the S-Box.
3. **`shiftRows`:** Performs the row shift operation.
4. **`mixColumns`:** Mixes the columns of the block using matrix multiplication.
5. **`addRoundKey`:** XORs the block with the round key.
6. **`pad`:** Pads the plaintext to a multiple of the block size.
7. **`encrypt`:** Combines all the steps to encrypt the plaintext.

## Possible Optimizations

1. **NumPy Optimization:** Use NumPy for matrix operations to improve performance.
2. **Parallelization:** Implement parallel processing for encryption of multiple blocks.
    - For example, on a multi-core system use the `threading` library to encrypt multiple blocks concurrently if the length of the plaintext is large.
3. **Numba JIT Compilation:** Numba is an open source JIT compiler that translates a subset of Python and NumPy code into fast machine code. It can be used to optimize the performance of the encryption algorithm.
   - This can be done by adding the `@numba.jit` decorator to the functions that perform the encryption steps.
4. **Loop Unrolling:** Manually unroll loops to reduce the overhead of loop control.
   - For example in the `mixColumns` function, the loop can be unrolled to directly calculate the matrix multiplication.