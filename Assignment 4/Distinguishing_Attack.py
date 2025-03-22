import os
from AES import AES128
from tabulate import tabulate


class DistinguishingAttack:

    def __init__(self):
        '''Initialize AES with a random key and 3 rounds'''

        self.AES = AES128(os.urandom(16).decode('latin-1'), rounds=3)

    def generatePlaintexts(self):
        '''Generate 256 plaintexts with one active byte (0x00 to 0xFF)'''

        return [bytearray([i] + [0] * 15) for i in range(256)]

    def performAttack(self):
        '''Perform the Distinguishing Attack on the Oracle'''

        tmp = bytearray(16)  # 16 bytes, initialized to 0

        plaintexts = self.generatePlaintexts()

        for plaintext in plaintexts:

            '''Converting plaintext bytes to string then encrypting the 
                    plaintext and converting the ciphertext hex string to bytes'''

            plaintext_str = bytes(plaintext).decode('latin-1')
            ciphertext_hex = self.AES.encrypt(plaintext_str)
            ciphertext = bytearray.fromhex(ciphertext_hex)

            '''XOR the ciphertext with the temporary variable'''

            tmp = [tmp[i] ^ ciphertext[i] for i in range(16)]

        print("\n\033[1;34mXOR Sum of each byte in the Ciphertexts\n\033[0m")
        print(tabulate([[hex(j) for j in tmp[i: i + 4]]
              for i in range(0, 16, 4)], tablefmt="simple_grid", numalign="center"))
        print(
            f"\n\033[1;34mOracle Implements the AES Reduced to Three Rounds:\033[0m \033[1;92m{all(byte == 0 for byte in tmp)}\033[0m\n")


if __name__ == "__main__":

    DistinguishingAttack().performAttack()
