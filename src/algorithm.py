from blackbox37 import check


class Individu:
    def __init__(self,g):
        self.fitness = -1
        #generer taille aleatoire
        self.bio = g
        self.fitness = check(4,self.bio.phenotype)



    def setFitt(self):
        self.fitness = check(4, self.bio.phenotype)





if __name__ == "__main__":
    print()