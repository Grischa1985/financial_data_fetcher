# financial_data_fetcher
Ein Modul, um Finanzdaten von Yahoo Finance abzurufen und in CSV-Dateien zu speichern. 

Funktionen:
-----------
fetch_financial_data(ticker, data_types)
Ruft Finanzkennzahlen wie Bilanzdaten, Cashflow und G/V-Rechnung ab.


import financial_data_fetcher as fd

# Finanzkennzahlen für SAP abrufen
ticker = "SAP"
data_types = ["balance-sheet", "cash-flow", "financials"]
df = fd.fetch_financial_data(ticker, data_types)

# Finanzdaten anzeigen
print(df.head())

# Als CSV speichern
csv_filename = f"{ticker}_financial_data.csv"
df.to_csv(csv_filename, index=True)
print(f"Die Daten wurden in {csv_filename} gespeichert.")
