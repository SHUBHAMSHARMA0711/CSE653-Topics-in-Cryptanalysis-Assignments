# TC-Assignment - 3: Differential Cryptanalysis of Toy Cipher

## Part 1: Implementing the Toy Cipher

### Encryption Process

The encryption function consists of multiple steps:

1. **Key Generation**  
   - The function `generateRoundKeys()` generates **6 random 16-bit round keys**.
   - These keys are uniformly distributed over the 16-bit space.

2. **S-Box Substitution**  
   - The S-Box is a predefined **non-linear transformation** that maps a 4-bit nibble to another 4-bit value.
   - The function `substitute(nibble)` performs this transformation.

3. **Permutation**  
   - The function `permute(bits)` performs a **bitwise permutation** based on a predefined P-Box.
   - The P-Box ensures diffusion by rearranging the bits across rounds.

4. **Encryption Rounds**
   - **Key Mixing:** Each round starts with an **XOR operation** between the current state and the corresponding round key.
   - **Substitution:** Each 4-bit nibble is transformed using the **S-Box**.
   - **Permutation:** The permuted value is calculated before moving to the next round (except for the last round).
   - **Final XOR:** After the last round, the last key is XORed with the state to produce the ciphertext.

### Modification in Encryption Process After GC Comment

In the previous implementation, the state transformation processed nibbles in **LSB to MSB order**, which led to an unintended byte arrangement in the final ciphertext. This issue has been corrected by ensuring that **nibbles are now processed in MSB to LSB order**, preserving the expected encryption behavior and correct output format.

## Part 2: Constructing the Difference Distribution Table (DDT)

### Difference Distribution Table (DDT)

1. **Computing the DDT**
   - The function `computeDDT()` initializes a **16×16 matrix** with zeros.
   - It iterates over all possible **input differences** (`ΔX`) and **input values** (`X`) and records the **output difference** (`ΔY = S[X] ⊕ S[X ⊕ ΔX]`).
   - The table is filled based on these computed values.

2. **Tabular Representation**
   - The DDT is displayed in a formatted table using the `tabulate` library for better readability.


## Part 3: Constructing a Differential Trail for 4 Rounds

### Steps to Construct a Differential Trail

1. **Generating Input Differences**
   - Generated a list of **all possible 4-nibble input differences**, ensuring that only one nibble has a nonzero value.
   - These differences are used as potential starting points for high-probability differential trails.

2. **Computing the Best Trails**
   - For each input difference:
     - The corresponding **output difference** is determined using the **Difference Distribution Table (DDT)** from Part 2.
     - The **probability** of each transition is calculated based on the DDT values and the probabilities are multiplied to get the total probability of the trail.
     - The **number of active S-boxes** is tracked, as fewer active S-boxes typically indicate a better trail and it used in case of a tie in probabilities.

3. **Permutation & Propagation**
   - The output difference after each round is permuted using the **P-Box** to become the next input difference for the next round.
   - This process is repeated for **4 rounds** to construct a complete trail.

4. **Sorting the Trails**
   - The trails are **sorted by highest probability** first and then by the **fewest active S-boxes** to identify the most exploitable trail.


## Part 4: Key Recovery Using Differential Cryptanalysis

### Steps to Recover the Key

1. **Generating Plaintext Pairs**
   - We generate **2¹⁶ plaintext pairs** (`m, m'`) based on the **best differential trail** from Part 3.
   - The pairs are created such that `m' = m ⊕ Δx`, where **Δx** is the input difference of the best trail.
   - Only **unique pairs** are considered.

2. **Encrypting Plaintext Pairs**
   - Each plaintext pair is encrypted using a **fixed 5-round key** to obtain their ciphertexts (`c, c'`).
   - The encryption follows the **Toy Cipher (TC1)** algorithm from Part 1.

3. **Filtering Valid Pairs**
   - We filter out pairs that do not satisfy the expected output difference (`Δy`).
   - The **Difference Distribution Table (DDT)** from Part 2 helps identify valid differences that can propagate through the S-Box.
   - Specifically, we check whether the difference between the ciphertext pairs, `(c ⊕ c')`, falls within the expected values derived (`z` set) from the DDT.
   - If a ciphertext pair does not match an expected difference, it is discarded.
   - This step significantly reduces the number of pairs, ensuring only those that adhere to the differential trail are considered for key recovery.

4. **Recovering Last Non-Zero Nibble of Last Round Key**
   - We initialize **key counters** for all **possible 4-bit keys**.
   - For each candidate key nibble (`k₅`):
     - Compute the **inverse S-Box** transformation for both ciphertexts after XORing with the candidate key nibble.
     - Check if the resulting difference matches the expected output difference **Δy**.
     - If a match is found, increment the counter for that particular key nibble.
   - The key nibble with the **highest count** is chosen as the most probable candidate, as it satisfies the differential property across the highest number of pairs.

5. **Exhaustive Search for Remaining Key Bits**
   - Using the recovered nibble, an **exhaustive search** is performed to determine remaining 12 bits of the last round key.
   - A known plaintext-ciphertext pair is used for verification.
   - The correct key is identified when encryption using the guessed key matches the known ciphertext.
