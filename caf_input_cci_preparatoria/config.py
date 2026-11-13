"""Rutas del proyecto. Los notebooks las toman de aquí."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data"
RAW = DATA / "raw"  # originales, no se modifican
INTERIM = DATA / "interim"  # extracciones y resultados de trabajo
PROCESSED = DATA / "processed"  # productos finales
EXTERNAL = DATA / "external"

RAW_LIBROS = RAW / "Libros excel"
RAW_IDOS_INPUT = RAW / "2. IDOs - Input CCI"
RAW_PREPARATORIA = RAW / "4. Preparatoria CCI"  # una carpeta por sesión con sus PDF

REFERENCES = ROOT / "references"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
