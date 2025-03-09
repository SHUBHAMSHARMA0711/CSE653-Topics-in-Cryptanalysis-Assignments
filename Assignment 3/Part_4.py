import tqdm
import random
from Part_1 import TC
from Part_2 import DDT
from Part_3 import ConstructDifferentialTrails


class KeyRecovery:

    def __init__(self):

        self.keys = set()
        __S_BOX = TC.S_BOX
        self.pairs = 2 ** 16
        self.num_keys = 2 ** 4
        self.plain_textss = set()
        self.cipher_texts = set()
        self.INV_S_BOX = [__S_BOX.index(i) for i in range(16)]
        self.diff = ConstructDifferentialTrails().getBestTrail()[0]
        self.key = [0x1111, 0x2222, 0x3333, 0x4444, 0x5555, 0x6666]

        self.generatePlaintexts()
        self.generateRandomKeys()
        self.queryOracle()
        self.filter()

    def generatePlaintexts(self):
        '''Generate self.pairs unique plaintext pairs.'''

        print(f"\nGenerating {self.pairs} Plaintext Pairs...\n")

        pbar = tqdm.tqdm(total=self.pairs,
                         desc="Generating Plaintexts", colour="green")

        while len(self.plain_textss) < self.pairs:
            m = random.randint(0, 0xFFFF)
            m_prime = m ^ int("".join(map(str, self.diff)), 16)

            if (m, m_prime) not in self.plain_textss:
                self.plain_textss.add((m, m_prime))
                pbar.update(1)

        pbar.close()

        print(f"\nGenerated {len(self.plain_textss)} Plaintext Pairs.\n")

    def generateRandomKeys(self):
        '''Generate 2^16 unique keys.'''

        while len(self.keys) < self.num_keys:
            self.keys.add(random.randint(0, 0xF))

        print(f"\nGenerated {len(self.keys)} Random Keys.\n")

    def queryOracle(self):
        '''Encrypt all plaintext pairs using the fixed key.'''

        print("\nQuerying the Oracle...\n")

        for m, m_prime in tqdm.tqdm(self.plain_textss, desc="Querying Oracle", colour="green"):
            self.cipher_texts.add(
                (TC().encrypt(m, self.key), TC().encrypt(m_prime, self.key)))

        print(
            f"\nEncrypted {len(self.cipher_texts)} Plaintext Pairs to Generate Ciphertexts.\n")

    def filter(self):
        '''Filter out ciphertext pairs that do not satisfy the differential property.'''

        print("\nFiltering Invalid Pairs...\n")

        valid_pairs = []

        z = {i for i in range(16) if DDT().computeDDT()[sum(self.diff)][i] > 0}

        for c, c_prime in tqdm.tqdm(self.cipher_texts, desc="Filtering Pairs", colour="green"):
            if ((c ^ c_prime) & 0xFFF0) == 0 and ((c ^ c_prime) & 0xF) in z:
                valid_pairs.append((c, c_prime))

        print(
            f"\nFiltered {len(self.cipher_texts) - len(valid_pairs)} Invalid Pairs.")
        print(f"Remaining {len(valid_pairs)} Valid Pairs.\n")

        self.cipher_texts = valid_pairs

    def recoverKey(self):
        '''Recover the last round key using differential cryptanalysis.'''

        print("\nRecovering the Non-Zero Nibble of the Last Round Key...\n")

        key_counters = {k: 0 for k in self.keys}

        for c, c_prime in tqdm.tqdm(self.cipher_texts, desc="Recovering Key", colour="green"):
            for key in self.keys:
                v = self.INV_S_BOX[(c ^ key) & 0xF]
                v_prime = self.INV_S_BOX[(c_prime ^ key) & 0xF]

                if v ^ v_prime == int("".join(map(str, self.diff)), 16):
                    key_counters[key] += 1

        nibble = max(key_counters, key=key_counters.get)

        print(f"\nRecovered Nibble: {hex(nibble)}\n")

        return self.__exhaustiveSearch(nibble)

    def __exhaustiveSearch(self, nibble):
        '''Exhaustively search for the last key nibbles.'''

        print("\nExhaustively Searching for the Last Key Nibble...\n")

        cipher_text = TC().encrypt(0x1234, self.key)

        for i in tqdm.tqdm(range(16), desc="Exhaustive Search Progress", colour="green"):
            for j in range(16):
                for k in range(16):
                    lastKey = int(f"{i:X}{j:X}{k:X}{nibble:X}", 16)
                    key = [0x1111, 0x2222, 0x3333, 0x4444, 0x5555, lastKey]

                    if TC().encrypt(0x1234, key) == cipher_text:
                        return lastKey

        print("\nKey not found!\n")


if __name__ == "__main__":

    print(f"\nRecovered Key: {hex(KeyRecovery().recoverKey())}\n")
