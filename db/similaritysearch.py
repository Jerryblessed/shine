from flask import Flask, render_template_string, request
import sqlite3
from peewee import Model, MySQLDatabase, TextField, SQL
from tidb_vector.peewee import VectorField
import google.generativeai as genai  # Hypothetical import for Gemini API client
import threading
import time


# Import the necessary modules and functions
from modules import (
    Log,  # A class for logging messages
    Blueprint,  # A class for creating Flask blueprints
    render_template,  # A function for rendering Jinja templates
)

# Create a blueprint for the search bar route
similaritySearchBlueprint = Blueprint(
    "similaritySearch", __name__
)  # Pass the name of the blueprint and the current module name as arguments



# Init Gemini client
genai.configure(api_key='AIzaSyDDEdN89laTbTO8JEHJULde5fPm-h1GRGY')
embedding_model = 'models/embedding-001'
embedding_dimensions = 768

# Init TiDB connection
db = MySQLDatabase(
    'test',
    user='GLhAdq53EXzFzXf.root',
    password='tbt7GsoxCY0cHvVs',
    host='gateway01.eu-central-1.prod.aws.tidbcloud.com',
    port=4000,
    ssl_verify_cert=True,
    ssl_verify_identity=True
)

# Define a model with a VectorField to store the embeddings
class DocModel(Model):
    text = TextField()
    embedding = VectorField(dimensions=embedding_dimensions)

    class Meta:
        database = db
        table_name = "gemini_embedding_test"

    def __str__(self):
        return self.text

def fetch_titles():
    """Fetch titles from the local SQLite database."""
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM posts")
    titles = cursor.fetchall()
    conn.close()
    return [title[0] for title in titles]

def update_tidb():
    """Update TiDB with titles from the posts table."""
    documents = fetch_titles()

    # Fetch existing titles from TiDB to avoid duplication
    existing_titles = set(doc.text for doc in DocModel.select(DocModel.text))

    # Filter out titles that are already in TiDB
    new_documents = [doc for doc in documents if doc not in existing_titles]

    if new_documents:
        # Insert only new documents and their embeddings into TiDB
        embeddings = genai.embed_content(model=embedding_model, content=new_documents, task_type="retrieval_document")
        data_source = [{"text": doc, "embedding": emb} for doc, emb in zip(new_documents, embeddings['embedding'])]
        DocModel.insert_many(data_source).execute()
        print(f"Inserted {len(new_documents)} new documents into TiDB.")
    else:
        print("No new documents to insert into TiDB.")

def background_updater():
    """Background thread function that updates TiDB every 10 seconds."""
    while True:
        update_tidb()
        time.sleep(10)  # Wait for 10 seconds before the next update


@similaritySearchBlueprint.route('/similaritySearch', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']

        question_embedding = genai.embed_content(model=embedding_model, content=[question], task_type="retrieval_query")['embedding'][0]
        related_docs = DocModel.select(
            DocModel.text, DocModel.embedding.cosine_distance(question_embedding).alias("distance")
        ).order_by(SQL("distance")).limit(3)

        related_docs_list = [(doc.distance, doc.text) for doc in related_docs]

        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Question Response</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f0f0f0;
                        color: #333;
                        margin: 0;
                        padding: 20px;
                    }
                    h1 {
                        color: #0056b3;
                    }
                    h2 {
                        margin-top: 40px;
                    }
                    ul {
                        list-style-type: none;
                        padding: 0;
                    }
                    li {
                        background-color: #fff;
                        border: 1px solid #ccc;
                        margin-bottom: 10px;
                        padding: 15px;
                        border-radius: 8px;
                        cursor: pointer;
                        transition: background-color 0.3s;
                    }
                    li:hover {
                        background-color: #e0e0e0;
                    }
                    .copied {
                        color: green;
                        font-weight: bold;
                        margin-left: 10px;
                    }
                    a {
                        display: block;
                        margin-top: 20px;
                        text-align: center;
                        padding: 10px;
                        background-color: #0056b3;
                        color: white;
                        text-decoration: none;
                        border-radius: 8px;
                    }
                    a:hover {
                        background-color: #004494;
                    }
                    .loader {
                        font-weight: bold;
                        font-family: sans-serif;
                        font-size: 30px;
                        animation: l1 1s linear infinite alternate;
                        text-align: center;
                        margin-top: 20px;
                    }
                    .loader:before {
                        content:"Please be patient...";
                    }
                    @keyframes l1 {
                        to { opacity: 0; }
                    }
                </style>
                <script>
                    function copyText(text) {
                        navigator.clipboard.writeText(text).then(() => {
                            document.getElementById('feedback').innerText = 'Text copied!';
                        });
                    }
                </script>
            </head>
            <body>
                <h1>Question: {{ question }}</h1>
                <h2> Related result:</h2>
                <ul>
                    {% for distance, text in related_docs_list %}
                    <li onclick="copyText('{{ text }}')">{{ text }}</li>
                    {% endfor %}
                </ul>
                <div id="feedback" class="copied"></div>
                <a href="/">Ask another question</a>
                <a href="/">Go back home</a>
            </body>
            </html>
        ''', question=question, related_docs_list=related_docs_list)

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ask a Question</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #0056b3;
                text-align: center;
            }
            form {
                max-width: 600px;
                margin: auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }
            label {
                display: block;
                margin-bottom: 10px;
                font-weight: bold;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 8px;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 10px;
                background-color: #0056b3;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #004494;
            }
            .placeholder {
                font-size: 16px;
                color: #888;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                white-space: nowrap;
                pointer-events: none;
                animation: typing 5s steps(40) 1s forwards;
            }
            @keyframes typing {
                from { width: 0; }
                to { width: 100%; }
            }
            .loader {
                font-weight: bold;
                font-family: sans-serif;
                font-size: 30px;
                animation: l1 1s linear infinite alternate;
                text-align: center;
                margin-top: 20px;
            }
            .loader:before {
                content:"Please be patient...";
            }
            @keyframes l1 {
                to { opacity: 0; }
            }
            .styled-div {
                max-width: 600px;
                margin: auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
        </style>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const inputField = document.getElementById('question');
                inputField.addEventListener('focus', function() {
                    const placeholderText = document.querySelector('.placeholder');
                    if (placeholderText) {
                        placeholderText.remove();
                    }
                });
            });
        </script>
    </head>
    <body>
        <h1>Ask a Question</h1>
        <form method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />

            <label for="question">Enter your question:</label>
            <input type="text" id="question" name="question" required>
            <button type="submit">Submit</button>
        </form>

        <div class="styled-div">
            <a href="https://www.google.com">
                <button type="button">Go back home</button>
            </a>
        </div>

    </body>
    </html>
''')
