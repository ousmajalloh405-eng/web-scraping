"""Chargement des citations dans SQLite."""

import sqlite3
from pathlib import Path
from typing import List, Dict


def initialiser_base(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS citations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citation TEXT,
            auteur TEXT,
            tags TEXT,
            page INTEGER,
            longueur INTEGER
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_auteur ON citations(auteur)")
    conn.commit()
    return conn


def charger(conn: sqlite3.Connection, data: List[Dict]) -> int:
    conn.execute("DELETE FROM citations")
    for c in data:
        conn.execute(
            "INSERT INTO citations (citation, auteur, tags, page, longueur) VALUES (?, ?, ?, ?, ?)",
            (c["citation"], c["auteur"], c["tags"], c["page"], c["longueur"]),
        )
    conn.commit()
    return len(data)
