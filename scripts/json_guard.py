import os, json
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

class Product(BaseModel):
    name: str
    price: float = Field(ge=0)
    currency: str

def ask_json(llm: ChatOpenAI, prompt: str, tries: int = 2) -> Optional[Product]:
    system = SystemMessage(content="Respond STRICTLY in JSON matching {name:str, price:float, currency:str}. No prose.")
    user = HumanMessage(content=prompt)
    for _ in range(tries):
        txt = llm.invoke([system, user]).content.strip()
        try:
            data = json.loads(txt)
            return Product(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            user = HumanMessage(content=f"Reformulate as STRICT JSON only. Error: {e}")
    return None

if __name__ == "__main__":
    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME", "mistralai/mistral-7b-instruct:free"),
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
        temperature=0,
    )
    prod = ask_json(llm, "Extract a product: 'Office chair, 129.9 EUR'.")
    print("JSON RESULT >>>", prod)
