# main.py
from scraper import scrape_live_events
from spotify_client import SpotifyEnricher
from database import DatabaseManager
import datetime

def run_etl_pipeline():
    print(f"--- Starting Live Event Impact ETL: {datetime.datetime.now()} ---")
    
    # 1. Initialize Clients
    spotify = SpotifyEnricher()
    db = DatabaseManager()

    # 2. Extract Events (Web Scraping)
    df_events = scrape_live_events()

    # 3. Enrich Events with Spotify Artist IDs
    spotify_ids = []
    for artist in df_events["Artist_Name"]:
        metrics = spotify.get_artist_metrics(artist)
        spotify_ids.append(metrics["Spotify_Artist_ID"] if metrics else None)
    
    df_events["Spotify_Artist_ID"] = spotify_ids

    # 4. Load Events into MS SQL Server
    db.insert_events(df_events)

    # 5. Fetch & Load Daily Time-Series Metrics for All Tracked Artists
    tracked_artists = db.get_tracked_artists()
    daily_snapshots = []
    
    for artist_name in tracked_artists:
        metrics = spotify.get_artist_metrics(artist_name)
        if metrics:
            daily_snapshots.append(metrics)

    db.insert_daily_metrics(daily_snapshots)
    db.close()
    
    print("--- ETL Pipeline Execution Complete ---")

if __name__ == "__main__":
    run_etl_pipeline()