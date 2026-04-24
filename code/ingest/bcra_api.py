"""Descarga series monetarias diarias de la API v4 del BCRA.

Endpoint: api.bcra.gob.ar/estadisticas/v4.0/Monetarias/{idVariable}
Catálogo completo en api.bcra.gob.ar/estadisticas/v4.0/Monetarias

Output como JSON crudo en `data/raw/bcra_api/{idVar:03d}_{short_name}.json`.
"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
from paths import RAW
from manifest import sha256_of, append_entry, relpath


ROOT = RAW / "bcra_api"
BASE = "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias"
DESDE = "2015-01-01"  # ventana en match con los dumps IEF
LIMIT = 3000          # cubre ~11 años de daily

# (id, short_name, descripcion, primer_dato_disponible)
SERIES = [
    (5,  "tc_mayorista_a3500",       "Tipo de cambio mayorista de referencia (Com. A-3500)", "2002-03-04"),
    (4,  "tc_minorista_vendedor",    "Tipo de cambio minorista - promedio vendedor",          "2010-06-01"),
    (1,  "reservas_internacionales", "Reservas internacionales del BCRA",                     "1996-01-03"),
    (15, "base_monetaria",           "Base monetaria",                                        "1996-01-02"),
    (7,  "badlar_privados",          "Tasa BADLAR bancos privados",                           "1996-01-02"),
    (30, "cer",                      "Coeficiente de Estabilización de Referencia",           "2002-02-02"),
    (31, "uva",                      "Unidad de Valor Adquisitivo",                           "2016-03-31"),
    (32, "uvi",                      "Unidad de Vivienda",                                    "2016-03-31"),
    (81, "var_reservas_efectivo_min","Variación de reservas internacionales por efectivo mínimo", "2003-01-02"),
]


def fetch(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    r = subprocess.run(
        ["curl", "-sSL", "--fail", "--max-time", "120", "-o", str(tmp), url],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        if tmp.exists(): tmp.unlink()
        raise RuntimeError(f"curl falló {url}: {r.stderr.strip()[:200]}")
    tmp.rename(dest)
    return True


def main():
    today = time.strftime("%Y-%m-%d")
    hasta = today
    for varid, short, desc, primer in SERIES:
        desde = max(DESDE, primer)
        url = f"{BASE}/{varid}?desde={desde}&hasta={hasta}&limit={LIMIT}"
        dest = ROOT / f"{varid:03d}_{short}.json"
        try:
            dl = fetch(url, dest)
            append_entry({
                "id": f"bcra_api_monetarias_{varid:03d}",
                "source": f"BCRA API v4 - Monetarias id={varid}: {desc}",
                "organism": "Banco Central de la Republica Argentina (BCRA)",
                "url": url,
                "methodology_url": "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias",
                "downloaded_at": today,
                "snapshot_date": f"{desde}_to_{hasta}",
                "path": relpath(dest),
                "sha256": sha256_of(dest),
                "size_bytes": dest.stat().st_size,
                "license": "Dominio publico (BCRA)",
                "notes": f"Serie diaria {desc}. Endpoint oficial JSON. Cobertura desde {primer}.",
            })
            print(f"{'DL' if dl else 'SK'}  {dest.name}")
        except Exception as e:
            print(f"ERR {dest.name}: {e}")


if __name__ == "__main__":
    main()
