import tabulate
from Part_1 import TC


class DDT:

    def __init__(self):
        self.S_BOX = TC.S_BOX

    def computeDDT(self):
        '''Construct the Difference Distribution Table (DDT) for S-box.'''

        # Initialized a 16x16 table with zeros
        DDT = [[0] * 16 for _ in range(16)]

        '''Iterate over all possible input differences 
                and inputs and increment the count in the DDT'''

        for i in range(16):
            for j in range(16):
                DDT[i][self.S_BOX[j] ^ self.S_BOX[i ^ j]] += 1

        return DDT


if __name__ == "__main__":

    print("\nDifference Distribution Table (DDT):-\n")

    header = ["X"] + [f"{i:X}" for i in range(16)]
    table = [[f"{i:X}"] + row for i, row in enumerate(DDT().computeDDT())]

    print(tabulate.tabulate(table, header, tablefmt="pretty", numalign="center"))
