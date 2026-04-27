# Crosswalks: decisiones de investigador

Documenta el contenido y la lógica detrás de los archivos de `data/external/crosswalks/`. Estos archivos son las **decisiones del investigador** para pasar de los paneles largos (raw del BCRA) a las tablas de análisis. Si una de estas decisiones cambia, hay que actualizar el CSV correspondiente y volver a correr los notebooks de `code/analisis/` que dependan de ella.

## 1. `cuenta_categoria.csv` — códigos BCRA → categorías económicas

### Por qué existe

El plan de cuentas BCRA tiene 5,519 cuentas. Las categorías económicas que aparecen en una regresión típica son ~20 ("crédito USD al sector privado", "depósitos CERA", etc.). Hay que mapear el primero al segundo.

### Aclaración crítica sobre la fuente del mapeo

**El BCRA no publica un mapeo formal entre el plan de cuentas (`cuentas.txt`) y los destinos del régimen de Aplicación de Recursos en ME ni con cualquier otro régimen regulatorio.** Los textos ordenados (Política de Crédito, PGNME, Efectivo Mínimo) usan **lenguaje económico** ("prefinanciación de exportaciones", "Tesoro en moneda extranjera", "depósitos a la vista en ME") sin referirse a códigos del plan de cuentas. El Régimen Informativo Contable Mensual de Efectivo Mínimo y Aplicación de Recursos (Com. A 8420, sec. 6.3) tiene su **propio sistema de "partidas"** (100000, 750000, 903000, etc.) que **no son** los códigos del plan de cuentas (135799, 115015, etc.). El balance resumido `balres` consolida pesos y ME, sin permitir desagregado por moneda × destino.

Como consecuencia, el mapeo en este crosswalk se construye sobre **dos tipos de fuente**:

- **`denominacion_explicita`**: la denominación literal de la cuenta en `cuentas.txt` replica casi textualmente el lenguaje del TO regulatorio. Caso típico: la cuenta `135799` se llama "PR.PREFINANC.Y FINANC.EXPORT.", y el art. 2.1.1 del TO Política de Crédito habla de "prefinanciación y financiación de exportaciones". El mapeo es directo aunque inferencial.
- **`inferencia_capitulo`** o **`inferencia_subcuenta`**: el mapeo se infiere por la estructura jerárquica del plan, sin denominación literal coincidente. Ejemplo: el capítulo 115 entero como "efectivo y depósitos en ME" (pero el BCRA no dice formalmente que `115%` corresponde al "canal de encaje" del régimen).

La columna `fuente_mapeo` del CSV indica para cada par cuál es el caso. Esto es importante para auditoría: las inferencias son razonables pero deberían poder cuestionarse.

### Estructura del plan de cuentas relevante

El activo en moneda extranjera (residentes en el país) se organiza en cuatro capítulos principales:

| Capítulo | Concepto |
|---|---|
| `115` | Efectivo y depósitos en bancos en ME |
| `125` | Títulos públicos y privados en ME |
| `135` | Préstamos en ME a residentes en el país |
| `145` / `155` / `175` | Otros créditos por intermediación financiera, leasing, créditos diversos en ME |

Y separadamente, los préstamos en ME a residentes del exterior viven en el capítulo `136` (no en `135`).

Dentro del capítulo `135`, las sub-cuentas están organizadas por **sector del prestatario**:

| Sub-cuenta | Sector |
|---|---|
| `1351xx` | Sector Público No Financiero (SP) |
| `1352xx` | Intereses SP |
| `1353xx` | Previsiones SP (regularizadoras) |
| `1354xx` | Sector Financiero (interbancario doméstico ME) |
| `1355xx` | Intereses SF |
| `1356xx` | Previsiones SF |
| `1357xx` | Sector Privado No Financiero (SPNF) |
| `1358xx` | Intereses SPNF |
| `1359xx` | Previsiones SPNF |

**Corrección de versión anterior del crosswalk**: en versiones previas, este documento mapeaba `interbancario_me` al capítulo `136`. Eso era incorrecto. El interbancario doméstico en ME vive en `1354xx`-`1356xx`. El capítulo `136` corresponde a préstamos crossborder (a residentes del exterior), un destino distinto del menú regulatorio (sec. 2.1.16 y 2.1.17 del TO Política de Crédito).

### Categorías principales (v2)

#### Lado pasivo — el shock CERA

| Categoría | Cuentas | Fuente del mapeo |
|---|---|---|
| `cera_total` | 311793 + 312183 + 315794 + 316147 | denominación explícita; coincide literalmente con Com. A 8071 |
| `cera_ars` | 311793 + 312183 | denominación explícita |
| `cera_me` | 315794 + 316147 | denominación explícita (★ 315794 captura 96.6% del peak) |
| `deposito_me_spnf_total` | Capítulo 315 entero | inferencia capítulo (incluye CERA + cuentas exportadores + depósitos USD regulares) |
| `deposito_me_spnf_exterior` | Capítulo 316 entero | inferencia capítulo |

#### Lado activo — los cuatro canales del régimen de Aplicación de Recursos en ME

| Categoría | Cuentas | Fuente |
|---|---|---|
| `canal_encaje_efectivo_me` | Capítulo 115 entero | inferencia capítulo (canal del menú regulatorio) |
| `encaje_bcra_me_estricto` | 115015 + 115017 + 115025 | denominación explícita (subset estricto del encaje) |
| `canal_titulos_publicos_me` | Capítulo 125 entero | inferencia capítulo |
| `tesoro_usd` | 125003 + 125016 + 125042 + 125090 | denominación explícita ("Títulos Públicos") |
| `letras_notas_bcra_me` | 125036, 125038-125044, 125058, 125059 | denominación explícita ("Letras BCRA", "Notas BCRA", "LEDIV", "NODO") |
| `canal_credito_me_residentes_pais` | Capítulo 135 entero | inferencia capítulo |
| `credito_me_spnf` | 1357% + 1358% (capitales + intereses) | inferencia subcuenta (denominación de 135700 dice "SECTOR PRIVADO NO FIN") |
| `credito_me_sf_interbancario_domestico` | 1354% + 1355% | inferencia subcuenta (denominación de 135400 dice "SECTOR FINANCIERO") |
| `credito_me_sector_publico` | 1351% + 1352% | inferencia subcuenta |
| `prefinanc_export_total` | 135199 + 135499 + 135799 | denominación explícita ("PR.PREFINANC.Y FINANC.EXPORT.") |
| `canal_credito_me_crossborder` | Capítulo 136 entero | inferencia capítulo (préstamos a residentes del exterior, sec. 2.1.16-2.1.17 menú) |

#### Sub-aperturas relevantes del SPNF en ME

| Categoría | Cuenta | Concepto |
|---|---|---|
| `prefinanc_export_total` | 135799 | ★ destino primario sec. 2.1.1 |
| `credito_me_documentos_sola_firma_spnf` | 135715 | crédito comercial SPNF |
| `credito_me_documentos_comprados_spnf` | 135721 | crédito comercial SPNF |
| `credito_me_hipotecarios_spnf` | 135708 | hipotecarios SPNF |
| `credito_me_creditos_documentarios` | 135133 | financiación de comercio exterior |

#### Cuentas especiales (no son CERA pero comparten estructura)

| Categoría | Cuenta | Tratamiento prudencial |
|---|---|---|
| `deposito_me_cuenta_exportadores` | 315791 | encaje 0% (TO Efectivo Mínimo sec. 1.3.15.2); excluida de PGNME |
| `deposito_ars_cuenta_exportadores` | 311792 | encaje 3.5% (sec. 1.3.15.1); excluida de PGNME |
| `deposito_ars_cuenta_agro` | 311791 | encaje 3.5%; excluida de PGNME |

#### Proxies regulatorios construidos desde el balance

| Categoría | Cuentas | Uso |
|---|---|---|
| `patrimonio_neto_proxy` | 400000 + 500000 + 650000 | Proxy de RPC (responsabilidad patrimonial computable) |
| `activos_me_total_pgnme` | 115% + 116% + 125% + 126% + 135% + 136% + 145% + 146% + 155% + 175% | Componente activos ME del proxy PGNME |
| `pasivos_me_total_pgnme` | 315% + 316% + 325% + 326% | Componente pasivos ME del proxy PGNME |
| `deuda_bcra_pesos_unificada` | 121024-121026, 121041, 121056-121058, 121091-121093 | Unión temporal LELIQ + LEFI + otras Letras BCRA en pesos |

### Cuestiones pendientes

- **Regularizadoras**: el campo `nivel = detalle` o `principal` del CSV indica si la categoría puede contener regularizadoras. Para variables que miden saldo neto (crédito neto de previsiones), hay que restar las cuentas con `dim_cuentas.es_regularizadora = True` en el notebook de análisis.
- **Cuentas-madre vs hojas**: cuando una categoría se define como `135%`, el join LIKE matchea todas las cuentas-hoja del capítulo. Las cuentas-madre típicamente tienen saldo cero (solo reportan las hojas) pero conviene validar.
- **Cobertura post-régimen**: si nuevas cuentas se dan de alta (como `121091`-`121093` para LEFI en 2023), hay que actualizar el crosswalk explícitamente. El plan no avisa.

## 2. `fusiones.csv` — eventos institucionales

### Por qué existe

El BCRA usa `CODIGO_ENTIDAD` como identificador, pero cuando hay fusiones, absorciones o cambios de denominación, el comportamiento del código cambia y eso puede romper paneles. Decisión metodológica §3.1 de `metodologia_paneles.md`:

- **Panel principal** (`bank-as-is`): cada código es una entidad independiente. Los saltos contables se manejan con efectos fijos y exclusión selectiva.
- **Panel auxiliar** (`pro-forma`): construye una entidad sintética que consolida absorbente + absorbido hacia atrás.

Para construir el segundo, necesitamos saber qué fusiones hubo. Eso vive en este CSV.

### Cómo se construyó la lista v1

Inspección manual de los archivos `Info_Hist/Activas/*.txt` e `Info_Hist/Bajas/*.txt` del dump 202601 (las "leyendas históricas" que cada archivo trae), priorizando los eventos que caen en la ventana 2020+ del paper.

### Distinción crítica: fecha legal vs fecha contable

La leyenda histórica del BCRA registra la **fecha del acto societario** (publicación en Boletín Oficial, resolución del BCRA, etc.), que no coincide con el momento en que el absorbido **deja de reportar balance separado**. En la práctica observamos que:

- El absorbido deja de reportar **uno o dos meses antes** de la fecha legal (presumiblemente porque la operación ya está administrativamente consolidada).
- El absorbente muestra **el salto de saldos en el mes en que el absorbido dejó de reportar** (es el primer balance consolidado).

Por eso `fusiones.csv` tiene tres columnas temporales: `fecha_legal`, `fecha_ultimo_balance_absorbido` y `fecha_primer_balance_consolidado`. Para construir el panel pro-forma usamos `fecha_ultimo_balance_absorbido` como corte.

### Eventos que caen dentro de la ventana 2020+ (columna `cae_en_ventana_blanqueo`)

**1. Galicia absorbe HSBC Argentina / Banco GGAL** — `cae_en_ventana_blanqueo = parcial`

Timeline verificado contra el panel de balance:
- 12-sep-2024: Galicia + Grupo Galicia adquieren 99.99% de HSBC (**cambio de control, no fusión**; HSBC sigue operando como entidad independiente con código 00150).
- 20-dic-2024: HSBC cambia de denominación a "Banco GGAL S.A." (solo nombre; sigue reportando balance separado).
- Mayo-2025: último balance separado de Banco GGAL (código 00150).
- 23-jun-2025: fusión legal por absorción.
- Julio-2025: primer balance consolidado en Galicia (saltos de ~+21.7% en depósitos USD).

**Conclusión para el paper**: durante toda la Etapa 1 del blanqueo (jul-oct 2024) y la mayor parte de Etapa 2/3, HSBC/GGAL es entidad **independiente**. No hay contaminación de la señal CERA. El cuidado hay que tenerlo solo para análisis que extiendan la ventana más allá de jun-2025.

**2. Banco Macro absorbe Banco BMA SAU** — `cae_en_ventana_blanqueo = SI` — **CASO CRÍTICO**

Timeline:
- 05-ene-2024: cambio de control (Itaú Argentina pasa a Macro, se renombra Banco BMA SAU).
- Octubre-2024: BMA deja de reportar balance separado.
- 19-nov-2024: fusión legal por absorción.

**Observación preocupante**: Macro muestra un salto del **+118% en depósitos USD en sep-2024**, muy por encima del de cualquier otro banco comparable. Esto **no se explica solo por flujo CERA** (Macro tiene ~11% del pico CERA, que serían ~USD 1.4B adicionales; pero el salto en depósitos USD es de ~USD 1.4T nominal, que convertido al TC de sep-2024 da casi todo el aumento de depósitos USD).

El salto de Macro sep-nov 2024 es una **mezcla de flujo CERA genuino + absorción pre-fusión de saldos de BMA**. Requiere tratamiento especial en el análisis:
- **Opción 1**: excluir Macro de la muestra principal. Pérdida: es banco grande, 11% del CERA.
- **Opción 2**: construir un "Macro pro-forma" restando los saldos de BMA del dump de sep-2024 retroactivamente. Requiere el último balance disponible de BMA (oct-2024 o dic-2023).
- **Opción 3**: usar Macro solo en regresiones de "panel consolidado pro-forma" y no en las de "bank-as-is".

**3. Galicia cambio de denominación de SAU a SA** (jun-2025) — solo cambio formal de nombre. No afecta nada operativo.

### Eventos pre-2020 (informativo)

Documentados pero no críticos para la ventana del event study del blanqueo 2024. Sirven para la robustez con el blanqueo Macri 2016-17 y para la historia del sistema bancario argentino.

### Cuestiones pendientes

- Verificar fechas exactas de cierre operativo de la operación Galicia-HSBC.
- Completar el listado: hubo otras operaciones menores (cooperativas absorbidas por bancos, sucursales transferidas) que no están todas inventariadas. Para cada nueva fusión que se descubra, agregar fila al CSV.
- Definir qué hacer cuando el banco absorbente y el absorbido tienen códigos distintos pero la "actividad" del absorbido se transfirió antes del cierre formal (caso típico: operación financiera ocurre N meses antes que la fecha legal). Para v1 usamos la fecha legal; en robustez se puede sensibilizar.

## 3. `provincias_iso.csv` — codificación de jurisdicciones

24 jurisdicciones argentinas + el residual `OPERAC.RESIDENTES EN EL EXTERIOR` que el BCRA usa en `distribgeo`. El crosswalk lo genera el notebook `04_dim_provincias.ipynb`. No hay decisiones métodológicas relevantes acá: es un mapeo 1-a-1 entre la denominación del BCRA y los códigos ISO 3166-2:AR.
