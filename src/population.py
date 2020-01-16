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
            ind = Individu(18, 12, g)
            self.individus.append(ind)
        self.evaluation()

    def cross_over(self,bbyoda1 ,bbyoda2):
        lengthmin =bbyoda1.genotype.length_max
        if bbyoda2.genotype.length_max<lengthmin:
            lengthmin=bbyoda2.genotype.length_max

        crossLen = random.randint(1,round((lengthmin-1)*0.75))
        genYoda1=bbyoda1.genotype.genotype;
        genYoda2 = bbyoda2.genotype.genotype;
        debutYoda1=genYoda1[:crossLen]
        finYoda1=genYoda1[crossLen:]
        debutYoda2 = genYoda1[:crossLen]
        finYoda2 = genYoda1[crossLen:]
        genYoda1=debutYoda2+finYoda1
        genYoda2=debutYoda1+finYoda2
        bbyoda1.genotype.genotype=genYoda1
        bbyoda2.genotype.genotype = genYoda2


    def generate_child(self, maman, papa):

        randcross = random.random()
        child1 = maman
        child2 = papa
        if randcross <= self.cross:
            self.cross_over(child1,child2)
        # child 1 mutation

        # child 2 muation
        
        self.individus.append(child1)
        self.individus.append(child2)

    def generate_newPop(self):
        self.individus.clear()
        while len(self.individus) < self.nb:
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
            #print(tulpleM[0].fitness)
            #print(tulpleM[0].genotype.phenotype)
            lst.remove(tulpleM)
            i += 1


if __name__ == "__main__":
    pop = Population(100, 0.05, 0.5, 0.5)
    pop.generate_newPop()
    # pop.generatenew pop
    #
