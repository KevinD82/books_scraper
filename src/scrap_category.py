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
# CONFIGURATION
# -----------------------------
base_url = "https://books.toscrape.com/catalogue/category/books/fantasy_19/"
current_page = "page-1.html"

# Création du dossier images
os.makedirs("data/images", exist_ok=True)

# -----------------------------
# RÉCUPÉRATION DU NOM DE LA CATÉGORIE
# -----------------------------
response = requests.get(base_url + current_page)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

breadcrumb = soup.find("ul", class_="breadcrumb").find_all("li")
category_name = breadcrumb[-1].text.strip()  # ex: "Fantasy"

safe_category = clean_filename(category_name)
csv_filename = f"data/Scrap_{safe_category}.csv"

print(f"Scraping catégorie : {category_name}")
print(f"Fichier CSV : {csv_filename}")

# -----------------------------
# CRÉATION DU FICHIER CSV
# -----------------------------
with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # En-têtes CSV
    writer.writerow([
        "product_page_url", "upc", "title", "price_incl", "price_excl",
        "availability", "description", "category", "rating", "image_url"
    ])

    # -----------------------------
    # BOUCLE SUR TOUTES LES PAGES
    # -----------------------------
    while True:
        url = base_url + current_page
        print(f"\n--- Lecture de : {url} ---\n")

        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        # -----------------------------
        # BOUCLE SUR CHAQUE LIVRE
        # -----------------------------
        for book in books:
            relative_url = book.h3.a["href"]
            product_url = "https://books.toscrape.com/catalogue/" + relative_url.replace("../", "")

            print(f"Scraping livre : {product_url}")

            # -----------------------------
            # SCRAPING DU LIVRE (PHASE 1)
            # -----------------------------
            response_book = requests.get(product_url)
            response_book.encoding = "utf-8"
            soup_book = BeautifulSoup(response_book.text, "html.parser")

            # URL page produit
            product_page_url = product_url

            # UPC
            upc = soup_book.find("th", string="UPC").find_next("td").text.strip()

            # Titre
            title = soup_book.find("h1").text.strip()

            # Prix TTC
            price_incl = soup_book.find("p", class_="price_color").text.strip()

            # Prix HT
            price_excl = soup_book.find("th", string="Price (excl. tax)").find_next("td").text.strip()

            # Disponibilité
            availability = soup_book.find("p", class_="instock availability").text.strip()
            availability = " ".join(availability.split())

            # Description
            description_tag = soup_book.find("div", id="product_description")
            if description_tag:
                description = description_tag.find_next("p").text.strip()
            else:
                description = "Aucune description"

            # Catégorie
            breadcrumb = soup_book.find("ul", class_="breadcrumb").find_all("li")
            category = breadcrumb[2].text.strip()

            # Rating
            rating_tag = soup_book.find("p", class_="star-rating")
            rating_class = rating_tag.get("class")[1]
            rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            rating = rating_map.get(rating_class, 0)

            # Image
            image_relative_url = soup_book.find("img")["src"]
            image_url = "https://books.toscrape.com/" + image_relative_url.replace("../", "")

            # Télécharger l'image
            image_data = requests.get(image_url).content
            image_filename = f"data/images/{upc}.jpg"

            with open(image_filename, "wb") as img_file:
                img_file.write(image_data)

            print("Image téléchargée :", image_filename)

            # -----------------------------
            # ÉCRITURE DANS LE CSV
            # -----------------------------
            writer.writerow([
                product_page_url, upc, title, price_incl, price_excl,
                availability, description, category, rating, image_url
            ])

        # -----------------------------
        # PAGINATION
        # -----------------------------
        next_button = soup.find("li", class_="next")

        if next_button:
            current_page = next_button.a["href"]
            print("\nPage suivante détectée :", current_page)
        else:
            print("\nAucune page suivante. Fin du scraping.")
            break

print(f"\nCSV généré : {csv_filename}")
