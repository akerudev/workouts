import csv
from datetime import datetime
from collections import defaultdict
import os
import matplotlib.pyplot as plt

FILE_NAME = "allenamenti.csv"

def inizializza_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["data", "km"])

def aggiungi_allenamento():
    data_str = input("Inserisci la data (formato YYYY-MM-DD): ")
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        print("⚠️ Formato data non valido.")
        return
    
    try:
        km = float(input("Inserisci i km percorsi: "))
    except ValueError:
        print("⚠️ Valore km non valido.")
        return
    
    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([data, km])
    print(f"✅ Allenamento aggiunto: {data} - {km} km")

def mostra_allenamenti():
    if not os.path.exists(FILE_NAME):
        print("Nessun allenamento registrato.")
        return
    
    with open(FILE_NAME, newline="") as f:
        reader = csv.DictReader(f)
        print("\n📘 Diario Allenamenti:")
        for row in reader:
            print(f"{row['data']} - {row['km']} km")

def somma_mensile():
    if not os.path.exists(FILE_NAME):
        print("Nessun dato disponibile.")
        return {}
    
    km_mensili = defaultdict(float)
    with open(FILE_NAME, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = datetime.strptime(row["data"], "%Y-%m-%d")
            chiave_mese = data.strftime("%Y-%m")
            km_mensili[chiave_mese] += float(row["km"])
    
    print("\n📊 Chilometri mensili:")
    for mese, km in sorted(km_mensili.items()):
        print(f"{mese}: {km:.1f} km")
    
    return km_mensili

def grafico_mensile():
    km_mensili = somma_mensile()
    if not km_mensili:
        return

    mesi = sorted(km_mensili.keys())
    km_totali = [km_mensili[mese] for mese in mesi]

    plt.figure(figsize=(8,5))
    plt.bar(mesi, km_totali)
    plt.xlabel("Mese")
    plt.ylabel("Chilometri totali")
    plt.title("📈 Chilometri percorsi per mese")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.show()

def menu():
    inizializza_file()
    while True:
        print("\n--- Diario Allenamento Ciclismo ---")
        print("1️⃣  Aggiungi allenamento")
        print("2️⃣  Mostra tutti gli allenamenti")
        print("3️⃣  Totale chilometri per mese")
        print("4️⃣  Mostra grafico mensile")
        print("5️⃣  Esci")
        
        scelta = input("Scegli un'opzione: ")
        
        if scelta == "1":
            aggiungi_allenamento()
        elif scelta == "2":
            mostra_allenamenti()
        elif scelta == "3":
            somma_mensile()
        elif scelta == "4":
            grafico_mensile()
        elif scelta == "5":
            print("👋 Alla prossima pedalata!")
            break
        else:
            print("❌ Scelta non valida.")

if __name__ == "__main__":
    menu()
