from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import pandas as pd
from dotenv import load_dotenv
import sys  # Don't forget to import sys for sys.exit(1)

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")


database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# Create SQLAlchemy engine
engine = create_engine(database_url)

# Base directory
basepath = '../data'

# List all subdirectories using os.listdir
for entry in os.listdir(basepath):
    if os.path.isdir(os.path.join(basepath, entry)):
        # Read the CSV file in the subdirectory
        df = pd.read_csv(os.path.join(basepath, entry, 'merged_data.csv'))

        # Write the DataFrame to a PostgreSQL table named after the subdirectory
        df.to_sql(entry, engine, if_exists='replace', index=False)