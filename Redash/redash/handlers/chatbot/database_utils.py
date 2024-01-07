from sqlalchemy import create_engine, inspect
import os

def create_database_engine():
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_DATABASE")

    database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    # Establish a connection to the PostgreSQL database
    engine = create_engine(database_url)
    return engine

def get_table_names(engine):
    """Return a list of table names."""
    table_names = []
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        table_names.append(f'"{table_name}"')  # Add double quotes around table name
    return table_names

def get_column_names(engine, table_name):
    """Return a list of column names."""
    column_names = []
    inspector = inspect(engine)

    try:
        columns = inspector.get_columns(table_name)

        if columns is not None:  # Check if columns is not None
            for column in columns:
                column_names.append(f'"{column["name"]}"')  # Add double quotes around column name
        else:
            print(f"No columns found for table: {table_name}")

    except Exception as e:
        print(f"Error fetching columns for table {table_name}: {e}")

    return column_names

def get_database_info(engine):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        columns_names = get_column_names(engine, table_name)
        table_dicts.append({"table_name": f'"{table_name}"', "column_names": columns_names})  # Add double quotes around table name
    return table_dicts
