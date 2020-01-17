import random
from individu import Individu
from adn import Adn
from configuration import *
import heapq


class Population:
    def __init__(self):
        self.individus = []
        self.individusBest = []
        self.percentage_selection = PARAMETERS['population_best']
        self.pop = PARAMETERS['population']
        self.pop_best = PARAMETERS['population_best']
        self.mutation_threshold = PARAMETERS['mutation']
        self.crossover_threshold = PARAMETERS['crossover']
        self.adn = Adn()

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
        iteration = 0
        self.initialize_population()
        while fitness_max != 1:
            self.compute_fitness()
            fitness_max, best_phenotype, best_genotype = self.fitness_max()
            print("Generation ", generation, "| Best fitness : ", fitness_max, " with (", best_phenotype, ", ",
                  best_genotype, ")")
            best = self.get_best_individus()
            new_genotypes = self.cross_over(best)
            self.individus.clear()
            for i in new_genotypes:
                phenotype = self.adn.update_phenotype(i)
                individu = Individu(i, phenotype)
                self.individus.append(individu)
            generation += 1
            iteration += 1

    def get_best_individus(self):
        best_genotypes = []
        fitness = []
        for i in range(len(self.individus)):
            fitness.append(self.individus[i].fitness)
        index = heapq.nlargest(self.pop_best, range(len(fitness)), fitness.__getitem__)
        for i in index:
            best_genotypes.append(self.individus[i].genotype)
        return best_genotypes

    def cross_over(self, best):
        children_produced = 1
        children = [best[0], best[1]]  # elitism
        while children_produced < self.pop:
            parents = random.sample(best, 2)
            rand = random.random()
            if rand <= self.crossover_threshold:
                dad = parents[0]
                mom = parents[1]

                # Apply cross-over
                baby_yoda = dad[:6] + mom[6:]
                master_yoda = mom[:6] + dad[6:]

                # Appy mutation
                baby_yoda_mut = self.mutation(baby_yoda)
                master_yoda_mut = self.mutation(master_yoda)

                # Save the children
                children.append(baby_yoda_mut)
                children.append(master_yoda_mut)
                children_produced += 2
        return children

    def mutation(self, genotype):
        new_genotype = []
        for i in range(len(genotype)):
            rand = random.random()
            if rand <= self.mutation_threshold:
                new_gene = self.adn.generate_gene(gene=True)
                new_genotype.append(new_gene)
            else:
                new_genotype.append(genotype[i])
        return new_genotype