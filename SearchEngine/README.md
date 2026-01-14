# TP3 - Moteur de Recherche (Search Engine)

Ce projet finalise le moteur de recherche en exploitant les index construits précédemment. Il permet d'interroger la base de produits avec une gestion des synonymes et un algorithme de ranking pondéré.

## 🚀 Fonctionnalités Implémentées

### 1. Traitement de la requête (NLP)
* **Tokenization & Nettoyage :** Utilisation de `NLTK` pour retirer les stopwords (mots vides) et la ponctuation.
* **Expansion par Synonymes :** La requête est enrichie automatiquement.
    * *Exemple :* Une recherche sur "US" cherchera aussi "USA", "United States" et "America" grâce au dictionnaire `synonyms.json`.

### 2. Algorithme de Ranking (Score Linéaire)
Nous avons choisi une approche de scoring linéaire combinant plusieurs signaux pour classer les documents pertinents.

**Formule de score :**
`Score = (Freq_Titre * 3.0) + (Bonus_Position_Titre * 0.2) + (Freq_Desc * 1.0) + (Score_Avis * 0.5)`

**Justification des poids :**
* **Titre (3.0) :** C'est le signal le plus fort. Un mot dans le titre indique généralement le sujet principal du produit.
* **Description (1.0) :** Important pour le contexte, mais pondéré plus faiblement pour éviter que les longues descriptions ne faussent les résultats (spam de mots-clés).
* **Position (0.2) :** Un bonus est accordé si le mot-clé apparaît au tout début du titre.
* **Avis (0.5) :** Les produits bien notés et populaires reçoivent un petit "boost", favorisant la qualité sans éclipser la pertinence textuelle. Le nombre d'avis est passé au logarithme pour lisser les écarts.

### 3. Filtrage Booléen
Le moteur utilise une logique **OR (Union)** par défaut : un document est retenu s'il contient *au moins un* des mots de la requête (ou leurs synonymes). Cela maximise le nombre de résultats ("Recall").

## 🛠️ Installation et Exécution

1.  **Prérequis :**
    * Les fichiers d'index (`title_index.json`, etc.) doivent être dans le dossier `input/`.
    * Le fichier `rearranged_products.jsonl` doit être à la racine.
    * Librairie : `pip install nltk`

2.  **Lancement :**
    ```bash
    python main.py
    ```

3.  **Résultats :**
    Les résultats de la dernière recherche sont sauvegardés dans `output/search_results.json` au format demandé (Titre, URL, Description, Score).

## 🧪 Exemple de test
**Requête :** "US Bag"
1.  Le moteur étend la requête à : *{"us", "usa", "america", "bag", "pouch", "sack"}*.
2.  Il filtre les documents contenant l'un de ces termes.
3.  Il calcule le score. Les sacs fabriqués aux USA ayant "USA" dans le titre remontent en premier.