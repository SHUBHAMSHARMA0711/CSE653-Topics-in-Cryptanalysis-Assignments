from Part_1 import TC
from Part_2 import DDT


class ConstructDifferentialTrails:

    def __init__(self):

        self.trails = []
        self.DDT = DDT().computeDDT()
        self.input_diffs = self.generateInputDiffs()

    def generateInputDiffs(self):
        '''Generate all valid input pairs.'''

        input_diffs = []

        for i in range(1, 16):
            input_diffs.append((0, 0, 0, i))
            input_diffs.append((0, 0, i, 0))
            input_diffs.append((0, i, 0, 0))
            input_diffs.append((i, 0, 0, 0))

        return input_diffs

    def tupleToInt(self, diff):
        '''Convert 4-nibble tuple to 16-bit integer.'''

        return (diff[0] << 12) | (diff[1] << 8) | (diff[2] << 4) | (diff[3] << 0)

    def intToTuple(self, diff):
        '''Convert 16-bit integer to 4-nibble tuple.'''

        return ((diff >> 12) & 0xF, (diff >> 8) & 0xF, (diff >> 4) & 0xF, (diff >> 0) & 0xF)

    def constructTrails(self):
        '''Construct differential trails for the given DDT.'''

        for inp_diff in self.input_diffs:
            total_sboxes = 0
            probability = 1.0
            trail = [inp_diff]

            current_diff = self.tupleToInt(inp_diff)

            for _ in range(4):
                round_prob = 1
                active_sboxes = 0
                output_diff = [0] * 4

                '''Extract 4-bit nibbles from the input difference,
                        find the maximum probability in the DDT, and calculate the output difference.'''

                for i in range(4):
                    inn = (current_diff >> (4 * (3 - i))) & 0xF

                    if inn != 0:
                        active_sboxes += 1
                        maxi = max(self.DDT[inn])
                        round_prob *= maxi / 16
                        out = self.DDT[inn].index(maxi)

                    else:
                        out = 0

                    output_diff[i] = out

                probability *= round_prob
                total_sboxes += active_sboxes

                '''Aftter permuting the output difference, convert it to a 4-nibble tuple 
                    and append it to the trail to get the next input difference'''

                trail.append(self.intToTuple(current_diff := TC().permute(
                    self.tupleToInt(tuple(output_diff)))))

            self.trails.append((trail, probability, total_sboxes))

        '''Returned the sorted trails.
                The trails are sorted first by highest probability and then by fewest active S-boxes.'''

        return sorted(self.trails, key=lambda x: (-x[1], x[2]))

    def printTrails(self, flag=False, n=5):
        '''Print the top 10 trails with highest probability.'''

        self.constructTrails()

        if self.trails and flag:
            print(f"\nTop {n} Differential Trails:-\n")

        if flag:
            for i in range(n):
                print("\nTrail {0}:-\n".format(i + 1))
                print(f"Active S-boxes: {self.trails[i][2]}")
                print(f"Maximum Probability: {self.trails[i][1]}")
                print(
                    f"Input Difference (Δx): {self.trails[i][0][0]} \u2192 {self.trails[i][0][1]} \u2192 {self.trails[i][0][2]} \u2192 {self.trails[i][0][3]} \u2192 {self.trails[i][0][4]}\n")
                print("-" * 50)

    def getBestTrail(self, flag=False):
        '''Return the best trail with highest probability and fewest active S-boxes.'''

        self.printTrails(flag)

        return self.trails[0][0][-1], self.trails[0][1], self.trails[0][2]


if __name__ == "__main__":

    trail = ConstructDifferentialTrails().getBestTrail(True)

    print(f"\n\nBest Trail:- \n")
    print(f"Active S-boxes: {trail[2]}")
    print(f"Maximum Probability: {trail[1]}")
    print(f"Input Difference (Δx): {trail[0]}\n")
