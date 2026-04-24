"""Descarga las series trimestrales de Préstamos por actividad económica del BCRA.

Tres variantes por año:
- act{YYYY}.xls       — total sistema × CIIU
- act{YYYY}grup.xls   — por grupo de entidad × CIIU
- loc{YYYY}.xls       — por provincia/localidad

Output en `data/raw/bcra_prestamos_actividad/`.
Configurar la ventana con YEARS al inicio del script.
"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
from paths import RAW
from manifest import sha256_of, append_entry, relpath


YEARS = range(2015, 2026)
ROOT = RAW / "bcra_prestamos_actividad"
BASE = "https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas"
UA = "Mozilla/5.0"


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


def main():
    today = time.strftime("%Y-%m-%d")
    n_dl = n_sk = 0
    for y in YEARS:
        for prefix, kind, desc_template in [
            ("act", "actividad",
             "Préstamos por actividad económica (CIIU) - total sistema - {y} (trimestral)."),
            ("actgrup", "actividad_grupo_entidad",
             "Préstamos por actividad económica × grupo de entidad - {y} (trimestral)."),
            ("loc", "localidad",
             "Préstamos por provincia/localidad - total sistema - {y} (trimestral)."),
        ]:
            # naming en BCRA: act{YYYY}.xls, act{YYYY}grup.xls, loc{YYYY}.xls
            if prefix == "actgrup":
                fname = f"act{y}grup.xls"
            else:
                fname = f"{prefix}{y}.xls"
            url = f"{BASE}/{fname}"
            dest = ROOT / fname
            try:
                dl = fetch(url, dest)
                n_dl += dl; n_sk += not dl
                append_entry({
                    "id": f"bcra_prestamos_{kind}_{y}",
                    "source": f"BCRA - Préstamos por actividad económica ({fname})",
                    "organism": "Banco Central de la Republica Argentina (BCRA)",
                    "url": url,
                    "methodology_url": "https://www.bcra.gob.ar/prestamos-y-otros-activos-de-las-entidades-financieras/",
                    "downloaded_at": today,
                    "snapshot_date": f"{y}",
                    "path": relpath(dest),
                    "sha256": sha256_of(dest),
                    "size_bytes": dest.stat().st_size,
                    "license": "Dominio publico (BCRA)",
                    "notes": desc_template.format(y=y),
                })
                print(f"{'DL' if dl else 'SK'}  {fname}")
            except Exception as e:
                print(f"ERR {fname}: {e}")
    print(f"Done. downloaded={n_dl} skipped={n_sk}")


if __name__ == "__main__":
    main()
