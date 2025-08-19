# core/secure_llm.py

from dotenv import load_dotenv
import os
from langchain_community.chat_models import ChatOpenAI
from pipeline.sanitizer import PromptSanitizer
from pipeline.prompt_builder import PromptBuilder
from pipeline.validator import PromptValidator
from pipeline.logger import PromptLogger

class SecureLLM:
    """
    Classe centrale qui encapsule tout le pipeline de sécurité autour du LLM :
    - Nettoyage du prompt (sanitization)
    - Structuration (shielding)
    - Validation d’entrée
    - Appel du LLM (OpenRouter)
    - Validation de sortie (optionnelle)
    - Logging
    """

    def __init__(self):
        # Chargement des variables d'environnement
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY")
        base_url = os.getenv("OPENROUTER_BASE_URL")
        model_name = os.getenv("MODEL_NAME")

        if not api_key:
            raise EnvironmentError("La variable OPENROUTER_API_KEY est manquante.")

        # Initialisation du LLM (via OpenRouter)
        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            base_url=base_url,
            model_name=model_name
        )

        # Injection des composants SOLID
        self.sanitizer = PromptSanitizer()
        self.builder = PromptBuilder()
        self.validator = PromptValidator()
        self.logger = PromptLogger()

    def run(self, user_input: str) -> dict:
        """
        Exécute tout le pipeline de traitement sécurisé sur le prompt utilisateur.
        Retourne un dictionnaire avec toutes les étapes.
        """
        result = {
            "input": user_input,
            "sanitized": None,
            "metrics": None,
            "prompt": None,
            "response": None,
            "verdict": None
        }

        # 1. Nettoyage
        cleaned, metrics = self.sanitizer.sanitize(user_input)
        result["sanitized"] = cleaned
        result["metrics"] = metrics

        # 2. Structuration du prompt
        prompt = self.builder.build(cleaned)
        result["prompt"] = [msg.dict() for msg in prompt]  # Convert to JSON-serializable

        # 3. Validation de l'entrée
        if not self.validator.validate_input(cleaned):
            result["verdict"] = "rejected_input"
            self.logger.log(result)
            return result

        # 4. Appel au LLM
        try:
            output = self.llm.invoke(prompt)
            result["response"] = output.content
        except Exception as e:
            result["verdict"] = f"error: {str(e)}"
            self.logger.log(result)
            return result

        # 5. Validation de sortie (optionnelle)
        if not self.validator.validate_output(output.content):
            result["verdict"] = "rejected_output"
        else:
            result["verdict"] = "accepted"

        # 6. Logging final
        self.logger.log(result)
        return result
