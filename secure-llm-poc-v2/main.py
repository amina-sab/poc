# main.py
from __future__ import annotations
import sys
from core.secure_llm import SecureLLM
from rich import print

def main():
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        print("[bold cyan]Secure LLM v2[/] — tape ton prompt (Ctrl+C pour quitter) :")
        user_input = input("> ")

    engine = SecureLLM()
    try:
        result = engine.ask(user_input)
        print("\n[bold green]Réponse:[/]\n", result["output"])
    except Exception as e:
        print(f"[bold red]Bloqué par le validateur[/]: {e}")

if __name__ == "__main__":
    main()
