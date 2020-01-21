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
        while iteration < 1000: #fitness_max != 1:
            print('Generation :', iteration)
            self.compute_fitness()
            fitness_max, best_phenotype, best_genotype = self.fitness_max()
            print("Generation ", generation, "| Best fitness : ", fitness_max, " | Password : ",self.display_password(best_phenotype))
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
        children_produced = 2
        children = [best[0], best[0]]   # elitism
        while children_produced < self.pop:
            parents = random.sample(best, 2)
            rand = random.random()
            dad = parents[0]
            mom = parents[1]
            if rand <= self.crossover_threshold:
                point = random.randint(1, 4)
                c = list(zip(dad[point:], mom[point:]))
                random.shuffle(c)
                dad_s, mom_s = zip(*c)

                # Apply cross-over
                child1 = dad[:point] + list(mom_s)
                child2 = mom[:point] + list(dad_s)
            else:
                child1 = dad
                child2 = mom

            baby_yoda = self.mutation(child1)
            master_yoda = self.mutation(child2)
            # Save the children
            children.append(baby_yoda)
            children.append(master_yoda)
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

    def display_password(self, phenotype):
        password = ""
        for i in phenotype:
            password += i
        return password
