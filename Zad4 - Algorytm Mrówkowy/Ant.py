import random

import numpy as np

'''Klasa mrówki przechowuje:
     punkt początkowy, 
     aktualnie odwiedzaną atrakcję, 
     zbiór atrakcji pozostałych do odwiedzenia,
     listę odwiedzonych atrakcji w ramach wędrówki
     długość aktualnej wędrówki,
     listę odwiedzonych atrakcji w ramach najlepszej wędrówki
     długość najkrótszej wędrówki'''
class Ant:
    def __init__(self, attraction_id, attractions_number):
        self.start_point = attraction_id
        self.attraction_id = attraction_id #aktualna atrakcja

        self.unvisited = set(range(attractions_number))
        self.unvisited.remove(self.start_point)

        self.track_length = 0.0
        self.tour = [attraction_id]

        self.best_track_length = None
        self.best_tour = []


    ''' Funkcja dokonuje wyboru nastepnej atrakcji do odwiedzenia przez mrowke, 
        na podstawie odpowiedniego wzoru oraz selekcji ruletkowej,
        jesli mrówka odwiedzila wszystkie atrakcje to zwracamy None'''
    def nextAttraction(self, matrix, p_random, alpha, beta):
        # odwiedzono wszystkie atrakcje
        if not self.unvisited:
            return None

        # wybor losowej atrakcji
        if random.random() < p_random:
            next = random.choice(list(self.unvisited))
        #wybór względem śladu feromonów i heurystyki odległości
        else:
            i = self.attraction_id
            attractions = list(self.unvisited)
            chances = [[0.0, 0] for _ in range(len(attractions))]

            # dodaje malutki epsilon żeby uniknąć dzielenia przez 0 jako, że w jednym z plików dwie atrakcje są w tym samym miejscu
            eps = 0.0000000001
            for k, j in enumerate(attractions):
                chances[k][0] = np.power(matrix[max(i,j)][min(i,j)], alpha) * np.power(1 / (matrix[min(i,j)][max(i,j)] + eps), beta)
                chances[k][1] = j


            chances_array = np.array(chances)
            propability = chances_array[:, 0]/np.sum(chances_array)
            propability /= np.sum(propability) #normalizujemy

            #selekcja ruletkowa
            next = int(np.random.choice(chances_array[:, 1], p=propability))

        distance = matrix[min(next, self.attraction_id)][max(next, self.attraction_id)]
        self.attraction_id = next
        self.unvisited.remove(next)
        self.tour.append(next)
        self.track_length += distance
        return next

    '''aktualizacja mrówki przed kolejnym wyruszeniem w trasę
        sprawdzamy czy nie poprawiono najlepszej ścieżki, 
        oraz przygotowujemy zmienne przechowujące: dlugosc aktualnej drogi, punkt początkowy, 
        aktualną atrakcję, zbiór nieodwiedzonych i listę odwiedzonych atrakcji do kolejnej wędrówki,
        podobnie jak przy inicjalizacji mrówki'''
    def updateAnt(self, attraction_id, attractions_number):
        if self.best_track_length is None or self.track_length < self.best_track_length:
            self.best_track_length = self.track_length
            self.best_tour = self.tour

        self.track_length = 0.0
        self.start_point = attraction_id
        self.attraction_id = attraction_id  # aktualna atrakcja
        self.unvisited = set(range(attractions_number))
        self.unvisited.remove(self.start_point)
        self.tour = [attraction_id]