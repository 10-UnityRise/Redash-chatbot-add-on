from sqlalchemy import create_engine
import os

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# Establish a connection to the PostgreSQL database
engine = create_engine(database_url)

class DatabaseHandler:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)

    def save_conversation(self, user_question, assistant_answer):
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    "INSERT INTO conversation_log (user_question, assistant_answer) VALUES (%s, %s)",
                    (user_question, assistant_answer)
                )
        except Exception as e:
            print(f"Error saving conversation to the database: {e}")
