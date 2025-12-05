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

    summary_df = df.groupby(param).agg(
        mean_duration=('duration', 'mean')
    ).reset_index()
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


def drawAllPlots(filename):
    boxPlot(filename)
    meanPlot(filename)
    timePlot(filename)


drawAllPlots('results/alpha-output-32.json')
drawAllPlots('results/alpha-output-80.json')
drawAllPlots('results/beta-output-32.json')
drawAllPlots('results/beta-output-80.json')
drawAllPlots('results/m-output-32.json')
drawAllPlots('results/m-output-80.json')
drawAllPlots('results/p_random-output-32.json')
drawAllPlots('results/p_random-output-80.json')
drawAllPlots('results/rho-output-32.json')
drawAllPlots('results/rho-output-80.json')
drawAllPlots('results/T-output-32.json')
drawAllPlots('results/T-output-80.json')
