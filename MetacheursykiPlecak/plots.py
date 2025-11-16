import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import ast


def load_data_from_file(filename):
    data = pd.read_csv(filename, sep=';')
    data['Time'] = data['Time'].apply(lambda x: ast.literal_eval(x))
    data['best'] = data['best'].apply(lambda x: ast.literal_eval(x))
    data['worst'] = data['worst'].apply(lambda x: ast.literal_eval(x))
    return data


def time_N_plot(data):

    plt.figure(figsize=(10, 8))
    sns.barplot(data = data, x = 'run', y = 'time', hue='N', errorbar=None, palette='crest')
    plt.title(f'Czas wykonania algorytmu dla wielkosci populacji N')
    plt.xlabel('Nr iteracji')
    plt.ylabel('Czas wykonania [s]')
    plt.legend(title = 'N')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def best_pc_plot(data):

    plt.figure(figsize=(10, 8))
    plt.yscale('log')
    sns.barplot(data = data, x = 'run', y = 'best', hue='Pc', errorbar=None, palette='crest')
    plt.title(f'Najlepsze wyniki wzgledem parametru Pc')
    plt.xlabel('Nr iteracji')
    plt.ylabel('Ocena wyniku')
    plt.legend(title = 'Pc')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def best_pm_plot(data):

    plt.figure(figsize=(10, 8))
    plt.yscale('log')
    sns.barplot(data = data, x = 'run', y = 'best', hue='Pm', errorbar=None, palette='crest')
    plt.title(f'Najlepsze wyniki wzgledem parametru Pm')
    plt.xlabel('Nr iteracji')
    plt.ylabel('Ocena wyniku')
    plt.legend(title = 'Pm')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def extract_time_data(data):
    rows = []

    for _, row in data.iterrows():
        for i, t in enumerate(row['Time']):
            rows.append({
                'Pc': row['Pc'],
                'Pm': row['Pm'],
                'N': row['N'],
                'T': row['T'],
                'run': i + 1,
                'time': t
            })
    return pd.DataFrame(rows)


def extract_best_data(data):
    rows = []

    for _, row in data.iterrows():
        for i, b in enumerate(row['best']):
            rows.append({
                'Pc': row['Pc'],
                'Pm': row['Pm'],
                'N': row['N'],
                'T': row['T'],
                'run': i + 1,
                'best': b
            })
    return pd.DataFrame(rows)


def draw_plots():
    T1_data = load_data_from_file('T1_results')
    T2_data = load_data_from_file('T2_results')
    T3_data = load_data_from_file('T3_results')
    extracted_time_t1 = extract_time_data(T1_data)
    extracted_best_t1 = extract_best_data(T1_data)
    extracted_time_t2 = extract_time_data(T2_data)
    extracted_best_t2 = extract_best_data(T2_data)
    extracted_time_t3 = extract_time_data(T3_data)
    extracted_best_t3 = extract_best_data(T3_data)


    time_N_plot(extracted_time_t1)
    best_pc_plot(extracted_best_t1)
    best_pm_plot(extracted_best_t1)

    time_N_plot(extracted_time_t2)
    best_pc_plot(extracted_best_t2)
    best_pm_plot(extracted_best_t2)

    time_N_plot(extracted_time_t3)
    best_pc_plot(extracted_best_t3)
    best_pm_plot(extracted_best_t3)



    # liczymy średnią, medianę, minimum, maksimum i odchylenie standardowe najlepszych wyników
    # dla każdej kombinacji parametrów z zaprojektowanych eksperymentów
    stats_t1 = extracted_best_t1.groupby(['Pc', 'Pm', 'N', 'T'])['best'].agg(
    mean='mean',
    median='median',
    minimum='min',
    maximum='max',
    std_dev='std'
    ).reset_index()
    stats_t1['std_dev'] = stats_t1['std_dev'].round(3)
    stats_t1.to_csv("best_stats_t1.csv", sep=';', index=False)

    stats_t2 = extracted_best_t2.groupby(['Pc', 'Pm', 'N', 'T'])['best'].agg(
        mean='mean',
        median='median',
        minimum='min',
        maximum='max',
        std_dev='std'
    ).reset_index()
    stats_t2['std_dev'] = stats_t2['std_dev'].round(3)
    stats_t2.to_csv("best_stats_t2.csv", sep=';', index=False)

    stats_t3 = extracted_best_t3.groupby(['Pc', 'Pm', 'N', 'T'])['best'].agg(
        mean='mean',
        median='median',
        minimum='min',
        maximum='max',
        std_dev='std'
    ).reset_index()
    stats_t3['std_dev'] = stats_t3['std_dev'].round(3)
    stats_t3.to_csv("best_stats_t3.csv", sep=';', index=False)



draw_plots()