from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Initialize OpenAI client with key from env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_entities(text):
    prompt = f"""
Pull out the main entities and how they relate from this text:

{text}

Return it in JSON:
{{
  "entities": ["Andre Achtar-Zadeh", "OpenAI"],
  "relationships": [["Andre Achtar-Zadeh", "works_at", "OpenAI"]]
}}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content
