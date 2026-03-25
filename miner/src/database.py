import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="/app/data/storage.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS word_counts (
                    word TEXT PRIMARY KEY,
                    count INTEGER DEFAULT 0
                )
            """)

    def save_words(self, words):
        """Guarda una lista de palabras de forma atómica."""
        if not words:
            return
            
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for word in words:
                cursor.execute("""
                    INSERT INTO word_counts (word, count) 
                    VALUES (?, 1)
                    ON CONFLICT(word) DO UPDATE SET count = count + 1
                """, (word,))
            conn.commit()