from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import os
import pandas as pd
from schema import Base, MergedData
from dotenv import load_dotenv
import sys
import psycopg2

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

# Add error checking or default values
if None in (username, password, host, port, database):
    print("Error: Some environment variables are missing.")
    sys.exit(1)


database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"


def create_database():
    # Create an SQLAlchemy engine
    engine = create_engine(database_url, echo=True)  # Set echo=True for debug logging

    # Create the table in the database
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    return Session()

def load_data(session, subfolder):
    try:
        # Read the merged data from CSV
        merged_data = pd.read_csv(merged_data_path)

        # Convert the DataFrame to a list of dictionaries
        data_to_insert = merged_data.to_dict(orient='records')

        # Insert data into the database
        session.bulk_insert_mappings(MergedData, data_to_insert)

    except Exception as e:
        print(f"Error processing {subfolder}: {str(e)}")

def main():
    # Specify the base folder
    base_folder = '../data'

    # Get a list of all subfolders in the base folder
    subfolders = [f.path for f in os.scandir(base_folder) if f.is_dir()]

    # Create a session and connect to the database
    session = create_database()

    # Iterate through each subfolder
    for subfolder in subfolders:
        load_data(session, subfolder)

    # Commit the changes to the database
    session.commit()

    # Close the database session
    session.close()

if __name__ == "__main__":
    main()
