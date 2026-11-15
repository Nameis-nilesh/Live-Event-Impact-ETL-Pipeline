# spotify_client.py
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from datetime import datetime

class SpotifyEnricher:
    def __init__(self):
        auth_manager = SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_artist_metrics(self, artist_name):
        """
        Searches for an artist by name, fetches full artist details by ID, 
        and safely pulls daily follower, popularity, and top track metrics.
        """
        try:
            # 1. Search for the artist to get their ID
            results = self.sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
            items = results.get("artists", {}).get("items", [])
            
            if not items:
                print(f"[Spotify API] No match found for artist: {artist_name}")
                return None

            artist_id = items[0].get("id")

            # 2. Fetch the FULL artist object by ID (contains followers & popularity)
            artist = self.sp.artist(artist_id)
            
            exact_name = artist.get("name", artist_name)
            followers = artist.get('followers', {}).get('total', 0)
            popularity = artist.get('popularity', 0)

            # 3. Fetch the artist's most popular track using Track Search
            track_results = self.sp.search(q=f"artist:{artist_name}", type="track", limit=10)
            tracks = track_results.get("tracks", {}).get("items", [])
            
            if tracks:
                # Sort tracks by popularity score safely
                sorted_tracks = sorted(tracks, key=lambda x: x.get("popularity", 0), reverse=True)
                
                # Safely extract name and popularity using .get() to prevent KeyErrors
                top_track_name = sorted_tracks[0].get("name", "Unknown")
                top_track_pop = sorted_tracks[0].get("popularity", 0)
            else:
                top_track_name = "N/A"
                top_track_pop = 0

            return {
                "Spotify_Artist_ID": artist_id,
                "Artist_Name": exact_name,
                "Followers": followers,
                "Popularity_Score": popularity,
                "Top_Track_Name": top_track_name,
                "Top_Track_Popularity": top_track_pop,
                "Snapshot_Date": datetime.today().date()
            }

        except Exception as e:
            print(f"[Spotify API Error] Failed to fetch data for {artist_name}: {e}")
            return None