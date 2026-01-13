import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.indexer import Indexer
from src.text_processor import tokenize, remove_stopwords

class TestIndexer(unittest.TestCase):

    def setUp(self):
        """Prépare une instance vierge de l'indexeur avant chaque test."""
        self.indexer = Indexer()

    def test_text_processing(self):
        """Valide le découpage en mots et le filtrage des stopwords."""
        text = "Hello! The-World."
        tokens = tokenize(text)
        self.assertEqual(tokens, ["hello", "the", "world"])
        clean = remove_stopwords(tokens)
        self.assertNotIn("the", clean)

    def test_positional_index(self):
        """Vérifie que la position des mots est correctement enregistrée dans l'index."""
        doc = {"url": "http://example.com/1", "title": "Nike Air", "description": ""}
        self.indexer.index_document(doc)
        self.assertEqual(self.indexer.pos_title_index["nike"]["http://example.com/1"], [0])

    def test_reviews_logic(self):
        """Teste le calcul des statistiques (nombre d'avis) pour un produit."""
        doc = {"url": "http://a.com", "product_reviews": [{"rating": 5}]}
        self.indexer.index_document(doc)
        self.assertEqual(self.indexer.reviews_index["http://a.com"]["count"], 1)

    def test_feature_simple(self):
        """Contrôle la normalisation (minuscules) et le stockage direct des features."""
        doc = {
            "url": "http://example.com/3",
            "product_features": {
                "Made In": "France",
                "Brand": "Nike"
            }
        }
        self.indexer.index_document(doc)

        self.assertIn("france", self.indexer.features_indexes["made in"])
        self.assertIn("nike", self.indexer.features_indexes["brand"])

if __name__ == '__main__':
    unittest.main()