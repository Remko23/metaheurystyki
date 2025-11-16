import pandas as pd
import random
import time

data = pd.read_csv('problem_plecakowy_dane.csv', sep='\t' ,header=None)
weight = data.iloc[1:,2]
value = data.iloc[1:,3]
weight = [int(w.replace(" ","")) for w in weight]
value = [int(v.replace(" ","")) for v in value]
wv_ratio = [w / v for w, v in zip(weight, value)]
knapsack_limit = 6404180

'''Generowanie pojedynczych chromosomow. Zwracamy liste z wartosciami True/False'''
def initialize_chromosome():
    is_in = [False for _ in range(len(wv_ratio))]
    for i in range(len(is_in)):
       is_in[i] = random.choice([True, False])
    return is_in


'''Generowanie populacji - zwracamy liste gdzie kazda komorka to lista wartosci True/False'''
def initialize_population(N):
    population = []
    grading_list = []
    for i in range(N):
        population.append(initialize_chromosome())
    for elem in population:
        grading_list.append(grading(elem))
    return population, grading_list


'''Funckja do oceny przystosowania danego osobnika - sprawdzamy czy miescie sie w plecaku
    jesli nie nakladamy kare zmniejszajac ocene o wartosc X za kazdy kilogram ponad limit.
    Funkcja zwraca roznice wartosi calego plecaka pomniejszana o kare (przy przekreczeniu
    wagi o duza wartosc mozemy dosatc wartosc ujemna)'''
def grading(is_in):
    total_weight = 0
    total_value = 0
    for gen, w, v in zip(is_in, weight, value):
        if gen:
            total_weight += w
            total_value += v

    if total_weight > knapsack_limit:
        penalty = 5 * (total_weight - knapsack_limit)
    else:
        penalty = 0

    return total_value - penalty


'''Funckja wybiera rodzicow metoda turnieju. Wybieramy losowo po 2 osobniki ktore laczymy w pary
    a nastepnie z kazdej pary wybieramy tego o wiekszym przystosowaniu. Koncowo dostajemy liste 
    "najlepszych" rodzicow'''
def parents_selection(population, grading_list):
    parents = []
    for i in range(len(population)):
        p1, p2 = random.sample(range(len(population)), 2)
        if grading_list[p1] > grading_list[p2]:
            parents.append(population[p1])
        else:
            parents.append(population[p2])

    return parents


'''Funckja odpowiada ze krzyzowanie rodzicow. Z listy parents wybieramy rodzic1 i rodzic2
    a nastepnie sprawdzamy czy sachodzi krzyzowanie jesli tak to losujemy punkt w ktorym 
    przecinamy geny i laczymy by powstaly dzieci. Jesli nie to przypsujemy rodzicow tak jak sa
    Przed dodaniem do listy sprawdzamy czy zachodzi mutacja. Funkcja zwraca liste dzieci'''
def crossing(parents, Pc, Pm):
    shuffled = parents[:]
    random.shuffle(shuffled)
    children = []
    graded_child = []

    for i in range(0, len(shuffled), 2):
        parent1, parent2 = shuffled[i], shuffled[i + 1]

        if random.random() < Pc:
            point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
        else:
            child1, child2 = parent1[:], parent2[:]

        child1 = mutation(child1, Pm)
        child2 = mutation(child2, Pm)
        graded_child.append(grading(child1))
        graded_child.append(grading(child2))

        children.extend([child1, child2])
    return children, graded_child


'''Sprawdzamy czy zachodzi mutacja. Zwracamy pojedyczne dziecko'''
def mutation(child, Pm):

    for i in range(len(child)):
        if random.random() < Pm:
            child[i] = not child[i]

    return child


'''Glowna funckja w ktorej wywolujemy wszystkie inne funkcje. Tutaj sprawdzamy jaki wynik
    jest najlepszy, najgorszy oraz liczymy srednie wyniki po kazdej iteracji. 
    Funckja zwraca same wyniki'''
def symulation(Pc, Pm, N, T):
    i = 0
    avg_solution = []
    population, grading_list = initialize_population(N)

    best = max(grading_list)
    best_index = grading_list.index(best)
    best_chromosome = population[best_index][:]
    worst = min(grading_list)

    while i < T:
        parents = parents_selection(population, grading_list)
        population, grading_list = crossing(parents, Pc, Pm)

        new_best = max(grading_list)
        new_best_index = grading_list.index(new_best)
        new_worst = min(grading_list)
        avg = sum(grading_list) / len(grading_list)

        avg_solution.append(avg)

        if new_best > best:
            best = new_best
            best_index = new_best_index
            best_chromosome = population[best_index][:]
        if new_worst < worst:
            worst = new_worst


        i += 1
    return best, worst, avg_solution, best_chromosome


def T1_experiment():
    run_experiment(
    Pc_values = [0.6, 0.8, 1.0],
    Pm_values = [0.01, 0.05, 0.1],
    N_values = [50, 100, 200],
    T = 200,
    filename = 'T1_results.csv'
    )


def T2_experiment():
    run_experiment(
    Pc_values = [0.6, 0.8, 1.0],
    Pm_values = [0.01, 0.05, 0.1],
    N_values = [50, 100, 200],
    T = 500,
    filename = 'T2_results.csv'
    )


def T3_experiment():
    run_experiment(
    Pc_values = [0.6, 0.8, 1.0],
    Pm_values = [0.01, 0.05, 0.1],
    N_values = [50, 100, 200],
    T = 1000,
    filename = 'T3_results.csv'
    )


'''Funkcja menu sluzy do obslugi symulacji. W niej odbywa sie przypisanie parametrow
    oraz zapis do pliku .csv'''
def run_experiment(Pc_values, Pm_values, N_values, T, filename):
    results = []

    runs_counter = 5


    for pm in Pm_values:
        for n in N_values:
            for pc in Pc_values:
                print(f"\n🔹 Testuję kombinację: Pc={pc}, Pm={pm}, N={n}, T={T}")

                run_best = []
                run_worst = []
                run_time = []
                run_avg = []
                run_best_chrom = []

                for run in range(runs_counter):
                    start = time.time()
                    best, worst, avg, best_chromosome = symulation(pc, pm, n, T)
                    end = time.time()

                    run_best.append(best)
                    run_worst.append(worst)
                    run_time.append(round(end - start, 5))
                    run_avg.append(sum(avg)/len(avg))
                    run_best_chrom.append(best_chromosome)

                    print(f"  🔸 Run {run + 1}: best={best}, worst={worst}, time={end - start:.2f}s")

                results.append({
                    'Pc': pc,
                    'Pm': pm,
                    'N': n,
                    'T': T,
                    'Time': run_time,
                    'best': run_best,
                    'worst': run_worst,
                    'best_chrom': run_best_chrom,
                    'avg': run_avg,
                })
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False, sep=';')
    print('Zapisano ES?')

    return df


T1_experiment()
T2_experiment()
T3_experiment()


#test1, test2 = initialize_population(20)
#parents = parents_selection(test1, test2)
#new_population = crossing(parents, 0.6, 0.05)

#symulation(0.8, 0.1, 100,200)

#print("Nowe dzieci:")
#for child in new_population:
#    print(child)





