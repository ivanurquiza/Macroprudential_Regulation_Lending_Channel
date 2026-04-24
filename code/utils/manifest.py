"""Helpers para registrar fuentes en data/manifest/sources.yaml.

Mantiene el registro de procedencia de cada archivo bajado.
Los scripts de `code/ingest/` lo usan para appendear una entrada por descarga.
"""
import hashlib
from pathlib import Path

from paths import MANIFEST, REPO


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def already_in_manifest(entry_id: str) -> bool:
    f = MANIFEST / "sources.yaml"
    if not f.exists():
        return False
    return f"id: {entry_id}\n" in f.read_text()


def append_entry(entry: dict) -> None:
    """Append una entrada al sources.yaml. No-op si el id ya existe."""
    if already_in_manifest(entry["id"]):
        return
    f = MANIFEST / "sources.yaml"
    lines = [
        f"  - id: {entry['id']}\n",
        f"    source: {entry['source']}\n",
        f"    organism: {entry.get('organism', 'NA')}\n",
        f"    url: {entry['url']}\n",
        f"    methodology_url: {entry.get('methodology_url', 'NA')}\n",
        f"    downloaded_at: {entry['downloaded_at']}\n",
        f"    snapshot_date: {entry['snapshot_date']}\n",
        f"    path: {entry['path']}\n",
        f"    sha256: {entry['sha256']}\n",
        f"    size_bytes: {entry['size_bytes']}\n",
        f"    license: {entry.get('license', 'Dominio publico')}\n",
        f"    notes: {entry['notes']}\n",
    ]
    with open(f, "a") as fh:
        fh.writelines(lines)


def relpath(p: Path) -> str:
    """Path relativo al root del repo, como string POSIX."""
    return str(p.relative_to(REPO))
