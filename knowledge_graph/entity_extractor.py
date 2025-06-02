from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_entities(text):
    prompt = f"""
You are an information extractor. Given the input below, extract the main entities and their relationships.

Input text:
\"\"\"
{text}
\"\"\"

Return only a valid JSON object in the following structure:
{{
  "entities": ["Entity1", "Entity2", ...],
  "relationships": [["Entity1", "relation", "Entity2"], ...]
}}

Only return the JSON — do not include any explanation or additional text.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content
