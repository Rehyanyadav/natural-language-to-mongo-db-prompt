import os
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# MongoDB setup
MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.get_database(os.environ.get("MONGODB_DB", "nl_db"))

# collection name
COLL_NAME = os.environ.get("MONGODB_COLL", "people")

# placeholder for LLM conversion; integrate MCP or OpenAI
from mcp import convert_to_mongo_query

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    nl = request.form.get("natural_language")
    if not nl:
        flash("Please enter a query.")
        return redirect(url_for("index"))
    try:
        # convert to Mongo query using LLM
        mongo_query = convert_to_mongo_query(nl)
        results = list(db[COLL_NAME].find(mongo_query))
        return render_template("results.html", query=nl, mongo_query=mongo_query, results=results)
    except Exception as e:
        flash(f"Error processing query: {e}")
        return redirect(url_for("index"))

@app.route("/load_sample")
def load_sample():
    # populate sample data
    sample_data = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "San Francisco"},
        {"name": "Charlie", "age": 35, "city": "Boston"},
    ]
    coll = db[COLL_NAME]
    coll.delete_many({})
    coll.insert_many(sample_data)
    flash("Sample data loaded into MongoDB.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
