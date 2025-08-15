import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
model = os.getenv("MODEL_NAME", "mistralai/mistral-7b-instruct:free")

resp = client.chat.completions.create(
    model=model,
    messages=[{"role":"user","content":"Say hello in one short sentence."}],
)
print(json.dumps(resp.model_dump(), ensure_ascii=False, indent=2))
print("\nCONTENT >>>", resp.choices[0].message.content)
