import re
import nltk
from nltk.corpus import stopwords

# S'assurer que les stopwords sont téléchargés
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

STOPWORDS = set(stopwords.words('english'))

def tokenize(text):
    """Découpe le texte en mots (tokens) et nettoie la ponctuation."""
    if not text: return []
    
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    
    return text.split()

def remove_stopwords(tokens):
    """Filtre la liste des tokens."""
    return [t for t in tokens if t not in STOPWORDS]