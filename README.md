# Natural Language Database Interface

This project demonstrates an experiment where users can query a MongoDB database using plain English. An LLM (via OpenAI's API) translates the natural language into a MongoDB `find` query. The Flask backend executes the translated query and returns results.

## Features

- Load sample data into MongoDB.
- Enter natural language questions in the web UI.
- See the translated MongoDB query and returned documents.
- Uses MCP-style integration via `mcp.py` as a simple wrapper around the LLM call.

## Requirements

- Python 3.10+
- MongoDB instance (local or cloud)
- OpenAI API key

## Setup

1. **Clone workspace** (already set up here).
2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment**:
   - Copy `.env` and set `OPENAI_API_KEY`.
   - Adjust `MONGODB_URI` if using remote database.

5. **Load sample data**:
   ```bash
   FLASK_APP=app.py flask run
   # then visit http://localhost:5000 and click "Load sample data"
   ```

## Usage

- Navigate to the home page, type a question (e.g. "Find people older than 30").
- Submit and see results.

## MCP Integration

`mcp.py` contains a simple function demonstrating how an LLM can be prompted to produce a MongoDB query object. This mimics the conversion step in an MCP pipeline.

## Notes

- This is a minimal example; production use would require input sanitization, more robust prompt engineering, and error handling.
- You can expand to support SQL by adjusting the prompt and database client.

## License

MIT
