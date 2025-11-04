import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def wczytaj_dane_z_json(nazwa_pliku):
    with open(nazwa_pliku, 'r') as file:
        dane_json = json.load(file)
        return dane_json

def wykres_czasu(dane, parametr, f):
    plt.figure(figsize=(10, 6))
    plt.yscale('log')
    sns.barplot(x=parametr, y='czas', hue='nr_iteracji', data=dane, errorbar='sd', palette='viridis')
    plt.title(f'Czas wykonania algorytmu wględem {parametr} dla {f}')
    plt.xlabel(f'Parametr {parametr}')
    plt.ylabel('Czas [s] (Średnia)')
    plt.grid(axis='y', linestyle='--')
    plt.legend(title='Numer iteracji', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.9, 1])
    plt.savefig(f'wykresy/wykres_czasu_{parametr}_{f}.png')
    plt.show()
    plt.close()

def wykres_dokladnosci(dane, parametr, f):
    plt.figure(figsize=(10, 6))
    plt.yscale('log')
    sns.barplot(x=parametr, y='dokladnosc', hue='nr_iteracji', data=dane, errorbar='sd', palette='viridis')
    plt.title(f'Błąd bezwzględny względem zmiany {parametr} dla {f}')
    plt.xlabel(f'Parametr {parametr}')
    plt.ylabel('Dokładność')
    plt.grid(axis='y', linestyle='--')
    plt.legend(title='Numer iteracji', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.9, 1])
    plt.savefig(f'wykresy/wykres_dokladnosci_{parametr}_{f}.png')
    plt.show()
    plt.close()

def wykres_iteracji(dane, parametr, f):
    plt.figure(figsize=(10, 6))
    plt.yscale('log')
    sns.barplot(x=parametr, y='best_it', hue='nr_iteracji', data=dane, errorbar='sd', palette='viridis')
    plt.title(f'Liczba iteracji potrzebna w względem zmiany {parametr} dla {f}')
    plt.xlabel(f'Parametr {parametr}')
    plt.ylabel('Numer iteracji')
    plt.grid(axis='y', linestyle='--')
    plt.legend(title='Numer iteracji', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.9, 1])
    plt.savefig(f'wykresy/wykres_iteracji_{parametr}_{f}.png')
    plt.show()
    plt.close()

def narysuj_wykresy(plik):
    dane_json = wczytaj_dane_z_json(plik)
    dane = pd.DataFrame(dane_json)
    parametry_df = dane['parametry'].apply(pd.Series)
    dane = pd.concat([dane.drop('parametry', axis=1), parametry_df], axis=1)

    parametr, f = parametr_funkcja(plik)
    #sortowanie
    dane[parametr] = pd.to_numeric(dane[parametr], errors='coerce')
    dane = dane.sort_values(by=parametr)
    dane[parametr] = dane[parametr].astype(str)
    dane['nr_iteracji'] = dane['nr_iteracji'].astype(str)

    dane[parametr] = dane[parametr].astype(str)
    wykres_czasu(dane, parametr, f)
    wykres_dokladnosci(dane, parametr, f)
    wykres_iteracji(dane, parametr, f)


def parametr_funkcja(nazwa_pliku):
    temp = nazwa_pliku.replace('wyniki/', '')
    segmenty = temp.split('_')
    return segmenty[0], segmenty[2].replace('.json', '')

# ------------------ Funkcja1
narysuj_wykresy('wyniki/T_output_f1.json')
narysuj_wykresy('wyniki/M_output_f1.json')
narysuj_wykresy('wyniki/N_output_f1.json')
narysuj_wykresy('wyniki/k_output_f1.json')
narysuj_wykresy('wyniki/alfa_output_f1.json')

# ------------------ Funkcja2
narysuj_wykresy('wyniki/T_output_f2.json')
narysuj_wykresy('wyniki/M_output_f2.json')
narysuj_wykresy('wyniki/N_output_f2.json')
narysuj_wykresy('wyniki/k_output_f2.json')
narysuj_wykresy('wyniki/alfa_output_f2.json')

