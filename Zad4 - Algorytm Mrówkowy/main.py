from random import randint

import Ant
import pandas as pd
import numpy as np


def menu():
    files_name = ['data/A-n32-k5.txt', 'data/A-n80-k10.txt']
    wybor_pliku = 0
    while wybor_pliku != 1 and wybor_pliku != 2:
        wybor_pliku = int(input(f'Wybierz liczbę atrakcji: \n 1 - 32 \n 2 - 80\n'))
    data = pd.read_csv(
        files_name[wybor_pliku-1],
        sep=r'\s+',
        header=None,
        names=['attractionID', 'X', 'Y'],
        comment='['
    )
    return data


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


# TEST

data = menu()

# wczytanie parametrow z pliku
# PARAMS = pd.read_csv('data/PARAMS.txt', sep=r'\s+')

# poki co wstepne wartosci parametrow
m = 50
p_random = 0.01
T = 100
rho = 0.1
alpha = 1.0
beta = 1.0


colony, matrix = initializeAntColony(m)

for ant in colony:
    print('-----------------------------------------------')
    print(f'Pierwsza atrakcja mrowki: {ant.attraction_id}')
    while ant.nextAttraction(matrix, p_random, alpha, beta) != None:
        print(f'Aktualna atrakcja mrowki: {ant.attraction_id}')
    print(f'Koniec trasy, dlugosc: {ant.track_length}')


matrix = pheromoneUpdate(colony, matrix, rho)
colonyUpdate(colony, matrix)