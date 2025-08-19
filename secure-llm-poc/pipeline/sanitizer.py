import re
import base64
import ftfy
from typing import Tuple


class PromptSanitizer:
    """
    Classe responsable du nettoyage et de la normalisation de l'entrée utilisateur.
    Respecte le principe de responsabilité unique (SRP) du SOLID.
    """

    def __init__(self):
        self.patterns = [
            re.compile(r"(?i)ignore\s+all\s+previous\s+instructions"),
            re.compile(r"(?i)you\s+are\s+now\s+DAN"),
            re.compile(r"(?i)simulate\s+an\s+evil\s+mode"),
        ]

    def normalize_text(self, text: str) -> str:
        """Nettoyage Unicode et homoglyphes"""
        return ftfy.fix_text(text)

    def detect_base64(self, text: str) -> bool:
        """Détecte une injection codée en base64"""
        try:
            decoded = base64.b64decode(text.encode(), validate=True)
            return decoded.decode("utf-8").isascii()
        except Exception:
            return False

    def contains_suspicious_patterns(self, text: str) -> bool:
        return any(p.search(text) for p in self.patterns)

    def sanitize(self, raw_input: str) -> Tuple[str, dict]:
        """
        Nettoie l'entrée utilisateur et retourne :
        - le texte nettoyé
        - un dictionnaire de métriques d'analyse
        """
        cleaned = self.normalize_text(raw_input)
        metrics = {
            "base64_encoded": self.detect_base64(cleaned),
            "suspicious_patterns": self.contains_suspicious_patterns(cleaned),
        }
        return cleaned, metrics
