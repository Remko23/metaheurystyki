from collections import defaultdict

import matplotlib.pyplot as plt
import json

import numpy as np
import seaborn as sns
import pandas as pd


def readfile(filename):
    with open(filename, mode='r', encoding='utf-8') as f:
        return json.load(f)


def groups(data, keys):
    grouped = defaultdict(list)
    for i in data:
        key = tuple(i[k] for k in keys)
        grouped[key].append(i)
    return grouped


def standardowe(group):
    values = np.array([i['best_value'] for i in group])
    return {
        'mean': np.mean(values),
        'std': np.std(values),
        'min': np.min(values),
        'max': np.max(values)
    }

def time_N(data):
    grouped_by_N = defaultdict(list)
    for i in data:
        grouped_by_N[i['N']].append(i['run_time'])

    N_keys = sorted(grouped_by_N.keys())

    means = []

    for n in N_keys:
        m = np.mean(grouped_by_N[n])
        means.append(m)

    rows = []
    for N, times in grouped_by_N.items():
        rows.append({
            'N': N,
            'mean_time': np.mean(times)
        })

    df = pd.DataFrame(rows)

    plt.figure(figsize=(10,8))
    sns.barplot(data = df, x = 'N', y = 'mean_time', errorbar=None, palette='crest')
    plt.xlabel("Liczba cząstek N")
    plt.ylabel("Czas wykonania [s]")
    plt.title("Czas wykonania programu w zależności od N")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def time_T(data):
    grouped_by_T = defaultdict(list)
    for i in data:
        grouped_by_T[i['iteracje']].append(i['run_time'])

    T_keys = sorted(grouped_by_T.keys())

    means = []

    for n in T_keys:
        m = np.mean(grouped_by_T[n])
        means.append(m)

    rows = []
    for T, times in grouped_by_T.items():
        rows.append({
            'T': T,
            'mean_time': np.mean(times)
        })

    df = pd.DataFrame(rows)

    plt.figure(figsize=(10,8))
    sns.barplot(data = df, x = 'T', y = 'mean_time', errorbar=None, palette='crest')
    plt.xlabel("Liczba iteracji T")
    plt.ylabel("Czas wykonania [s]")
    plt.title("Czas wykonania programu w zależności od T")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def best_value_N(data):
    grouped_by_N = defaultdict(list)
    for i in data:
        grouped_by_N[i['N']].append(i['best_value'])

    N_keys = sorted(grouped_by_N.keys())

    means = []

    for n in N_keys:
        m = np.mean(grouped_by_N[n])
        means.append(m)

    rows = []
    for N, bv in grouped_by_N.items():
        rows.append({
            'N': N,
            'mean_bv': np.mean(bv)
        })

    df = pd.DataFrame(rows)

    plt.figure(figsize=(10,8))
    sns.barplot(data = df, x = 'N', y = 'mean_bv', errorbar=None, palette='crest')
    plt.xlabel("Liczba cząstek N")
    plt.ylabel("Best value")
    plt.title("Najlepsze wyniki wzgledem ilosci czastek")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def best_value_T(data):
    grouped_by_T = defaultdict(list)
    for i in data:
        grouped_by_T[i['iteracje']].append(i['best_value'])

    T_keys = sorted(grouped_by_T.keys())

    means = []

    for n in T_keys:
        m = np.mean(grouped_by_T[n])
        means.append(m)

    rows = []
    for T, times in grouped_by_T.items():
        rows.append({
            'T': T,
            'mean_time': np.mean(times)
        })

    df = pd.DataFrame(rows)

    plt.figure(figsize=(10,8))
    plt.yscale('log')
    sns.barplot(data = df, x = 'T', y = 'mean_time', errorbar=None, palette='crest')
    plt.xlabel("Liczba iteracji T")
    plt.ylabel("Best value")
    plt.title("Najlepsze wyniki wzgledem ilosci iteracji")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def best_value_inercja(data):
    grouped_by_in = defaultdict(list)
    for i in data:
        grouped_by_in[i['inercja']].append(i['best_value'])

    I_keys = sorted(grouped_by_in.keys())

    means = []

    for n in I_keys:
        m = np.mean(grouped_by_in[n])
        means.append(m)

    rows = []
    for iner, times in grouped_by_in.items():
        rows.append({
            'iner': iner,
            'mean_time': np.mean(times)
        })

    df = pd.DataFrame(rows)

    plt.figure(figsize=(10,8))
    plt.yscale('log')
    sns.barplot(data = df, x = 'iner', y = 'mean_time', errorbar=None, palette='crest')
    plt.xlabel("Inercja")
    plt.ylabel("Best value")
    plt.title("Najlepsze wyniki w zaloznosci od inercji")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def best_value_poznawcza(data):
    grouped_by_poz = defaultdict(list)
    for i in data:
        grouped_by_poz[i['poznawcza']].append(i['best_value'])

    P_keys = sorted(grouped_by_poz.keys())

    means = []

    for n in P_keys:
        m = np.mean(grouped_by_poz[n])
        means.append(m)

    rows = []
    for poz, times in grouped_by_poz.items():
        rows.append({
            'poz': poz,
            'mean_time': np.mean(times)
        })

    df = pd.DataFrame(rows)

    plt.figure(figsize=(10,8))
    sns.barplot(data = df, x = 'poz', y = 'mean_time', errorbar=None, palette='crest')
    plt.xlabel("komponent poznawczy")
    plt.ylabel("Best value")
    plt.title("Najlepsze wyniki w zaloznosci od komponentu poznawczego")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


data1 = readfile('choice1.json')
data2 = readfile('choice2.json')

time_N(data1)
time_T(data1)
best_value_N(data1)
best_value_T(data1)
best_value_inercja(data1)
best_value_poznawcza(data1)

time_N(data2)
time_T(data2)
best_value_N(data2)
best_value_T(data2)
best_value_inercja(data2)
best_value_poznawcza(data2)


grouped1 = groups(data1, ['N', 'inercja', 'poznawcza', 'spoleczna', 'iteracje'])
grouped2 = groups(data2, ['N', 'inercja', 'poznawcza', 'spoleczna', 'iteracje'])


with open("odchylenie1.txt", "w", encoding="utf-8") as f:
    f.write("N, inercja, poznawcza, spoleczna, T, mean, std, min, max\n")

    for params, group in grouped1.items():
        stats = standardowe(group)
        line = f"{params}, {stats['mean']:.3e}, {stats['std']:.3e}, {stats['min']:.3e}, {stats['max']:.3e}\n"
        f.write(line)

with open("odchylenie2.txt", "w", encoding="utf-8") as f:
    f.write("N, inercja, poznawcza, spoleczna, T, mean, std, min, max\n")

    for params, group in grouped2.items():
        stats = standardowe(group)
        line = f"{params}, {stats['mean']:.3e}, {stats['std']:.3e}, {stats['min']:.3e}, {stats['max']:.3e}\n"
        f.write(line)