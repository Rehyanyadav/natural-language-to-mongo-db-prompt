import os
import openai

# Configure OpenAI key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Example of using a prompt to translate natural language into a MongoDB query
PROMPT_TEMPLATE = (
    "You are a helpful assistant that converts plain English into a MongoDB "
    "find() query object. \n"
    "Return only the JSON object representing the query, without the "
    "find() wrapper. For example, if the query is 'find all people older than 30', "
    "you would output `{\"age\": {\"$gt\": 30}}`. "
)


def convert_to_mongo_query(natural_language: str) -> dict:
    """Call the LLM to convert a natural language description into a MongoDB query."""
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable must be set")

    prompt = PROMPT_TEMPLATE + f"\n\nUser query: {natural_language}\n\nMongo query:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0,
        top_p=1,
        n=1,
        stop=["\n"],
    )
    text = response.choices[0].text.strip()
    # attempt to parse JSON from the response
    import json

    try:
        query_obj = json.loads(text)
    except Exception:
        # if parsing fails, return an empty query or raise
        raise ValueError(f"Failed to parse LLM output as JSON: {text}")

    return query_obj
