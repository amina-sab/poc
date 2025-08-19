# pipeline/validator.py

from guardrails import Guard
import re

class PromptValidator:
    """
    Validator principal combinant une règle Guardrails (unusual_prompt)
    et une validation personnalisée par expressions régulières.
    """

    def __init__(self):
        self.block_patterns = [
            re.compile(r"(?i)(ignore|override|forget).*instruction"),
            re.compile(r"(?i)simulate.*evil"),
            re.compile(r"(?i)jailbreak"),
            re.compile(r"(?i)d[a@]n")
        ]

    def validate_input(self, prompt: str) -> bool:
        """
        Applique les règles heuristiques personnalisées au prompt utilisateur.
        Retourne True si le prompt est acceptable, False sinon.
        """
        for pattern in self.block_patterns:
            if pattern.search(prompt):
                return False
        return True

    def validate_output(self, response: str) -> bool:
        """
        (Optionnel) Valide la sortie du LLM si nécessaire.
        Peut être étendu pour filtrer les sorties toxiques ou interdites.
        """
        return True  # placeholder
