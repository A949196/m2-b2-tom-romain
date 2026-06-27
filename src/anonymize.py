"""M2-B2 — Fonction d'anonymisation à compléter (phase async individuelle).

Stratégie choisie : Hash : empreinte irréversible
"""
from __future__ import annotations

import re
import os
from hashlib import sha256
import spacy
NLP = spacy.load("en_core_web_md")  # ou "fr_core_news_md" selon ton dataset

# Regex de complément (spaCy ne couvre pas tout — email, IBAN partiel, téléphone US)
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
PHONE_RE = re.compile(r"\b\d{3}[.-]?\d{3}[.-]?\d{4}\b")
IBAN_PARTIAL_RE = re.compile(r"\*{2,}\d{4}")

# Sel récupéré depuis l'environnement — jamais en dur dans le code committé.
# Valeur de secours fournie uniquement pour les tests locaux.
HASH_SALT: str = os.environ.get("ANONYMIZE_SALT", "atos_m2_b2_dev_salt_tom")
 

def _hash(value: str) -> str:
    """Calcule un hash court (8 hex chars) salé d'une valeur de PII.
 
    Args:
        value: la valeur brute de l'entité à hasher (ex. un nom).
 
    Returns:
        Une empreinte hexadécimale tronquée à 8 caractères.
    """
    return sha256((HASH_SALT + value).encode()).hexdigest()[:8]

def anonymize_comments(text: str) -> str:
    """Anonymise un commentaire manager.
 
    Args:
        text: Texte libre potentiellement contenant des PII.
 
    Returns:
        Texte anonymisé selon la stratégie choisie. Retourne une chaîne
        vide si l'entrée n'est pas une chaîne (valeur manquante / NaN).
    """
    if not isinstance(text, str):
        return ""
 
    # 1 — Détection des entités avec spaCy (PERSON) → stratégie HASH
    doc = NLP(text)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
 
    # On remplace après avoir collecté tous les noms, pour ne pas décaler
    # les positions des entités suivantes pendant l'itération sur doc.ents.
    for name in persons:
        text = text.replace(name, f"[PERSON_{_hash(name)}]")
 
    # 2 — Complément regex (spaCy ne détecte ni email ni IBAN partiel ni tel)
    # → stratégie SUPPRESSION
    text = EMAIL_RE.sub("[EMAIL]", text)
    text = PHONE_RE.sub("[PHONE]", text)
    text = IBAN_PARTIAL_RE.sub("[IBAN]", text)
 
    return text


if __name__ == "__main__":
    # Test rapide
    sample = (
        "Allison Hill is a strong promotion candidate this year. "
        "Discussed with HR (Rhonda Smith, 651.216.1559). "
        "Budget pre-approved on account ****3503."
    )
    print("Avant :", sample)
    print("Après :", anonymize_comments(sample))