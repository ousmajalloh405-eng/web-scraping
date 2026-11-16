"""Nettoyage et validation des produits et avis."""

from datetime import date
from typing import Dict, List


def nettoyer_produits(produits: List[Dict]) -> List[Dict]:
    propres = []
    ids_vus = set()

    for produit in produits:
        product_id = str(produit.get("product_id", "")).strip()
        name = str(produit.get("name", "")).strip()

        if not product_id or not name or product_id in ids_vus:
            continue

        ids_vus.add(product_id)

        propres.append({
            "product_id": product_id,
            "name": name,
            "description": str(produit.get("description") or "").strip(),
            "catalog_price": produit.get("catalog_price"),
            "detail_price": produit.get("detail_price"),
            "image_url": produit.get("image_url"),
            "product_url": produit.get("product_url"),
        })

    return propres


def nettoyer_avis(avis: List[Dict]) -> List[Dict]:
    propres = []
    ids_vus = set()

    for item in avis:
        review_id = str(item.get("review_id") or "").strip()
        product_id = str(item.get("product_id") or "").strip()
        text = str(item.get("text") or "").strip()
        rating = item.get("rating")
        review_date = str(item.get("review_date") or "").strip()

        if not review_id or not product_id or not text:
            continue

        if review_id in ids_vus:
            continue

        if not isinstance(rating, int) or isinstance(rating, bool):
            continue

        if not 1 <= rating <= 5:
            continue

        try:
            date.fromisoformat(review_date)
        except ValueError:
            continue

        ids_vus.add(review_id)

        propres.append({
            "review_id": review_id,
            "product_id": product_id,
            "text": text,
            "rating": rating,
            "review_date": review_date,
        })

    return propres


def transformer(donnees: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
    """Nettoie les produits et les avis extraits."""
    produits = nettoyer_produits(donnees.get("products", []))
    avis = nettoyer_avis(donnees.get("reviews", []))

    ids_produits = {p["product_id"] for p in produits}
    avis = [a for a in avis if a["product_id"] in ids_produits]

    print(f"Produits après nettoyage : {len(produits)}")
    print(f"Avis après nettoyage : {len(avis)}")

    return {
        "products": produits,
        "reviews": avis,
    }
