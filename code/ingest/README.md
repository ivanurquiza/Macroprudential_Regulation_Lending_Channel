# Scripts de ingesta

Cada script baja una fuente a `data/raw/` (o la normativa a `docs/Regulacion_BCRA/`) y registra cada archivo en `data/manifest/sources.yaml` con SHA-256, URL original y fecha de descarga.

Todos son idempotentes: corren sin re-descargar lo ya presente.

| Script | Output | Fuente |
|---|---|---|
| `bcra_ief.py` | `data/raw/bcra_ief/` | BCRA - Información de Entidades Financieras (dumps mensuales 7z) |
| `bcra_sistema.py` | `data/raw/bcra_sistema/` | BCRA - Anexo Informe sobre Bancos, Boletín Estadístico, series diarias |
| `bcra_prestamos_actividad.py` | `data/raw/bcra_prestamos_actividad/` | BCRA - Préstamos por actividad económica (act, grup, loc) |
| `bcra_api.py` | `data/raw/bcra_api/` | BCRA API v4 (monetarias: A-3500, CER, UVA, reservas, base, BADLAR) |
| `indec.py` | `data/raw/indec_ipc/`, `indec_opex/`, `indec_poblacion/` | INDEC - IPC, OPEX histórico, proyecciones Censo 2022 |
| `sipa_oede.py` | `data/raw/sipa_oede/` | Ministerio de Capital Humano - OEDE - SIPA |
| `cotizaciones_dolar.py` | `data/raw/cotizaciones_dolar/` | argentinadatos.com (scraper de DolarHoy) - secundaria |
| `cera_regulation.py` | `docs/Regulacion_BCRA/cera_ley_27743/` | Normativa Ley 27.743: ley, decretos, RG AFIP, Res. Mecon, Com. A BCRA |

## Cómo correr

Desde la raíz del repo:

```bash
python code/ingest/bcra_ief.py
python code/ingest/bcra_sistema.py
# etc.
```

Los scripts resuelven la raíz del repo automáticamente; no importa el cwd desde el que se ejecuten.

## Fuente de verdad: manifest

`data/manifest/sources.yaml` es el registro canónico de qué archivos vinieron de dónde, cuándo y con qué hash. Cada script appendea entradas. Ver también `data/manifest/fuentes.md` para el documento narrativo de trazabilidad.

## Observación sobre descargas incrementales

Algunos archivos son snapshots vivos (se actualizan en el servidor): el Anexo del Informe sobre Bancos, el IPC, las cotizaciones del dólar. Correr de nuevo el script **no re-descarga** el archivo si ya existe localmente con tamaño > 0. Para refrescar, borrar el archivo local antes de correr.
