import json
import os
from .text_processor import normalize_query, load_synonyms
from .ranker import Ranker

class SearchEngine:
    def __init__(self, input_dir, products_file):
        self.input_dir = input_dir
        self.products_file = products_file
        self.synonyms = {}
        self.indexes = {}
        self.documents_map = {}
        self.ranker = None
        self._load_data()

    def _load_data(self):
        # [cite_start]Chargement des synonymes (origin_synonyms.json) [cite: 11]
        syn_path = os.path.join(self.input_dir, "origin_synonyms.json")
        self.synonyms = load_synonyms(syn_path)

        # [cite_start]Chargement des index [cite: 6]
        index_files = [
            "title_index.json", "description_index.json", 
            "review_index.json", "brand_index.json", "origin_index.json"
        ]
        
        for filename in index_files:
            path = os.path.join(self.input_dir, filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    key = filename.replace(".json", "")
                    self.indexes[key] = json.load(f)

        # [cite_start]Chargement des produits pour l'affichage (rearranged_products.jsonl) [cite: 49-53]
        if os.path.exists(self.products_file):
            with open(self.products_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            doc = json.loads(line)
                            if 'url' in doc:
                                self.documents_map[doc['url']] = doc
                        except json.JSONDecodeError:
                            continue

        self.ranker = Ranker(len(self.documents_map))

    def filter_documents(self, tokens, strict=False):
        """Filtre les documents contenant les tokens (OR par défaut)."""
        if not tokens: return set()
        
        title_idx = self.indexes.get("title_index", {})
        desc_idx = self.indexes.get("description_index", {})
        
        candidate_docs = []
        for token in tokens:
            docs_with_token = set()
            if token in title_idx:
                docs_with_token.update(title_idx[token].keys())
            if token in desc_idx:
                docs_with_token.update(desc_idx[token].keys())
            candidate_docs.append(docs_with_token)

        if not candidate_docs:
            return set()

        if strict:
            return set.intersection(*candidate_docs)
        else:
            return set.union(*candidate_docs)

    def search(self, query):
        # [cite_start]1. Normalisation et synonymes [cite: 20-21]
        tokens = normalize_query(query, self.synonyms)
        if not tokens:
            return {"metadata": {"count": 0}, "results": []}

        # [cite_start]2. Filtrage [cite: 22-24]
        matching_urls = self.filter_documents(tokens, strict=False)
        scored_results = []
        
        title_idx = self.indexes.get("title_index", {})
        desc_idx = self.indexes.get("description_index", {})
        review_idx = self.indexes.get("review_index", {})

        # [cite_start]3. Ranking [cite: 33-39]
        for url in matching_urls:
            # Récupération des positions pour le scoring
            t_hits = {}
            d_hits = {}
            for token in tokens:
                if token in title_idx and url in title_idx[token]:
                    t_hits[url] = title_idx[token][url]
                if token in desc_idx and url in desc_idx[token]:
                    d_hits[url] = desc_idx[token][url]

            review_data = review_idx.get(url, {})
            score = self.ranker.compute_linear_score(tokens, url, t_hits, d_hits, review_data)
            scored_results.append((url, score))

        # Tri décroissant par score
        scored_results.sort(key=lambda x: x[1], reverse=True)

        formatted_results = []
        for url, score in scored_results:
            doc = self.documents_map.get(url, {})
            formatted_results.append({
                "title": doc.get("title", "N/A"),
                "url": url,
                "description": doc.get("description", "")[:200] + "...",
                "score": round(score, 4)
            })

        return {
            "metadata": {
                "total_documents": len(self.documents_map),
                "filtered_documents": len(formatted_results),
                "query_tokens": tokens
            },
            "results": formatted_results
        }