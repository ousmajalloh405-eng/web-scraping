"""Extraction de citations depuis quotes.toscrape.com."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict


def extraire_citations(pages: int = 3) -> List[Dict]:
    """Scrape plusieurs pages de citations."""
    base_url = "https://quotes.toscrape.com/page/{}/"
    resultats = []

    for page in range(1, pages + 1):
        try:
            response = requests.get(base_url.format(page), timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for quote in soup.select(".quote"):
                texte = quote.select_one(".text").get_text(strip=True)
                auteur = quote.select_one(".author").get_text(strip=True)
                tags = [t.get_text(strip=True) for t in quote.select(".tag")]
                resultats.append({
                    "citation": texte,
                    "auteur": auteur,
                    "tags": ", ".join(tags),
                    "page": page,
                })
            print(f"Page {page} : {len(soup.select('.quote'))} citations")
        except Exception as e:
            print(f"Erreur page {page}: {e}")
            break

    return resultats
