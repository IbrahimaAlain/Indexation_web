import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.indexer import Indexer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "input", "products.jsonl")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def load_data(filepath):
    """Charge les données depuis un fichier JSON standard ou JSONL (JSON Lines)."""
    if not os.path.exists(filepath):
        print(f"Fichier introuvable : {filepath}")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            f.seek(0)
            return [json.loads(line) for line in f if line.strip()]

def save_json(data, filename):
    """Sauvegarde les données fournies dans un fichier JSON formaté."""
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    """Orchestre le chargement, l'indexation et la génération des 5 fichiers de sortie."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Lecture de : {INPUT_FILE}")
    data = load_data(INPUT_FILE)
    if not data: return

    indexer = Indexer()
    print(f"Indexation de {len(data)} documents...")
    
    for doc in data:
        indexer.index_document(doc)

    print("Génération des fichiers d'index...")

    save_json(indexer.pos_title_index, "title_index.json")
    save_json(indexer.pos_desc_index, "description_index.json")
    save_json(indexer.reviews_index, "review_index.json")
    
    save_json(indexer.features_indexes.get("brand", {}), "brand_index.json")
    save_json(indexer.features_indexes.get("made in", {}), "origin_index.json")

    print(f"Terminé. Fichiers disponibles dans {OUTPUT_DIR}")

if __name__ == "__main__":
    main()