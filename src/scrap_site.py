import requests
from bs4 import BeautifulSoup
import csv
import os
import re

BASE_URL = "https://books.toscrape.com/"

def get_soup(url):
    """Télécharge une page HTML et renvoie un objet BeautifulSoup."""
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def scrape_site():
    print("Scraping du site BooksToScrape démarré !")

    # --- Étape 0 : Préparation des dossiers et du CSV ---
    os.makedirs("data/images", exist_ok=True)

    with open("data/Scrap_BooksToScrape.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "product_page_url",
            "universal_product_code",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url",
            "image_path"
        ])

        # --- Étape 1 : Récupérer la page d’accueil ---
        home_soup = get_soup(BASE_URL)

        # --- Étape 2 : Extraire la liste des catégories ---
        categories = home_soup.select("ul.nav-list ul li a")
        print(f"{len(categories)} catégories trouvées.")

        # --- Étape 3 : Boucle sur chaque catégorie ---
        for cat in categories:
            category_name = cat.text.strip()
            category_url = BASE_URL + cat["href"]
            print(f"\nCatégorie : {category_name}")

            # --- Étape 4 : Boucle sur les pages de la catégorie ---
            while True:
                cat_soup = get_soup(category_url)
                books = cat_soup.select("article.product_pod h3 a")

                # --- Étape 5 : Boucle sur chaque livre ---
                for book in books:

                    # URL de la page produit
                    product_page_url = BASE_URL + "catalogue/" + book["href"].replace("../", "")
                    book_soup = get_soup(product_page_url)

                    # Extraction des données du livre
                    title = book_soup.h1.text
                    print(f"  Livre : {title}")

                    table = book_soup.select("table tr")
                    universal_product_code = table[0].td.text
                    price_excl = table[2].td.text
                    price_incl = table[3].td.text
                    availability_text = table[5].td.text

                    # Extraction du nombre disponible
                    numbers = re.findall(r'\d+', availability_text)
                    number_available = numbers[0] if numbers else "0"

                    desc_tag = book_soup.select_one("#product_description")
                    product_description = desc_tag.find_next("p").text if desc_tag else ""

                    category = book_soup.select("ul.breadcrumb li a")[-1].text

                    review_rating = book_soup.select_one("p.star-rating")["class"][1]

                    img_rel = book_soup.select_one("div.item.active img")["src"]
                    image_url = BASE_URL + img_rel.replace("../", "")

                    # Téléchargement de l’image
                    image_path = f"data/images/{title}.jpg"
                    img_data = requests.get(image_url).content
                    with open(image_path, "wb") as img_file:
                        img_file.write(img_data)

                    # --- Étape 6 : Écriture dans le CSV ---
                    writer.writerow([
                        product_page_url,
                        universal_product_code,
                        title,
                        price_incl,
                        price_excl,
                        number_available,
                        product_description,
                        category,
                        review_rating,
                        image_url,
                        image_path
                    ])

                # --- Pagination : passer à la page suivante si elle existe ---
                next_btn = cat_soup.select_one("li.next a")
                if next_btn:
                    category_url = BASE_URL + "catalogue/" + next_btn["href"]
                else:
                    break
