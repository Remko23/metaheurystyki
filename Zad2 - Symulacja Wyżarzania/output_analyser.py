import json

def wczytaj_dane_z_json(nazwa_pliku):
    with open(nazwa_pliku, 'r') as file:
        dane_json = json.load(file)
        return dane_json

nazwa_pliku = 'T_output_f1.json'
dane = wczytaj_dane_z_json(nazwa_pliku)

print(json.dumps(dane, indent=4))
print(dane[0]['Parametry_Aktualne']['T0'])