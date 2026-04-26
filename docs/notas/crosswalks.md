# Crosswalks: decisiones de investigador

Documenta el contenido y la lógica detrás de los archivos de `data/external/crosswalks/`. Estos archivos son las **decisiones del investigador** para pasar de los paneles largos (raw del BCRA) a las tablas de análisis. Si una de estas decisiones cambia, hay que actualizar el CSV correspondiente y volver a correr los notebooks de `code/analisis/` que dependan de ella.

## 1. `cuenta_categoria.csv` — códigos BCRA → categorías económicas

### Por qué existe

El plan de cuentas BCRA tiene 5,519 cuentas. Las categorías económicas que aparecen en una regresión típica son ~20 ("crédito USD al sector privado", "depósitos CERA", etc.). Hay que mapear el primero al segundo, y este mapeo es:

1. **Una decisión de investigador** (qué cuentas conforman cada concepto).
2. **No invertible automáticamente** desde el plan: requiere leer las denominaciones, conocer la regulación BCRA y a veces el contexto histórico (por ejemplo, saber que LELIQ y LEFI son "lo mismo" en períodos distintos).

Por eso vive como CSV editable, no como código Python.

### Categorías definidas en v1

Lista completa con su justificación. La columna "fuente" indica de dónde sale la decisión metodológica (proposal, paper de referencia, normativa BCRA).

| Categoría | Cuentas | Fuente |
|---|---|---|
| `cera_total` | 311793 + 312183 + 315794 + 316147 | Com. "A" 8071 BCRA. Ver `docs/notas/cera_regimen.md`. Tratamiento bruto del shock del blanqueo. |
| `cera_ars` / `cera_me` | Subset de las anteriores por moneda | Útil para separar el efecto del shock por dolarización del depositante. |
| `cera_residente_pais` / `cera_residente_exterior` | Subset por residencia del titular | Para distinguir el shock que viene del blanqueo doméstico vs. repatriación de fondos del exterior. |
| `credito_ars_spnf` | Capítulo 131 completo | Crédito al sector privado en pesos. Variable de respuesta del lending channel doméstico. |
| `credito_me_spnf` | Capítulo 135 completo | Crédito al sector privado en moneda extranjera. **Variable principal del paper**: el blanqueo aumenta los depósitos USD y la pregunta es si eso se traduce en crédito USD al sector real. |
| `credito_me_prefinanc_export` | 135199, 135499, 135799 | Prefinanciación y financiación de exportaciones. Subset de capítulo 135 que va específicamente a transables (test del canal). |
| `credito_me_documentos_sola_firma` | 135115 | Sub-apertura adicional de capítulo 135. |
| `credito_me_documentos_comprados` | 135121 | Idem. |
| `credito_me_hipotecarios` | 135108 | Idem. |
| `deposito_ars_spnf` | Capítulo 311 completo | Depósitos pesos residentes país (incluye CERA pesos y otras especiales). |
| `deposito_me_spnf` | Capítulo 315 completo | Depósitos USD residentes país (incluye CERA USD y otras especiales). |
| `deposito_ars_spnf_exterior` | Capítulo 312 | Depósitos pesos de no residentes (incluye CERA pesos exterior). |
| `deposito_me_spnf_exterior` | Capítulo 316 | Depósitos USD de no residentes (incluye CERA USD exterior). |
| `deposito_me_cuenta_exportadores` | 315791 | Cuenta especial para acreditar financiación de exportaciones — para distinguir del shock CERA. |
| `titulos_publicos_ars` | Capítulo 121 completo | Tenencias de títulos públicos en pesos (incluye Tesoro y deuda BCRA). |
| `titulos_publicos_me` | Capítulo 125 completo | Tenencias de títulos públicos en ME (incluye Tesoro USD y Letras BCRA en ME). Crítico para el test del kink del tope de aplicaciones ME en Tesoro. |
| `leliq` | 121056, 121057, 121058 | Letras del BCRA — vigentes hasta agosto 2023. |
| `lefi` | 121091, 121092, 121093 | Letras Fiscales de Liquidez — vigentes desde agosto 2023. Reemplazaron a las LELIQ. |
| `letras_bcra_otros` | 121024, 121025, 121026, 121041 | Otras Letras BCRA. |
| `deuda_bcra_pesos` | Unión temporal de LELIQ + LEFI + Letras BCRA varias | **Categoría continua**: "deuda BCRA en pesos en cualquier momento". Resuelve la discontinuidad LELIQ→LEFI. |
| `interbancario_ars` | Capítulo 132 | Operaciones interbancarias en pesos (call entre EEFF, pases). |
| `interbancario_me` | Capítulo 136 | Operaciones interbancarias en moneda extranjera. |
| `encajes_proxy_ars` | 111015, 111025 | **Proxy de integración de Efectivo Mínimo en pesos** (saldos en BCRA cuenta corriente). Ver `metodologia_paneles.md` §3.7 y `cera_regimen.md` §8. |
| `encajes_proxy_me` | 115015 | Proxy de integración de Efectivo Mínimo en ME. |
| `patrimonio_neto_proxy` | 400000 + 500000 + 650000 | **Proxy de RPC** (Responsabilidad Patrimonial Computable). PN contable = Patrimonio neto básico + Resultados + ORI. |
| `activos_me_total` | 115% + 116% + 125% + 126% + 135% + 136% | Suma de activos en moneda extranjera. **Componente del proxy de PGNME** (activos ME menos pasivos ME, sobre RPC). |
| `pasivos_me_total` | 315% + 316% + 325% + 326% | Suma de pasivos en moneda extranjera. **Componente del proxy de PGNME**. |

### Cuestiones pendientes

- **Regularizadoras**: el campo `nota` aclara cuándo una categoría incluye o excluye las cuentas regularizadoras. Para variables que miden saldo neto (crédito neto de previsiones, por ejemplo), hay que restarlas en el notebook de análisis usando `dim_cuentas.es_regularizadora`. Por defecto el panel largo no las consolida.
- **Cuentas-madre vs hojas**: cuando una categoría se define como `135%`, el join con el panel matchea todas las cuentas-hoja del capítulo 135. Si en `bal_hist` el BCRA reporta saldo en la cuenta-madre `135000` (improbable pero posible), también se agrega. Hay que cuidar de no doble-contar (típicamente las cuentas-madre tienen saldo cero porque solo las hojas reportan, pero conviene chequear).
- **Cobertura del capítulo**: para `credito_me_spnf = 135%`, asumimos que TODO el capítulo 135 es relevante. Si en una regresión específica querés excluir, por ejemplo, los préstamos a entidades financieras del exterior que estén dentro del capítulo, hay que ajustar.

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
