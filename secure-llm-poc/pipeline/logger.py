# pipeline/logger.py

import json
import os
from datetime import datetime

class PromptLogger:
    """
    Enregistre les interactions avec le LLM de façon structurée dans un fichier JSON.
    Chaque entrée contient le prompt, la réponse, les verdicts et les métriques d'analyse.
    """

    def __init__(self, log_dir: str = "logs", filename: str = "interaction_log.json"):
        os.makedirs(log_dir, exist_ok=True)
        self.path = os.path.join(log_dir, filename)

    def log(self, data: dict):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **data
        }
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
