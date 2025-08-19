# main.py

from core.secure_llm import SecureLLM

def main():
    model = SecureLLM()

    print("--- Secure LLM Prompt Interface ---")
    while True:
        try:
            user_input = input("\nPrompt utilisateur > ")
            if user_input.lower() in {"exit", "quit"}:
                print("Fin du programme.")
                break

            result = model.run(user_input)

            print("\n--- Résultat ---")
            print(f"Statut : {result['verdict']}")
            print(f"Sortie : {result['response']}")

        except KeyboardInterrupt:
            print("\nArrêt par l'utilisateur.")
            break

if __name__ == "__main__":
    main()
