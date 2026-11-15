# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_live_events(url=None):
    """
    Scrapes live music events and returns a cleaned DataFrame.
    Update the CSS selectors below based on your target ticketing site.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    events_data = []

    if url:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Example CSS selectors for an event aggregator (e.g., Songkick / Insider)
            event_cards = soup.find_all("div", class_="event-card")
            
            for card in event_cards:
                artist = card.find("h3", class_="artist-name").text.strip()
                event_name = card.find("p", class_="event-title").text.strip()
                venue = card.find("span", class_="venue-name").text.strip()
                city = card.find("span", class_="city-name").text.strip()
                raw_date = card.find("time")["datetime"] # e.g., '2026-12-15'
                
                events_data.append({
                    "Artist_Name": artist,
                    "Event_Name": event_name,
                    "Venue": venue,
                    "City": city,
                    "Event_Date": raw_date
                })
        except Exception as e:
            print(f"[Scraper Warning] Live scrape failed or blocked: {e}. Loading seed events.")

    # Seed data fallback for immediate pipeline testing
    if not events_data:
        events_data = [
            {"Artist_Name": "Coldplay", "Event_Name": "Music of the Spheres Tour", "Venue": "D.Y. Patil Stadium", "City": "Navi Mumbai", "Event_Date": "2026-11-20"},
            {"Artist_Name": "Arijit Singh", "Event_Name": "Live in Concert", "Venue": "Jio World Garden", "City": "Mumbai", "Event_Date": "2026-12-05"},
            {"Artist_Name": "Diljit Dosanjh", "Event_Name": "Dil-Luminati Tour", "Venue": "Mahalaxmi Race Course", "City": "Mumbai", "Event_Date": "2026-11-28"},
            {"Artist_Name": "Prateek Kuhad", "Event_Name": "Silhouettes Tour", "Venue": "NESCO Center", "City": "Mumbai", "Event_Date": "2026-12-12"}
        ]

    df_events = pd.DataFrame(events_data)
    df_events["Event_Date"] = pd.to_datetime(df_events["Event_Date"]).dt.date
    return df_events