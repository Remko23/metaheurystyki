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

PARAMS = pd.read_csv('data/PARAMS.txt', sep=r'\s+')

""" Funkcja zwraca macierz, w której górna część to odległości między atrakcjami, a dolna część to ślady feromonowe (przy inicjalizacji ustawione na 0)"""
def buildMatrix(data):
    N = len(data)
    matrix = [[0.0 for _ in range(N)] for _ in range(N)]

    print(matrix)
    for i in range(N):
        for j in range(N):
            if i == j:
                matrix[i][j] = np.nan
            elif i < j:
                matrix[i][j] = np.sqrt(np.power(data['X'][i] - data['X'][j], 2) + np.power(data['Y'][i] - data['Y'][j], 2))

    return matrix

matrix = buildMatrix(data)
