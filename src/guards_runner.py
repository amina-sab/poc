# src/guards_runner.py
from typing import List, Dict, Optional
import logging
from guardrails import Guard

log = logging.getLogger("guardrails-ai")
logging.basicConfig(level=logging.INFO)

def _extract_text(result) -> str:
    for attr in ("validated_output", "raw_llm_output", "output"):
        val = getattr(result, attr, None)
        if isinstance(val, str) and val.strip():
            return val
    if isinstance(result, str):
        return result
    return str(result) if result is not None else ""

def _try_use(guard: Guard, validator_id: str, **kwargs) -> bool:
    """Essaye de charger un validateur Hub; renvoie False s'il n'est pas trouvé."""
    try:
        guard.use(validator_id, **kwargs)
        log.info(f"Validator loaded: {validator_id}")
        return True
    except Exception as e:
        log.warning(f"Validator '{validator_id}' not available: {e}. Continuing without it.")
        return False

class GuardRunner:
    """Pré- et post-validation Guardrails via IDs Hub, mais résiliente si non installés."""

    def __init__(
        self,
        use_unusual: bool = True,
        use_detect_injection: bool = False,
        pinecone_index: Optional[str] = None,
    ):
        # Pré-validation (entrée)
        self.guard_in = Guard()
        self.in_has_unusual = False
        if use_unusual:
            self.in_has_unusual = _try_use(
                self.guard_in,
                "hub://guardrails/unusual_prompt",
                on="prompt",
                on_fail="exception",
            )

        self.in_has_dpi = False
        if use_detect_injection and pinecone_index:
            self.in_has_dpi = _try_use(
                self.guard_in,
                "hub://guardrails/detect_prompt_injection",
                on="prompt",
                on_fail="exception",
                pinecone_index=pinecone_index,
            )

        # Post-validation (sortie)
        self.guard_out = Guard()
        self.out_has_unusual = False
        if use_unusual:
            self.out_has_unusual = _try_use(
                self.guard_out,
                "hub://guardrails/unusual_prompt",
                on="output",
                on_fail="exception",
            )

    def call_with_entry_guards(
        self,
        llm_api,  # Callable[..., str]
        *,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        **kwargs
    ) -> str:
        """Appelle le LLM via Guard (pré-validateurs) et renvoie un texte."""
        # Si aucun validateur d'entrée n'est dispo, appelle direct
        if not (self.in_has_unusual or self.in_has_dpi):
            return llm_api(messages=messages, prompt=prompt, **kwargs)
        try:
            res = self.guard_in(llm_api, prompt=prompt, messages=messages, **kwargs)
            return _extract_text(res)
        except Exception:
            return ("Je ne peux pas traiter cette requête car elle ressemble à une tentative "
                    "de manipulation (prompt injection). Reformule de manière légitime.")

    def validate_output(self, text: str) -> str:
        """Applique les validateurs de sortie (post-guards) et renvoie un texte."""
        if not self.out_has_unusual:
            return text
        try:
            res = self.guard_out.parse(llm_output=text)
            return _extract_text(res) or text
        except Exception:
            return ("Je ne peux pas fournir ces détails. Reformule ta question de manière légitime.")
