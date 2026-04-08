#  Books Scraper — Web Scraping en Python

Un projet de scraping conçu pour extraire automatiquement les données du site *Books to Scrape* et les exporter dans un fichier CSV.

---

##  Ce que fait le script

-  Récupère les informations essentielles d’un livre  
-  Génère un fichier `output.csv`  
-  Nettoie et structure les données  
-  Convertit les notes (One, Two, Three…) en valeurs numériques  

---

##  Stack technique

- Python 3  
- BeautifulSoup4  
- Requests  
- CSV  

---

##  Installation & exécution

```bash
git clone https://github.com/KevinD82/books_scraper.git
cd books_scraper
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python Main.py