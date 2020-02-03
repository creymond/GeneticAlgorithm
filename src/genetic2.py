import random
from individu import Individu
from adn import Adn
from configuration import *
import heapq
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from numpy.random import choice


class Genetic2:
    def __init__(self):
        self.individus = []
        self.individusBest = []
        self.percentage_selection = PARAMETERS['population_best']
        self.pop = PARAMETERS['population']
        self.pop_best = PARAMETERS['population_best']
        self.pop_worst = PARAMETERS['population_worst']
        self.mutation_threshold = PARAMETERS['mutation']
        self.crossover_threshold = PARAMETERS['crossover']
        self.muta_supr = PARAMETERS['muta_suppr']
        self.muta_add = PARAMETERS['muta_add']
        self.length_min = PARAMETERS['length_min']
        self.length_max = PARAMETERS['length_max']
        self.c = PARAMETERS['c']
        self.adn = Adn()
        self.x = []
        self.y = []

    def initialize_population(self):
        for i in range(self.pop):
            phenotype = self.adn.generate_phenotype()
            genotype = self.adn.generate_genotype(phenotype)
            individu = Individu(genotype, phenotype)
            self.individus.append(individu)

    def fitness_max(self):
        m_fitness = 0
        m_phenotype = None
        m_genotype = None
        for i in self.individus:
            if i.fitness >= m_fitness:
                m_fitness = i.fitness
                m_phenotype = i.phenotype
                m_genotype = i.genotype
        return m_fitness, m_phenotype, m_genotype

    def compute_fitness(self):
        for i in self.individus:
            i.compute_fitness()

    def run(self):

        generation = 0
        fitness_max = 0
        self.initialize_population()
        while fitness_max != 1:
            self.compute_fitness()
            fitness_max, best_phenotype, best_genotype = self.fitness_max()
            print("Generation ", generation, "| Best fitness : ", fitness_max,
                  " | Password : ", self.display_password(best_phenotype),
                  ' | Size : ', len(best_phenotype))
            best = self.roulette_wheel_exponential()
            new_genotypes = self.cross_over(best)
            self.individus.clear()
            for i in new_genotypes:
                phenotype = self.adn.update_phenotype(i)
                individu = Individu(i, phenotype)
                self.individus.append(individu)
            self.x.append(fitness_max)
            self.plot_evolution(self.x)
            generation += 1

    def roulette_wheel_exponential(self):
        weights = []
        sorted_individus = sorted(self.individus, key=lambda x: x.fitness, reverse=True)
        size = len(sorted_individus)
        for i in range(len(sorted_individus)+1):
            if i != 0:
                w = ((self.c - 1) / (pow(self.c, size) - 1)) * pow(self.c, size - i)
                weights.append(w)
        selected = choice(self.individus, self.pop_best, p=weights)
        selected_genotypes = []
        for i in range(len(selected)):
            selected_genotypes.append(selected[i].genotype)
        return selected_genotypes

    def cross_over(self, best):
        children_produced = 0
        children = []
        while children_produced < self.pop:
            parents = random.sample(best, 2)
            rand = random.random()
            if rand <= self.crossover_threshold:
                dad = parents[0]
                mom = parents[1]
                child = []
                if len(dad) >= len(mom):
                    for i in range(len(dad)):
                        if random.random() > 0.5:
                            child.append(dad[i])
                        elif i < len(mom):
                            child.append(mom[i])
                        else:
                            child.append(dad[i])
                else:
                    for i in range(len(mom)):
                        if random.random() > 0.5:
                            child.append(mom[i])
                        elif i < len(dad):
                            child.append(dad[i])
                        else:
                            child.append(mom[i])
                mutated_child = self.mutation_2(child)
                children.append(mutated_child)
                children_produced += 1
        return children

    def mutation(self, genotype):
        new_genotype = []
        lGen = len(genotype)
        for i in range(lGen):
            rand = random.random()
            if rand <= self.mutation_threshold:
                r2 = random.random()
                if r2 <= self.muta_supr or lGen <= self.length_min:
                    new_gene = self.adn.generate_gene(gene=True)
                    new_genotype.append(new_gene)
                else:
                    lGen -= 1
                    pass
            else:
                new_genotype.append(genotype[i])
        r3 = random.random()
        if r3 <= self.muta_add and lGen < self.length_max:
            new_gene = self.adn.generate_gene(gene=True)
            new_genotype.append(new_gene)
        return new_genotype

    def mutation_2(self, genotype):
        new_genotype = []
        size = len(genotype)
        for i in range(size):
            rand = random.random()
            if rand <= self.mutation_threshold:
                new_gene = self.adn.generate_gene(gene=True)
                new_genotype.append(new_gene)
            else:
                new_genotype.append(genotype[i])
        # print(new_genotype)
        rand2 = random.random()
        rand3 = random.random()
        if rand2 <= self.muta_supr and size > self.length_min:
            new_genotype = new_genotype[:-1]
        elif rand3 <= self.muta_add and size < self.length_max:
            new_gene = self.adn.generate_gene(gene=True)
            new_genotype.append(new_gene)

        return new_genotype

    def display_password(self, phenotype):
        password = ""
        for i in phenotype:
            password += i
        return password

    def plot_evolution(self, data):
        plt.figure(1)
        plt.clf()
        plt.title("Evolution of fitness maxmimum")
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.plot(data)
        plt.draw()
        plt.grid()
        plt.pause(0.001)
