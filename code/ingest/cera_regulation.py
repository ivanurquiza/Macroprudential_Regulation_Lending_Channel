"""Descarga la normativa completa del régimen CERA (Ley 27.743).

Cuatro capas:
- Ley 27.743 + decretos reglamentarios (PEN) desde Boletín Oficial.
- Resoluciones generales AFIP que operan el régimen.
- Resoluciones del Ministerio de Economía que definen destinos de inversión.
- Comunicaciones "A" del BCRA específicas del régimen.

Output en `docs/Regulacion_BCRA/cera_ley_27743/`.
Ver también `docs/notas/cera_regimen.md` para la síntesis operativa.
"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
from paths import DOCS
from manifest import sha256_of, append_entry, relpath


ROOT = DOCS / "Regulacion_BCRA/cera_ley_27743"
UA = "Mozilla/5.0"
BCRA = "https://www.bcra.gob.ar/archivos/Pdfs/comytexord"
BO = "https://www.boletinoficial.gob.ar/pdf/aviso/primera"


# (url, destino_relativo_a_ROOT, id, snapshot_date, source_label, organism, notes)
LEYES_DECRETOS = [
    (f"{BO}/310191/20240708",
     "leyes_decretos/ley_27743_2024-07-08.pdf", "reg_ley_27743", "2024-07-08",
     "Boletin Oficial - Ley 27.743 (Medidas Fiscales Paliativas y Relevantes)",
     "Congreso de la Nacion / PEN",
     "Ley 27.743. Título II crea el Régimen de Regularización de Activos."),
    (f"{BO}/310371/20240712",
     "leyes_decretos/decreto_608_2024-07-12.pdf", "reg_decreto_608_2024", "2024-07-12",
     "Boletin Oficial - Decreto 608/2024", "Poder Ejecutivo Nacional (PEN)",
     "Decreto 608/2024 - Reglamentación de la Ley 27.743 Título II. Define las tres Etapas y condiciones de la CERA."),
    (f"{BO}/313080/20240830",
     "leyes_decretos/decreto_773_2024-08-30.pdf", "reg_decreto_773_2024", "2024-08-30",
     "Boletin Oficial - Decreto 773/2024", "Poder Ejecutivo Nacional (PEN)",
     "Decreto 773/2024 - Modifica Decreto 608/2024. Adecuaciones a las Etapas."),
    (f"{BO}/314801/20240930",
     "leyes_decretos/decreto_864_2024-09-30.pdf", "reg_decreto_864_2024", "2024-09-30",
     "Boletin Oficial - Decreto 864/2024", "Poder Ejecutivo Nacional (PEN)",
     "Decreto 864/2024 - Prórroga Etapa 1 hasta 31-oct-2024."),
    (f"{BO}/316055/20241025",
     "leyes_decretos/decreto_953_2024-10-25.pdf", "reg_decreto_953_2024", "2024-10-25",
     "Boletin Oficial - Decreto 953/2024", "Poder Ejecutivo Nacional (PEN)",
     "Decreto 953/2024 - Disuelve AFIP y crea ARCA. Afecta referencias operativas del régimen."),
    (f"{BO}/310619/20240717",
     "leyes_decretos/rg_afip_5528_2024-07-17.pdf", "reg_rg_afip_5528_2024", "2024-07-17",
     "Boletin Oficial - RG AFIP 5528/2024", "AFIP (hoy ARCA)",
     "RG AFIP 5528/2024 - Reglamenta el Régimen de Regularización de Activos."),
    (f"{BO}/311454/20240730",
     "leyes_decretos/rg_afip_5536_2024-07-30.pdf", "reg_rg_afip_5536_2024", "2024-07-30",
     "Boletin Oficial - RG AFIP 5536/2024", "AFIP (hoy ARCA)",
     "RG AFIP 5536/2024 - Modifica RG 5528/2024. Anexo con documentación para acreditar titularidad."),
    (f"{BO}/310776/20240719",
     "leyes_decretos/res_mecon_590_2024-07-19.pdf", "reg_res_mecon_590_2024", "2024-07-19",
     "Boletin Oficial - Res. 590/2024 Ministerio de Economia",
     "Ministerio de Economia de la Nacion",
     "Res. 590/2024 Mecon - Enumera los destinos de inversión permitidos para fondos CERA."),
    (f"{BO}/312506/20240820",
     "leyes_decretos/res_mecon_759_2024-08-20.pdf", "reg_res_mecon_759_2024", "2024-08-20",
     "Boletin Oficial - Res. 759/2024 Ministerio de Economia",
     "Ministerio de Economia de la Nacion",
     "Res. 759/2024 Mecon - Complementa/ajusta Res. 590/2024 respecto a destinos."),
]

BCRA_COMS = [
    ("8062", "2024-07-15", "creacion",
     "Com. A 8062 - OPASI 2-721. Crea la CERA. Reglamentación original en TO Depósitos §3.16."),
    ("8071", "2024-07-23", "alta_cuentas_plan_contable",
     "Com. A 8071 - CONAU 1-1638. Da de alta las 4 cuentas CERA (311793, 312183, 315794, 316147) y la 325195 en el Plan de Cuentas."),
    ("8090", "2024-08-15", "adecuacion_1",
     "Com. A 8090 - OPASI 2-723. Admite transferencias a otras CERAs o a cuentas monitoreadas por AFIP para destinos permitidos."),
    ("8106", "2024-09-19", "adecuacion_2",
     "Com. A 8106 - OPASI 2-725. Habilita tarjeta de débito y medios electrónicos de pago vinculados a la CERA."),
    ("8110", "2024-09-30", "etapa1_limite_100k",
     "Com. A 8110 - OPASI 2-726. Plazos de indisponibilidad Etapa 1; umbral USD 100.000 y operaciones onerosas documentadas."),
    ("8123", "2024-11-01", "prorroga_etapa1",
     "Com. A 8123 - OPASI 2-727. Prórroga en línea con extensión del régimen."),
    ("8140", "2024-12-02", "arca_actualizacion_regimenes",
     "Com. A 8140 - CONAU 1-1650. Actualización de TOs por disolución AFIP y creación ARCA (Decreto 953/24)."),
    ("8343", "2025-10-14", "operatoria_pagos_DPA_DZV",
     "Com. A 8343 - SINAP 1-237. Incorpora operatorias DPA (transferencias de terceros con CERA) y DZV (devoluciones) al MEP."),
]


def fetch(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 1000:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    r = subprocess.run(
        ["curl", "-sSL", "--fail", "-A", UA, "--max-time", "90", "-o", str(tmp), url],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        if tmp.exists(): tmp.unlink()
        raise RuntimeError(f"curl falló {url}: {r.stderr.strip()[:200]}")
    tmp.rename(dest)
    return True


def main():
    today = time.strftime("%Y-%m-%d")
    print("=== Leyes, decretos y resoluciones ===")
    for url, rel_dest, eid, snap, src, org, notes in LEYES_DECRETOS:
        dest = ROOT / rel_dest
        try:
            dl = fetch(url, dest)
            append_entry({
                "id": eid, "source": src, "organism": org, "url": url,
                "methodology_url": "NA",
                "downloaded_at": today, "snapshot_date": snap,
                "path": relpath(dest), "sha256": sha256_of(dest),
                "size_bytes": dest.stat().st_size,
                "license": "Dominio publico (Boletin Oficial)",
                "notes": notes,
            })
            print(f"{'DL' if dl else 'SK'}  {rel_dest}")
        except Exception as e:
            print(f"ERR {rel_dest}: {e}")

    print("=== BCRA Comunicaciones A ===")
    for num, fecha, suffix, notes in BCRA_COMS:
        url = f"{BCRA}/A{num}.pdf"
        dest = ROOT / f"bcra_comunicaciones/A{num}_{fecha}_{suffix}.pdf"
        try:
            dl = fetch(url, dest)
            append_entry({
                "id": f"reg_bcra_com_a{num}",
                "source": f"BCRA Comunicacion A {num}",
                "organism": "Banco Central de la Republica Argentina (BCRA)",
                "url": url,
                "methodology_url": "https://www.bcra.gob.ar/SistemasFinancierosYdePagos/Normativa.asp",
                "downloaded_at": today, "snapshot_date": fecha,
                "path": relpath(dest), "sha256": sha256_of(dest),
                "size_bytes": dest.stat().st_size,
                "license": "Dominio publico (BCRA)",
                "notes": notes,
            })
            print(f"{'DL' if dl else 'SK'}  A{num}_{fecha}_{suffix}.pdf")
        except Exception as e:
            print(f"ERR A{num}: {e}")


if __name__ == "__main__":
    main()
