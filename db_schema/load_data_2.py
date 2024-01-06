from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import pandas as pd
from schema import Base, MergedData
from dotenv import load_dotenv

# 1. Database connection setup
# 1.1 Loading environment variables
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

# 1.2 Construction of database connection string
database_url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"

def create_database():
    #Create an SQLAlchemy engine using the connection string
    engine = engine_create(database_url, echo=True)  # set echo=True for debug logging

    # create the table in the database
    Base.metadata.create_all(engine)

    # create a session to interact with the database
    session = sessionmaker(bind = engine)

    return session()

def load_data(session, subfolder):
    try: 
        # construct the file path for each CSV within ghe subfolder
        merged_data_path = os.path.join(subfolder, 'chart_totals_table.csv')

        # Read the merged data from CSV
        chart_totals_table = pd.read_csv(chart_totals_table)    

        # Convert the DataFrame to a list of dictionaries
        data_to_insert = chart_totals_table.to_dict(orient = 'records')

        # Insert data into the database
        session.bulk_insert_mappings(MergedData, data_to_insert)

    except Exception as e:
        print(f"Error processing {subfolder}: {e}")


def main():
    # specify the base folder
    base_folder = 'data'

    # Get a list of all subfolders in the base folder
    subfolders_2 = [f.path for f in os.scandir(base_folder) if f.is_dir()]

    # Create a session and connect to the database
    session = create_database()

    # Iterate through each subfolder
    for subfolder in subfolders_2:
        load_data(session, subfolder)

    # Commit the changes to the database
    session.commit()

    # Close the database session
    session.close()

if __name__ == "__main__":
    main()





