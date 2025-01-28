# TC-Assignment-2: Exhaustive Search and TMTO Attack on a TOY CIPHER (TC)

## Overview

This Assignment is the  implementation of a simplified encryption system called Toy Cipher (TC) and demonstrates two key recovery techniques:

1. **Exhaustive Search**: Brute-force method to recover encryption keys.
2. **Time-Memory Trade-Off (TMTO) Attack**: Efficient precomputation-based method for key recovery.

The code is written in C++ and includes the following components:

- Implementation of Toy Cipher encryption.
- Exhaustive key search.
- Offline and Online phases of the TMTO attack.

---

## Code Breakdown

### Part 1: Toy Cipher (TC) Implementation

#### Sub-Components

1. **Add Roundkey (AR)**
   - XORs the input state with the round key.

2. **S-Box Layer (SB)**
   - Applies a substitution box (S-Box) to each element of the input state.

3. **Linear Mixing (LM)**
   - Computes XOR of all input elements and mixes the result back into the state.

4. **Encryption Round**
   - Performs one round of AR, SB, and LM transformations.

5. **Full Encryption**
   - Iteratively applies 10 encryption rounds to the plaintext using a fixed key.

---

### Part 2: Exhaustive Search for Key Recovery

- **Objective**: Recover the key by brute-forcing all possible key combinations.
- **Implementation**:
  - Iterates through all possible values (0 to 255) for each key byte.
  - For simplicity, the first of key is fixed to `0x00` and we have to find the remaining 3 bytes exhaustively.
  - Compares the encrypted output with the given ciphertext to identify the correct key.

Test Case 1:
```bash
Plaintext: 0, 0, 0, 0
Ciphertext: 180, 31, 145, 240
Key: 0, 2, 3, 4
```

Test Case 2:
```bash
Plaintext: 1, 2, 3, 4
Ciphertext: 228, 99, 105, 79
Key: 0, 2, 3, 4
```
---

### Part 3: Time-Memory Trade-Off (TMTO) Attack

#### Offline Phase

1. **Random Key Generation**:
   - Generates unique random keys for precomputing encryption chains.
   - Uses `random_device` and `mt19937` for random number generation.
2. **Table Generation**:
   - Generated the TMTO table for `m = 2^16` and `t = 2^16`, where `m` is the number of chains and `t` is the chain length.
   - Computes encryption chains of fixed length (`t`).
   - Stores starting and ending points of each chain in a table.
3. **File Persistence**:
   - Saves the table to a file (`table.txt`) for reuse.

#### Online Phase

1. **Search for Key**:
   - It starts with given ciphertext as a key.
   - It iterates for each value of `t`.
   - In each iteration, it checks in table, if the current value is matching with any ending points from the table.
   - If there is any match then it reconstructs chains to recover the encryption key.
   - If no match is found, it moves to the next value of `t`.

---

## Helper Functions

- **`vectorToString`**: Converts `vector<int>` to a comma-separated string.
- **`stringToVector`**: Parses a comma-separated string into `vector<int>`.
- **`randomKeyGenerator`**: Generates unique random keys.

---

## Usage


1. **Compile the Code**
   ```sh
   g++ A2.cpp -o A2
   ```

2. **Run the Program**
     ```sh
     ./A2
     ```
