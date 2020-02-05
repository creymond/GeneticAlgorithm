from genetic1 import Genetic1
from genetic2 import Genetic2
from genetic3 import Genetic3

if __name__ == "__main__":
    algo = 3
    number_test = 10

    if algo == 1:
        gen1 = Genetic1()
        gen1.run()
    elif algo == 2:
        gen2 = Genetic2()
        gen2.run()
    elif algo == 3:
        max = 10
        j = 0
        total = 0
        while j < max:
            i = 0
            total_score = 0
            while i < number_test:
                print('**** Population ', i, ' ****')
                gen3 = Genetic3()
                score = gen3.run()
                if score > 0:
                    total_score += score
                i += 1
            print("Score : ", total_score, "/", number_test)
            total += total_score
            j += 1
        print("Score final pour ", max, " itérations : ", total, "/", max * number_test)
    else:
        gen3 = Genetic3()
        gen3.run()