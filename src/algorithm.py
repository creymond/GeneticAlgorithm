from blackbox37 import check


class Individu:
    def __init__(self, length_max, length_min,g):
        self.length_max = length_max
        self.length_min = length_min
        self.fitness = -1
        #generer taille aleatoire
        self.genotype = g
        self.fitness = check(4,self.genotype.phenotype)









if __name__ == "__main__":
    print()