import random
from individu import Individu
from adn import Adn
from configuration import *
import heapq
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class Genetic1:
    def __init__(self):
        self.individus = []
        self.individusBest = []
        self.percentage_selection = PARAMETERS['population_best']
        self.pop = PARAMETERS['population']
        self.pop_best = PARAMETERS['population_best']
        self.mutation_threshold = PARAMETERS['mutation']
        self.crossover_threshold = PARAMETERS['crossover']
        self.muta_supr = PARAMETERS['muta_suppr']
        self.muta_add = PARAMETERS['muta_add']
        self.length_min = PARAMETERS['length_min']
        self.length_max = PARAMETERS['length_max']
        self.adn = Adn()
        self.x = []
        self.y = []

    # Generate a new population
    def initialize_population(self):
        for i in range(self.pop):
            phenotype = self.adn.generate_phenotype()
            genotype = self.adn.generate_genotype(phenotype)
            individu = Individu(genotype, phenotype)
            self.individus.append(individu)

    # Compute the maximum fitness within the current population
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

    def fitness_average(self):
        total = 0
        for i in self.individus:
            total += i.fitness
        return round(total / len(self.individus), 2)

    # Main method of genetic algorithm
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
            best = self.selection()
            new_genotypes = self.cross_over(best)
            self.individus.clear()
            for i in new_genotypes:
                phenotype = self.adn.update_phenotype(i)
                individu = Individu(i, phenotype)
                self.individus.append(individu)
            avg = self.fitness_average()
            self.x.append(fitness_max)
            self.plot_evolution(self.x, avg)
            generation += 1

    # Select best individus
    def selection(self):
        best_genotypes = []
        fitness = []
        for i in range(len(self.individus)):
            fitness.append(self.individus[i].fitness)
        index = heapq.nlargest(len(self.individus), range(len(fitness)), fitness.__getitem__)
        for i in index:
            if len(best_genotypes) < self.pop_best:
                individu = self.individus[i].genotype
                best_genotypes.append(individu)
            else:
                break
        return best_genotypes

    # Single break point crossover
    def cross_over(self, best):
        children_produced = 0
        children = []  # elitism
        while children_produced < self.pop:
            parents = random.sample(best, 2)
            rand = random.random()
            if rand <= self.crossover_threshold:
                dad = parents[0]
                mom = parents[1]
                lengthmin = len(dad)
                if len(mom) < lengthmin:
                    lengthmin = len(mom)
                lengthmin = random.randint(1, round((lengthmin - 1) * 0.5))
                # Apply cross-over
                baby_yoda = dad[:lengthmin] + mom[lengthmin:]
                master_yoda = mom[:lengthmin] + dad[lengthmin:]
            else:
                baby_yoda = parents[0]
                master_yoda = parents[1]
            # Appy mutation
            baby_yoda_mut = self.mutation(baby_yoda)
            master_yoda_mut = self.mutation(master_yoda)

            # Save the children
            children.append(baby_yoda_mut)
            children.append(master_yoda_mut)
            children_produced += 2
        return children

    # Mutation possible on every gene
    def mutation(self, genotype):
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
        rand = random.random()
        if rand <= self.muta_supr and size > self.length_min:
            new_genotype = new_genotype[:-1]
        elif size < self.length_max:
            new_gene = self.adn.generate_gene(gene=True)
            new_genotype.append(new_gene)
        return new_genotype


    def display_password(self, phenotype):
        password = ""
        for i in phenotype:
            password += i
        return password

    def plot_evolution(self, data, average):
        plt.figure(1)
        plt.clf()
        plt.title("Evolution of fitness maximum")
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.plot(data)
        # plt.plot(average)
        plt.draw()

        plt.grid()
        plt.pause(0.001)
