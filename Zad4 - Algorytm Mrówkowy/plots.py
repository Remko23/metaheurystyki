from adjustText import adjust_text
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def readFile(filename):
    input_files = {
        '32': 'A-n32-k5',
        '80': 'A-n80-k10',
    }
    with open(filename, 'r') as file:
        data_json = json.load(file)
        temp = filename.replace('results/', '')
        segments = temp.split('-')
        return data_json, segments[0], input_files[segments[2].replace('.json', '')]

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
    plt.yscale('log')
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
    plt.yscale('log')
    plt.title(f'Sredni czas trwania algorytmu dla różnych wartości {param} (Plik: {input_file})')
    plt.ylabel('Sredni czas (s)')
    plt.xlabel(f'Wartosc parametru {param}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


def drawBestMaps():
    files_names = [
        ['results/STATS-32.json', 'data/A-n32-k5.txt', 'A-n32-k5.txt'],
        ['results/STATS-80.json', 'data/A-n80-k10.txt', 'A-n80-k10.txt']
    ]

    for stats_filename, coords_filename, map_title in files_names:
        with open(stats_filename, 'r') as file:
            stats_data = json.load(file)

        coords = pd.read_csv(
            coords_filename,
            sep=r'\s+',
            header=None,
            names=['attractionID', 'X', 'Y'],
            comment='['
        )
        best = float('inf')
        best_tour = []
        best_params = {}

        for stat in stats_data:
            if stat['min'] < best:
                best = stat['min']
                best_tour = stat['best_tour']
                best_params = stat['parameters']

        tour_X = [coords['X'][i] for i in best_tour]
        tour_Y = [coords['Y'][i] for i in best_tour]
        plt.figure(figsize=(10, 8))
        plt.scatter(coords['X'], coords['Y'], color='orange', s=50, label='Atrakcje')
        texts = []  # Utwórz listę na obiekty tekstowe
        for index, row in coords.iterrows():
            texts.append(plt.text(row['X'], row['Y'], row['attractionID'], fontsize=9))
        adjust_text(texts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5)) #dopasowanie tekstu żeby się nie pokrywały numery atrakcji

        plt.plot(tour_X, tour_Y, color='orange', linestyle='-', linewidth=2, label=f'Najlepsza trasa (Długość: {best:.2f})')

        plt.plot(tour_X[0], tour_Y[0], 'o', markersize=10, color='lightgreen', label='Start')

        plt.title(f'Najlepsza trasa dla pliku: {map_title}.txt'
                        f'\n Długość trasy: {best:.2f} '
                        f'\n (m = {best_params['m']}, '
                        f'p_random = {best_params['p_random']}, '
                        f'T = {best_params['T']}, '
                        f'alpha = {best_params['alpha']}, '
                        f'beta = {best_params['beta']}, '
                        f'rho = {best_params['rho']})', fontsize=14)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()



def drawAllPlots(results_file_names):
    for filename in results_file_names:
        boxPlot(filename)
        meanPlot(filename)
        timePlot(filename)
    drawBestMaps()

results_file_names = [
    'results/alpha-output-32.json',
    'results/alpha-output-80.json',
    'results/beta-output-32.json',
    'results/beta-output-80.json',
    'results/m-output-32.json',
    'results/m-output-80.json',
    'results/p_random-output-32.json',
    'results/p_random-output-80.json',
    'results/rho-output-32.json',
    'results/rho-output-80.json',
    'results/T-output-32.json',
    'results/T-output-80.json'
]

drawAllPlots(results_file_names)
