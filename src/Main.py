import requests
from bs4 import BeautifulSoup
import csv


# URL du livre à scraper
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Requête HTTP
response = requests.get(url)
response.encoding = "utf-8"  # Correction de l'encodage

print("Status code :", response.status_code)

# Parsing HTML avec BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extraction du titre
title = soup.find("h1").text.strip()
print("Titre :", title)

# Extraction du prix TTC
price_incl = soup.find("p", class_="price_color").text.strip()
print("Prix TTC :", price_incl)

# Extraction du prix HT
price_excl = soup.find("th", string="Price (excl. tax)").find_next("td").text.strip()
print("Prix HT :", price_excl)

# Extraction de l'UPC
upc = soup.find("th", string="UPC").find_next("td").text.strip()
print("UPC :", upc)

# Extraction de la disponibilité
availability = soup.find("p", class_="instock availability").text.strip()
availability = " ".join(availability.split())  # Nettoyage pour supprimer les sauts de lignes
print("Disponibilité :", availability)

# Extraction de la description
description_tag = soup.find("div", id="product_description")
if description_tag:
    description = description_tag.find_next("p").text.strip()
else:
    description = "Aucune description"
print("Description :", description)

# Extraction de la catégorie
breadcrumb = soup.find("ul", class_="breadcrumb").find_all("li")
category = breadcrumb[2].text.strip()
print("Catégorie :", category)

# Extraction du rating
rating_tag = soup.find("p", class_="star-rating")
rating_class = rating_tag.get("class")[1]  # ex: "Three"

# Conversion texte → chiffre
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}
rating = rating_map.get(rating_class, 0)

print("Rating :", rating)

# -----------------------------
# EXPORT CSV
# -----------------------------

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # En-têtes
    writer.writerow([
        "title", "price_incl", "price_excl", "upc",
        "availability", "description", "category", "rating"
    ])
    
    # Données
    writer.writerow([
        title, price_incl, price_excl, upc,
        availability, description, category, rating
    ])

print("CSV généré : output.csv")
