# Architecture — Web Scraping

## Flux

```
Site public (quotes.toscrape.com)
          │
          ▼
    extract.py
  (requests + BeautifulSoup)
          │
          ▼
   transform.py
          │
          ▼
     load.py
          │
          ▼
   citations.db
```

## Table `citations`

- citation, auteur, tags, page, longueur
