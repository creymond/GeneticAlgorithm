from genetic1 import Genetic1
from genetic1bis import Genetic1bis
from genetic2 import Genetic2
from genetic3 import Genetic3
from genetic4 import Genetic4

if __name__ == "__main__":
    algo = 3
    number_test = 10

    if algo == 1:
        gen1 = Genetic1()
        gen1.run()
    elif algo == 2:
        gen2 = Genetic2()
        gen2.run()
    elif algo == 4:
        gen4 = Genetic4()
        gen4.run()
    elif algo == 3:
        max = 1
        j = 0
        total = 0
        while j < max:
            i = 0
            total_score = 0
            total_generation = 0
            while i < number_test:
                print('**** Population ', i, ' ****')
                gen3 = Genetic3()
                score, generation = gen3.run()
                if score > 0:
                    total_score += score
                if generation > 0:
                    total_generation += generation
                i += 1
            print("Score : ", total_score, "/", number_test)
            total += total_score
            j += 1
        print("Score final pour ", max, " itérations : ", total, "/", max * number_test)
        print("Nombre moyen de générations pour trouver le mot de passe : ", round(total_generation/number_test, 2))
    else:
        gen3 = Genetic1bis()
        gen3.run()