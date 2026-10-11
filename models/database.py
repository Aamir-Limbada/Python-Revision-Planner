
import sqlite3
from pathlib import Path


class Database:
    def __init__(self, database_name="byteback.db"):
        project_folder = Path(__file__).resolve().parent.parent
        self.database_path = project_folder / database_name

        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.database_path)

    def create_tables(self):
        with self.connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    category TEXT NOT NULL,
                    confidence INTEGER NOT NULL
                        CHECK(confidence BETWEEN 1 AND 5),
                    created TEXT NOT NULL
                )
            """)
    
    def add_topic(self, topic):
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO topics (name, category, confidence, created)
                VALUES (?, ?, ?, ?)
                """,
                (
                    topic.name,
                    topic.category,
                    topic.confidence,
                    topic.created.isoformat(),
                ),
            )

    def get_topics(self):
        from datetime import datetime
        from .topic import Topic

        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT name, category, confidence, created
                FROM topics
                ORDER BY id
                """
            ).fetchall()

        topics = []

        for name, category, confidence, created in rows:
            topic = Topic(name, category, confidence)
            topic.created = datetime.fromisoformat(created)
            topics.append(topic)

        return topics

    def delete_topic(self, topic_name):
        with self.connect() as connection:
            connection.execute(
                "DELETE FROM topics WHERE name = ?",
                (topic_name,),
            )
