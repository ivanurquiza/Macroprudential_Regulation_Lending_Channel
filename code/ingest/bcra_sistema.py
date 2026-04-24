"""Descarga las series del sistema financiero del BCRA (agregadas, no por entidad).

Tres conjuntos:
- Anexo del Informe sobre Bancos (xlsx con indicadores por grupo homogéneo).
- Series históricas del Boletín Estadístico (panhis, balsishis, liqhis, etc.).
- Series diarias relevantes para event study (saldos diarios de préstamos, depósitos, tasas).

Output en `data/raw/bcra_sistema/{subdir}/{archivo}`.
Idempotente: saltea archivos ya bajados con tamaño > 0.
"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
from paths import RAW
from manifest import sha256_of, append_entry, relpath


ROOT = RAW / "bcra_sistema"
BASE = "https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas"
UA = "Mozilla/5.0"


FILES = [
    # Informe sobre Bancos (anexo único)
    ("informe_sobre_bancos", "informes/InfBanc_Anexo.xlsx", "InfBanc_Anexo.xlsx",
     "bcra_informe_bancos_anexo",
     "Indicadores del sistema por grupo homogéneo: RPC, Tier1, liquidez, ROA/ROE, irregularidad. Cobertura 2002+."),
]

BOLETIN = [
    ("panhis",      "Panorama monetario y financiero histórico."),
    ("balsishis",   "Balance del sistema financiero histórico."),
    ("balbanhis",   "Balance bancos histórico."),
    ("balenthis",   "Balance total entidades (consolidado) histórico."),
    ("baldethis",   "Balance detallado histórico."),
    ("balbcrhis",   "Balance BCRA histórico."),
    ("liqhis",      "Indicadores de liquidez del sistema histórico."),
    ("pashis",      "Pasivos del sistema histórico."),
    ("calhis",      "Calidad de cartera histórica."),
    ("perser_priv", "Préstamos y depósitos del sector privado."),
    ("perser_pub",  "Préstamos y depósitos del sector público."),
    ("perser_dest", "Préstamos por destino (familias/empresas)."),
    ("titpubser",   "Tenencia de títulos públicos por entidad (snapshot)."),
    ("tasser",      "Tasas de interés - series mensuales."),
    ("preser_mon",  "Préstamos al sector privado no financiero por moneda."),
    ("preser_pla",  "Préstamos por plazo."),
    ("preser_tas",  "Préstamos - tasas por línea."),
]

DIARIAS = [
    ("diar_fin", "Préstamos - saldos diarios."),
    ("diar_dep", "Depósitos - saldos diarios."),
    ("diar_tim", "Tasas de interés diarias."),
]

for name, desc in BOLETIN:
    FILES.append(("boletin_estadistico", f"{name}.xls", f"{name}.xls",
                  f"bcra_boletin_{name}", desc))

for name, desc in DIARIAS:
    FILES.append(("series_diarias", f"{name}.xls", f"{name}.xls",
                  f"bcra_diario_{name}", desc))


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
    for subdir, remote, localname, sid, desc in FILES:
        url = f"{BASE}/{remote}"
        dest = ROOT / subdir / localname
        try:
            dl = fetch(url, dest)
            n_dl += dl; n_sk += not dl
            append_entry({
                "id": sid,
                "source": "BCRA - Estadisticas del Sistema Financiero (sistema/grupo, no por entidad)",
                "organism": "Banco Central de la Republica Argentina (BCRA)",
                "url": url,
                "methodology_url": "https://www.bcra.gob.ar/publicaciones-estadisticas/",
                "downloaded_at": today,
                "snapshot_date": "current",
                "path": relpath(dest),
                "sha256": sha256_of(dest),
                "size_bytes": dest.stat().st_size,
                "license": "Dominio publico (BCRA)",
                "notes": desc,
            })
            print(f"{'DL' if dl else 'SK'}  {subdir}/{localname}")
        except Exception as e:
            print(f"ERR {subdir}/{localname}: {e}")
    print(f"Done. downloaded={n_dl} skipped={n_sk}")


if __name__ == "__main__":
    main()
