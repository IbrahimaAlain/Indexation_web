from collections import defaultdict
from .text_processor import tokenize, remove_stopwords

class Indexer:
    def __init__(self):
        """Initialise les structures internes pour les différents index."""
        self.pos_title_index = defaultdict(dict)
        self.pos_desc_index = defaultdict(dict)
        self.reviews_index = {}
        self.features_indexes = defaultdict(lambda: defaultdict(list))

    def add_positional(self, content, url, target_index):
        """Construit un index inversé positionnel associant les tokens à l'URL et leurs positions."""
        tokens = tokenize(content)
        clean_tokens = set(remove_stopwords(tokens))
        
        for pos, token in enumerate(tokens):
            if token in clean_tokens:
                if url not in target_index[token]:
                    target_index[token][url] = []
                target_index[token][url].append(pos)

    def process_reviews(self, reviews, url):
        """Calcule et stocke les statistiques des avis (nombre, moyenne, dernière note) pour une URL."""
        if not reviews:
            self.reviews_index[url] = {"count": 0, "avg_rating": 0, "last_rating": None}
            return

        ratings = [r.get('rating', 0) for r in reviews]
        count = len(ratings)
        self.reviews_index[url] = {
            "count": count,
            "avg_rating": round(sum(ratings) / count, 2),
            "last_rating": ratings[-1] if ratings else 0
        }

    def process_features(self, features, url):
        """Indexe les caractéristiques produit en stockant l'URL sous des clés et valeurs normalisées."""
        if not features: return

        for name, value in features.items():
            clean_name = name.lower().strip()
            clean_val = value.lower().strip()
            self.features_indexes[clean_name][clean_val].append(url)

    def index_document(self, doc):
        """Orchestre l'indexation du titre, de la description, des avis et des caractéristiques d'un document."""
        url = doc.get('url')
        if not url: return

        self.add_positional(doc.get('title', ''), url, self.pos_title_index)
        self.add_positional(doc.get('description', ''), url, self.pos_desc_index)
        self.process_reviews(doc.get('product_reviews', []), url)
        self.process_features(doc.get('product_features', {}), url)