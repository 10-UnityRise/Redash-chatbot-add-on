from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(10), nullable=False)
    text = db.Column(db.String(255), nullable=False)

@app.route('/save_chat', methods=['POST'])
def save_chat():
    try:
        data = request.get_json()

        if 'sender' not in data or 'text' not in data:
            return jsonify({'error': 'Invalid data format'}), 400

        sender = data['sender']
        text = data['text']

        # Save chat message to the database
        chat_message = ChatHistory(sender=sender, text=text)
        db.session.add(chat_message)
        db.session.commit()

        return jsonify({'message': 'Chat saved successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
