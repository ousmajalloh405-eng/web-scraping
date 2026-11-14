"""Pipeline Web Scraping — Citations."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from extract import extraire_citations
from transform import transformer
from load import initialiser_base, charger


DB_PATH = Path(__file__).parent / "data" / "citations.db"


def afficher_resume(conn):
    print("\n=== Résumé ===")
    total = conn.execute("SELECT COUNT(*) FROM citations").fetchone()[0]
    print(f"Total citations : {total}")

    print("\nTop auteurs :")
    for row in conn.execute("""
        SELECT auteur, COUNT(*) AS nb
        FROM citations
        GROUP BY auteur
        ORDER BY nb DESC
        LIMIT 5
    """):
        print(f"  {row[0]:25} {row[1]} citations")


def main():
    print("=== Pipeline Web Scraping ===\n")

    brut = extraire_citations(pages=3)
    print(f"\nCitations extraites : {len(brut)}")

    propres = transformer(brut)
    print(f"Après nettoyage : {len(propres)}")

    conn = initialiser_base(DB_PATH)
    nb = charger(conn, propres)
    print(f"Chargées dans {DB_PATH} : {nb}")

    afficher_resume(conn)
    conn.close()
    print("\nPipeline terminé.")


if __name__ == "__main__":
    main()
