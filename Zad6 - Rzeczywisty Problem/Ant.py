import random

import numpy as np

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


    def getAvailibleCustomers(self, matrix, demands, ready_times, due_dates, service_times):
        availible_customers = []
        i = self.tour[-1]

        for j in self.unvisited:
            distance = matrix[min(i,j)][max(i,j)]
            # przyjmujemy że długość trasy to jej czas bo chyba sie nie da inaczej
            arrival_time = self.time + distance

            if self.load + demands[j] > self.capacity:
                continue
            if arrival_time > due_dates[j]:
                continue
            # musimy zdazyc wrocic do depozytu
            if max(arrival_time, ready_times[j]) + service_times[j] + matrix[0][j] > due_dates[0]:
                continue

            availible_customers.append(j)

        return availible_customers



    ''' Funkcja dokonuje wyboru nastepnego miejsca (klienta lub depozytu)
        do odwiedzenia przez mrowke, na podstawie odpowiedniego wzoru oraz selekcji ruletkowej,
        jesli mrówka odwiedzila wszystkie miejsca to zwracamy None'''
    def nextPlace(self, matrix, p_random, alpha, beta, demands, ready_times, due_dates, service_times):
        i = self.tour[-1]
        available = self.getAvailibleCustomers(matrix, demands, ready_times, due_dates, service_times)

        # wybor losowej miejsc
        if random.random() < p_random:
            next = random.choice(available)
        #wybór względem śladu feromonów i heurystyki odległości
        else:

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
        start_service = max(arrival_time, ready_times[next])

        self.track_length += distance
        self.time = start_service + service_times[next]
        self.load += demands[next]
        self.tour.append(next)
        self.unvisited.remove(next)


    '''Funkcja implementująca powrót do depozytu'''
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
    def updateAnt(self, matrix, demands, ready_times, due_dates, service_times):
        if len(self.unvisited) > 0: #mrowce nie udalo sie odwiedzic wszystkich klientow
            self.track_length = float('inf')
        else:
            if self.best_track_length is None or self.track_length < self.best_track_length:
                self.best_track_length = self.track_length
                self.best_solution = list(self.solution)

        self.unvisited = set(range(1, self.places_nr))
        self.solution = []
        self.tour = [0]
        self.load = 0.0
        self.time = 0.0
        self.track_length = 0.0

    '''Funkcja slużąca do optymalizacji rozwiązania mrówki 
       alorytmem lokalnej optymalizcji 2-opt'''
    def twoOpt(self, matrix, demands, ready_times, due_dates, service_times):
        opt_solution = []
        total_distance = 0.0

        for tour in self.solution:
            best_tour = list(tour)
            pom, best_distance = self.checkTwoOpt(best_tour, matrix, demands, ready_times, due_dates, service_times)
            improved = True

            while improved:
                improved = False
                for i in range(1, len(best_tour) - 2):
                    for j in range(i+1, len(best_tour) - 1):
                        reversed = best_tour[i:j+1]
                        reversed.reverse()
                        new_tour = best_tour[:i] + reversed + best_tour[j+1:]

                        #sprawdzamy czy to nie powoduje problemow z oknami czasowymi
                        valid, new_distance = self.checkTwoOpt(new_tour, matrix, demands, ready_times, due_dates, service_times)

                        if valid and new_distance < best_distance:
                            best_tour = new_tour
                            best_distance = new_distance
                            improved = True

            opt_solution.append(best_tour)
            total_distance += best_distance

        self.solution = opt_solution
        self.track_length = total_distance


    '''Funkcja sprawdzająca czy 2-opt nie powoduje problemów z oknami czasowymi'''
    def checkTwoOpt(self, tour, matrix, demands, ready_times, due_dates, service_times):
        time = 0.0
        load = 0.0
        total_distance = 0.0
        for k in range(len(tour)-1):
            distance = matrix[min(tour[k],tour[k+1])][max(tour[k],tour[k+1])]
            arrival_time = time + distance
            if arrival_time > due_dates[tour[k+1]]:
                return False, 0
            time = max(arrival_time, ready_times[tour[k+1]]) + service_times[tour[k+1]]
            load = load + demands[tour[k+1]]
            if load > self.capacity:
                return False, 0
            total_distance += distance
        return True, total_distance