"""Extraction des produits et avis depuis web-scraping.dev."""

import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from urllib.parse import urljoin

BASE_URL = "https://web-scraping.dev"
TIMEOUT = 20


def creer_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; PortfolioDataProject/1.0)"
    })
    return session


def extraire_produits(session) -> List[Dict]:
    """Parcourt le catalogue et récupère les fiches produits."""
    produits = {}
    page = 1

    while True:
        url = f"{BASE_URL}/products?page={page}"
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        cartes = soup.select("div.row.product")
        nouveaux = 0

        for carte in cartes:
            lien = carte.select_one("h3 a")
            if not lien:
                continue

            product_url = urljoin(BASE_URL, lien.get("href", ""))
            match = re.search(r"/product/(\d+)", product_url)
            if not match:
                continue

            product_id = match.group(1)
            if product_id in produits:
                continue

            image = carte.select_one("img")
            description = carte.select_one(".short-description")
            prix = carte.select_one(".price")

            produits[product_id] = {
                "product_id": product_id,
                "name": lien.get_text(strip=True),
                "description": description.get_text(" ", strip=True) if description else "",
                "catalog_price": prix.get_text(strip=True) if prix else None,
                "detail_price": None,
                "image_url": urljoin(BASE_URL, image.get("src", "")) if image else None,
                "product_url": product_url,
            }
            nouveaux += 1

        print(f"Catalogue page {page} : {nouveaux} nouveaux produits")

        if not cartes or nouveaux == 0:
            break

        page += 1

    return list(produits.values())


def extraire_avis_produit(session, produit: Dict) -> List[Dict]:
    """Récupère les avis d'un produit en parcourant toutes les pages API."""
    response = session.get(produit["product_url"], timeout=TIMEOUT)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    titre = soup.select_one(".product-title")
    description = soup.select_one(".product-description")
    prix = soup.select_one("span.product-price")
    image = soup.select_one("img.product-img")
    token = soup.select_one('input[name="csrf-token"]')

    if titre:
        produit["name"] = titre.get_text(" ", strip=True)
    if description:
        produit["description"] = description.get_text(" ", strip=True)
    if prix:
        produit["detail_price"] = prix.get_text(" ", strip=True)
    if image:
        produit["image_url"] = urljoin(BASE_URL, image.get("src", ""))

    if not token or not token.get("value"):
        print(f"  Aucun token CSRF pour le produit {produit['product_id']}")
        return []

    headers = {"x-csrf-token": token["value"]}
    product_id = produit["product_id"]
    avis = []
    page = 1

    while True:
        api_url = f"{BASE_URL}/api/reviews"
        api_response = session.get(
            api_url,
            params={"product_id": product_id, "page": page},
            headers=headers,
            timeout=TIMEOUT,
        )
        api_response.raise_for_status()
        data = api_response.json()

        for item in data.get("results", []):
            avis.append({
                "review_id": item.get("id"),
                "product_id": product_id,
                "text": item.get("text", ""),
                "rating": item.get("rating"),
                "review_date": item.get("date"),
            })

        if page >= data.get("page_total", 1):
            break

        page += 1

    return avis


def extraire_donnees() -> Dict[str, List[Dict]]:
    """Exécute l'extraction complète des produits et de leurs avis."""
    session = creer_session()
    produits = extraire_produits(session)
    tous_les_avis = []

    print(f"\nProduits trouvés : {len(produits)}")

    for index, produit in enumerate(produits, start=1):
        try:
            avis = extraire_avis_produit(session, produit)
            tous_les_avis.extend(avis)
            print(
                f"[{index}/{len(produits)}] {produit['name']} "
                f": {len(avis)} avis"
            )
        except requests.RequestException as erreur:
            print(f"Erreur réseau pour {produit['name']} : {erreur}")
        except (ValueError, KeyError) as erreur:
            print(f"Erreur de données pour {produit['name']} : {erreur}")

    session.close()

    return {
        "products": produits,
        "reviews": tous_les_avis,
    }
