import requests
from bs4 import BeautifulSoup
import pandas as pd


def fetch_financial_data(ticker, data_types=None):
    """
    Ruft Finanzkennzahlen von Yahoo Finance ab.
    Args:
        ticker (str): Das Tickersymbol der Aktie (z. B. 'KO', 'SAP').
        data_types (list): Liste von Typen der Finanzdaten (z. B. ['balance-sheet', 'cash-flow']).
    Returns:
        pd.DataFrame: Ein DataFrame mit den Finanzkennzahlen.
    """
    if data_types is None:
        data_types = ["balance-sheet"]
    all_data = {}

    for data_type in data_types:
        base_url = f"https://de.finance.yahoo.com/quote/{ticker}/{data_type}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, wie Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(base_url, headers=headers)
        if response.status_code != 200:
            print(f"Fehler beim Abrufen der Seite für {data_type}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        # Tabelle finden
        table_container = soup.find("div", {"class": "tableContainer"})
        if not table_container:
            print(f"Keine Daten für {ticker} gefunden oder die Inhalte sind dynamisch geladen.")
            continue

        rows = table_container.find_all("div", {"class": "row"})
        # Daten extrahieren
        data = []
        for row in rows:
            cells = row.find_all("div", {"class": "column"})
            row_data = [cell.text.strip() for cell in cells]
            if row_data:
                data.append(row_data)

        # Header dynamisch extrahieren
        header_row = table_container.find("div", {"class": "tableHeader"})
        headers = ["Description"]
        if header_row:
            columns = header_row.find_all("div", {"class": "column"})
            headers += [col.text.strip() for col in columns]

        # DataFrame erstellen und in das Dictionary einfügen
        df = pd.DataFrame(data, columns=headers[:len(data[0])])
        all_data[data_type] = df

    # Alle DataFrames kombinieren
    combined_df = pd.concat(all_data.values(), keys=all_data.keys(), names=['Data Type', 'Index'])
    return combined_df


def main():
    """
    Hauptfunktion, die den Benutzer nach einer Aktie fragt
    und die Finanzkennzahlen für die gewünschte Kategorie abruft.
    """
    print("Willkommen zur Finanzdatenanalyse!")
    ticker = input("Gib das Tickersymbol der Aktie ein (z. B. KO für Coca-Cola): ").strip().upper()

    data_types = ["balance-sheet", "cash-flow", "financials"]  # Alle Datentypen
    print(f"\nAbrufen von '{', '.join(data_types)}'-Daten für {ticker}...\n")

    df = fetch_financial_data(ticker, data_types)
    if df is not None:
        df = df[['Description', 'Aufschlüsselung']]
        df = df.dropna(subset=['Aufschlüsselung'])
        df_clean = df
        print(df_clean)
        # Als CSV speichern
        csv_filename = f"{ticker}_financial_data.csv"
        df.to_csv(csv_filename, index=True)
        print(f"\nDie Daten wurden in der Datei '{csv_filename}' gespeichert.")


if __name__ == "__main__":
    main()
