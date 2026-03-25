import sqlite3
import pandas as pd
import os

class DataLoader:
    def __init__(self, db_path="/app/data/storage.db"):
        self.db_path = db_path

    def _get_connection(self):
        if not os.path.exists(self.db_path):
            return None
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def get_top_words(self, limit=10):
        conn = self._get_connection()
        if conn is None:
            return pd.DataFrame(columns=['word', 'count'])
        
        query = "SELECT word, count FROM word_counts ORDER BY count DESC LIMIT ?"
        try:
            df = pd.read_sql_query(query, conn, params=(limit,))
            return df
        except Exception:
            return pd.DataFrame(columns=['word', 'count'])
        finally:
            conn.close()

    def get_stats(self):
        conn = self._get_connection()
        if conn is None:
            return 0, 0
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), SUM(count) FROM word_counts")
            unique, total = cursor.fetchone()
            return unique or 0, total or 0
        except Exception:
            return 0, 0
        finally:
            if conn:
                conn.close()