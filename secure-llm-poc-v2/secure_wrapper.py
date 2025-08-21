import sys, json
from core.secure_llm import SecureLLM  # ton pipeline sécurisé

secure_llm = SecureLLM()

def main():
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
    prompt = data.get("prompt", "") or data.get("input", "")
    response = secure_llm.run(prompt)   # ou .ask(prompt) selon ton code
    print(json.dumps({"output": response}))

if __name__ == "__main__":
    main()
