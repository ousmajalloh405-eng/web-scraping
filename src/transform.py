"""Transformation des citations scrapées."""

from typing import List, Dict


def transformer(citations: List[Dict]) -> List[Dict]:
    """Nettoie les données."""
    propres = []
    for c in citations:
        if not c.get("citation") or not c.get("auteur"):
            continue
        propres.append({
            "citation": c["citation"].strip(),
            "auteur": c["auteur"].strip(),
            "tags": c.get("tags", "").strip(),
            "page": c.get("page", 0),
            "longueur": len(c["citation"]),
        })
    return propres
