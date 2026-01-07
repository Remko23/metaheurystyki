import random

import numpy as np
from fontTools.ufoLib import anchorsValidator
from shapely.speedups import available

'''Klasa mrówki przechowuje: 
     aktualnie odwiedzane miejsce, 
     zbiór miejsc pozostałych do odwiedzenia,
     listę odwiedzonych miejsc w ramach wędrówki
     długość aktualnej wędrówki,
     listę odwiedzonych miejsc w ramach najlepszej wędrówki
     długość najkrótszej wędrówki,
     czas,
     załadunek'''
class Ant:
    def __init__(self, places_nr, capacity):
        self.places_nr = places_nr
        self.capacity = capacity
        self.best_track_length = None
        self.best_solution = []

        self.unvisited = set(range(1, places_nr))
        self.solution = []
        self.tour = [0]
        self.load = 0.0
        self.time = 0.0
        self.track_length = 0.0


    def getAvailibleCustomers(self, matrix, data):
        availible_customers = []
        i = self.tour[-1]

        for j in self.unvisited:
            distance = matrix[min(i,j)][max(i,j)]
            # przyjmujemy że długość trasy to jej czas bo chyba sie nie da inaczej
            arrival_time = self.time + distance

            if self.load + data.iloc[j]['DEMAND'] > self.capacity:
                continue
            if arrival_time >= data.iloc[j]['DUE_DATE']:
                continue
            # musimy zdazyc wrocic do depozytu
            if max(arrival_time, data.iloc[j]['READY_TIME']) + data.iloc[j]['SERVICE_TIME'] + matrix[0][j] > data.iloc[0]['DUE_DATE']:
                continue

            availible_customers.append(j)

        return availible_customers



    ''' Funkcja dokonuje wyboru nastepnego miejsca (klienta lub depozytu)
        do odwiedzenia przez mrowke, na podstawie odpowiedniego wzoru oraz selekcji ruletkowej,
        jesli mrówka odwiedzila wszystkie miejsca to zwracamy None'''
    def nextPlace(self, matrix, p_random, alpha, beta, data):
        i = self.tour[-1]
        available = self.getAvailibleCustomers(matrix, data)

        # wybor losowej miejsc
        if random.random() < p_random:
            next = random.choice(available)
        #wybór względem śladu feromonów i heurystyki odległości
        else:

            places = list(self.unvisited)
            chances = []

            # dodaje malutki epsilon żeby uniknąć dzielenia przez 0 jako, że w jednym z plików dwie atrakcje są w tym samym miejscu
            eps = 0.0000000001
            for j in available:
                chances.append(np.power(matrix[max(i,j)][min(i,j)], alpha) * np.power(1 / (matrix[min(i,j)][max(i,j)] + eps), beta))

            chances = np.array(chances)
            propability = chances/chances.sum()

            #selekcja ruletkowa
            next = np.random.choice(available, p=propability)

        distance = matrix[min(i,next)][max(i,next)]
        arrival_time = self.time + distance
        start_service = max(arrival_time, data.iloc[next]['READY_TIME'])

        self.track_length += distance
        self.time = start_service + data.iloc[next]['SERVICE_TIME']
        self.load += data.iloc[next]['DEMAND']
        self.tour.append(next)
        self.unvisited.remove(next)

    def returnToDepot(self, matrix):
        i = self.tour[-1]
        distance = matrix[0][i]
        self.track_length += distance
        self.tour.append(0)
        self.solution.append(list(self.tour))
        self.tour = [0]
        self.load = 0.0
        self.time = 0.0

    '''aktualizacja mrówki przed kolejnym wyruszeniem w trasę
        sprawdzamy czy nie poprawiono najlepszej ścieżki'''
    def updateAnt(self):
        if len(self.unvisited) > 0: #mrowce nie udalo sie odwiedzic wszystkich klientow
            self.track_length = float('inf')
        elif self.best_track_length is None or self.track_length < self.best_track_length:
            self.best_track_length = self.track_length
            self.best_solution = list(self.solution)

        self.unvisited = set(range(1, self.places_nr))
        self.solution = []
        self.tour = [0]
        self.load = 0.0
        self.time = 0.0
        self.track_length = 0.0