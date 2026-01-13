TP2 - Indexation Web

Ce projet implémente la phase d'indexation d'un moteur de recherche. Il transforme un flux de données produits (format JSONL) en structures d'index optimisées.

Structures d'Index

Les fichiers de sortie sont générés dans le dossier output/.

1. Index Inversés Positionnels (title_index.json, description_index.json)

Utilisés pour les champs Titre et Description. Contrairement à un index inversé simple, cette structure stocke la position de chaque token dans le document, permettant une future implémentation de recherche de phrases ou de classement par proximité.

Clé : Token (mot).
Valeur : Dictionnaire où les clés sont les URLs de documents et les valeurs sont des listes de positions.
Prétraitement : Minuscules, suppression de la ponctuation, suppression des mots vides (Stopwords).

Tokenisation et Nettoyage

Le fichier src/text_processor.py assure un nettoyage robuste :

Mise en minuscules : Insensibilité à la casse (ex: "Nike" == "nike").
Suppression de la ponctuation : Tous les caractères non alphanumériques sont remplacés par des espaces.
Filtrage NLTK : Utilisation de la librairie NLTK pour une liste exhaustive de stopwords anglais, réduisant le bruit bien mieux qu'une liste manuelle.

Exemple :

{
  "sneaker": {
    "https://web-scraping.dev/product/1": [0, 15],
    "https://web-scraping.dev/product/5": [2]
  },
  "running": {
    "https://web-scraping.dev/product/1": [4]
  }
}

2. Index de Caractéristiques (brand_index.json, origin_index.json)

Index inversés pour les caractéristiques catégorielles (Facettes). Le script extrait les données brutes (ex: "Made In") et les redirige vers le fichier approprié.

Clé : Valeur de la caractéristique (normalisée en minuscules).
Valeur : Liste des URLs de documents contenant cette caractéristique.

Exemple (Origine) :

{
  "italy": [
    "https://web-scraping.dev/product/11",
    "https://web-scraping.dev/product/23"
  ],
  "usa": [
    "https://web-scraping.dev/product/12"
  ]
}

3. Index des Avis (review_index.json)

Un index direct (non inversé) stockant des métadonnées statistiques sur les avis produits. Il est utilisé pour le ranking (classement) des résultats.

Clé : URL du document.
Valeur : Objet contenant :

count : Nombre total d'avis.
avg_rating : Note moyenne (arrondie à 2 décimales).
last_rating : La note de l'avis le plus récent.

Exemple :

{
  "https://web-scraping.dev/product/1": {
    "count": 5,
    "avg_rating": 4.2,
    "last_rating": 5
  }
}

Choix Techniques et Features Supplémentaires

Identifiant Unique (URL) : J'ai choisi de conserver l'URL complète comme identifiant dans les index. Cela évite une table de correspondance supplémentaire et permet un accès direct à la page.

Gestion "Agnostique" des Features : L'indexeur stocke la clé telle quelle (ex: "made in"). La transformation vers le fichier origin_index.json se fait explicitement lors de la sauvegarde dans main.py, gardant la logique de classe pure.

Support Hybride : Le script de chargement détecte automatiquement si le fichier d'entrée est un JSON standard ou du JSON Lines (JSONL).

Auto-configuration NLTK : Le script vérifie la présence des stopwords NLTK et les télécharge automatiquement si nécessaire au premier lancement.

Script

Générer les index

Assurez-vous que products.jsonl est dans le dossier input/. Pour lancer l'indexation :

python main.py

Note : Si vous n'avez pas la librairie nltk, installez-la via pip install nltk. Le script se chargera de télécharger les données nécessaires.

Exécuter les Tests

Une suite de tests unitaires valide la tokenization, le calcul des scores et le stockage des features.

python -m unittest discover tests
