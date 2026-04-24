"""Descarga las series provinciales de empleo y remuneraciones del SIPA vía OEDE.

OEDE = Observatorio de Empleo y Dinámica Empresarial, Ministerio de Capital Humano.
Los archivos se sirven desde argentina.gob.ar/sites/default/files/.

Output en `data/raw/sipa_oede/`.
"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
from paths import RAW
from manifest import sha256_of, append_entry, relpath


ROOT = RAW / "sipa_oede"
BASE = "https://www.argentina.gob.ar/sites/default/files"
UA = "Mozilla/5.0"
METHOD = "https://www.argentina.gob.ar/trabajo/estadisticas/oede-estadisticas-provinciales"


FILES = [
    ("provinciales_serie_empleo_trimestral_2dig_5.xlsx",
     "Empleo asalariado registrado SIPA - provincia × CIIU 2 dígitos - trimestral desde 1T1996."),
    ("provinciales_serie_empleo_trimestral_4dig_6.xlsx",
     "Empleo asalariado registrado SIPA - provincia × CIIU 4 dígitos - trimestral."),
    ("provinciales_serie_empleo_anual_2.xlsx",
     "Empleo asalariado registrado SIPA - provincia - anual."),
    ("provinciales_serie_remuneraciones_mensual_2dig_7.xlsx",
     "Remuneraciones promedio SIPA - provincia × CIIU 2 dígitos - mensual."),
    ("provinciales_serie_remuneraciones_anual_2.xlsx",
     "Remuneraciones promedio SIPA - provincia - anual."),
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


def main():
    today = time.strftime("%Y-%m-%d")
    for fname, desc in FILES:
        url = f"{BASE}/{fname}"
        dest = ROOT / fname
        try:
            dl = fetch(url, dest)
            append_entry({
                "id": f"sipa_oede_{fname.split('.')[0]}",
                "source": f"SIPA via OEDE ({fname})",
                "organism": "Ministerio de Capital Humano - Observatorio de Empleo y Dinamica Empresarial (OEDE)",
                "url": url,
                "methodology_url": METHOD,
                "downloaded_at": today,
                "snapshot_date": "current",
                "path": relpath(dest),
                "sha256": sha256_of(dest),
                "size_bytes": dest.stat().st_size,
                "license": "Dominio publico (Ministerio de Capital Humano)",
                "notes": desc,
            })
            print(f"{'DL' if dl else 'SK'}  {fname}")
        except Exception as e:
            print(f"ERR {fname}: {e}")


if __name__ == "__main__":
    main()
