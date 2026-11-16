"""Stockage des produits et avis dans SQLite."""

import sqlite3
from pathlib import Path
from typing import Dict, List


def initialiser_base(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            catalog_price TEXT,
            detail_price TEXT,
            image_url TEXT,
            product_url TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id TEXT PRIMARY KEY,
            product_id TEXT NOT NULL,
            text TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            review_date TEXT NOT NULL,
            FOREIGN KEY(product_id)
                REFERENCES products(product_id)
                ON DELETE CASCADE
        )
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_reviews_product
        ON reviews(product_id)
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_reviews_date
        ON reviews(review_date)
    """)

    conn.commit()
    return conn


def charger(conn: sqlite3.Connection, donnees: Dict[str, List[Dict]]) -> Dict:
    produits = donnees.get("products", [])
    avis = donnees.get("reviews", [])

    with conn:
        conn.executemany("""
            INSERT INTO products (
                product_id, name, description, catalog_price,
                detail_price, image_url, product_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(product_id) DO UPDATE SET
                name = excluded.name,
                description = excluded.description,
                catalog_price = excluded.catalog_price,
                detail_price = excluded.detail_price,
                image_url = excluded.image_url,
                product_url = excluded.product_url
        """, [
            (
                p["product_id"], p["name"], p["description"],
                p["catalog_price"], p["detail_price"],
                p["image_url"], p["product_url"]
            )
            for p in produits
        ])

        curseur = conn.executemany("""
            INSERT OR IGNORE INTO reviews (
                review_id, product_id, text, rating, review_date
            )
            VALUES (?, ?, ?, ?, ?)
        """, [
            (
                a["review_id"], a["product_id"], a["text"],
                a["rating"], a["review_date"]
            )
            for a in avis
        ])

    return {
        "products_processed": len(produits),
        "reviews_processed": len(avis),
        "reviews_inserted": curseur.rowcount,
    }


def afficher_statistiques(conn: sqlite3.Connection):
    print("\n=== STATISTIQUES SQLITE ===")

    for table in ("products", "reviews"):
        total = conn.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]
        print(f"{table}: {total}")

    print("\nNote moyenne des avis :")
    moyenne = conn.execute(
        "SELECT ROUND(AVG(rating), 2) FROM reviews"
    ).fetchone()[0]
    print(moyenne if moyenne is not None else "Aucune donnée")

    print("\nRépartition des notes :")
    for rating, total in conn.execute("""
        SELECT rating, COUNT(*)
        FROM reviews
        GROUP BY rating
        ORDER BY rating DESC
    """):
        print(f"{rating}/5 : {total}")
