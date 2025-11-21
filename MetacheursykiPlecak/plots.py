import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import ast
from collections import Counter


def load_items():
    items = pd.read_csv("problem_plecakowy_dane.csv", sep="\t")

    items = items.rename(columns={
        "Numer": "item_id",
        "Nazwa": "name",
        "Waga (kg)": "weight",
        "Wartość (zł)": "value"
    })

    items["weight"] = items["weight"].astype(str).str.replace(" ", "").astype(int)
    items["value"] = items["value"].astype(str).str.replace(" ", "").astype(int)

    items["item_id"] = items["item_id"] - 1

    items = items.sort_values("item_id").reset_index(drop=True)

    return items


def load_data_from_file(filename):
    data = pd.read_csv(filename, sep=';')
    data['Time'] = data['Time'].apply(lambda x: ast.literal_eval(x))
    data['best'] = data['best'].apply(lambda x: ast.literal_eval(x))
    data['worst'] = data['worst'].apply(lambda x: ast.literal_eval(x))
    data['best_chrom'] = data['best_chrom'].apply(lambda x: ast.literal_eval(x))
    data['avg'] = data['avg'].apply(lambda x: ast.literal_eval(x))
    data['bst_sol'] = data['bst_sol'].apply(lambda x: ast.literal_eval(x))
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
    sns.barplot(data = data, x = 'run', y='best', hue='Pm', errorbar=None, palette='crest')
    plt.title(f'Najlepsze wyniki wzgledem parametru Pm')
    plt.xlabel('Nr iteracji')
    plt.ylabel('Ocena wyniku')
    plt.legend(title = 'Pm')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def avg_pm_plot(data):

    plt.figure(figsize=(10, 8))
    plt.yscale('log')
    sns.barplot(data = data, x = 'run', y='avg', hue='Pm', errorbar=None, palette='crest')
    plt.title(f'Srednia wynikow wzgledem parametru Pm')
    plt.xlabel('Nr iteracji')
    plt.ylabel('Srednia wynikow')
    plt.legend(title = 'Pm')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def avg_pc_plot(data):

    plt.figure(figsize=(10, 8))
    plt.yscale('log')
    sns.barplot(data = data, x = 'run', y='avg', hue='Pc', errorbar=None, palette='crest')
    plt.title(f'Srednia wynikow wzgledem parametru Pc')
    plt.xlabel('Nr iteracji')
    plt.ylabel('Srednia wynikow')
    plt.legend(title = 'Pc')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def best_solutions_plot(row, T):
    plt.figure(figsize=(12, 6))
    plt.yscale('log')

    for i, run_values in enumerate(row['bst_sol']):
        plt.plot(range(len(run_values)), run_values, linewidth=1, label=f"Run {i + 1}")

    plt.xlabel("Iteracja")
    plt.ylabel("Wartość najlepszego rozwiązania")
    plt.title(f"Zmiana najlepszego rozwiązania w czasie (T = {T}) | Pc={row['Pc']}, Pm={row['Pm']}, N={row['N']}")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
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


def extract_avg_data(data):
    rows = []

    for _, row in data.iterrows():
        for i, a in enumerate(row['avg']):
            rows.append({
                'Pc': row['Pc'],
                'Pm': row['Pm'],
                'N': row['N'],
                'T': row['T'],
                'run': i + 1,
                'avg': a
            })
    return pd.DataFrame(rows)


def extract_best_items_data(data):
    rows = []

    for _, row in data.iterrows():
            rows.append({
                'Pc': row['Pc'],
                'Pm': row['Pm'],
                'N': row['N'],
                'T': row['T'],
                'best_chrom': row['best_chrom']
            })
    return pd.DataFrame(rows)


def extract_best_solutions_data(data):
    rows = []

    for _, row in data.iterrows():
            rows.append({
                'Pc': row['Pc'],
                'Pm': row['Pm'],
                'N': row['N'],
                'T': row['T'],
                'bst_sol': row['bst_sol']
            })

    return pd.DataFrame(rows)


def decode_chromosome(best_chromosome, items):
    chosen_items = items[best_chromosome]

    total_weight = chosen_items["weight"].sum()
    total_value = chosen_items["value"].sum()

    return chosen_items, total_weight, total_value


def items_count(best_items, items):
    decoded_results = []

    for idx, row in best_items.iterrows():
        chrom_list = row['best_chrom']
        for chrom in chrom_list:
            chosen_items, _, _ = decode_chromosome(chrom, items)
            decoded_results.extend(chosen_items['name'].tolist())

    item_counts = Counter(decoded_results)
    summary = items.copy()
    summary['count'] = summary['name'].map(item_counts).fillna(0).astype(int)
    summary = summary.sort_values('count', ascending=False).reset_index(drop=True)

    return summary




def draw_plots():
    T1_data = load_data_from_file('T1_results.csv')
    T2_data = load_data_from_file('T2_results.csv')
    T3_data = load_data_from_file('T3_results.csv')
    extracted_time_t1 = extract_time_data(T1_data)
    extracted_best_t1 = extract_best_data(T1_data)
    extracted_avg_t1 = extract_avg_data(T1_data)
    extracted_best_items_t1 = extract_best_items_data(T1_data)
    extracted_best_solutions_t1 = extract_best_solutions_data(T1_data)
    extracted_time_t2 = extract_time_data(T2_data)
    extracted_best_t2 = extract_best_data(T2_data)
    extracted_avg_t2 = extract_avg_data(T2_data)
    extracted_best_items_t2 = extract_best_items_data(T2_data)
    extracted_best_solutions_t2 = extract_best_solutions_data(T2_data)
    extracted_time_t3 = extract_time_data(T3_data)
    extracted_best_t3 = extract_best_data(T3_data)
    extracted_avg_t3 = extract_avg_data(T3_data)
    extracted_best_items_t3 = extract_best_items_data(T3_data)
    extracted_best_solutions_t3 = extract_best_solutions_data(T3_data)

    for idx, row in extracted_best_solutions_t1.iterrows():
        best_solutions_plot(row, 200)

    for idx, row in extracted_best_solutions_t2.iterrows():
        best_solutions_plot(row, 500)

    for idx, row in extracted_best_solutions_t3.iterrows():
        best_solutions_plot(row, 1000)


    items = load_items()

    count_t1 = items_count(extracted_best_items_t1, items)
    count_t1.to_csv('count_t1.csv', sep=';', index=False)
    print(count_t1)

    count_t2 = items_count(extracted_best_items_t2, items)
    count_t2.to_csv('count_t2.csv', sep=';', index=False)
    print(count_t2)

    count_t3 = items_count(extracted_best_items_t3, items)
    count_t3.to_csv('count_t3.csv', sep=';', index=False)
    print(count_t3)


    time_N_plot(extracted_time_t1)
    best_pc_plot(extracted_best_t1)
    best_pm_plot(extracted_best_t1)
    avg_pc_plot(extracted_avg_t1)
    avg_pm_plot(extracted_avg_t1)

    time_N_plot(extracted_time_t2)
    best_pc_plot(extracted_best_t2)
    best_pm_plot(extracted_best_t2)
    avg_pc_plot(extracted_avg_t2)
    avg_pm_plot(extracted_avg_t2)

    time_N_plot(extracted_time_t3)
    best_pc_plot(extracted_best_t3)
    best_pm_plot(extracted_best_t3)
    avg_pc_plot(extracted_avg_t3)
    avg_pm_plot(extracted_avg_t3)


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