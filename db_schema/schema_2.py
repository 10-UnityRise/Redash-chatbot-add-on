# Schema
# Loading CSV files into PostgreSQL database using SQLAlchemy in python

# importing libraries
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import pandas as pd
from dotenv import load_dotenv

# 1. Database connection setup
# 1.1 Loading environment variables
username = os.getenv("DB_USERNAME")
passwrod = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

# 1.2 Construction of database connection string
database_url = f"postgresql+psycopg2://{username}:{passwrod}@{host}:{port}/{database}"

# 2. Engine and Base setup
# 2.1. Create an SQLAlchemy engine using the connection string
engine = engine_create(database_url, echo=True)  # set echo=True for debug logging

# 2.2. Define the SQLAlchemy declarative base
Base = declarative_base()  

# 3. Define the MergedData class representing the table in the database
class MergedData(Base):
    __tablename__ = 'merged_data_2'

    # Define columns based on your data structure
    id = Column(Integer, primary_key = True)
    date = Column(DateTime)
    cities = Column(String)
    city_name = Column(String)
    geography = Column(String)
    views = Column(Integer)
    watch_time_hours = Column(Float)
    average_view_duration = Column(String)

# 4. Create the table in the database
Base.metadata.create_all(engine)

# 5. Create a session to interact with the database
session = sessionmaker(bind=engine)

# 6. Data Loading
# 6.1. Specify the base folder
base_folder = 'data'
# 6.2. Get a list of all subfolders in the base folder
subfolders_2 = [f.path for f in os.scandir(base_folder) if f.is_dir()]
# 6.3. Iterate through each subfoler
for subfolder in subfolders_2:
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

# commit the change to the database
session.commit()

# Close the database session
session.close()


