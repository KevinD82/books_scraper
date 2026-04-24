#  Books Scraper — Scraping complet du site BooksToScrape

Ce projet Python réalise un scraping complet du site **BooksToScrape.com**, un site de démonstration conçu pour l’apprentissage du web scraping.  
Le programme permet d’extraire toutes les informations des livres, de télécharger les images et de générer des fichiers CSV structurés.

---

##  Fonctionnalités

###  Phase 1 — Scraping d’un produit
- Extraction des informations d’un livre :
  - URL de la page produit  
  - UPC  
  - Titre  
  - Prix TTC / HT  
  - Disponibilité  
  - Description  
  - Catégorie  
  - Rating (converti en chiffre)  
  - URL de l’image  
- Téléchargement de l’image du livre  
- Génération d’un fichier CSV nommé automatiquement :  
  **`Scrap_<Nom_du_livre>.csv`**

---

###  Phase 2 — Scraping d’une catégorie
- Parcours automatique de toutes les pages d’une catégorie (pagination)
- Extraction de tous les livres de la catégorie
- Téléchargement des images
- Génération d’un fichier CSV :  
  **`Scrap_<Nom_de_la_catégorie>.csv`**

---

###  Phase 3 — Scraping complet du site
- Récupération automatique de toutes les catégories
- Scraping de tous les livres du site (1000 livres)
- Téléchargement de toutes les images
- Génération d’un CSV global :  
  **`Scrap_BooksToScrape.csv`**

---

##  Structure du projet
```
books_scraper/
|__ scrap_product.py        # Phase 1
|__ scrap_category.py       # Phase 2
|__ scrap_site.py           # Phase 3
|__ main.py                 # Point d'entrée du programme

|__ data/
    |__ Scrap_.csv
    |__ Scrap_.csv
    |__ Scrap_BooksToScrape.csv

|__ images/
    |__ .jpg

|__ requirements.txt
```

## Installation & exécution

### 1. Cloner le projet
```
git clone https://github.com/KevinD82/books_scraper.git
cd books_scraper
```
### 2. créer l'environnement virtuel
```
python -m venv .venv
```

### 3. Activer l'environnement virtuel
```
.venv\Scripts\activate
```

### 4. Installer les dépendances
```
pip install -r requirements.txt
```

### 5. Executer le script
```
python main.py
```

### Dépendances
- Python 3.x
- BeautifulSoup4
- Requests

Toutes les dépendances sont listées dans requirements.txt.

