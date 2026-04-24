"""Descarga datos primarios del INDEC.

Tres conjuntos:
- IPC nacional con aperturas y divisiones (carpeta FTP indec.gob.ar/ftp/cuadros/economia/).
- OPEX (Origen Provincial de Exportaciones) histórico 1993-2018.
- Proyecciones poblacionales provinciales (Censo 2022).

Output en `data/raw/indec_ipc/`, `data/raw/indec_opex/`, `data/raw/indec_poblacion/`.
"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
from paths import RAW
from manifest import sha256_of, append_entry, relpath


UA = "Mozilla/5.0"
INDEC_BASE = "https://www.indec.gob.ar/ftp/cuadros/economia"
INDEC_OLD  = "https://sitioanterior.indec.gob.ar/ftp/cuadros/economia"
CENSO_BASE = "https://censo.gob.ar/wp-content/uploads/2025/10"


IPC_FILES = [
    ("sh_ipc_aperturas.xls",
     "IPC nacional - variaciones mensuales por aperturas (base dic-2016)."),
    ("serie_ipc_aperturas.csv",
     "IPC nacional - serie histórica por aperturas (CSV)."),
    ("serie_ipc_divisiones.csv",
     "IPC nacional - serie histórica por divisiones COICOP (CSV)."),
]

OPEX_FILES = [
    ("sh_opex_principales_grubros_1993_2018.xls",
     "OPEX - principales grandes rubros exportados - serie 1993-2018."),
    ("sh_opex_regiones_economicas_grubros_1993_2018.xls",
     "OPEX - grandes rubros × regiones económicas - serie 1993-2018."),
    ("sh_opex_regiones_economicas_provincias_1993_2018.xls",
     "OPEX - regiones económicas × provincias - serie 1993-2018."),
    ("opex_anexo_cuadros.xls",
     "OPEX - cuadros anexos (diccionario de complejos exportadores)."),
]

CENSO_FILES = [
    ("proyecciones_jurisdicciones_2022_2040_base.csv",
     "Proyecciones por jurisdicciones - base CSV - sexo × edad simple × año (2022-2040)."),
    ("proyecciones_jurisdicciones_2022_2040_c1.xlsx",
     "Cuadro 1 - proyecciones por jurisdicción (totales por año)."),
    ("proyecciones_jurisdicciones_2022_2040_c2.xlsx",
     "Cuadro 2 - proyecciones por jurisdicción (por sexo)."),
    ("proyecciones_jurisdicciones_2022_2040_c3_c4.xlsx",
     "Cuadros 3 y 4 - proyecciones por jurisdicción (por grupos quinquenales de edad)."),
    ("proyecciones_jurisdicciones_2022_2040.pdf",
     "PDF - proyecciones de población por jurisdicciones 2022-2040."),
    ("proyecciones_nacionales_2022_2040.pdf",
     "PDF - proyecciones nacionales 2022-2040 (cross-check del total)."),
    ("metadatos_proyecciones_provinciales_2022_2040_base.pdf",
     "Metodología oficial de las proyecciones provinciales."),
]


def fetch(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    r = subprocess.run(
        ["curl", "-sSL", "--fail", "-A", UA, "--max-time", "180", "-o", str(tmp), url],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        if tmp.exists(): tmp.unlink()
        raise RuntimeError(f"curl falló {url}: {r.stderr.strip()[:200]}")
    tmp.rename(dest)
    return True


def descargar(grupo: str, base_url: str, files: list, subdir: str,
              source_label: str, methodology_url: str, snapshot: str):
    today = time.strftime("%Y-%m-%d")
    out = RAW / subdir
    print(f"=== {grupo} ===")
    for fname, desc in files:
        url = f"{base_url}/{fname}"
        dest = out / fname
        try:
            dl = fetch(url, dest)
            append_entry({
                "id": f"{subdir}_{fname.rsplit('.', 1)[0]}",
                "source": f"{source_label} - {fname}",
                "organism": "Instituto Nacional de Estadistica y Censos (INDEC)",
                "url": url,
                "methodology_url": methodology_url,
                "downloaded_at": today,
                "snapshot_date": snapshot,
                "path": relpath(dest),
                "sha256": sha256_of(dest),
                "size_bytes": dest.stat().st_size,
                "license": "Dominio publico (INDEC)",
                "notes": desc,
            })
            print(f"{'DL' if dl else 'SK'}  {fname}")
        except Exception as e:
            print(f"ERR {fname}: {e}")


def main():
    descargar("IPC", INDEC_BASE, IPC_FILES, "indec_ipc",
              "INDEC - Indice de Precios al Consumidor Nacional",
              "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31",
              "current")
    descargar("OPEX", INDEC_OLD, OPEX_FILES, "indec_opex",
              "INDEC - Origen Provincial de las Exportaciones (OPEX)",
              "https://sitioanterior.indec.gob.ar/nivel4_default.asp?id_tema_1=3&id_tema_2=2&id_tema_3=79",
              "1993-01_to_2018-12")
    descargar("Censo - Proyecciones provinciales", CENSO_BASE, CENSO_FILES, "indec_poblacion",
              "INDEC / Censo 2022 - Proyecciones poblacionales",
              "https://censo.gob.ar/index.php/proyecciones/",
              "2022-2040")


if __name__ == "__main__":
    main()
