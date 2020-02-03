import random
from individu import Individu
from adn import Adn
from configuration import *
import heapq
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class Genetic3:
    def __init__(self):
        self.individus = []
        self.population1 = []
        self.population2 = []
        self.percentage_selection = PARAMETERS['population_best']
        self.pop = PARAMETERS['population']
        self.pop_best = PARAMETERS['population_best']
        self.mutation_threshold = PARAMETERS['mutation']
        self.crossover_threshold = PARAMETERS['crossover']
        self.muta_supr = PARAMETERS['muta_suppr']
        self.muta_add = PARAMETERS['muta_add']
        self.length_min = PARAMETERS['length_min']
        self.length_max = PARAMETERS['length_max']
        self.merge = PARAMETERS['population_merge']
        self.adn = Adn()
        self.x = []
        self.y = []

    def initialize_population(self):
        population = []
        for i in range(self.pop):
            phenotype = self.adn.generate_phenotype()
            genotype = self.adn.generate_genotype(phenotype)
            individu = Individu(genotype, phenotype)
            population.append(individu)
        return population

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

    def compute_fitness_pop1(self):
        for i in self.population1:
            i.compute_fitness()

    def compute_fitness_pop2(self):
        for i in self.population2:
            i.compute_fitness()

    def compute_fitness_pop_final(self):
        for i in self.individus:
            i.compute_fitness()

    def run(self):
        generation = 0
        fitness_max = 0
        self.population1 = self.initialize_population()
        self.population2 = self.initialize_population()

        while generation <= self.merge:
            self.compute_fitness_pop1()
            self.compute_fitness_pop2()
            best_pop1 = self.selection(self.population1)
            best_pop2 = self.selection(self.population2)
            cross_pop1 = self.cross_over(best_pop1)
            cross_pop2 = self.cross_over(best_pop2)
            self.population1.clear()
            self.population2.clear()
            for i in cross_pop1:
                phenotype = self.adn.update_phenotype(i)
                individu = Individu(i, phenotype)
                self.population1.append(individu)

            for i in cross_pop2:
                phenotype = self.adn.update_phenotype(i)
                individu = Individu(i, phenotype)
                self.population2.append(individu)

            generation += 1

        self.individus = self.population1 + self.population2
        print("Merged")
        while fitness_max != 1:
            self.compute_fitness_pop_final()
            fitness_max, best_phenotype, best_genotype = self.fitness_max()
            print("Generation ", generation, "| Best fitness : ", fitness_max,
                  " | Password : ", self.display_password(best_phenotype),
                  ' | Size : ', len(best_phenotype))
            best = self.selection(self.individus)
            new_genotypes = self.cross_over(best)
            self.individus.clear()
            for i in new_genotypes:
                phenotype = self.adn.update_phenotype(i)
                individu = Individu(i, phenotype)
                self.individus.append(individu)
            self.x.append(fitness_max)
            self.plot_evolution(self.x)
            generation += 1

    def selection(self, population):
        best_genotypes = []
        fitness = []
        for i in range(len(population)):
            fitness.append(population[i].fitness)
        index = heapq.nlargest(len(population), range(len(fitness)), fitness.__getitem__)
        for i in index:
            if len(best_genotypes) < self.pop_best:
                individu = population[i].genotype
                best_genotypes.append(individu)
            else:
                break
        return best_genotypes

    def cross_over(self, best):
        children_produced = 1
        children = [best[0]]
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
                mutated_child = self.mutation(child)
                children.append(mutated_child)
                children_produced += 1
        return children

    def mutation(self, genotype):
        # 4 mutations possibles si threshold atteint
        size = len(genotype)
        rand = random.random()
        if rand <= self.mutation_threshold:
            rand_mut = random.random()

            # Single gene modification
            if rand_mut <= 0.25:
                position = random.randint(0, size - 1)
                new_gene = self.adn.generate_gene(gene=True)
                genotype[position] = new_gene

            # Swap two genes
            elif rand_mut <= 0.5:
                positions = random.sample(range(0, size - 1), 2)
                pos1 = positions[0]
                pos2 = positions[1]
                gene1 = genotype[pos1]
                genotype[pos1] = genotype[pos2]
                genotype[pos2] = gene1

            # Add one gene
            elif rand_mut <= 0.75:
                if size < self.length_max:
                    position = random.randint(0, size - 1)
                    new_gene = self.adn.generate_gene(gene=True)
                    genotype.insert(position, new_gene)

            # Delete one gene
            else:
                if size > 12:
                    position = random.randint(0, size - 1)
                    genotype.pop(position)
        return genotype

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
