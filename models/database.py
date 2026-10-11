
import sqlite3
from pathlib import Path


class Database:
    def __init__(self, database_name="byteback.db"):
        project_folder = Path(__file__).resolve().parent.parent
        self.database_path = project_folder / database_name

        self.create_tables()
        self.create_session_table()

    
    def connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

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
            cursor = connection.execute(
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

            topic.id = cursor.lastrowid


    def get_topics(self):
        from datetime import datetime
        from .topic import Topic

        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT id, name, category, confidence, created
                FROM topics
                ORDER BY id
                """
            ).fetchall()

        
        topics = []

        for topic_id, name, category, confidence, created in rows:
            topic = Topic(
                name,
                category,
                confidence,
                topic_id=topic_id,
            )
            topic.created = datetime.fromisoformat(created)
            topics.append(topic)

        return topics


    def delete_topic(self, topic_name):
        with self.connect() as connection:
            connection.execute(
                "DELETE FROM topics WHERE name = ?",
                (topic_name,),
            )

    
    def create_session_table(self):
        with self.connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    attempted INTEGER NOT NULL CHECK(attempted > 0),
                    correct INTEGER NOT NULL CHECK(
                        correct >= 0 AND correct <= attempted
                    ),
                    confidence INTEGER NOT NULL CHECK(
                        confidence BETWEEN 1 AND 5
                    ),
                    FOREIGN KEY (topic_id)
                        REFERENCES topics(id)
                        ON DELETE CASCADE
                )
            """)

