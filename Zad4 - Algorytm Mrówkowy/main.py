from random import randint
import Ant
import json
import numpy as np
import pandas as pd
import time


def menu():
    files_name = ['data/A-n32-k5.txt', 'data/A-n80-k10.txt']
    attractions_nr = [32, 80]
    wybor_pliku = 0
    while wybor_pliku not in [1, 2]:
        wybor_pliku = int(input(f'Wybierz plik danych do eksperymentu: \n 1 - A-n32-k5.txt \n 2 - A-n80-k10.txt\n'))
    data = pd.read_csv(
        files_name[wybor_pliku-1],
        sep=r'\s+',
        header=None,
        names=['attractionID', 'X', 'Y'],
        comment='['
    )
    return data, attractions_nr[wybor_pliku-1]


'''Funkcja zwraca macierz, w której górna część to odległości między atrakcjami, 
    a dolna część to ślady feromonowe (przy inicjalizacji ustawione na 0)'''
def initializeMatrix(data):
    N = len(data)
    matrix = [[0.0 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            # przekatna macierzy bedzie nieuzywana
            if i == j:
                continue
            elif i < j:
                # górna czesc macierzy będzie mieć odległosci miedzy atrakcjami
                matrix[i][j] = np.sqrt(np.power(data['X'][i] - data['X'][j], 2) + np.power(data['Y'][i] - data['Y'][j], 2))
            # dolna czesc (slady feromonowe) ustawiamy na 1
            elif i > j:
                matrix[i][j] = 1

    numpy_matrix = np.array(matrix)
    return numpy_matrix


''' Funkcja inicjalizuje i zwraca kolonię mrówek'''
def initializeAntColony(m):
    colony = []
    matrix = initializeMatrix(data)
    # print(matrix)
    for i in range(m):
        colony.append(Ant.Ant(randint(0,len(data)-1), len(matrix)))
    return colony, matrix


def pheromoneUpdate(colony, matrix, rho):
    # wyparowywanie
    N = len(matrix)
    for i in range(N):
        for j in range(i):
            matrix[i][j] *= (1-rho)

    # dodawanie
    for ant in colony:
        trail = 1/ant.track_length
        for k in range(N-1):
            i = ant.tour[k]
            j = ant.tour[k+1]
            matrix[max(i,j)][min(i,j)] += trail

    return matrix


def colonyUpdate(colony, matrix):
    for ant in colony:
        ant.updateAnt(randint(0,len(data)-1), len(matrix))


def saveOutput():
    print('Dopisac zapis danych')

# wartosci parametrow
VALUES = {
    'm': [10, 20, 50, 100],
    'p_random': [0.01, 0.0, 0.1, 0.3],
    'T': [100, 10, 200, 500],
    'rho': [0.1, 0.3, 0.5, 0.8],
    'alpha': [2.0, 0.5, 1.0, 5.0],
    'beta': [1.0, 2.0, 4.0, 10.0]
}

PARAMS = {
    'm': VALUES['m'][0],                #domyslnie: 10
    'p_random': VALUES['p_random'][0],  #domyslnie: 0.01
    'T': VALUES['T'][0],                #domyslnie: 200
    'rho': VALUES['rho'][0],            #domyslnie: 0.1
    'alpha': VALUES['alpha'][0],        #domyslnie: 2.0
    'beta': VALUES['beta'][0]           #domyslnie: 1.0
}


stats_json = []

data, attractions_nr = menu()

for param in ['m', 'p_random', 'alpha', 'beta', 'T', 'rho']:
    print(f'------------------------------------------------------------------------\n'
          f'          Badanie wpływu parametru: {param}: ({param} = {VALUES[param]})  '
          f'\n------------------------------------------------------------------------')

    all_results_json = []
    for p in range(0, len(VALUES[param])):
        PARAMS[param] = VALUES[param][p]
        bests = []
        current_params_results = []
        stats = []

        print(f'PARAMS: {PARAMS}')
        for i in range(1,6):
            start_time = time.time()
            colony, matrix = initializeAntColony(PARAMS['m'])

            for j in range (1, PARAMS['T']+1):
                for ant in colony:
                    while ant.nextAttraction(matrix, PARAMS['p_random'], PARAMS['alpha'], PARAMS['beta']) != None:
                        continue
                matrix = pheromoneUpdate(colony, matrix, PARAMS['rho'])
                colonyUpdate(colony, matrix)

            best_track = float('inf')
            best_tour = []
            ant_bests = []
            for ant in colony:
                ant_bests.append(ant.best_track_length)
                if ant.best_track_length < best_track:
                    best_track = ant.best_track_length
                    best_tour = ant.best_tour
            end_time = time.time()
            duration = end_time - start_time
            bests.append(best_track)
            results = {
                    'itteration_nr': i,
                    'parameters': {
                        'm': PARAMS['m'],
                        'p_random': PARAMS['p_random'],
                        'T': PARAMS['T'],
                        'alpha': PARAMS['alpha'],
                        'beta': PARAMS['beta'],
                        'rho': PARAMS['rho']
                    },
                    'best_track': best_track,
                    'best_tour': best_tour,
                    'mean_track': np.mean(ant_bests),
                    'worst_track': np.max(ant_bests),
                    'duration': duration,
            }
            print(f'Iteracja nr. {i}, najkrótsza trasa: {best_track}, czas wykonania: {duration}')
            current_params_results.append(results)
            statistics = {
                'parameters': {
                    'm': PARAMS['m'],
                    'p_random': PARAMS['p_random'],
                    'T': PARAMS['T'],
                    'alpha': PARAMS['alpha'],
                    'beta': PARAMS['beta'],
                    'rho': PARAMS['rho']
                },
                'min': np.min(bests),
                'max': np.max(bests),
                'mean': np.mean(bests),
                'median': np.median(bests),
                'std': np.std(bests)
            }
            stats.append(statistics)


        all_results_json.extend(current_params_results)
        filename = f'results/{param}-output-{attractions_nr}.json'
        with open(filename, 'w') as file:
            json.dump(all_results_json, file, indent=4)

        stats_json.extend(stats)
        filename = f'results/STATS-{attractions_nr}.json'
        with open(filename, 'w') as file:
            json.dump(stats_json, file, indent=4)

    PARAMS[param] = VALUES[param][0]