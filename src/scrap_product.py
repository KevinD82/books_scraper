import requests
from bs4 import BeautifulSoup
import csv
import os

# -----------------------------
# FONCTION UTILITAIRE
# -----------------------------
def clean_filename(name):
    """Nettoie un nom pour qu'il soit compatible avec un fichier."""
    return "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).rstrip()


# -----------------------------
# URL DU LIVRE À SCRAPER
# -----------------------------
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Requête HTTP
response = requests.get(url)
response.encoding = "utf-8"

print("Status code :", response.status_code)

# Parsing HTML
soup = BeautifulSoup(response.text, "html.parser")

# URL de la page produit
product_page_url = url
print("URL du produit :", product_page_url)

# Extraction de l'UPC
upc = soup.find("th", string="UPC").find_next("td").text.strip()
print("UPC :", upc)

# Extraction du titre
title = soup.find("h1").text.strip()
print("Titre :", title)

# Extraction du prix TTC
price_incl = soup.find("p", class_="price_color").text.strip()
print("Prix TTC :", price_incl)

# Extraction du prix HT
price_excl = soup.find("th", string="Price (excl. tax)").find_next("td").text.strip()
print("Prix HT :", price_excl)

# Extraction de la disponibilité
availability = soup.find("p", class_="instock availability").text.strip()
availability = " ".join(availability.split())
print("Disponibilité :", availability)

# Description
description_tag = soup.find("div", id="product_description")
if description_tag:
    description = description_tag.find_next("p").text.strip()
else:
    description = "Aucune description"
print("Description :", description)

# Catégorie
breadcrumb = soup.find("ul", class_="breadcrumb").find_all("li")
category = breadcrumb[2].text.strip()
print("Catégorie :", category)

# Rating
rating_tag = soup.find("p", class_="star-rating")
rating_class = rating_tag.get("class")[1]

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}
rating = rating_map.get(rating_class, 0)
print("Rating :", rating)

# Image
image_relative_url = soup.find("img")["src"]
image_url = "https://books.toscrape.com/" + image_relative_url.replace("../", "")
print("Image du livre :", image_url)


# -----------------------------
# TÉLÉCHARGEMENT DE L’IMAGE
# -----------------------------
os.makedirs("data/images", exist_ok=True)

image_data = requests.get(image_url).content
image_filename = f"data/images/{upc}.jpg"

with open(image_filename, "wb") as img_file:
    img_file.write(image_data)

print("Image téléchargée :", image_filename)


# -----------------------------
# EXPORT CSV — NOM DYNAMIQUE
# -----------------------------
safe_title = clean_filename(title)
csv_filename = f"data/Scrap_{safe_title}.csv"

with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "product_page_url", "upc", "title", "price_incl", "price_excl",
        "availability", "description", "category", "rating", "image_url"
    ])

    writer.writerow([
        product_page_url, upc, title, price_incl, price_excl,
        availability, description, category, rating, image_url
    ])

print(f"CSV généré : {csv_filename}")
