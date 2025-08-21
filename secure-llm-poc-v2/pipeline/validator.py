# pipeline/validator.py
from __future__ import annotations
import base64
import re
from typing import Dict, List, Optional

# ⚠️ L'API qui ne casse pas : on hérite d'un Validator et on renvoie PassResult/FailResult
from guardrails.validator_base import (
    Validator,
    register_validator,
    ValidationResult,
    PassResult,
    FailResult,
)

# Patterns classiques de prompt injection (tu peux en ajouter)
INJECTION_PATTERNS: List[str] = [
    r"ignore\s+(all|previous|above)\s+(instructions|rules)",
    r"disregard\s+.*\s+safety",
    r"reveal\s+(system|hidden|internal)\s+(prompt|rules)",
    r"(show|print)\s+.*\s+(system\s+prompt|instructions)",
    r"(do\s*anything\s*now|DAN)",
    r"act\s+as\s+.*(jailbreak|no\s*rules)",
    r"(password|api[_-]?key|secret|token)",
]

def _maybe_b64_decode(text: str) -> str:
    """Essaie de décoder base64 si possible, sinon renvoie le texte original."""
    try:
        decoded = base64.b64decode(text).decode("utf-8", errors="strict")
        # filtra les contenus trop “brouillés” (bruit, caractères nuls)
        if any(c == "\x00" for c in decoded):
            return text
        return decoded
    except Exception:
        return text

@register_validator(name="no_prompt_injection", data_type="string")
class NoPromptInjection(Validator):
    """
    Valide qu'une entrée ne ressemble pas à une tentative de prompt injection.
    - Détection heuristique (regex)
    - Optionnel: vérification LLM de second avis (Mistral via OpenRouter) — à brancher plus tard
    """

    def __init__(
        self,
        threshold: float = 0.5,
        use_llm_check: bool = False,
    ):
        super().__init__()
        self.threshold = threshold
        self.use_llm_check = use_llm_check
        self._compiled = [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in INJECTION_PATTERNS]

    def validate(self, value: str, metadata: Optional[Dict] = None) -> ValidationResult:
        text = value or ""
        text_or_decoded = _maybe_b64_decode(text)

        reasons: List[str] = []
        for pat, rx in zip(INJECTION_PATTERNS, self._compiled):
            if rx.search(text_or_decoded):
                reasons.append(f"matched:{pat}")

        # Score simple : nb de hits / 3, borné à 1.0
        score = min(1.0, len(reasons) / 3.0)

        # Hook optionnel pour un “second avis” LLM (laisse OFF par défaut pour rester simple)
        # if self.use_llm_check:
        #     verdict = call_mistral_judge(text_or_decoded)  # à implémenter si tu veux
        #     if verdict == "malicious":
        #         score = max(score, 0.8)

        if score >= self.threshold:
            return FailResult(
                error_message="Prompt injection suspectée.",
                fix_value=None,
                metadata={"score": score, "signals": reasons},
            )

        return PassResult(metadata={"score": score, "signals": reasons})


# Petit helper pour l'utiliser sans spécifier Guardrails end-to-end
def validate_prompt_or_raise(prompt: str, threshold: float = 0.5) -> None:
    """Lève ValueError si le prompt est jugé malveillant."""
    v = NoPromptInjection(threshold=threshold)
    res = v.validate(prompt, metadata={})
    if isinstance(res, FailResult):
        raise ValueError(f"Validation échouée: {res.error_message} | {res.metadata}")
