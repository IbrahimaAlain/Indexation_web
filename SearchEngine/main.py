import os
import json
import sys

# Ajout du dossier src au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.search_engine import SearchEngine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
# Le fichier produits est à la racine, comme demandé
PRODUCTS_FILE = os.path.join(BASE_DIR, "rearranged_products.jsonl")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def save_results(data, filename="search_results.json"):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Résultats sauvegardés dans {path}")

def main():
    if not os.path.exists(PRODUCTS_FILE):
        print(f"ERREUR: Fichier produits introuvable : {PRODUCTS_FILE}")
        return

    print("Initialisation du moteur de recherche...")
    engine = SearchEngine(INPUT_DIR, PRODUCTS_FILE)

    while True:
        try:
            query = input("\nRecherche (q pour quitter) : ")
        except EOFError:
            break
            
        if query.lower() == 'q':
            break
        
        results = engine.search(query)
        
        count = results["metadata"].get("filtered_documents", 0)
        print(f"\n{count} résultats trouvés.\n")
        
        # Affichage des 3 premiers résultats
        for i, res in enumerate(results["results"][:3]):
            print(f"{i+1}. [{res['score']}] {res['title']}")
            print(f"   {res['url']}")
            
        save_results(results)

if __name__ == "__main__":
    main()