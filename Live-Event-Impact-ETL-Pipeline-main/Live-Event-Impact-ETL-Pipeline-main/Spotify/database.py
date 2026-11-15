# database.py
import mysql.connector
from config import MYSQL_CONFIG

class DatabaseManager:
    def __init__(self):
        # Connects using your MySQL configuration from config.py
        self.conn = mysql.connector.connect(**MYSQL_CONFIG)
        self.cursor = self.conn.cursor()

    def insert_events(self, df_events):
        """Inserts new concert events into Dim_Events using MySQL duplicate-handling logic."""
        query = """
        INSERT INTO Dim_Events (Artist_Name, Spotify_Artist_ID, Event_Name, Venue, City, Event_Date)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            Event_Name = VALUES(Event_Name),
            Venue = VALUES(Venue);
        """
        for _, row in df_events.iterrows():
            self.cursor.execute(
                query,
                (
                    row["Artist_Name"], 
                    row.get("Spotify_Artist_ID", None),
                    row["Event_Name"], 
                    row["Venue"], 
                    row["City"], 
                    row["Event_Date"]
                )
            )
        self.conn.commit()
        print(f"[Database] Processed {len(df_events)} event records into MySQL.")

    def insert_daily_metrics(self, metrics_list):
        """Inserts daily artist streaming snapshots into Fact_Artist_Daily_Metrics."""
        query = """
        INSERT INTO Fact_Artist_Daily_Metrics (
            Spotify_Artist_ID, Artist_Name, Followers, 
            Popularity_Score, Top_Track_Name, Top_Track_Popularity, Snapshot_Date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            Followers = VALUES(Followers),
            Popularity_Score = VALUES(Popularity_Score),
            Top_Track_Popularity = VALUES(Top_Track_Popularity);
        """
        inserted_count = 0
        for m in metrics_list:
            if m:
                self.cursor.execute(
                    query,
                    (
                        m["Spotify_Artist_ID"], 
                        m["Artist_Name"], 
                        m["Followers"],
                        m["Popularity_Score"], 
                        m["Top_Track_Name"],
                        m["Top_Track_Popularity"], 
                        m["Snapshot_Date"]
                    )
                )
                inserted_count += 1
        self.conn.commit()
        print(f"[Database] Logged daily Spotify metrics for {inserted_count} artists into MySQL.")

    def get_tracked_artists(self):
        """Retrieves distinct artists currently stored in the database for daily tracking."""
        self.cursor.execute("SELECT DISTINCT Artist_Name FROM Dim_Events")
        return [row[0] for row in self.cursor.fetchall()]

    def close(self):
        self.cursor.close()
        self.conn.close()