# pipeline/prompt_builder.py

from langchain.schema import SystemMessage, HumanMessage

class PromptBuilder:
    """
    Classe responsable de la construction d'un prompt structuré (system + user) pour le LLM.
    Cette structuration renforce la clarté des rôles et peut aider à limiter l'impact des attaques contextuelles.
    """

    def __init__(self):
        self.system_instruction = (
            "Tu es un assistant IA utile, honnête et inoffensif."
            " Réponds de manière factuelle et polie. Ne sors jamais de ton rôle."
        )

    def build(self, user_input: str) -> list:
        """
        Construit un prompt sous forme de liste de messages (format attendu par les modèles de chat).
        """
        return [
            SystemMessage(content=self.system_instruction),
            HumanMessage(content=user_input)
        ]
