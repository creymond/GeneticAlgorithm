from operator import itemgetter

from algorithm import Individu
import numpy as np

class Population:
    def __init__(self, nb, percent):
        self.individus = []
        self.individusBest = []
        self.percent = percent
        self.nb = nb
        for lettre in range(nb):
            ind = Individu(18, 12)
            self.individus.append(ind)
        self.evaluation()

    def cross_over(self):
        pass

    def generate_child(self, parent1, parent2):

        pass

    def generate_newPop(self):
        self.individus.clear()
        self.generate_child(self, parent1, parent2)

        # clean elite
        self.individusBest.clear()
        self.evaluation()
        pass
    def evaluation(self):
        lst=[]
        for ind in self.individus:
            tulple= (ind,ind.fitness)
            lst.append(tulple)

        i=0
        while i<=(len(self.individus)/self.percent):
            tulpleM=max(lst, key=itemgetter(1))
            self.individusBest.append(tulpleM[0])
            print(tulpleM[0].fitness)
            lst.remove(tulpleM)
            i+=1



if __name__ == "__main__":
    pop = Population(10,4)
    pop.generate_newPop()
    #pop.generatenew pop
    #