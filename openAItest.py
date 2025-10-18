import os
from openai import OpenAI

# Try to load .env automatically if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv is optional; environment variables may already be set
    pass

API_KEY = os.getenv("PITCH_PANDA_API_KEY")
if not API_KEY:
    raise RuntimeError("PITCH_PANDA_API_KEY is not set. Copy .env.example to .env and add your key, or set the environment variable.")

client = OpenAI(api_key=API_KEY)

response = client.responses.create(
    model="gpt-5",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)