# Macroprudential Regulation and the Lending Channel

Research project on macroprudential segmentation and the transmission of dollar funding shocks in Argentina.

## Repository layout

```
.
├── data/
│   ├── raw/           # original downloads (not tracked)
│   ├── external/      # manual crosswalks and dictionaries (tracked)
│   ├── interim/       # intermediate outputs (not tracked)
│   ├── processed/     # clean panels ready for Stata (not tracked)
│   └── manifest/
│       └── sources.yaml   # provenance of every external source
├── code/
│   ├── python/        # Jupyter notebooks + utils for ETL and panel construction
│   └── stata/         # .do files, one per regression
├── output/
│   ├── tables/        # .tex tables (esttab)
│   └── figures/
└── docs/
    ├── Papers/
    ├── Regulacion_BCRA/
    └── notas/         # methodological notes, data descriptions
```

## Workflow

1. Raw data is downloaded into `data/raw/<source>/<snapshot>/` and logged in `data/manifest/sources.yaml`.
2. Python notebooks in `code/python/` read from `data/raw/`, apply crosswalks from `data/external/`, and write clean panels to `data/processed/` as `.dta`.
3. Stata `.do` files in `code/stata/` consume only `data/processed/*.dta` and export tables to `output/tables/` via `esttab`.
4. LaTeX tables are imported directly into the paper.

## Reproducibility

- Python environment: see `requirements.txt`.
- External data sources are listed in `data/manifest/sources.yaml` with URL, download date, snapshot date, and SHA-256.
