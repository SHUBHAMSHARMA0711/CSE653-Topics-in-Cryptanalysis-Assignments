import random


class TC:

    NUM_ROUNDS = 5

    S_BOX = [0x6, 0x4, 0xC, 0x5, 0x0, 0x7, 0x2, 0xE,
             0x1, 0xF, 0x3, 0xD, 0x8, 0xA, 0x9, 0xB]

    P_BOX = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

    def generateRoundKeys(self):
        '''Generate random round keys.'''

        # return [0x1111, 0x2222, 0x3333, 0x4444, 0x5555, 0x6666]
        return [random.randint(0, 0xFFFF) for _ in range(6)]

    def substitute(self, nibble):
        '''Perform S-box substitution.'''

        return self.S_BOX[nibble]

    def permute(self, bits):
        '''Perform bit-level permutation.'''

        return sum(((bits >> i) & 1) << self.P_BOX[i] for i in range(16))

    def encrypt(self, plaintext, round_keys):
        '''Encrypt plaintext with given round keys.'''

        state = plaintext

        for i in range(self.NUM_ROUNDS):
            state ^= round_keys[i]  # XOR with round key

            y3 = self.substitute((state >> 12) & 0xF) << 12
            y2 = self.substitute((state >> 8) & 0xF) << 8
            y1 = self.substitute((state >> 4) & 0xF) << 4
            y0 = self.substitute((state >> 0) & 0xF) << 0

            state = y3 | y2 | y1 | y0

            if i < self.NUM_ROUNDS - 1:
                state = self.permute(state)  # Permutation before next round

        return state ^ round_keys[-1]


if __name__ == "__main__":

    TC = TC()
    plaintext = 0x1234
    round_keys = TC.generateRoundKeys()
    ciphertext = TC.encrypt(plaintext, round_keys)

    print(f"\nPlaintext : {hex(plaintext)}")
    print(f"Ciphertext: {hex(ciphertext)}")
    print(f"Random Round Keys: {[hex(i) for i in round_keys]}\n")
