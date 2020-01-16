from operator import itemgetter
import random
from algorithm import Individu
import numpy as np

from genotype import Genotype


class Population:
    def __init__(self, nb, percent, muta, cross):
        self.individus = []
        self.individusBest = []
        self.percent = percent
        self.nb = nb
        self.muta = muta
        self.cross = cross
        for lettre in range(nb):
            r = random.randint(12, 18);
            g = Genotype(r)
            ind = Individu( g)
            self.individus.append(ind)
        self.evaluation()

    def cross_over(self,bbyoda1 ,bbyoda2):
        lengthmin =bbyoda1.bio.length_max
        if bbyoda2.bio.length_max<lengthmin:
            lengthmin=bbyoda2.bio.length_max

        crossLen = random.randint(1,round((lengthmin-1)*0.75))

        genYoda1=bbyoda1.bio.genotype
        genYoda2 = bbyoda2.bio.genotype

        genYoda1=genYoda2[:crossLen]+genYoda1[crossLen:]
        genYoda2=genYoda1[:crossLen]+genYoda2[crossLen:]
        print("genYoda1",genYoda1)
        bbyoda1.bio.genotype=genYoda1
        bbyoda2.bio.genotype = genYoda2


    def generate_child(self, maman, papa):

        randcross = random.random()
        child1 = maman
        child2 = papa
        if randcross <= self.cross:
            self.cross_over(child1,child2)
            print("cross")
        # child 1 mutation
        child1.bio.mutation()
        print("3", child1.bio.genotype)
        # child 2 muation
        child2.bio.mutation()
        print("4", child2.bio.genotype)
        child1.setFitt()
        print("5", child1.bio.genotype)
        child2.setFitt()

        print("6", child1.bio.genotype)
        self.individus.append(child1)
        self.individus.append(child2)

    def generate_newPop(self):
        self.individus.clear()
        while len(self.individus) < self.nb+2:
            rmaman = random.randint(0, len(self.individusBest)-1)
            rpapa = random.randint(0, len(self.individusBest)-1)
            self.generate_child(self.individusBest[rmaman], self.individusBest[rpapa])
            # clean elite
        self.individusBest.clear()
        self.evaluation()

    def evaluation(self):
        lst = []
        for ind in self.individus:
            tulple = (ind, ind.fitness)
            lst.append(tulple)

        i = 0
        print("Gen")
        while i <= (len(self.individus) * self.percent):
            tulpleM = max(lst, key=itemgetter(1))
            self.individusBest.append(tulpleM[0])
            print(tulpleM[0].fitness)
            print(tulpleM[0].bio.phenotype)
            lst.remove(tulpleM)
            i += 1


if __name__ == "__main__":
    pop = Population(20, 0.05, 0.5, 0.85)
    pop.generate_newPop()
    # pop.generatenew pop
    #
