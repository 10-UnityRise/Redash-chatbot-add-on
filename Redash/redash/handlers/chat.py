from flask import Flask, request, jsonify
from redash.handlers.base import BaseResource
from sqlalchemy import create_engine, inspect
from tenacity import retry, wait_random_exponential, stop_after_attempt
import os
import openai
import re
import requests
import json

app = Flask(__name__)

VARIABLE_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = VARIABLE_KEY

GPT_MODEL = "gpt-3.5-turbo-0613"

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# Establish a connection to the PostgreSQL database
engine = create_engine(database_url)

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
    columns = inspector.get_columns(table_name)
    
    if columns:
        for column in columns:
            column_names.append(f'"{column["name"]}"')  # Add double quotes around column name
    
    return column_names

def get_database_info(engine):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        columns_names = get_column_names(engine, table_name)
        table_dicts.append({"table_name": f'"{table_name}"', "column_names": columns_names})  # Add double quotes around table name
    return table_dicts

def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response.json()
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

class ChatResource(BaseResource):
    database_schema_dict = get_database_info(engine)
    database_schema_string = "\n".join(
        [
            f'Table: "{table["table_name"]}"\nColumns: {", ".join([f"{col}" for col in table["column_names"]])}'
            for table in database_schema_dict
        ]
    )

    @staticmethod
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + openai.api_key,
        }
        json_data = {"model": model, "messages": messages}
        if tools is not None:
            json_data.update({"tools": tools})
        if tool_choice is not None:
            json_data.update({"tool_choice": tool_choice})
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=json_data,
            )
            return response.json()
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def post(self):
        try:
            value = request.get_json()
            question = value.get('question')
            
            # Define the 'tools' variable here or pass it as a parameter based on your needs
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "ask_database",
                        "description": "Use this function to answer user questions about youtube. Input should be a fully formed SQL query.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": f"""
                                            SQL query extracting info to answer the user's question.
                                            SQL should be written using this database schema:
                                            {self.database_schema_string}
                                            The query should be returned in plain text, not in JSON.
                                            """,
                                }
                            },
                            "required": ["query"],
                        },
                    }
                }
            ]

            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
            # Inside the post method
            response = self.chat_completion_request(messages, tools)

            # Check if 'choices' is present in the response and has content
            if 'choices' in response and response['choices']:
                assistant_message = response['choices'][0].get('message', {}).get('content')
                if assistant_message is not None:
                    assistant_message = assistant_message.strip()
            else:
                assistant_message = ""

            if "ask_database" in assistant_message:
                query_match = re.search(r'ask_database\((.*?)\)', assistant_message)
                if query_match:
                    query = query_match.group(1)
                    results = self.ask_database(engine, query)
                    response_data = {"answer": results, "query": query}
                else:
                    response_data = {"answer": "Invalid 'ask_database' format in the assistant's message"}
            else:
                response_data = {"answer": assistant_message}

            return jsonify(response_data), 200
        except Exception as error:
            print(error)
            return jsonify({"error": str(error)}), 500

    def ask_database(self, engine, query):
        """Function to query PostgreSQL database with a provided SQL query."""
        try:
            with engine.connect() as conn:
                result = conn.execute(query)
                results = [dict(row) for row in result]
        except Exception as e:
            results = f"Query failed with error: {e}"
        return results

if __name__ == "__main__":
    app.run(debug=True)