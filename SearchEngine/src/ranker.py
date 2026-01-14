import math

class Ranker:
    def __init__(self, total_docs):
        self.total_docs = total_docs
        self.weights = {
            "title": 3.0,
            "description": 1.0,
            "reviews": 0.5,
            "position": 0.2
        }

    def compute_linear_score(self, query_tokens, url, title_hits, desc_hits, review_data):
        """Calcule le score de pertinence d'un document en combinant les correspondances (titre, description) et les avis."""
        score = 0.0

        if url in title_hits:
            positions = title_hits[url]
            freq = len(positions)
            # Bonus si le mot apparaît au début du titre
            pos_bonus = sum([1/(p+1) for p in positions])
            score += (freq * self.weights["title"]) + (pos_bonus * self.weights["position"])

        if url in desc_hits:
            positions = desc_hits[url]
            freq = len(positions)
            score += freq * self.weights["description"]

        if review_data:
            avg_rating = review_data.get("avg_rating", 0)
            count = review_data.get("count", 0)
            
            if count > 0:
                # Logarithme pour amortir l'impact des produits avec énormément d'avis
                review_score = avg_rating * math.log(1 + count)
                score += review_score * self.weights["reviews"]

        return score