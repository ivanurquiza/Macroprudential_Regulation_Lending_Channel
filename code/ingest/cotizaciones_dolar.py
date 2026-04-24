"""Descarga las cotizaciones diarias del dólar desde argentinadatos.com.

FUENTE SECUNDARIA: argentinadatos.com es un proyecto comunitario open source
(github.com/enzonotario/esjs-dolar-api) que scrapea DolarHoy.com.

Antes de usar en análisis hay que correr el cross-check:
- oficial/mayorista vs BCRA A-3500 (id=5 en data/raw/bcra_api/)
- ratio esperado = 1.00 ± 0.5% en ventana de solapamiento

Output en `data/raw/cotizaciones_dolar/{casa}.json`.
"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
from paths import RAW
from manifest import sha256_of, append_entry, relpath


ROOT = RAW / "cotizaciones_dolar"
BASE = "https://api.argentinadatos.com/v1/cotizaciones/dolares"
UA = "Mozilla/5.0"
METHOD = "https://github.com/enzonotario/esjs-dolar-api"


CASAS = [
    ("oficial",         "Dólar oficial minorista - scrape DolarHoy (origen: BNA)."),
    ("mayorista",       "Dólar mayorista - scrape DolarHoy. Cross-check contra BCRA A-3500 (id=5)."),
    ("blue",            "Dólar blue (informal) - polled. Sin upstream primario."),
    ("bolsa",           "Dólar MEP - computado desde AL30/AL30D. Cobertura desde 2018-10."),
    ("contadoconliqui", "Dólar CCL - computado desde GD30/GD30D. Cobertura desde 2013-01."),
]


def fetch(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    r = subprocess.run(
        ["curl", "-sSL", "--fail", "-A", UA, "--max-time", "60", "-o", str(tmp), url],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        if tmp.exists(): tmp.unlink()
        raise RuntimeError(f"curl falló {url}: {r.stderr.strip()[:200]}")
    tmp.rename(dest)
    return True


def main():
    today = time.strftime("%Y-%m-%d")
    for casa, desc in CASAS:
        url = f"{BASE}/{casa}"
        dest = ROOT / f"{casa}.json"
        try:
            dl = fetch(url, dest)
            append_entry({
                "id": f"cotizaciones_{casa}",
                "source": f"argentinadatos.com - cotizaciones/dolares/{casa}",
                "organism": "argentinadatos.com (community; scraper de DolarHoy.com)",
                "url": url,
                "methodology_url": METHOD,
                "downloaded_at": today,
                "snapshot_date": "historico_completo",
                "path": relpath(dest),
                "sha256": sha256_of(dest),
                "size_bytes": dest.stat().st_size,
                "license": "Datos publicos agregados; scraper MIT",
                "notes": desc + " FUENTE SECUNDARIA: cross-check obligatorio contra BCRA A-3500 antes de usar.",
            })
            print(f"{'DL' if dl else 'SK'}  {dest.name}")
        except Exception as e:
            print(f"ERR {dest.name}: {e}")


if __name__ == "__main__":
    main()
