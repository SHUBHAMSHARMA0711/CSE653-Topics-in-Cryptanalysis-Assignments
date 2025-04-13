# TC-Assignment - 5: MD5 Hashing Algorithm Implementation

## Overview

This assignemnt implements the **MD5 hashing algorithm**. It reads a plain-text message from the user and generates a **128-bit (32-character hexadecimal)** MD5 hash. The implementation closely follows the original MD5 specification, manually performing each step of the hashing process without relying on external libraries.

---

## Step-by-Step Explanation

### Step 1: Appending Padding Bits

The first step in the MD5 algorithm is to prepare the message by aligning it to the required length. Padding is added so that the final message length is **64 bits short of a multiple of 512 bits**.

- A **single '1' bit** is appended to the message (represented as `0x80` in byte form).
- This is followed by **enough '0' bits** to ensure that the message becomes congruent to **448 modulo 512 bits**.

This padding guarantees that the message can be evenly split into 512-bit blocks, leaving space for appending the original message length in the next step.

---

### Step 2: Appending Message Length

Once the message is padded, the **original length** of the input (in **bits**) is appended as a **64-bit little-endian integer**.

This allows the MD5 algorithm to preserve information about the message size, which is crucial to ensure consistency across different inputs and environments. It also ensures that the final message length is an **exact multiple of 512 bits**, which is required for block processing.

---

### Step 3: Initialization of MD5 Buffer Values

The MD5 algorithm uses four 32-bit buffers to maintain the running hash values. These buffers are initialized with predefined constants:

- `A = 0x67452301`
- `B = 0xefcdab89`
- `C = 0x98badcfe`
- `D = 0x10325476`

These constants are defined by the MD5 standard and form the **initial state** of the hash computation.

Additionally, a **64-element constant table (K)** is generated using the sine function:

- `K[i] = floor(abs(sin(i + 1)) * 2^32)`

#### Why Static Casting is Used in MD5 Constants Generation?

The sine function returns a `double`, while MD5 requires 32-bit unsigned integers. **Static casting** is used to explicitly convert the result into `unsigned int` to avoid implicit conversions and ensure correctness in the generated constants.

---

### Step 4: Block Processing and Transformation Rounds

The padded message is processed in **512-bit (64-byte) blocks**. Each block is divided into **sixteen 32-bit words** using **little-endian byte order**. The core of the MD5 algorithm is a **transformation function** that operates on each block and modifies the state variables `A`, `B`, `C`, and `D`.

Each 512-bit block undergoes **64 operations**, grouped into four rounds (16 operations each), using different nonlinear functions:

- **Round 1:** `(B & C) | (~B & D)`
- **Round 2:** `(D & B) | (~D & C)`
- **Round 3:** `B ^ C ^ D`
- **Round 4:** `C ^ (B | ~D)`

For each operation:
- A word from the current message block is selected using a round-specific formula.
- The nonlinear function is applied to three of the four state variables.
- The result is added to one of the MD5 constants (`K[i]`), the selected message word, and one of the state variables.
- A **bitwise left rotation** is applied using a predefined shift value.
- The state variables are updated in a cyclic fashion.

#### Why Bitwise AND with 0xFFFFFFFF is Used

To ensure all arithmetic stays within the bounds of 32-bit unsigned integers (as required by MD5), bitwise AND with `0xFFFFFFFF` is applied after additions and rotations. This simulates **modulo 2³²** behavior, ensuring wrap-around on overflow.

After each block is processed, the results are added back into the main buffer variables `A`, `B`, `C`, and `D`.

---

### Step 5: Final Hash Construction

Once all message blocks are processed, the final hash is constructed by concatenating the buffer values `A`, `B`, `C`, and `D` in **little-endian format**. Each 32-bit value is broken down into four bytes and converted into hexadecimal, producing the final **32-character MD5 hash**.

---

## Usage


1. **Compile the Code**
   ```sh
   g++ MD5.cpp -o MD5
   ```

2. **Run the Program**
     ```sh
     ./MD5
     ```
