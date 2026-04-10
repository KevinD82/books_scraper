import requests
from bs4 import BeautifulSoup

# URL de base de la catégorie Fantasy
base_url = "https://books.toscrape.com/catalogue/category/books/fantasy_19/"
current_page = "page-1.html"   # On commence toujours par page-1.html

while True:
    # Construire l'URL complète de la page actuelle
    url = base_url + current_page
    print(f"\n--- Lecture de : {url} ---\n")

    # Télécharger la page
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraire les livres de la page
    books = soup.find_all("article", class_="product_pod")

    print("Livres trouvés :")
    for book in books:
        relative_url = book.h3.a["href"]
        product_url = "https://books.toscrape.com/catalogue/" + relative_url.replace("../", "")
        print(product_url)

    # Vérifier s'il y a une page suivante
    next_button = soup.find("li", class_="next")

    if next_button:
        current_page = next_button.a["href"]  # ex: "page-2.html"
        print("\nPage suivante détectée :", current_page)
    else:
        print("\nAucune page suivante. Fin du scraping.")
        break
