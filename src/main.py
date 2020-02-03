from genetic1 import Genetic1
from genetic2 import Genetic2
from genetic3 import Genetic3

if __name__ == "__main__":
    algo = 3

    if algo == 1:
        gen1 = Genetic1()
        gen1.run()
    elif algo == 2:
        gen2 = Genetic2()
        gen2.run()
    elif algo == 3:
        gen3 = Genetic3()
        gen3.run()
    else:
        gen3 = Genetic3()
        gen3.run()