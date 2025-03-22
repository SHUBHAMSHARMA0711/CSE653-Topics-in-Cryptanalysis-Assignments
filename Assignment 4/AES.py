import numpy as np

S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

MIX_COLUMN_MATRIX = [
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2]]

RCON = [
    [0x01, 0x00, 0x00, 0x00],
    [0x02, 0x00, 0x00, 0x00],
    [0x04, 0x00, 0x00, 0x00],
    [0x08, 0x00, 0x00, 0x00],
    [0x10, 0x00, 0x00, 0x00],
    [0x20, 0x00, 0x00, 0x00],
    [0x40, 0x00, 0x00, 0x00],
    [0x80, 0x00, 0x00, 0x00],
    [0x1b, 0x00, 0x00, 0x00],
    [0x36, 0x00, 0x00, 0x00]]


class AES128():

    def __init__(self, key, words=4, rounds=10):

        self.key = key
        self.words = words
        self.rounds = rounds
        self.roundKeys = self.keyExpansion(self.key)

    
    def keyExpansion(self, key):

        '''Key Expansion for AES-128'''

        if len(key) != 16: 
            raise ValueError("Key length must be 16 bytes")

        words = []
        key = [ord(i) for i in key]

        '''Divide key into 4 words'''

        for i in range(self.words):
            words.append(key[4 * i : 4 * (i + 1)])

        '''Generate 4*(rounds+1) words'''

        for i in range(self.words, 4 * (self.rounds + 1)):
            temp = words[i - 1]

            '''Rotate the word if it is a multiple of the key size
                then substitute the word with S_BOX values and XOR with RCON'''
            
            if i % self.words == 0:
                temp = [S_BOX[b] for b in (temp[1:] + temp[:1])]
                temp = [t ^ r for t, r in zip(temp, RCON[i // self.words - 1])]

            elif self.words > 6 and i % self.words == 4:
                temp = [S_BOX[b] for b in temp]

            words.append([words[i - self.words][j] ^ temp[j] for j in range(4)])

        return words

    
    def substituteBlock(self, message):

        '''Substitute message block with S_BOX values'''

        return [S_BOX[message[i]] for i in range(16)]

    
    def shiftRows(self, message):

        '''Shift rows of the message block by 0, 1, 2, 3 bytes'''

        return [
            message[0], message[5], message[10], message[15],
            message[4], message[9], message[14], message[3],
            message[8], message[13], message[2], message[7],
            message[12], message[1], message[6], message[11]]

    
    def mixColumns(self, message):
        
        '''Mix columns of the message block using MIX_COLUMN_MATRIX'''

        res = np.zeros((4, 4), dtype=int)
        message = np.array(message).reshape(4, 4).T

        '''These nested loops implement the MixColumns step of the AES algorithm.
            The MixColumns transformation is performed in the Galois Field (GF(2^8)).
                For each column of the message matrix, the elements are mixed using the MIX_COLUMN_MATRIX.'''

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    if MIX_COLUMN_MATRIX[i][k] == 1:
                        res[i][j] ^= message[k][j]

                    elif MIX_COLUMN_MATRIX[i][k] == 2:
                        res[i][j] ^= (message[k][j] << 1) ^ (0x1B if message[k][j] & 0x80 else 0)

                    else:
                        res[i][j] ^= message[k][j] ^ ((message[k][j] << 1) ^ (0x1B if message[k][j] & 0x80 else 0))

                res[i][j] &= 0xFF

        return res.T.flatten().tolist()

    
    def addRoundKey(self, message, key):

        '''Add round key to the message block'''

        return [message[i] ^ key[i] for i in range(16)]
    
    
    def pad(self, extraMessage):

        '''Pad the message block with extra bytes'''

        return extraMessage + (16 - len(extraMessage) % 16) * chr(16 - len(extraMessage) % 16)

    
    def encrypt(self, plainMessage):
        
        cipher = ""

        '''Encrypting the plain message block by block
            for each block, substitute, shift rows, mix columns and add round key in n-1 rounds
                for last round, substitute, shift rows and add round key'''

        for i in range(0, len(plainMessage), 16):
            extraMessage = self.pad(plainMessage[i: i + 16])

            '''Initial round key addition'''
            message = self.addRoundKey(
                bytearray(extraMessage, 'latin-1'), sum(self.roundKeys[:4], []))

            '''n rounds'''
            for i in range(0, self.rounds):
                message = self.substituteBlock(message)
                message = self.shiftRows(message)
                message = self.mixColumns(message)
                message = self.addRoundKey(message, sum(self.roundKeys[4 * i : 4 * (i + 1)], []))

            cipher += "".join([hex(i)[2:].zfill(2) for i in message])

        return cipher


if __name__ == "__main__":
    
    print("\n" + "-" * 20 + "AES-128 Encryption" + "-" * 20 + "\n")

    aes = AES128(input("Enter Encryption Key: "), rounds=int(input("Enter number of rounds: ")))
    print(f"\nCipherText: {aes.encrypt(input('Enter Plain Text to Encrypt: '))}\n")
