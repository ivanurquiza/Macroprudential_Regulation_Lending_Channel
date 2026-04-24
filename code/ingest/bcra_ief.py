"""Descarga y extracción de los dumps mensuales IEF del BCRA.

Cada dump es un archivo .7z accesible en
`https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/Entidades/{yyyymm}d.7z`,
donde `yyyymm` es el mes de publicación (el corte de datos es el mes anterior).

Este script:
1. Construye el inventario de dumps disponibles (probe vía GET con range, porque
   HEAD devuelve respuestas inválidas en el servidor BCRA).
2. Descarga cada .7z a `data/raw/bcra_ief/_archives/{yyyymm}.7z`.
3. Extrae a `data/raw/bcra_ief/{yyyymm}/`.
4. Registra cada descarga en `data/manifest/sources.yaml`.

Idempotente: saltea archivos ya bajados con tamaño correcto.

Configurar la ventana temporal con la variable VENTANA al inicio del script.
"""
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import py7zr

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
from paths import RAW
from manifest import sha256_of, append_entry, relpath


VENTANA = (201501, 202601)  # (yyyymm_min, yyyymm_max)
ARCHIVES = RAW / "bcra_ief/_archives"
EXTRACT_ROOT = RAW / "bcra_ief"


def probar_existencia(yyyymm: str) -> tuple[str, int | None, int]:
    """Devuelve (yyyymm, status, full_size). status=206 -> existe."""
    url = f"https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/Entidades/{yyyymm}d.7z"
    r = subprocess.run(
        ["curl", "-sI", "-X", "GET", "-r", "0-0", "--max-time", "20", url],
        capture_output=True, text=True
    )
    status = None
    full_size = 0
    for line in r.stdout.splitlines():
        if line.startswith("HTTP/"):
            m = re.search(r"\s(\d{3})", line)
            if m: status = int(m.group(1))
        if line.lower().startswith("content-range:"):
            m = re.search(r"/(\d+)", line)
            if m: full_size = int(m.group(1))
    return yyyymm, status, full_size


def construir_inventario(min_yyyymm: int, max_yyyymm: int) -> list[tuple[str, int]]:
    """Lista los meses disponibles en BCRA dentro de la ventana."""
    meses = [f"{y}{m:02d}" for y in range(2002, 2027) for m in range(1, 13)]
    meses = [m for m in meses if min_yyyymm <= int(m) <= max_yyyymm]

    with ThreadPoolExecutor(max_workers=24) as ex:
        resultados = list(ex.map(probar_existencia, meses))

    disponibles = [(m, sz) for (m, st, sz) in resultados if st == 206]
    return disponibles


def bajar_y_extraer(yyyymm: str, expected_size: int) -> tuple[bool, bool]:
    """Descarga el .7z y lo extrae. Idempotente."""
    url = f"https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/Entidades/{yyyymm}d.7z"
    archive = ARCHIVES / f"{yyyymm}.7z"
    extract_dir = EXTRACT_ROOT / yyyymm

    descargado = False
    if not (archive.exists() and archive.stat().st_size == expected_size):
        archive.parent.mkdir(parents=True, exist_ok=True)
        tmp = archive.with_suffix(".7z.part")
        r = subprocess.run(
            ["curl", "-sS", "--fail", "--max-time", "600", "-o", str(tmp), url],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            if tmp.exists(): tmp.unlink()
            raise RuntimeError(f"curl falló para {yyyymm}: {r.stderr.strip()}")
        tmp.rename(archive)
        descargado = True

    extraido = False
    if not (extract_dir.exists() and any(extract_dir.iterdir())):
        extract_dir.mkdir(parents=True, exist_ok=True)
        with py7zr.SevenZipFile(archive, mode="r") as z:
            z.extractall(path=extract_dir)
        extraido = True

    return descargado, extraido


def registrar(yyyymm: str, archive: Path) -> None:
    today = time.strftime("%Y-%m-%d")
    snap_year, snap_mo = int(yyyymm[:4]), int(yyyymm[4:])
    if snap_mo == 1:
        snap_y, snap_m = snap_year - 1, 12
    else:
        snap_y, snap_m = snap_year, snap_mo - 1
    snap_date = f"{snap_y}-{snap_m:02d}"

    append_entry({
        "id": f"bcra_ief_{yyyymm}",
        "source": "BCRA - Información de Entidades Financieras (IEF, datos abiertos)",
        "organism": "Banco Central de la Republica Argentina (BCRA)",
        "url": f"https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/Entidades/{yyyymm}d.7z",
        "methodology_url": "https://www.bcra.gob.ar/informacion-sobre-entidades-financieras/",
        "downloaded_at": today,
        "snapshot_date": snap_date,
        "path": relpath(EXTRACT_ROOT / yyyymm) + "/",
        "sha256": sha256_of(archive),
        "size_bytes": archive.stat().st_size,
        "license": "Dominio publico (BCRA)",
        "notes": f"Dump IEF publicado en {yyyymm[:4]}-{yyyymm[4:]}; corte de datos = {snap_date}.",
    })


def main():
    print(f"Inventario en ventana {VENTANA[0]}-{VENTANA[1]}...")
    disponibles = construir_inventario(*VENTANA)
    print(f"Disponibles: {len(disponibles)} dumps")

    for i, (yyyymm, expected_size) in enumerate(disponibles, 1):
        try:
            dl, ex = bajar_y_extraer(yyyymm, expected_size)
            archive = ARCHIVES / f"{yyyymm}.7z"
            registrar(yyyymm, archive)
            print(f"[{i}/{len(disponibles)}] {yyyymm}  dl={dl} ex={ex}")
        except Exception as e:
            print(f"[{i}/{len(disponibles)}] {yyyymm}  ERROR: {e}")


if __name__ == "__main__":
    main()
