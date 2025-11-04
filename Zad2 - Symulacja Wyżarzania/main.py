import random as r
from math import exp, sin, pi
import time
import numpy as np
import json

def menu():
    print("1 - Podaj parametry i wykonaj dla nich symulowane wyzarzanie")
    print("2 - Przeprowadz symulację dla różnych wartości wybranego parametru")
    wybor = int(input("Twój wybór: "))
    if wybor == 1:
        T,M,N,ochl,k = pobierz_parametry()
        best, bestit, wyl_rozw = symulowane_wyzarzanie(M, N, start, koniec, T, ochl, k ,f)
        print(f"x = {best}\nf(x) = {f(best)}\nIteracji do znalezienia rozw = {bestit}\nWylosowane pierwsze rozwiazanie = {wyl_rozw}")
    elif wybor == 2:
        symulacja_symulowanego_wyzarzania(f, start, koniec)

def pobierz_parametry():
    T0 = float(input("Podaj temperaturę początkową T0: "))
    ochl = 1
    while ochl >= 1 or ochl <= 0:
        ochl = float(input("Podaj wartosc ochladzania z zakresu (0,1): "))
    l_e = 0
    l_p = 0
    while l_e < 1:
        l_e = int(input("Podaj liczbę epok (M): "))
    while l_p < 1:
        l_p = int(input("Podaj liczbę prób (N): "))
    k = float(input("Podaj stałą Boltzmanna (k): "))
    return T0, l_e, l_p, ochl, k

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
    all_results_json = []
    par = -1
    while par not in [0, 1, 2, 3, 4]:
        par = int(input("Wybierz parametr do symulacji: \nT - 0 \nM - 1\nN - 2\nalfa - 3\nk - 4\nTwój wybór: "))
    par_keys = ['T', 'M', 'N', 'alfa', 'k']
    key = par_keys[par]
    VALUES = {
        'T': [1000, 20, 50, 100, 200, 300, 400, 500, 700, 900],
        'M': [100, 5, 10, 20, 30, 50, 200, 500, 700, 1000],
        'N': [100, 5, 10, 20, 30, 50, 200, 500, 700, 1000],
        'alfa': [0.85, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.97, 0.99],
        'k': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    }
    PARAMS = {
        'T': VALUES['T'][0], #domyslnie: 1000
        'M': VALUES['M'][0], #domyslnie: 100
        'N': VALUES['N'][0], #domyslnie: 100
        'alfa': VALUES['alfa'][0], #domyslnie: 0.85
        'k': VALUES['k'][0], #domyslnie: 0.1
    }
    p = 0
    while p < len(VALUES[key]):
        PARAMS[key] = VALUES[key][p]
        current_param_results = []
        # wykonujemy 5 razy dla tych samych parametrow, aby sprawdzić stabilność algorytmu dla wylosowywanych pierwszych rozwiazan
        while i < 5:
            start_time = time.time()
            best_rozw, best_it, pierwsze_rozw = symulowane_wyzarzanie(PARAMS['M'], PARAMS['N'], start, koniec, PARAMS['T'], PARAMS['alfa'], PARAMS['k'], f)
            end_time = time.time()
            duration = end_time - start_time
            result_dict = {
                'best_rozw': best_rozw,
                'f(x)': f(best_rozw),
                'best_it': best_it,
                'poczatkowe_rozw': pierwsze_rozw,
                'czas': duration,
                'nr_iteracji': i + 1,
                'parametry': {
                    'T': PARAMS['T'],
                    'M': PARAMS['M'],
                    'N': PARAMS['N'],
                    'alfa': PARAMS['alfa'],
                    'k': PARAMS['k']
                }
            }
            current_param_results.append(result_dict)
            i += 1

        all_results_json.extend(current_param_results)
        filename = f'{key}_output_f1.json' if f == f1 else f'{key}_output_f2.json'
        with open(filename, 'w') as file:
            json.dump(all_results_json, file, indent=4)
        p+=1

f, start, koniec = wybierz_funkcje()
menu()