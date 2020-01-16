# chaîne de int (changer char en int avec orb())
# mutation
import random
from configuration import *

from src.configuration import PARAMETERS


class Genotype:
    def __init__(self, length):
        self.length_max = length
        self.genotype = []
        self.phenotype = []
        self.initialize_phenotype()
        self.initialize_genotype()

    def initialize_phenotype(self):
        for i in range(self.length_max):
            self.phenotype.append(self.generate_trait())

    def initialize_genotype(self):
        for i in range(len(self.phenotype)):
            self.genotype.append(ord(self.phenotype[i]))

    def generate_trait(self):
        nb = random.randint(48, 57)
        letter = random.randint(65, 90)
        value = random.choice([nb, letter])
        return chr(value)

    def generate_gene(self):
        nb = random.randint(48, 57)
        letter = random.randint(65, 90)
        value = random.choice([nb, letter])
        return value

    def replace_char(self):
        for i in range(len(self.genotype)):
            self.genotype[i] = ord(self.genotype[i])

    def update_phenotype(self):
        for i in range(len(self.phenotype)):
            self.phenotype[i] = chr(self.genotype[i])

    def mutation(self):
        threshold_mutation = PARAMETERS['mutation']
        for i in range(len(self.genotype)):
            r = random.random()
            if r <= threshold_mutation:
                # faire mut
                self.genotype[i] = self.generate_gene()
        self.update_phenotype()


    def __len__(self):
        return len(self.phenotype)


if __name__ == "__main__":
    g = Genotype(18)
    print(g.phenotype)
    print(g.genotype)
    # 48 - 57 : numbers
    # 65 - 90 : letters
