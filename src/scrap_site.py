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
# RÉCUPÉRATION DE TOUTES LES CATÉGORIES
# -----------------------------
def get_categories():
    base_url = "https://books.toscrape.com/"
    response = requests.get(base_url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    categories = []

    category_links = soup.select("ul.nav-list ul li a")

    for link in category_links:
        name = link.text.strip()
        url = base_url + link["href"]
        categories.append((name, url))

    return categories


# -----------------------------
# SCRAPING D'UNE CATÉGORIE (PAGINATION)
# -----------------------------
def scrape_category(category_url):
    base = category_url.rsplit("/", 1)[0] + "/"
    current_page = category_url.split("/")[-1]

    product_urls = []

    while True:
        url = base + current_page
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        for book in books:
            relative_url = book.h3.a["href"]
            product_url = "https://books.toscrape.com/catalogue/" + relative_url.replace("../", "")
            product_urls.append(product_url)

        next_button = soup.find("li", class_="next")

        if next_button:
            current_page = next_button.a["href"]
        else:
            break

    return product_urls


# -----------------------------
# SCRAPING D'UN LIVRE (PHASE 1)
# -----------------------------
def scrape_product(product_url):
    response = requests.get(product_url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    upc = soup.find("th", string="UPC").find_next("td").text.strip()
    title = soup.find("h1").text.strip()
    price_incl = soup.find("p", class_="price_color").text.strip()
    price_excl = soup.find("th", string="Price (excl. tax)").find_next("td").text.strip()

    availability = soup.find("p", class_="instock availability").text.strip()
    availability = " ".join(availability.split())

    description_tag = soup.find("div", id="product_description")
    description = description_tag.find_next("p").text.strip() if description_tag else "Aucune description"

    breadcrumb = soup.find("ul", class_="breadcrumb").find_all("li")
    category = breadcrumb[2].text.strip()

    rating_tag = soup.find("p", class_="star-rating")
    rating_class = rating_tag.get("class")[1]
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating = rating_map.get(rating_class, 0)

    image_relative_url = soup.find("img")["src"]
    image_url = "https://books.toscrape.com/" + image_relative_url.replace("../", "")

    # Télécharger l'image
    os.makedirs("data/images", exist_ok=True)
    image_data = requests.get(image_url).content
    image_filename = f"data/images/{upc}.jpg"

    with open(image_filename, "wb") as img_file:
        img_file.write(image_data)

    return {
        "product_page_url": product_url,
        "upc": upc,
        "title": title,
        "price_incl": price_incl,
        "price_excl": price_excl,
        "availability": availability,
        "description": description,
        "category": category,
        "rating": rating,
        "image_url": image_url
    }


# -----------------------------
# SCRAPING COMPLET DU SITE
# -----------------------------
def scrape_site():
    site_name = "BooksToScrape"
    safe_site = clean_filename(site_name)
    csv_filename = f"data/Scrap_{safe_site}.csv"

    os.makedirs("data", exist_ok=True)

    categories = get_categories()

    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "product_page_url", "upc", "title", "price_incl", "price_excl",
            "availability", "description", "category", "rating", "image_url"
        ])

        for category_name, category_url in categories:
            print(f"\n=== Catégorie : {category_name} ===")

            product_urls = scrape_category(category_url)

            for product_url in product_urls:
                print(f"Scraping livre : {product_url}")
                data = scrape_product(product_url)
                writer.writerow(data.values())

    print(f"\nScraping complet terminé !")
    print(f"CSV généré : {csv_filename}")
