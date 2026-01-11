from adjustText import adjust_text
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

def readFile(filename):
    with open(filename, 'r') as file:
        data_json = json.load(file)

    base_name = os.path.basename(filename).replace('.json', '')
    segments = base_name.split('-')
    dataset_name = segments[0]
    param_name = segments[2]

    return data_json, param_name, dataset_name

def boxPlot(filename):
    data, param, input_file = readFile(filename)

    results_list = []
    for entry in data:
        results_list.append({
            param: entry['parameters'][param],
            'best_track': entry['best_track']
        })

    df = pd.DataFrame(results_list)
    sorted_params = sorted(df[param].unique().tolist())
    boxplot_data = [df['best_track'][df[param] == p] for p in sorted_params]
    labels = [f"{param} = {b}" for b in df[param].unique()]

    plt.figure(figsize=(10, 6))
    plt.boxplot(boxplot_data, tick_labels=labels, patch_artist=True)
    plt.title(f'Rozkład długości najlepszych tras dla różnych wartości {param} (Plik: {input_file})')
    plt.ylabel('Dlugosc trasy')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

''' Wykres slupkowy sredniej dlugosci trasy z 5 iteracji wzgledem parametru '''
def meanPlot(filename):
    data, param, input_file = readFile(filename)

    results_list = []
    for entry in data:
        results_list.append({
            param: entry['parameters'][param],
            'best_track': entry['best_track'],
            'duration': entry['duration']
        })
    df = pd.DataFrame(results_list)

    summary_df = df.groupby(param).agg(
        mean_track=('best_track', 'mean')
    ).reset_index()

    summary_df = summary_df.sort_values(by=param)
    param_labels = [f"{param} = {p}" for p in summary_df[param].unique()]
    value_col = 'mean_track'
    ylabel = 'Srednia dlugosc trasy'

    plt.figure(figsize=(10, 6))
    sns.barplot(x=param, y=value_col, data=summary_df, errorbar=None, hue=param, legend=False)

    plt.xticks(ticks=range(len(summary_df)), labels=param_labels, rotation=0)
    plt.title(f'Srednia długość najlepszej trasy dla różnych wartości {param} (Plik: {input_file})')
    plt.ylabel(ylabel)
    plt.xlabel(f'Wartosc parametru {param}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


''' Wykres slupkowy sredniego czasu wykonania z 5 iteracji wzgledem parametru '''
def timePlot(filename):
    data, param, input_file = readFile(filename)
    results_list = []
    for entry in data:
        results_list.append({
            param: entry['parameters'][param],
            'best_track': entry['best_track'],
            'duration': entry['duration']
        })
    df = pd.DataFrame(results_list)

    summary_df = df.groupby(param).agg(mean_duration=('duration', 'mean')).reset_index()
    summary_df = summary_df.sort_values(by=param)
    param_labels = [f"{param} = {p}" for p in summary_df[param].unique()]
    value_col = 'mean_duration'

    plt.figure(figsize=(10, 6))
    sns.barplot(x=param, y=value_col, data=summary_df, errorbar=None, hue=param, legend=False)

    plt.xticks(ticks=range(len(summary_df)), labels=param_labels, rotation=0)
    plt.title(f'Sredni czas trwania algorytmu dla różnych wartości {param} (Plik: {input_file})')
    plt.ylabel('Sredni czas (s)')
    plt.xlabel(f'Wartosc parametru {param}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


def drawBestMaps():
    files_to_draw = ['r203', 'c203', 'rc203']

    for name in files_to_draw:
        stats_filename = f'results/STATS-{name}.json'
        coords_filename = f'data/{name}.txt'

        if not os.path.exists(stats_filename):
            print(f"Brak pliku statystyk dla {name}")
            continue

        with open(stats_filename, 'r') as file:
            stats_data = json.load(file)

        # Wczytanie współrzędnych (identycznie jak w main.py)
        coords = pd.read_csv(
            coords_filename,
            sep=r'\s+',
            skiprows=9,
            header=None,
            names=['CUST_NO', 'XCOORD', 'YCOORD', 'DEMAND', 'READY_TIME', 'DUE_DATE', 'SERVICE_TIME']
        )

        # Znalezienie absolutnie najlepszego wyniku w pliku STATS
        best_val = float('inf')
        best_tour = []
        best_params = {}

        for stat in stats_data:
            if stat['min'] < best_val:
                best_val = stat['min']
                best_tour = stat['best_tour']
                best_params = stat['parameters']

        if not best_tour:
            continue

        plt.figure(figsize=(12, 10))

        # Rysowanie klientów i depozytu
        plt.scatter(coords['XCOORD'][1:], coords['YCOORD'][1:], color='gray', s=20, label='Klienci', alpha=0.5)
        plt.scatter(coords['XCOORD'][0], coords['YCOORD'][0], color='red', s=150, marker='s', label='Depozyt', zorder=5)

        # Rysowanie tras (każda sub-lista w best_tour to jedna ciężarówka)
        # Używamy mapy kolorów, aby każda trasa miała inny kolor
        colors = plt.cm.get_cmap('tab20')(np.linspace(0, 1, len(best_tour)))

        for route_idx, route in enumerate(best_tour):
            # Wyciąganie współrzędnych dla punktów w trasie
            route_coords = coords.set_index('CUST_NO').loc[route]
            plt.plot(route_coords['XCOORD'], route_coords['YCOORD'],
                     color=colors[route_idx], linewidth=2, alpha=0.8,
                     marker='o', markersize=4)

        # Etykiety numerów klientów (opcjonalne, przy 100 klientach może być tłoczno)
        texts = []
        for i, row in coords.iterrows():
            if i % 5 == 0:  # Etykieta co 5 punktów, żeby zachować czytelność
                texts.append(plt.text(row['XCOORD'], row['YCOORD'], int(row['CUST_NO']), fontsize=8))
        adjust_text(texts, arrowprops=dict(arrowstyle="->", color='black', lw=0.5))

        title = (f"Najlepsza trasa VRPTW: {name}\nDystans: {best_val:.2f}, Trasy: {len(best_tour)}\n"
                 f"Parametry: m={best_params['m']}, T={best_params['T']}, α={best_params['alpha']}, β={best_params['beta']}")

        plt.title(title, fontsize=12)
        plt.xlabel('Współrzędna X')
        plt.ylabel('Współrzędna Y')
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.show()


def drawAllPlots(results_file_names):
    for filename in results_file_names:
        boxPlot(filename)
        meanPlot(filename)
        timePlot(filename)
    drawBestMaps()




results_file_names = [
    'results/c203-output-alpha.json',
    'results/c203-output-beta.json',
    'results/c203-output-m.json',
    'results/c203-output-p_random.json',
    'results/c203-output-rho.json',
    'results/c203-output-T.json',
    'results/r203-output-alpha.json',
    'results/r203-output-beta.json',
    'results/r203-output-m.json',
    'results/r203-output-p_random.json',
    'results/r203-output-rho.json',
    'results/r203-output-T.json',
    'results/rc203-output-alpha.json',
    'results/rc203-output-beta.json',
    'results/rc203-output-m.json',
    'results/rc203-output-p_random.json',
    'results/rc203-output-rho.json',
    'results/rc203-output-T.json',
]

drawAllPlots(results_file_names)
