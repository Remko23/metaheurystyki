import random as r
from math import exp, sin, pi

def alfa(T, ochlodzenie):
    return T*ochlodzenie;

def wybierz_funkcje():
    wybor_f = 0
    while wybor_f not in [1, 2]:
        wybor_f = int(input("Wybierz funkcję do optymalizacji (1=f1, 2=f2): "))

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

def menu():
    T0 = float(input("Podaj temperaturę początkową T0: "))
    ochl = 1
    while ochl>=1 or ochl<=0:
        ochl = float(input("Podaj wartosc ochladzania z zakresu (0,1): "))
    l_e = 0
    l_p = 0
    while l_e<1:
        l_e = int(input("Podaj liczbę epok (M): "))
    while l_p<1:
        l_p = int(input("Podaj liczbę prób (N): "))
    return T0, l_e, l_p, ochl


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

    print("x = ", best_rozw)
    print("f(x) = ", f(best_rozw))
    print("Liczba iteracji do znalezienia najlepszego rozw:", best_it)
    print("Wylosowane pierwsze rozwiazanie:", pierwsze_rozw)


T, l_epok, l_prob, ochlodzenie = menu()
f, start, koniec = wybierz_funkcje()
k = 0.1
i = 0

# wykonujemy 5 razy dla tych samych parametrow, aby sprawdzić stabilność algorytmu dla wylosowywanych pierwszych rozwiazan
print("-------------------------------------------------------")
while i<5:
    print("-------------- Wyniki dla iteracji nr.", i+1, "--------------")
    symulowane_wyzarzanie(l_epok, l_prob, start, koniec, T, ochlodzenie, k, f)
    print("-------------------------------------------------------")
    i+=1