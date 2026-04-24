# Metodología de construcción de paneles

Este documento fija las decisiones metodológicas y técnicas que rigen la construcción de los paneles largos en `data/interim/`. Cada notebook de construcción cita acá la sección correspondiente. Si una decisión cambia, se modifica este documento y se vuelven a correr los notebooks afectados.

## 1. Propósito de los paneles largos

Son la representación fiel del contenido del dump IEF del BCRA y de los dumps externos (actividad económica, SIPA, etc.), con el mínimo de transformaciones posibles. No incorporan decisiones de investigador sobre qué variables construir, qué categorías agregar o qué casos excluir. Esas decisiones viven en notebooks de análisis posteriores y en los crosswalks de `data/external/crosswalks/`.

La regla operativa es: si una transformación depende de un juicio del investigador, no va en el panel largo. Si es una limpieza necesaria para que los datos sean interpretables (parsear fechas, fijar encoding, validar integridad), va.

## 2. Stack técnico

**Almacenamiento**: Parquet. Preserva tipos, comprime ~10× respecto de CSV, permite lectura por columna sin cargar todo a memoria.

**Motor de consulta**: DuckDB. Lee Parquet directamente sin importar a una base. Sintaxis SQL estándar. Los notebooks de análisis querean los paneles largos con SQL; el resultado puede materializarse como `pandas.DataFrame` cuando haga falta para graficar o exportar.

**Crosswalks y decisiones de investigador**: CSV bajo `data/external/crosswalks/`. Versionados en git. Editables a mano. Joineables vía DuckDB como si fueran tablas más.

**Output a Stata**: `.dta` se genera en el último paso de los notebooks de análisis (no en los de construcción). Con `duckdb.sql("...").df().to_stata(...)` o `pyreadstat.write_dta(...)`.

## 3. Decisiones metodológicas

### 3.1 Tratamiento de fusiones y cambios de control

Cada `CODIGO_ENTIDAD` se trata como una entidad independiente ("bank-as-is"). Cuando un banco absorbe a otro, ambos mantienen su identidad: el absorbido queda con saldo cero o desaparece a partir de la fecha de fusión, el absorbente muestra un salto en sus saldos.

Este es el criterio estándar en la literatura reciente sobre canales de crédito (Khwaja & Mian 2008; Gilje 2019). La identificación en event studies se protege con efectos fijos de banco y con ventanas cortas alrededor del evento relevante.

Adicionalmente se construye en paralelo un panel pro-forma (`panel_balance_mensual_proforma.parquet`) donde las fusiones conocidas están consolidadas retrospectivamente en la entidad absorbente (Chodorow-Reich 2014). Está disponible como ejercicio de robustez. La tabla `dim_entidades.parquet` tiene columnas `id_bcra` (código original) e `id_proforma` (código consolidado post-fusión) para poder alternar entre ambas vistas con un join.

Las fusiones y cambios de denominación se toman de `Info_Hist/Activas/` e `Info_Hist/Bajas/` del IEF más reciente. Los casos relevantes se registran en `data/external/crosswalks/fusiones.csv`.

### 3.2 Cuentas regularizadoras

Las cuentas marcadas "REGULARIZADORA COM A3911" (y variantes) son cuentas-hijas de una cuenta-madre que restan por diseño del plan contable BCRA. Ejemplo: `135194` regulariza `135000` (préstamos ME al sector privado); el saldo neto del capítulo es madre menos regularizadora.

El panel largo deja las regularizadoras como filas normales, sin consolidar. Esto permite analizar las previsiones como variable propia (indicador de calidad de cartera). La consolidación, cuando haga falta, se aplica en el notebook de análisis usando la información de `dim_cuentas.parquet`, que expone las columnas `es_regularizadora: bool` y `cuenta_madre_id`.

### 3.3 Ventana temporal del panel principal

El panel de balance mensual se construye con dos recortes temporales:

- `panel_balance_mensual.parquet`: desde 2020-01, en moneda homogénea (NIC 29 / Com. "A" 6651).
- `panel_balance_mensual_pre2020.parquet`: desde 1994-11 hasta 2019-12, en moneda corriente.

El corte en 2020-01 se debe al cambio obligatorio a reporte en moneda homogénea. Los saldos pre- y post-2020 no son comparables directamente sin un ajuste no trivial (involucra NIIF 9 para valuación de instrumentos financieros, además del ajuste inflacionario). El BCRA mismo presenta sus series con dos pestañas separadas.

La ventana de interés para el evento del blanqueo 2024 (ventana ±12 meses centrada en ago-2024) queda completamente contenida en el panel principal post-2020. El panel pre-2020 se preserva para ejercicios de robustez que usen el blanqueo 2016-17 (Ley 27.260) como contrafactual descriptivo.

### 3.4 Zero-filling

El panel largo no contiene filas con saldo cero. Si una cuenta no aparece para una entidad en un mes, es porque `balhist.txt` no la reporta. La interpretación de saldo cero vs. ausencia se hace en el notebook de análisis, típicamente al agregar a capítulo o categoría.

Esta decisión es de performance: zero-fill a nivel cuenta-hoja expandiría el panel de ~9 millones a ~200 millones de filas, con el 95% de los nuevos registros siendo ceros.

### 3.5 Agrupamientos institucionales

El archivo `balhist.txt` incluye ~20 filas cuyo código empieza con `AA` (`AA121`, `AA123`, etc.). Son sumas pre-calculadas por el BCRA (sistema financiero total, bancos privados, top-10, etc.), no entidades individuales. Listado completo en `Grupos.txt` de cada dump.

Estas filas se separan del panel principal y se almacenan en `panel_balance_agregados.parquet`. El panel principal solo contiene entidades individuales. Los agregados sirven para validación (chequear que la suma de las entidades por grupo da el agregado reportado) y para análisis a nivel sistema.

### 3.6 Frecuencia nativa de cada panel

Cada panel largo mantiene la frecuencia en la que el BCRA reporta los datos:

- `panel_balance_mensual`: mensual.
- `panel_indicadores`: trimestral (los indicadores CAMELS).
- `panel_esd`: trimestral (estado de situación de deudores).
- `panel_estructura`: 5 fechas irregulares por dump (empleados, clientes, cuentas).
- `panel_distribgeo`: trimestral (préstamos y depósitos por provincia).
- `panel_sucursales_provincia`: snapshot a la fecha de cada dump.

Unir frecuencias (por ejemplo, pegar valores trimestrales al panel mensual con forward-fill) es decisión de análisis, no de construcción. Ocurre en los notebooks de análisis.

### 3.6.bis Convención de signos del balance BCRA

(Esta no era una decisión de investigador sino un hallazgo durante la validación; queda documentada acá porque afecta cualquier análisis sobre `panel_balance_mensual`.)

El BCRA reporta los saldos en `bal_hist.txt` siguiendo **convención contable**:
- **Activos**: saldo positivo (efectivo, préstamos, títulos).
- **Pasivos**: saldo **negativo** (depósitos, obligaciones).
- **Patrimonio neto**: saldo negativo (es de naturaleza acreedora).

Ejemplo: en agosto 2024 las cuentas CERA (que son depósitos, capítulo 31x del pasivo) tienen saldos negativos de ~$540 miles de millones de pesos. La magnitud económica es el `abs()` de esa cifra; el signo es solo convención débito-crédito.

**Implicancia operativa**: para analizar saldos económicos de pasivos hay que tomar `abs(saldo)` o multiplicar por -1 explícitamente. En `panel_balance_agregados` (que viene de `balres/` no de `bal_hist/`) la convención **puede ser distinta** porque ahí los saldos están agrupados a nivel capítulo — verificar caso por caso.

Cuando se construyan tablas de análisis, conviene crear una variable `saldo_economico = abs(saldo)` o aplicar el signo por categoría según el lado del balance (activo/pasivo/PN) usando `dim_cuentas`.

### 3.7 Conversión a dólares

Los saldos de cuentas en moneda extranjera se reportan en pesos, al tipo de cambio contable BCRA A-3500 de fin de mes. El panel largo preserva los saldos en pesos nominales tal como salen del `balhist.txt`.

La conversión a USD, cuando se necesita, ocurre en los notebooks de análisis, joineando con la serie A-3500 (`data/raw/bcra_api/005_tc_mayorista_a3500.json`). Dos razones: (a) si se guarda la conversión en el panel largo queda atada al TC usado en el momento y cualquier revisión del TC obliga a regenerar todo; (b) hay más de un TC posible (mayorista, minorista, MEP, CCL) y elegir uno es decisión de investigador.

### 3.8 Plan de cuentas con altas y bajas

Las cuentas del plan contable BCRA se dan de alta y de baja a lo largo del tiempo. Algunas cuentas de un período son sustituidas por otras con código distinto pero significado económico equivalente (por ejemplo, LELIQ `121058` reemplazada por LEFI `121091` en 2023).

La tabla `dim_cuentas.parquet` expone la columna `fecha_baja` tal como viene del plan de cuentas del BCRA, para permitir auditar la vida de cada cuenta. El panel largo contiene todas las cuentas, vigentes y discontinuadas.

El mapeo de cuentas a categorías económicas estables (por ejemplo, "deuda BCRA en ARS" abarcando LELIQ y LEFI) se define en `data/external/crosswalks/cuenta_categoria.csv`. Ese crosswalk se construye en una fase posterior, cuando se arman las tablas de análisis, y depende de la pregunta específica que se quiera responder.

## 4. Estructura de archivos

```
data/
├── raw/                                    # datos tal como salen de la fuente, no se editan
│   ├── bcra_ief/                           # dumps IEF mensuales
│   ├── bcra_sistema/                       # series agregadas BCRA
│   ├── bcra_prestamos_actividad/
│   ├── bcra_api/                           # series monetarias vía API v4
│   ├── indec_ipc/ indec_opex/ indec_poblacion/
│   ├── sipa_oede/
│   └── cotizaciones_dolar/
│
├── interim/                                # paneles largos, output de los notebooks 01-09
│   ├── paneles_largos/
│   │   ├── panel_balance_mensual.parquet
│   │   ├── panel_balance_mensual_pre2020.parquet
│   │   ├── panel_balance_agregados.parquet
│   │   ├── panel_balance_mensual_proforma.parquet
│   │   ├── panel_distribgeo.parquet
│   │   ├── panel_indicadores.parquet
│   │   ├── panel_esd.parquet
│   │   ├── panel_estructura.parquet
│   │   ├── panel_sucursales_provincia.parquet
│   │   └── panel_actividad.parquet
│   └── dimensiones/
│       ├── dim_entidades.parquet
│       ├── dim_cuentas.parquet
│       ├── dim_grupos.parquet
│       └── dim_provincias.parquet
│
├── external/                               # decisiones de investigador, editables a mano
│   └── crosswalks/
│       ├── cuenta_categoria.csv            # cuenta BCRA → categoría económica estable
│       ├── fusiones.csv                    # fusiones y cambios de control
│       └── provincias_iso.csv
│
├── processed/                              # tablas finales para Stata (.dta)
│
└── manifest/
    ├── sources.yaml
    └── fuentes.md
```

## 5. Convenciones

**Nombres de columnas**: snake_case en español cuando el término es específico del BCRA (`codigo_entidad`, `codigo_cuenta`, `yyyymm`, `saldo`, `denominacion`, `fecha_baja`). En inglés cuando la categoría es universal (`date`, `value`).

**Tipos**: fechas como `DATE` (no timestamps) cuando la frecuencia es mensual o menor; códigos como `VARCHAR` (no integer) para preservar ceros a la izquierda; saldos como `DOUBLE` (no decimal) para interoperabilidad.

**Identificador temporal**: se incluye siempre `yyyymm` como entero (`202408`) y `fecha` como fecha (`2024-08-31`, último día del mes). Ambos son redundantes pero uno u otro puede ser más cómodo según el contexto.

**Validaciones**: cada notebook de construcción cierra con un bloque de `assert` que verifica número de filas esperado, rango de fechas, completitud de columnas clave. Si un dump futuro rompe estas validaciones, el pipeline falla limpio.

**Paths**: se definen al inicio de cada notebook como constantes (`REPO_ROOT`, `RAW_DIR`, `INTERIM_DIR`). No se usan rutas relativas que dependan del directorio desde el que se corre el notebook.

## 6. Referencias

- Chodorow-Reich, G. (2014). "The employment effects of credit market disruptions: firm-level evidence from the 2008-09 financial crisis". *QJE*.
- Gilje, E. P. (2019). "Does local access to finance matter? Evidence from US oil and natural gas shale booms". *Management Science*.
- Khwaja, A. I., & Mian, A. (2008). "Tracing the impact of bank liquidity shocks: evidence from an emerging market". *AER*.
- Greenstone, M., Mas, A., & Nguyen, H.-L. (2020). "Do credit market shocks affect the real economy? Quasi-experimental evidence from the Great Recession and 'normal' economic times". *AEJ: Applied*.
- BCRA, "Ayuda IEF" (diccionario del dump IEF).
- BCRA, Comunicación "A" 6651 (adopción NIC 29 por entidades financieras).
