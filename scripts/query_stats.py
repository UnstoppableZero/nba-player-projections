import sqlite3
import pandas as pd

def check_data():
    # Connect to the database (adjust path if you run this from the root folder instead of /scripts)
    conn = sqlite3.connect('../nba_stats.sqlite')
    
    # Write a SQL query to pull Kevin Durant's stats
    query = "SELECT PLAYER_NAME, SEASON_ID, TEAM_ABBREVIATION, GP, PTS, AST, REB FROM career_stats WHERE PLAYER_NAME = 'Kevin Durant'"
    
    # Pandas makes it incredibly easy to read SQL directly into a DataFrame
    df = pd.read_sql(query, conn)
    
    print(f"Successfully loaded {len(df)} seasons for {df['PLAYER_NAME'].iloc[0]}!\n")
    print("Here are his first 5 seasons:")
    print(df.head())
    
    print("\nHere are his most recent 5 seasons:")
    print(df.tail())
    
    conn.close()

if __name__ == "__main__":
    check_data()
