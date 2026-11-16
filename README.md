# Pipeline Web Scraping — Avis E-commerce

Pipeline ETL Python de collecte, nettoyage et stockage de produits et avis clients depuis web-scraping.dev.

## Objectif
Collecter les produits et leurs avis pour préparer leur analyse.

## Architecture
- Extract : catalogue HTML, fiches produits et API paginée.
- Transform : nettoyage et validation.
- Load : stockage relationnel SQLite.

## Technologies
Python, Requests, BeautifulSoup, API JSON, SQLite et SQL.

## Résultats
- 25 produits collectés.
- 96 avis validés.
- Note moyenne : 4,36/5.
- Deuxième exécution : 0 nouvel avis inséré.

## Base de données

### products
product_id (PK), name, description, catalog_price, detail_price, image_url, product_url.

### reviews
review_id (PK), product_id (FK), text, rating, review_date.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
