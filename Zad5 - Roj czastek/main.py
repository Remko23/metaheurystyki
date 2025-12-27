import czastka
import math
import json
import time


class Simulation:
    def __init__(self, inercja, poznawcza, spoleczna,choice, N, T):
        self.inercja = inercja
        self.poznawcza = poznawcza
        self.spoleczna = spoleczna
        self.choice = choice
        self.N = N
        self.T = T

        if self.choice == 1:
            self.roj = [czastka.Czastka(inercja, poznawcza, spoleczna, 5) for _ in range(self.N)]
        elif self.choice == 2:
            self.roj = [czastka.Czastka(inercja, poznawcza, spoleczna, 10) for _ in range(self.N)]



    '''Pojedyncza symulacja. Zwraca parametry do dalszej analizy'''
    def simulate(self):
        i = 0
        g_best_x = 0
        g_best_y = 0
        g_best_przystosowanie = math.inf
        best_iter = 0

        for czst in self.roj:
            czst.grading(self.choice)
            if czst.przystosowanie < g_best_przystosowanie:
                g_best_przystosowanie = czst.przystosowanie
                g_best_x = czst.x
                g_best_y = czst.y

        while i < self.T:
            for czst in self.roj:
                czst.update_speed(g_best_x, g_best_y)
                czst.update_pos()
                czst.grading(self.choice)

                if czst.przystosowanie < g_best_przystosowanie:
                    g_best_przystosowanie = czst.przystosowanie
                    g_best_x = czst.x
                    g_best_y = czst.y
                    best_iter = i

            i += 1
        return g_best_x, g_best_y, g_best_przystosowanie, best_iter


'''Glowna funckja w kotrej przeprowadzamy symulacje 5 razy i zapisujemy wyniki do pliku json'''
def run_experiment(inercja, poznawcza, spoleczna, choice, N, T, filename):

        runs_counter = 5
        results = []
        for n in N:
            for iner in inercja:
                for pozn in poznawcza:
                    for t in T:
                        for run in range(runs_counter):
                            print(f"\n Kombinacja: N:{n}, inercja:{iner}, poznawcza:{pozn}, "
                                  f"spoleczna:{spoleczna}, T:{t}")
                            start_time = time.time()
                            sim = Simulation(
                                iner,
                                pozn,
                                spoleczna,
                                choice,
                                n,
                                t
                            )

                            best_x, best_y, best_val, best_iter = sim.simulate()
                            end = time.time()
                            results.append({
                                "N": n,
                                "inercja": iner,
                                "poznawcza": pozn,
                                "spoleczna": spoleczna,
                                "iteracje": t,
                                "run": run,
                                "run_time": round(end - start_time, 5),
                                "best_value": best_val,
                                "best_position": {
                                    "x": best_x,
                                    "y": best_y
                                },
                                "last_improvement_iteration": best_iter
                            })

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4)


run_experiment(
    inercja=[0.3, 0.6, 0.9],
    poznawcza=[0.5, 1.0, 1.5],
    spoleczna=1.0,
    choice=1,
    N=[20, 70, 200],
    T=[100, 400, 800],
    filename='choice1.json'
)

# T2
run_experiment(
    inercja=[0.3, 0.6, 0.9],
    poznawcza=[0.5, 1.0, 1.5],
    spoleczna=1.0,
    choice=2,
    N=[20, 70, 200],
    T=[100, 400, 800],
    filename='choice2.json'
)



