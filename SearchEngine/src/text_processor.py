import re
import os
import json
import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

STOPWORDS = set(stopwords.words('english'))

def load_synonyms(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def tokenize(text):
    if not text: return []
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.split()

def normalize_query(query, synonyms_dict=None):
    tokens = tokenize(query)
    filtered_tokens = [t for t in tokens if t not in STOPWORDS]
    
    if not synonyms_dict:
        return filtered_tokens

    expanded_tokens = set(filtered_tokens)
    for token in filtered_tokens:
        if token in synonyms_dict:
            # Ajoute tous les synonymes trouvés pour ce mot
            for syn in synonyms_dict[token]:
                expanded_tokens.add(syn)
    
    return list(expanded_tokens)