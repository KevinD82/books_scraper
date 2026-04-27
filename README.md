#  Books Scraper — Scraping complet du site BooksToScrape

Ce projet Python réalise un scraping complet du site **BooksToScrape.com**, un site de démonstration conçu pour l’apprentissage du web scraping.  
Le programme permet d’extraire toutes les informations des livres, de télécharger les images et de générer des fichiers CSV structurés.

---

##  Fonctionnalités

###  Phase 1 — recupération de la page d'accueil
- Extraction de la liste des catégories

---

###  Phase 2 — Parcours de chaque catégorie
- Construction de l’URL de la catégorie
- Gestion de la pagination (page suivante)

---

###  Phase 3 — Parcours de chaque page de la catégorie
- Extraction de la liste des livres

---

###  Phase 4 — Parcours de chaque livre
- Ouverture de la page du livre
- Extraction des informations :

  - Titre
  - Prix TTC
  - Prix HT
  - Disponibilité
  - Description
  - Catégorie
  - Note (rating)
  - URL de l’image

---

###  Phase 5 — Parcours de chaque livre

Enregistrement dans data/images/

---

###  Phase 6 — Parcours de chaque livre

- Une ligne par livre dans Scrap_BooksToScrape.csv

---

##  Structure du projet
```
books_scraper/
|__ scrap_site.py           
|__ main.py                

|__ data/
    |__ Scrap_BooksToScrape.csv
    |__ images/
        |__ .jpg

|__ README.md
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

