import random as r
from cmath import sin, pi


def alfa(T):
    return T*ochlodzenie;

def menu():
    T0 = float(input("Podaj temperaturę początkową T0: "))
    ochl = 1
    while ochl>=1 or ochl<0:
        ochl = float(input("Podaj wartosc ochladzania z zakresu [0,1]: "))
    l_e = 0
    while l_e<1:
        l_e = int(input("Podaj liczbę epok: "))
    while l_p<1:
        l_p = int(input("Podaj liczbę prób: "))

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

T, l_epok, l_prob, ochlodzenie = menu()
rozw = r.uniform(-10, 10)
print("Wylosowane pierwsze rozwiazanie =", rozw)
k = 1 #stała Boltzmana - DO ZMIANY

i=0
j=0
while i<l_epok:
    while j<l_prob:
        j+=1
    T=alfa(T)
    i+=1

print(rozw)
print(f2(1))