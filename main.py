"""Pipeline de collecte et d'analyse des avis e-commerce."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from extract import extraire_donnees
from transform import transformer
from load import initialiser_base, charger, afficher_statistiques


DB_PATH = Path(__file__).parent / "data" / "ecommerce.db"


def main():
    print("=" * 55)
    print("       PIPELINE WEB SCRAPING - E-COMMERCE")
    print("=" * 55)

    conn = None

    try:
        # 1. Extraction
        print("\n[1/3] EXTRACTION")
        donnees_brutes = extraire_donnees()

        # 2. Transformation
        print("\n[2/3] TRANSFORMATION")
        donnees_propres = transformer(donnees_brutes)

        # 3. Chargement
        print("\n[3/3] CHARGEMENT SQLITE")
        conn = initialiser_base(DB_PATH)
        resultat = charger(conn, donnees_propres)

        print(f"Produits traités : {resultat['products_processed']}")
        print(f"Avis traités : {resultat['reviews_processed']}")
        print(f"Nouveaux avis insérés : {resultat['reviews_inserted']}")

        afficher_statistiques(conn)

        print(f"\nBase de données : {DB_PATH}")
        print("\nPIPELINE TERMINÉ.")

    except Exception as erreur:
        print(f"\nERREUR PIPELINE : {erreur}")
        raise

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
