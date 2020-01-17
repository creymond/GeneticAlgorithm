from blackbox37 import check
from configuration import *


class Individu:
    def __init__(self, genotype, phenotype):
        self.genotype = genotype
        self.phenotype = phenotype
        self.fitness = 0

    def compute_fitness(self):
        self.fitness = check(PARAMETERS['groupe'], self.phenotype)
