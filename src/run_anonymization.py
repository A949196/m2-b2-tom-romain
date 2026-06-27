"""Script de test : exécute anonymize_comments sur les 10 premières lignes.
 
Usage :
    python src/run_anonymize_test.py
 
Place ce script à la racine du repo (au même niveau que src/ et data/),
ou ajuste les imports/chemins selon ton arborescence.
"""
from pathlib import Path
 
import pandas as pd
 
from anonymize import anonymize_comments
 
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
SAMPLE_PATH = DATA_DIR / "audit_sample.csv"
 
df = pd.read_csv(SAMPLE_PATH)
sample_10 = df["manager_comments"].head(10)

for i, text in enumerate(sample_10, 1):
    after = anonymize_comments(text)
    print(f"--- Exemple {i} ---")
    print(f"AVANT : {text}")
    print(f"APRÈS : {after}")
    print()
