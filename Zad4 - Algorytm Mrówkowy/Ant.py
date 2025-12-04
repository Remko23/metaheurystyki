import random

import numpy as np

'''Klasa mrówki przechowuje:
     punkt początkowy, 
     aktualnie odwiedzaną atrakcję, 
     wartości alfy i bety, 
     macierz śladów feromonowych oraz długości tras,
     zbiór atrakcji pozostałych do odwiedzenia,
     listę odwiedzonych atrakcji w ramach wędrówki
     długość aktualnej wędrówki,
     długość najkrótszej wędrówki'''
class Ant:
    def __init__(self,
                 attraction_id: int,
                 matrix: np.ndarray,
                 alpha: float,
                 beta: float,):
        self.start_point = attraction_id
        self.attraction_id = attraction_id #aktualna atrakcja
        self.alpha = alpha
        self.beta = beta
        self.matrix = matrix

        # Wartości początkowe dla wędrówki
        self.unvisited = set(range(len(self.matrix)))
        self.unvisited.remove(self.start_point)

        self.tour = [attraction_id]
        self.track_length = 0.0
        self.best_track_length = None

    ''' Funkcja wyboru nastepnej atrakcji do odwiedzenia przez mrowke '''
    def nextAttraction(self, p_random):
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

            for k, j in enumerate(attractions):
                if i < j:
                    chances[k][0] = np.power(self.matrix[j][i], self.alpha) * np.power(1 / self.matrix[i][j], self.beta)
                else:
                    chances[k][0] = np.power(self.matrix[i][j], self.alpha) * np.power(1 / self.matrix[j][i], self.beta)
                chances[k][1] = j


            chances_array = np.array(chances)
            propability = chances_array[:, 0]/np.sum(chances_array)
            propability /= np.sum(propability) #normalizujemy

            #selekcja ruletkowa
            next = int(np.random.choice(chances_array[:, 1], p=propability))

        distance = self.matrix[min(next, self.attraction_id)][max(next, self.attraction_id)]
        self.attraction_id = next
        self.unvisited.remove(next)
        self.track_length += distance
        return next