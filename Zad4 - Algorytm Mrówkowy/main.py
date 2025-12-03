from random import randint

import Ant
import pandas as pd
import numpy as np

files_name=['data/A-n32-k5.txt', 'data/A-n80-k10.txt']

data = pd.read_csv(
    files_name[0],
    sep=r'\s+',
    header=None,
    names=['attractionID', 'X', 'Y'],
    comment='['
)

# wczytanie parametrow z pliku
# PARAMS = pd.read_csv('data/PARAMS.txt', sep=r'\s+')

# poki co wstepne wartosci parametrow
m = 50
p_random = 0.01
T = 100
rho = 0.1
alpha = 1.0
beta = 1.0


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


''' Funkcja zwraca kolonię mrówek'''
def initializeAntColony(m):
    colony = []
    matrix = initializeMatrix(data)
    # print(matrix)
    for i in range(m):
        colony.append(Ant.Ant(randint(0,len(data)-1), matrix,alpha, beta))
    return colony


''' Funkcja wywołuje funkcję wyboru następnej atrakcji dla każdej mrówki z kolonii'''
def nextAttraction(colony):
    for ant in colony:
        ant.nextAttraction()
    return colony

colony = initializeAntColony(m)