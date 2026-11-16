import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import time

def setup_db():
    conn = sqlite3.connect('../nba_stats.sqlite')
    return conn

def scrape_recent_trades(season_year=2024):
    print(f"Scraping transactions for the {season_year} season...")
    url = f"https://www.basketball-reference.com/leagues/NBA_{season_year}_transactions.html"
    
    # Basketball-Reference requires a User-Agent header, or they block the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve page.")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the main transaction list
    transaction_list = soup.find("ul", class_="page_index")
    if not transaction_list:
        print("Could not find the transaction list on the page.")
        return None

    trade_records = []
    
    # Iterate through the dates and transactions
    for li in transaction_list.find_all("li", recursive=False):
        date_span = li.find("span")
        if not date_span:
            continue
            
        trade_date = date_span.text.strip()
        
        # Look at the transaction descriptions under this date
        for p in li.find_all("p"):
            transaction_text = p.text.strip()
            
            # We only care about trades for this ML model, not free agent signings
            if "traded" in transaction_text.lower():
                trade_records.append({
                    "Trade_Date": trade_date,
                    "Transaction_Details": transaction_text,
                    "Season": season_year
                })

    df = pd.DataFrame(trade_records)
    print(f"Found {len(df)} trades in {season_year}!")
    return df

if __name__ == "__main__":
    conn = setup_db()
    
    # Let's test it by pulling the 2023 and 2024 seasons (Kevin Durant was traded in Feb 2023)
    years_to_scrape = [2023, 2024]
    
    for year in years_to_scrape:
        trade_df = scrape_recent_trades(year)
        if trade_df is not None and not trade_df.empty:
            # Save the trades to a new table in our existing SQLite database
            trade_df.to_sql('trade_logs', conn, if_exists='append', index=False)
        
        # Sleep to respect Basketball-Reference's servers
        time.sleep(3)
        
    conn.close()
    print("Trade data saved to SQLite database successfully.")
