from redash.handlers.base import BaseResource
from tenacity import retry, wait_random_exponential, stop_after_attempt
import re
import requests
from chatbot.openai_utils import GPT_MODEL, chat_completion_request  # Update import
from chatbot.database_utils import get_database_info, create_database_engine  # Add imports

class ChatResource(BaseResource):
    engine = create_database_engine()
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

    # ... (rest of the class code)
