# Secure LLM PoC (Prompt Injection Defense)

## 🌍 Objectif

Ce projet de preuve de concept vise à protéger un modèle de langage open source (Mistral 7B via OpenRouter) contre les attaques par injection de prompt, en s’appuyant uniquement sur des outils open source. Il démontre la faisabilité d’une passerelle de sécurité modulaire intercalée entre l'utilisateur et le LLM.

## ⚖️ Stack technique

* **Modèle** : Mistral 7B (via OpenRouter API)
* **Langage** : Python 3.10+
* **Orchestration** : LangChain
* **Validation** : Guardrails AI + validateur custom
* **Sanitization** : `ftfy`, `regex`, `base64`
* **Journalisation** : `logging`, JSON
* **Tests d'attaque** : `promptfoo`

## 📊 Architecture du pipeline

```
[Entrée utilisateur]
   ↓
[Sanitization] ➔ [Prompt Shielding] ➔ [Validation Entrée] ➔ [Appel LLM via OpenRouter]
   ↓                                                                        ↓
[Journalisation] ← [Validation Sortie optionnelle]
```

## 🔄 Modules fonctionnels

* `BaseLLM` : classe centrale encapsulant l’ensemble du pipeline
* `sanitizer.py` : nettoyage lexical & Unicode
* `prompt_builder.py` : prompt structuré avec rôles via LangChain
* `validator.py` : Guardrails + validator Python custom
* `logger.py` : traçabilité JSON
* `test_prompts.txt` : corpus d’attaques à simuler

## 📂 Arborescence du projet

```bash
secure-llm-poc/
├── main.py
├── core/
│   ├─ base_llm.py
├── pipeline/
│   ├─ sanitizer.py
│   ├─ prompt_builder.py
│   ├─ validator.py
│   └─ logger.py
├── prompts/
│   └─ test_prompts.txt
├── config/
│   └─ guardrails.yaml
├── logs/
│   └─ interaction_log.json
```

## ✅ Fonctionnalités principales

* Prévention de prompt injection directe & obfusquée
* Validation dynamique de l’entrée et de la sortie
* Logging sécurisé pour analyse post-hoc
* Red teaming via prompts adverses

## 🌐 Tests et évaluation

* Simulation d’attaques (DAN, Base64, fragmentation)
* Métriques : ASR, taux de détection, faux positifs
* Export JSON des résultats

## 💼 Installation rapide

```bash
pip install -r requirements.txt
```

## 📖 Licence

Projet open source réalisé dans un cadre académique. Libre de modification pour usage personnel ou institutionnel.
