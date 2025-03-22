# TC-Assignment - 4: Distinguishing Attack with Integral Cryptanalysis against 3-Round AES

This assignment implements a **Distinguishing Attack** using **Integral Cryptanalysis** against a 3-round AES encryption system. The attack exploits the **balanced property** of the AES cipher after 3 rounds, where the XOR sum of ciphertexts for a specific set of plaintexts is zero.

---

## Implementation Overview

The implementation consists of two Python files:

1. **`Distinguishing_Attack.py`**: Performs the distinguishing attack by generating plaintexts, encrypting them, and analyzing the XOR sum of ciphertexts.
2. **`AES.py`**: Implements a 3-round AES encryption system, including key expansion, substitution, shifting, mixing, and round key addition.

---

## Working of the Code

### `Distinguishing_Attack.py`

1. **Initialization**:
   - The `DistinguishingAttack` class initializes a 3-round AES instance with a random key.

2. **Plaintext Generation**:
   - The `generatePlaintexts()` method generates 256 plaintexts, each with one active byte (ranging from `0x00` to `0xFF`) and the remaining 15 bytes set to zero. This ensures that the plaintexts have one byte with **all property**, where byte takes all possible values across the set.

3. **Attack Execution**:
   - The `performAttack()` method encrypts each plaintext using the 3-round AES oracle.
   - It computes the XOR sum of all ciphertexts. Due to the **balanced property** of 3-round AES, the XOR sum of ciphertexts should be zero.
   - If the XOR sum is zero, the oracle is confirmed to implement 3-round AES.

---

### `AES.py`

This file implements the 3-round AES encryption system. The `AES128` class provides the necessary methods for key expansion, substitution, shifting, mixing, and adding round keys.

1. **Key Expansion**:
   - The `keyExpansion()` method generates round keys from the initial encryption key using the AES key schedule.

2. **Encryption Process**:
   - The `encrypt()` method processes the plaintext in blocks:
     - **Initial Round**: Adds the first round key to the plaintext.
     - **Main Rounds**: Performs substitution (`substituteBlock()`), row shifting (`shiftRows()`), column mixing (`mixColumns()`), and round key addition (`addRoundKey()`) for each round.

3. **Helper Methods**:
   - `substituteBlock()`: Applies the AES S-box to each byte of the message block.
   - `shiftRows()`: Shifts the rows of the message block as per AES specifications.
   - `mixColumns()`: Mixes the columns using the AES MixColumns operation.
   - `addRoundKey()`: XORs the message block with the round key.

---

## Integral Cryptanalysis and Balanced Property

The distinguishing attack relies on the **integral property** of AES, specifically the **balanced property** after 3 rounds. Here’s how it works:

1. **Plaintext Set**:
   - A set of 256 plaintexts is generated, where one byte varies across all 256 values (all property), and the remaining bytes are constant.

2. **Encryption**:
   - Each plaintext is encrypted using the 3-round AES oracle.

3. **XOR Sum**:
   - The XOR sum of all ciphertexts is computed. For 3-round AES, this sum should be zero due to the balanced property.

4. **Distinguishing**:
   - If the XOR sum is zero, the oracle is confirmed to implement 3-round AES. Otherwise, it is likely a random permutation.

---

## Code Workflow

1. The `DistinguishingAttack` class initializes the AES oracle.
2. It generates 256 plaintexts with one active byte.
3. Each plaintext is encrypted, and the ciphertexts are XORed together.
4. The final XOR sum is checked to determine if the oracle implements 3-round AES.

---

## Running the Code

To execute the distinguishing attack, run the following command:
```bash
pip install tabulate
```
```bash
python Distinguishing_Attack.py
