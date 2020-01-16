from blackbox37 import check

from genotype import Genotype

class Individu:
    def __init__(self, length_max, length_min):
        self.length_max = length_max
        self.length_min = length_min
        self.fitness = -1
        self.genotype = Genotype()
        self.fitness = check(4, "AAAAAAAAAAAAA")









if __name__ == "__main__":
    print()