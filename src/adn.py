import random
from configuration import *


class Adn:
    def __init__(self):
        self.upper_length = PARAMETERS['length_max']
        self.lower_length = PARAMETERS['length_min']

    def generate_phenotype(self):
        phenotype = []
        size = random.randint(self.lower_length, self.upper_length)
        for i in range(size):
            phenotype.append(self.generate_gene(gene=False))
        return phenotype

    def generate_genotype(self, phenotype):
        genotype = []
        size = len(phenotype)
        for i in range(size):
            genotype.append(ord(phenotype[i]))
        return genotype

    def generate_gene(self, gene):
        nb = random.randint(48, 57)
        letter = random.randint(65, 90)
        value = random.choice([nb, letter])
        if gene:
            return value
        else:
            return chr(value)

    def update_phenotype(self, genotype):
        phenotype = []
        for i in range(len(genotype)):
            phenotype.append(chr(genotype[i]))
        return phenotype
