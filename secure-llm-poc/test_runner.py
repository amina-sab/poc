# test_runner.py

from core.secure_llm import SecureLLM
import os
import time

TEST_FILE = "prompts/test_prompts.txt"

def run_tests():
    model = SecureLLM()
    if not os.path.exists(TEST_FILE):
        raise FileNotFoundError(f"Fichier de test introuvable : {TEST_FILE}")
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        prompts = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print("--- Test des prompts adverses ---\n")
    for i, prompt in enumerate(prompts, 1):
        print(f"Test {i}: {prompt}")
        result = model.run(prompt)

        print(f"  → Verdict  : {result['verdict']}")
        if result["response"]:
            response = result["response"]
        else:
            response = "(Pas de réponse : prompt rejeté ou erreur LLM)"
        print(f"  → Réponse : {response[:200]}{'...' if len(response) > 200 else ''}\n")

        time.sleep(1.5)  # éviter de spammer l'API

if __name__ == "__main__":
    run_tests()
