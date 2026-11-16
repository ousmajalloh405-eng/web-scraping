# Architecture — Pipeline Web Scraping E-commerce

## 1. Vue générale

Le projet suit une architecture ETL en trois étapes :

1. Extract : collecte des produits et des avis.
2. Transform : nettoyage et validation.
3. Load : stockage dans SQLite.

## 2. Flux de données

```text
web-scraping.dev
       |
       v
src/extract.py
       |
       v
Catalogue HTML
Fiches produits
API JSON des avis
       |
       v
src/transform.py
       |
       v
Nettoyage et validation
       |
       v
src/load.py
       |
       v
data/ecommerce.db
      /       \
 products    reviews
