# Régimen de Regularización de Activos (Ley 27.743) — CERA

Síntesis operativa para el paper. Cubre: **(i) qué es la CERA**, **(ii) las cuatro cuentas del plan contable BCRA que la registran**, **(iii) el timeline normativo completo**, **(iv) las fechas binding del event study**, **(v) destinos permitidos y restricciones**. Todas las fuentes están bajadas en `docs/Regulacion_BCRA/cera_ley_27743/` y referenciadas en `data/manifest/sources.yaml`.

---

## 1. Qué es la CERA

La **Cuenta Especial de Regularización de Activos (CERA)** es una cuenta de depósito especial, a la vista, regulada por el BCRA mediante Comunicación "A" 8062 (15-jul-2024), en el marco del Título II de la **Ley 27.743** ("Medidas Fiscales Paliativas y Relevantes", B.O. 08-jul-2024) y del **Decreto 608/2024** (reglamentación).

Al ingresar al régimen, el declarante deposita la tenencia regularizada (efectivo en país o exterior, en pesos o moneda extranjera) en una cuenta CERA a su nombre. Esos fondos **quedan indisponibles** hasta la fecha límite de la etapa a la que adhirió; durante ese período solo pueden (i) permanecer depositados, (ii) aplicarse a **destinos de inversión autorizados** enumerados por la AFIP y el Ministerio de Economía, o (iii) retirarse pagando una retención especial (regla del **umbral USD 100.000**, ver §4).

---

## 2. Las cuatro cuentas del plan contable BCRA

La CERA aparece en el plan de cuentas (archivo `cuentas/cuentas.txt` dentro de cada dump IEF) como **cuatro códigos** dentro del capítulo **310000 — Depósitos**, todas con la leyenda literal `"Cuenta Especial de Regularización de Activos Ley 27.743"`:

| Código | Capítulo madre | Moneda | Residencia del titular | Uso esperado |
|---|---|---|---|---|
| **311793** | `311000 – Depósitos en pesos, residentes en el país` → SPNF | **ARS** | País | Regularización en pesos de residentes argentinos |
| **312183** | `312000 – Depósitos en pesos, residentes en el exterior` | **ARS** | Exterior | Residentes extranjeros con tenencias en pesos |
| **315794** ★ | `315000 – Depósitos en moneda extranjera, residentes en el país` → SPNF | **USD** (o ME admitida) | País | **Cuenta dominante**: regularización en dólares de residentes argentinos |
| **316147** | `316000 – Depósitos en moneda extranjera, residentes en el exterior` | **USD** | Exterior | Regularización de residentes no-argentinos |

**Interpretación empírica**: en `bal_hist/balhist.txt` estas cuatro cuentas ingresan con saldo cero hasta julio-2024. El tratamiento bruto del shock del blanqueo por banco × mes es la **suma** de las cuatro, y **315794** es la que concentra el grueso (blanqueo en dólares por residentes argentinos — población objetivo natural del régimen).

Convivencia con cuentas "especiales" previas en el mismo bloque 31x78x–31x79x (relevantes para no confundir):

- `311781–311783` y `315781–315783` — Ley 27.260 (blanqueo 2016-17, Macri).
- `311784–311789`, `315784–315789` — cuentas ajustables UVA/UVI y repatriación aporte solidario Ley 27.605 (2020).
- `311790`, `315790` — **CECON.Ar** (Leyes 27.613/26.679/27.701, construcción).
- `311791` — "Cuenta Especial para Titulares con Actividad Agrícola".
- `311792`, `315791` — Cuentas Especiales para Exportadores (financiación).
- `315792` — régimen de fomento de economía del conocimiento (Decreto 679/22).
- `315793` — **CEPRO.Ar** (Ley 27.701, inversión y producción).

Ninguna de estas es parte del blanqueo 2024 pero todas pueden ser referencias útiles como **contrafactuales administrativos** (otros regímenes especiales con mecánica de depósito afectado).

---

## 3. Las tres Etapas del régimen y sus fechas binding

Fijadas originalmente por el Decreto 608/24 y sucesivamente prorrogadas por los Decretos 773/24 y 864/24:

| Etapa | Adhesión desde | Plazo original de **indisponibilidad** | Prórroga final | Alícuota del impuesto especial |
|---|---|---|---|---|
| **Etapa 1** | jul-2024 | **hasta 30-sep-2024** | **hasta 31-oct-2024** (Dec. 864/24) | 5% sobre el excedente de USD 100.000 |
| **Etapa 2** | cierre Etapa 1 → | hasta 31-dic-2024 (original) | hasta ~28-feb-2025 (prorroga) | 10% |
| **Etapa 3** | cierre Etapa 2 → | hasta 31-mar-2025 (original) | hasta ~31-jul-2025 (prorroga Dec. 864/24 art. 8°) | 15% |

**Fecha clave de retención**: los fondos pueden mantenerse en CERA hasta el **31-dic-2025** sin pago adicional, siempre que se destinen a inversiones autorizadas o permanezcan en el sistema financiero. Retiros antes de esa fecha disparan una **retención especial del 5%** (salvo por las excepciones del art. 31 Ley 27.743 y el umbral de USD 100.000).

---

## 4. La regla del umbral USD 100.000

Esta es la regla más importante para nuestra estrategia de identificación porque **corta la población de declarantes en dos grupos con comportamiento muy distinto**.

Del texto de la Com. "A" 8062 punto 3 y su modificación por A 8110:

> "En el caso de que el importe total regularizado sea de hasta USD 100.000 (dólares estadounidenses cien mil) y el titular decida transferir el importe depositado en esta cuenta hacia otra cuenta propia antes de las fechas límites previstas para la manifestación de adhesión de la Etapa 1, la entidad financiera deberá requerir que este último manifieste —con carácter de declaración jurada— que ese monto será utilizado, hasta las fechas límites antes mencionadas, en **operaciones onerosas debidamente documentadas** —entendiéndose por tales a aquellas que cuenten con el correspondiente respaldo del comprobante pertinente (factura, boleto de compraventa, escritura, entre otros)."

Traducción:

- **Declarantes con regularización ≤ USD 100.000**: exentos del impuesto especial (0%). Pueden retirar los fondos antes del vencimiento de la Etapa 1 *si los destinan a consumo/inversión real documentado*. Efectivamente, el dinero sale rápido del sistema y entra al circuito real.
- **Declarantes con regularización > USD 100.000**: los fondos **deben** permanecer en CERA o aplicarse a los destinos de inversión autorizados **hasta 31-dic-2025** para evitar la retención del 5%. Los fondos se quedan en el sistema.

Los bancos ven esto como **dos flujos muy distintos**: depósitos de corta duración (≤100K) vs depósitos de larga duración "atados" (>100K) con restricciones de aplicación. Relevante para el `lending channel`: solo el segundo grupo funda nuevo crédito efectivamente.

---

## 5. Destinos de inversión permitidos

Regulados por **Ministerio de Economía** — Resolución 590/2024 (referida en Com. "A" 8090) y sucesivas. El BCRA no regula la lista directamente; se limita a registrar qué movimientos están autorizados de la CERA.

Las principales categorías son:

1. **Permanencia pasiva en la CERA** hasta 31-dic-2025.
2. **Transferencia a otra CERA** del titular (o a una "Cuenta Comitente Especial de Regularización de Activos" en un Agente de Liquidación y Compensación).
3. **Suscripción de títulos públicos** elegibles (p. ej. bonos duales ajustables en pesos o dólares, letras del Tesoro) — definidos por Mecon.
4. **Fondos comunes de inversión** específicos aprobados por CNV con destinos pre-establecidos.
5. **Operaciones del mercado de capitales** (Obligaciones negociables, CEDEARs, fideicomisos financieros, letras/bonos SGR) dentro de listados aprobados.
6. **Construcción inmobiliaria** vía CECON.Ar (ya existente) en ciertos proyectos elegibles.
7. **Pago de impuestos** (a través del sistema VEP de AFIP/ARCA).

Implicancia para nosotros: el banco receptor **no presta con estos fondos directamente**. Los aplica a los destinos autorizados o los inmoviliza. Por lo tanto, el shock al activo bancario que buscamos medir **no es un aumento mecánico del crédito con fondos CERA**, sino un efecto de **relajamiento de restricciones de fondeo en moneda extranjera** (la vía Bartik): recibir depósitos USD grandes afloja el cumplimiento de PGNME y libera capacidad de préstamo USD fuera del circuito CERA.

---

## 6. Timeline normativo completo

### Leyes, decretos y resoluciones (fuente: Boletín Oficial)

| Fecha | Norma | Rol |
|---|---|---|
| **27-jun-2024** (sanción) / **08-jul-2024** (B.O.) | **Ley 27.743** | Marco legal del régimen |
| **12-jul-2024** | Decreto 608/2024 | Reglamentación original (define Etapas) |
| **17-jul-2024** | **RG AFIP 5528/2024** | Reglamenta operatoria AFIP |
| **19-jul-2024** | **Res. Mecon 590/2024** | **Enumera los destinos de inversión permitidos** para la CERA (art. 31 Ley y art. 18 Decreto 608) |
| **30-jul-2024** | RG AFIP 5536/2024 | Modifica RG 5528/2024. Anexo con documentación para acreditar titularidad |
| **20-ago-2024** | Res. Mecon 759/2024 | Complementa / ajusta la Res. 590/2024 (destinos) |
| **30-ago-2024** | Decreto 773/2024 | Modifica Decreto 608 (flexibilizaciones) |
| **30-sep-2024** | Decreto 864/2024 | **Prórroga Etapa 1** hasta 31-oct-2024 y Etapas 2/3 hasta 31-jul-2025 |
| **25-oct-2024** | Decreto 953/2024 | Disolución AFIP → creación ARCA (referenciado por Com. A 8140) |

### BCRA Comunicaciones "A"

| Fecha | Com. | Título | Efecto |
|---|---|---|---|
| **15-jul-2024** | **A 8062** | OPASI 2-721 — Reglamentación | **Crea operativamente la CERA** (puntos 3.16 del TO Depósitos de Ahorro, Cuenta Sueldo y Especiales) |
| **23-jul-2024** | **A 8071** | CONAU 1-1638 — Plan de Cuentas | **Da de alta en el plan de cuentas las 4 partidas** 311793 / 312183 / 315794 / 316147 y la cuenta 325195 (Otras retenciones y percepciones USD). Puente entre regulación operativa y registro contable |
| **15-ago-2024** | A 8090 | OPASI 2-723 — Adecuación | Admite transferencias a otras CERAs y a cuentas AFIP-monitoreadas para destinos permitidos |
| **19-sep-2024** | A 8106 | OPASI 2-725 — Adecuación | Habilita **tarjeta de débito y medios electrónicos de pago** vinculados a la CERA |
| **30-sep-2024** | A 8110 | OPASI 2-726 — Adecuaciones | Actualiza fechas (30-sep → 31-oct) por Decreto 864/24; formaliza umbral USD 100.000 y regla de "operaciones onerosas documentadas" |
| **01-nov-2024** | A 8123 | OPASI 2-727 — Prórroga | Alinea CERA con nuevas fechas del régimen |
| **02-dic-2024** | A 8140 | CONAU 1-1650 | Actualiza regímenes informativos por transición AFIP → ARCA (Decreto 953/24) |
| **14-oct-2025** | A 8343 | SINAP 1-237 | Incorpora operatorias **DPA** (transferencias de terceros con CERA) y **DZV** (devoluciones) al Medio Electrónico de Pagos |

**Com. "A" peripheral con mención incidental de CERA** (republicaciones de TOs que incluyen la sección 3.16 como parte del conjunto; no modifican el régimen): A 8086 (08-08-2024, cheques), A 8131 (12-11-2024, TO depósitos consolidado), A 8168 / A 8220 / A 8249 / A 8278 / A 8280 / A 8288 / A 8300 / A 8307 / A 8315 (actualizaciones de normas prudenciales y regímenes informativos entre dic-2024 y sep-2025). No bajadas a `docs/` — las tomamos como contexto, no modifican la CERA.

### Cómo obtener versiones alternativas/actualizadas

- Índice anual BCRA: `https://www.bcra.gob.ar/archivos/Pdfs/SistemasFinancierosYdePagos/Comunicaciones/Indice{YYYY}.pdf` — busca por "27.743" o "CERA" o "Regularización de Activos".
- Boletín Oficial — búsqueda por norma en `https://www.boletinoficial.gob.ar/`.
- Infoleg (páginas estáticas): `https://servicios.infoleg.gob.ar/infolegInternet/verNorma.do?id={id}`.

---

## 7. Fechas binding para el event study

Lista corta de fechas que **todo diseño de event study debe incorporar explícitamente** como posibles break points (no arbitrar todas en el mismo día):

| Fecha | Evento | Por qué importa |
|---|---|---|
| **15-jul-2024** | BCRA publica A 8062 | Primera fecha operativa — bancos empiezan a abrir CERAs |
| **30-sep-2024** | Cierre Etapa 1 (original) | Con prórroga a 31-oct-2024 (Dec. 864/24) — dos fechas en una semana |
| **31-oct-2024** | Cierre **efectivo** Etapa 1 | Fin del período de ingreso sin alícuota para ≤USD 100.000 |
| **28-feb-2025 (aprox.)** | Cierre Etapa 2 | Alícuota sube a 15% |
| **31-jul-2025** | Cierre Etapa 3 | Último día para adherir |
| **31-dic-2025** | **Fecha de liberación sin retención** | Fondos que permanecieron en CERA pueden retirarse sin pagar 5% |

**Recomendación para el event study**: usar **ago-2024** como `t=0` (primer mes completo post-shock) porque el grueso del flujo entra entre mediados-jul y agosto. Las fechas de cierre de etapa sirven como controles de heterogeneidad en la dosis.

---

## 8. Qué significa todo esto para nuestra estrategia empírica

1. **Shock a nivel banco**: cuatro cuentas CERA en `bal_hist`. Se puede construir de manera limpia y directa.
2. **Heterogeneidad banco × banco**: el ingreso de depósitos CERA no es homogéneo — bancos con mayor presencia USD previa captaron más. Esto **es** nuestra variable de intensidad de tratamiento `γ̂_b` del Paso 1 del Greenstone-Mas-Nguyen.
3. **Mecanismo del lending channel**: el depósito CERA **no financia crédito directo** (por restricciones de aplicación). El efecto pasa por:
   - Aflojamiento de **PGNME** (recibir USD sin contraparte prestada en USD acerca a la banca al piso de −30% RPC del régimen PGN).
   - Cambio en la **composición del fondeo** (mayor ponderación de depósitos ME sobre depósitos pesos).
   - Señalización de mayor **liquidez** que afecta el costo de fondeo agregado.
4. **Heterogeneidad entre declarantes**: el umbral USD 100.000 genera dos poblaciones de depósitos CERA con dinámicas distintas (rotación rápida vs atado). Si pudiéramos separarlos (no es obvio desde el balance consolidado), sería una fuente extra de variación.
5. **Convivencia con regulación que cambia**: la ventana contiene cambios normativos (A 8090, 8106, 8110, 8123) que afectaron las reglas del juego *durante* el evento. **Hay que controlar por ellas** en el event study para no confundir efectos del shock con efectos de flexibilizaciones regulatorias.

---

## 9. Archivos bajados y referenciados

Todos en `docs/Regulacion_BCRA/cera_ley_27743/`, con entradas en `data/manifest/sources.yaml` (ids `reg_ley_27743`, `reg_decreto_608_2024`, `reg_decreto_773_2024`, `reg_decreto_864_2024`, `reg_rg_afip_5528_2024`, `reg_bcra_com_a8062`, …, `reg_bcra_com_a8343`).

```
docs/Regulacion_BCRA/cera_ley_27743/
├── leyes_decretos/
│   ├── ley_27743_2024-07-08.pdf
│   ├── decreto_608_2024-07-12.pdf
│   ├── decreto_773_2024-08-30.pdf
│   ├── decreto_864_2024-09-30.pdf
│   ├── decreto_953_2024-10-25.pdf              # AFIP → ARCA
│   ├── rg_afip_5528_2024-07-17.pdf
│   ├── rg_afip_5536_2024-07-30.pdf             # modifica 5528
│   ├── res_mecon_590_2024-07-19.pdf            # destinos permitidos
│   └── res_mecon_759_2024-08-20.pdf            # complementa 590
└── bcra_comunicaciones/
    ├── A8062_2024-07-15_creacion.pdf
    ├── A8071_2024-07-23_alta_cuentas_plan_contable.pdf   # 311793/312183/315794/316147
    ├── A8090_2024-08-15_adecuacion_1.pdf
    ├── A8106_2024-09-19_adecuacion_2.pdf
    ├── A8110_2024-09-30_etapa1_limite_100k.pdf
    ├── A8123_2024-11-01_prorroga_etapa1.pdf
    ├── A8140_2024-12-02_arca_actualizacion_regimenes.pdf
    └── A8343_2025-10-14_operatoria_pagos_DPA_DZV.pdf
```

## 10. Pendientes

1. **RG ARCA posteriores a oct-2024** que puedan haber ajustado el régimen — no crítico si el destino exacto de los fondos no entra en la especificación econométrica.
2. Si el mecanismo *destinos* pasa a ser relevante (test de canal), bajar Resoluciones Mecon posteriores a la 759/2024 que hayan ampliado la lista.
3. El scan del Indice2025 cubre solo hasta Com. A 8199 y un subconjunto hasta A 8343; si se detecta posteriormente otra Com. "A" > 8343 que toque CERA, incorporar acá.
