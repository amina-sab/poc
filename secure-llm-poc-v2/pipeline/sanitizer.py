# pipeline/sanitizer.py
import re

def sanitize_text(text: str) -> str:
    if not text:
        return ""
    # Normalisations simples (tu peux compléter)
    t = text.replace("\r\n", "\n").strip()
    # supprime caractères non imprimables
    t = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\u00A0-\uFFFF]", "", t)
    return t
