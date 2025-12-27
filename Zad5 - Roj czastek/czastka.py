import random
import math


class Czastka:
    def __init__(self, inercja, poznawcza, spoleczna, zakres):
        self.x = random.uniform(-zakres, zakres )
        self.y = random.uniform(-zakres, zakres )
        self.inercja = inercja
        self.poznawcza = poznawcza
        self.spoleczna = spoleczna
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.przystosowanie = math.inf
        self.best_przystosowanie = math.inf
        self.best_x = self.x
        self.best_y = self.y


    '''Oceniamy przystosowanie kazdej czastki '''
    def grading(self, choice):
        if choice == 1:
            grade = (-20 * math.exp(-0.2 * math.sqrt(0.5*(self.x**2 + self.y**2)))
                     - math.exp(0.5*(math.cos(2*math.pi*self.x) + math.cos(2*math.pi*self.y))) + math.e + 20)
        elif choice == 2:
            grade = (self.x + 2*self.y - 7)**2 + (2*self.x + self.y - 5)**2
        else:
            print('Wybierz ocpje 1 lub 2 ')
            return 0
        self.przystosowanie = grade

        if grade < self.best_przystosowanie:
            self.best_przystosowanie = grade
            self.best_x = self.x
            self.best_y = self.y


    '''Funckaj do aktualizowania predkosci (wyliczamy w niej wszystkie skladowe)'''
    def update_speed(self, g_best_x, g_best_y):
        r1 = random.random()
        r2 = random.random()

        inercja_x = self.inercja * self.speed_x
        inercja_y = self.inercja * self.speed_y

        poznawczy_x = self.poznawcza * r1 * (self.best_x - self.x)
        poznawczy_y = self.poznawcza * r1 * (self.best_y - self.y)

        spoleczny_x = self.spoleczna * r2 * (g_best_x - self.x)
        spoleczny_y = self.spoleczna * r2 * (g_best_y - self.y)

        self.speed_x = inercja_x + poznawczy_x + spoleczny_x
        self.speed_y = inercja_y + poznawczy_y + spoleczny_y

    '''Update pozycji czastki'''
    def update_pos(self):
        self.x += self.speed_x
        self.y += self.speed_y