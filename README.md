# Web Scraping — Citations

> Pipeline de scraping web sur un site public (quotes.toscrape.com), nettoyage et stockage SQL.

**Statut** : 🟢 Réalisé  
**Catégorie** : 📥 Système de collecte et de stockage  
**Portfolio** : [Profil GitHub](https://github.com/ousmajalloh405-eng)

---

## 1. Problème métier

Collecter automatiquement des données publiques (citations) pour analyse ultérieure.

## 2. Architecture

```
quotes.toscrape.com
        │
        ▼
   extract.py (BeautifulSoup)
        │
        ▼
  transform.py
        │
        ▼
    load.py → citations.db
```

## 3. Technologies

- Python 3
- `requests` + `BeautifulSoup`
- SQLite

## 4. Installation et exécution

```bash
git clone https://github.com/ousmajalloh405-eng/web-scraping.git
cd web-scraping
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## 5. Compétences pour le CV

Développement d’un pipeline de web scraping Python avec BeautifulSoup, nettoyage des données et stockage relationnel.

---

*Projet réalisé dans le cadre de la formation Data — Sonatel Academy.*  
*Site utilisé : quotes.toscrape.com (site de pratique).*
