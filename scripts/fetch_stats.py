import pandas as pd
import sqlite3
import time
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

def setup_db():
    # Connects to SQLite (creates the file if it doesn't exist)
    conn = sqlite3.connect('../nba_stats.sqlite')
    return conn

def fetch_player_stats(player_name):
    # Find the player ID
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name]
    
    if not player_dict:
        print(f"Player {player_name} not found.")
        return None
    
    player_id = player_dict[0]['id']
    
    # Fetch career stats using the API
    print(f"Fetching stats for {player_name}...")
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    
    # Extract the data to a Pandas DataFrame
    df = career.get_data_frames()[0]
    
    # Add a column for the player's name for easier querying later
    df.insert(0, 'PLAYER_NAME', player_name)
    
    return df

if __name__ == "__main__":
    # 1. Setup connection
    conn = setup_db()
    
    # 2. Test with a couple of players who changed teams recently
    test_players = ["James Harden", "Kevin Durant"]
    
    for player in test_players:
        df = fetch_player_stats(player)
        
        if df is not None:
            # 3. Save to the SQLite database
            # 'append' adds to the table, 'replace' would overwrite it
            df.to_sql('career_stats', conn, if_exists='append', index=False)
            print(f"Successfully saved {player} to SQLite!")
            
        # Sleep for 1 second between requests to avoid API rate limits
        time.sleep(1)
        
    conn.close()
    print("Database connection closed.")
