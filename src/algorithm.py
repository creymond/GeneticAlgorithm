from blackbox37 import check

similarity = check(4, 'AAAAAAAAAAAAAAAA')
print(similarity)


class Individu:
    def __init__(self, length_max, length_min):
        self.length_max = length_max
        self.length_min = length_min



    def compare_fitness(self):
        pass

    def mutation(self):
        pass

    def crossover(self):
        pass



if __name__ == "__main__":
    print()