"""Rutas absolutas del proyecto.

Detecta la raíz del repo caminando hacia arriba desde la ubicación de este
archivo hasta encontrar el directorio `.git`. Esto hace que las rutas funcionen
sin importar desde dónde se ejecute el código (notebook, script, REPL).

Uso desde un notebook:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.cwd().parent / "utils"))
    from paths import REPO, RAW, INTERIM, EXTERNAL
"""
from pathlib import Path


def _find_repo_root() -> Path:
    p = Path(__file__).resolve()
    while p != p.parent:
        if (p / ".git").exists():
            return p
        p = p.parent
    raise RuntimeError(
        "No se encontró la raíz del repo (busqué un directorio .git hacia arriba)"
    )


REPO = _find_repo_root()

RAW = REPO / "data/raw"
INTERIM = REPO / "data/interim"
EXTERNAL = REPO / "data/external"
PROCESSED = REPO / "data/processed"
MANIFEST = REPO / "data/manifest"
DOCS = REPO / "docs"

PANELES = INTERIM / "paneles_largos"
DIMENSIONES = INTERIM / "dimensiones"
CROSSWALKS = EXTERNAL / "crosswalks"
