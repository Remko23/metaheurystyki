import os

import Ant
import json
import numpy as np
import pandas as pd
import time


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


def colonyUpdate(colony, matrix, demands, ready_times, due_dates, service_times):
    for ant in colony:
        ant.updateAnt(matrix, demands, ready_times, due_dates, service_times)

def run_experiment(VALUES, PARAMS, data, vehicles_capacity, data_filename):
    stats_json = []
    demands = data['DEMAND'].values
    ready_times = data['READY_TIME'].values
    due_dates = data['DUE_DATE'].values
    service_times = data['SERVICE_TIME'].values

    clients_nr = 100 #(w danych wiersz o id 0 to depozyt)
    vehicles_nr = 25
    print(f'==================================================================================\n'
          f'                          Badanie pliku: {data_filename}.txt'
          f'\n==================================================================================\n')

    for param in ['m', 'p_random', 'alpha', 'beta', 'T', 'rho']:
        print(f'----------------------------------------------------------------------------------\n'
              f'                Badanie wpływu parametru: {param}: ({param} = {VALUES[param]})      '
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
                    best_ant = None
                    min_distance = float('inf')

                    for ant in colony:
                        while ant.unvisited:
                            available = ant.getAvailibleCustomers(matrix, demands, ready_times, due_dates, service_times)
                            if available:
                                ant.nextPlace(matrix, PARAMS['p_random'], PARAMS['alpha'], PARAMS['beta'], demands, ready_times, due_dates, service_times)
                            else:
                                ant.returnToDepot(matrix)
                        if ant.tour[-1] != 0:
                            ant.returnToDepot(matrix)

                        if ant.track_length < min_distance:
                            min_distance = ant.track_length
                            best_ant = ant

                    # wykonujemy 2-opt TYLKo na najlepszej mrówce aby przyspieszyc algorytm
                    if best_ant and best_ant.track_length != float('inf'):
                        best_ant.twoOpt(matrix, demands, ready_times, due_dates, service_times)
                    matrix = pheromoneUpdate(colony, matrix, PARAMS['rho'])
                    colonyUpdate(colony, matrix, demands, ready_times, due_dates, service_times)

                best_track = float('inf')
                best_tour = []
                ant_bests = []
                for ant in colony:
                    ant_bests.append(ant.best_track_length)
                    if ant.best_track_length < best_track:
                        best_track = ant.best_track_length
                        best_tour = ant.best_solution
                end_time = time.time()
                duration = end_time - start_time
                bests.append(best_track)
                bests_tour.append(best_tour)
                results = {
                        'itteration_nr': int(i),
                        'parameters': {
                            'm': PARAMS['m'],
                            'p_random': PARAMS['p_random'],
                            'T': PARAMS['T'],
                            'alpha': PARAMS['alpha'],
                            'beta': PARAMS['beta'],
                            'rho': PARAMS['rho']
                        },
                        'best_track': float(best_track),
                        'best_tour': [[int(place) for place in route] for route in best_tour], #konwersja z typow Numpy
                        'mean_track': float(np.mean(ant_bests)),
                        'worst_track': float(np.max(ant_bests)),
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
                'min': float(np.min(bests)),
                'max': float(np.max(bests)),
                'mean': float(np.mean(bests)),
                'median': float(np.median(bests)),
                'std': float(np.std(bests)),
                'best_tour': [[int(place) for place in route] for route in overall_best_tour], #konwersja z typow Numpy
            }
            stats.append(statistics)
            stats_json.extend(stats)

            all_results_json.extend(current_params_results)
        with open(f'results/{data_filename}-output-{param}.json', 'w') as file:
            json.dump(all_results_json, file, indent=4)

        PARAMS[param] = VALUES[param][0]
    with open(f'results/STATS-{data_filename}.json', 'w') as file:
        json.dump(stats_json, file, indent=4)


# wartosci parametrow
VALUES = {
    'm': [25, 10, 50],
    'p_random': [0.01, 0.0, 0.1],
    'T': [75, 50, 100],
    'rho': [0.1, 0.05, 0.15],
    'alpha': [2.5, 1.5, 2.0],
    'beta': [2.0, 1.5, 2.5]
}

PARAMS = {
    'm': VALUES['m'][0],                #domyslnie: 20
    'p_random': VALUES['p_random'][0],  #domyslnie: 0.01
    'T': VALUES['T'][0],                #domyslnie: 100
    'rho': VALUES['rho'][0],            #domyslnie: 0.1
    'alpha': VALUES['alpha'][0],        #domyslnie: 2.5
    'beta': VALUES['beta'][0]           #domyslnie: 2.0
}

#vehicles_capacity = [1000, 700, 1000]
for file_name in ['data/r203.txt', 'data/c203.txt', 'data/rc203.txt']:
    base_name = os.path.basename(file_name).split('.')[0]
    data = pd.read_csv(
        file_name,
        sep=r'\s+',
        skiprows=9,
        header=None,
        names=['CUST_NO', 'XCOORD', 'YCOORD', 'DEMAND', 'READY_TIME', 'DUE_DATE', 'SERVICE_TIME']
    )
    if file_name != 'data/c203.txt':
        run_experiment(VALUES, PARAMS, data, 1000, base_name)
    else:
        run_experiment(VALUES, PARAMS, data, 700, base_name)