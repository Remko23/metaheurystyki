import random as r
from math import exp, sin, pi
import time
import numpy as np
import pandas as pd

def alfa(T, ochlodzenie):
    return T*ochlodzenie;

def wybierz_funkcje():
    wybor_f = 0
    while wybor_f not in [1, 2]:
        wybor_f = int(input("Wybierz funkcję do symulowania (1=f1, 2=f2): "))

    if wybor_f == 1:
        f_wybrana = f1
        start_min = -150
        start_max = 150
        print(f"Przedział dla funkcji: [{start_min}, {start_max}]")
    else:
        f_wybrana = f2
        start_min = -1
        start_max = 2
        print(f"Przedział dla funkcji: [{start_min}, {start_max}]")

    return f_wybrana, start_min, start_max


#funkcja rozdzial 3 przyklad 1
def f1(x):
    if x<-95 and x>-105:
        return -2*abs(x+100)+10
    elif x<105 and x>95:
        return -2.2*abs(x-100)+11
    else:
        return 0

#funkcja rozdzial 4 przyklad 4
def f2(x):
    return x*sin(10*pi*x)+1

def P(rozw, rozw2, T, k):
    if(T==0):
        return 0.0

    return exp((f(rozw2)-f(rozw))/(k*T))

def symulowane_wyzarzanie(l_epok, l_prob, start, koniec, T, ochlodzenie, k, f):
    pierwsze_rozw = r.uniform(start, koniec)
    rozw = pierwsze_rozw
    best_rozw = rozw
    l_it = 0
    best_it = 0
    i = 0

    while i < l_epok:
        j = 0
        while j < l_prob:
            l_it += 1
            p_start = rozw - T
            p_koniec = rozw + T
            if (rozw - T < start):
                p_start = start
            if (rozw + T > koniec):
                p_koniec = koniec

            pom = r.uniform(p_start, p_koniec)
            if (f(pom) > f(rozw)):
                rozw = pom
            else:
                p = r.uniform(0, 1)
                if (P(rozw, pom, T, k) > p):
                    rozw = pom
            if (f(pom) > f(best_rozw)):
                best_rozw = pom
                best_it = l_it
            j += 1
        T = alfa(T, ochlodzenie)
        i += 1

    # print("x = ", best_rozw)
    # print("f(x) = ", f(best_rozw))
    # print("Liczba iteracji do znalezienia najlepszego rozw:", best_it)
    # print("Wylosowane pierwsze rozwiazanie:", pierwsze_rozw)
    return best_rozw, best_it, pierwsze_rozw

def symulacja_symulowanego_wyzarzania(f, start, koniec):
    i = 0
    results = []
    PARAMS = {
        'T': [50, 100, 200, 500, 1000],
        'M': [5, 20, 30, 50, 100],
        'N': [5, 20, 30, 50, 100],
        'alfa': [0.7, 0.8, 0.9, 0.95, 0.99],
        'k': [0.1, 0.3, 0.5, 0.8, 1]
    }
    it = [0,0,0,0,0]
    pom = 1
    # wykonujemy 5 razy dla tych samych parametrow, aby sprawdzić stabilność algorytmu dla wylosowywanych pierwszych rozwiazan
    while i < 5:
        start_time = time.time()

        best_rozw, best_it, pierwsze_rozw = symulowane_wyzarzanie(PARAMS['M'][0], PARAMS['N'][0], start, koniec, PARAMS['T'][0], PARAMS['alfa'][0], PARAMS['k'][0],f)

        end_time = time.time()
        duration = end_time - start_time

        results.append([best_rozw, f(best_rozw), best_it, pierwsze_rozw, duration, i+1, PARAMS['T'][0], PARAMS['M'][0], PARAMS['N'][0], PARAMS['alfa'][0], PARAMS['k'][0]])

        # Format pliku wynikowego:
        # [rozw, wartosc f(rozw), liczba iteracji do znalezienia najlepszego, wylosowane pierwsze rozw, czas trwania, numer iteracji (1-5), T, M, N, alfa, k]
        if f == f1:
            np.save('output.npy', np.array(results))
        elif f==f2:
            np.save('output2.npy', np.array(results))
        i += 1


f, start, koniec = wybierz_funkcje()
symulacja_symulowanego_wyzarzania(f, start, koniec)