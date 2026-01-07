import Ant
import json
import numpy as np
import pandas as pd
import time


def menu():
    files_name = ['data/r203.txt', 'data/c203.txt', 'data/rc203.txt']
    wybor_pliku = 0
    vehicles_capacity = [1000, 700, 1000]
    while wybor_pliku not in [1, 2, 3]:
        wybor_pliku = int(input(f'Wybierz plik danych do eksperymentu: \n 1 - r203.txt \n 2 - c203.txt\n 3 - rc203.txt \n Twój wybór: '))
    data = pd.read_csv(
        files_name[wybor_pliku - 1],
        sep=r'\s+',
        skiprows=9,
        header=None,
        names=['CUST_NO', 'XCOORD', 'YCOORD', 'DEMAND', 'READY_TIME', 'DUE_DATE', 'SERVICE_TIME']
    )
    return data, vehicles_capacity[wybor_pliku - 1]


'''Funkcja zwraca macierz, w której górna część to odległości między atrakcjami, 
    a dolna część to ślady feromonowe (przy inicjalizacji ustawione na 0)'''
def initializeMatrix(data):
    N = len(data)
    matrix = [[1.0 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            # przekatna macierzy bedzie nieuzywana
            if i == j:
                continue
            elif i < j:
                # górna czesc macierzy będzie mieć odległosci miedzy atrakcjami
                matrix[i][j] = np.sqrt(np.power(data['XCOORD'][i] - data['XCOORD'][j], 2) + np.power(data['YCOORD'][i] - data['YCOORD'][j], 2))
            # dolna czesc (slady feromonowe) ustawiamy na 1
            elif i > j:
                matrix[i][j] = 1

    numpy_matrix = np.array(matrix)
    return numpy_matrix


''' Funkcja inicjalizuje i zwraca kolonię mrówek'''
def initializeAntColony(m, capacity, data):
    colony = []
    matrix = initializeMatrix(data)
    for i in range(m):
        colony.append(Ant.Ant(len(matrix), capacity))
    return colony, matrix


def pheromoneUpdate(colony, matrix, rho):
    # wyparowywanie
    N = len(matrix)
    for i in range(N):
        for j in range(i):
            matrix[i][j] *= (1-rho)

    # dodawanie
    for ant in colony:
        if ant.track_length > 0 and ant.track_length != float('inf'):
            trail = 1/ant.track_length
            # dodajemy feromony w każdej trasie w rozwiązaniu mrówki
            for tour in ant.solution:
                for k in range(len(tour)-1):
                    i = tour[k]
                    j = tour[k+1]
                    matrix[max(i,j)][min(i,j)] += trail
    return matrix


def colonyUpdate(colony):
    for ant in colony:
        ant.updateAnt()

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

data, vehicles_capacity = menu()
clients_nr = 100 #(w danych wiersz o id 0 to depot)
vehicles_nr = 25

for param in ['m', 'p_random', 'alpha', 'beta', 'T', 'rho']:
    print(f'----------------------------------------------------------------------------------\n'
          f'          Badanie wpływu parametru: {param}: ({param} = {VALUES[param]})  '
          f'\n----------------------------------------------------------------------------------')

    all_results_json = []
    for p in range(0, len(VALUES[param])):
        PARAMS[param] = VALUES[param][p]
        bests = []
        bests_tour = []
        current_params_results = []
        stats = []

        print(f'PARAMS: {PARAMS}')
        for i in range(1,6):
            start_time = time.time()
            colony, matrix = initializeAntColony(PARAMS['m'], vehicles_capacity, data)

            for j in range (1, PARAMS['T']+1):
                for ant in colony:
                    while ant.unvisited:
                        available = ant.getAvailibleCustomers(matrix, data)
                        if available:
                            ant.nextPlace(matrix, PARAMS['p_random'], PARAMS['alpha'], PARAMS['beta'], data)
                        else:
                            ant.returnToDepot(matrix)
                    if ant.tour[-1] != 0:
                        ant.returnToDepot(matrix)
                matrix = pheromoneUpdate(colony, matrix, PARAMS['rho'])
                colonyUpdate(colony)

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
            bests_tour.append(best_tour)
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

        best_track_index = np.argmin(bests)
        overall_best_tour = bests_tour[best_track_index]
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
            'std': np.std(bests),
            'best_tour': overall_best_tour
        }
        stats.append(statistics)


        all_results_json.extend(current_params_results)
        filename = f'results/{param}-output-{clients_nr}.json'
        with open(filename, 'w') as file:
            json.dump(all_results_json, file, indent=4)

        stats_json.extend(stats)
        filename = f'results/STATS-{clients_nr}.json'
        with open(filename, 'w') as file:
            json.dump(stats_json, file, indent=4)

    PARAMS[param] = VALUES[param][0]