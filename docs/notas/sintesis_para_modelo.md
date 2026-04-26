# El canal de crédito sesgado a exportadores bajo segmentación macroprudencial por moneda

## Síntesis del proyecto para construcción del modelo teórico

**Documento de transferencia.** Consolida toda la información relevante para pensar el modelo teórico del paper sin requerir contexto previo. Fuente: documentación interna del proyecto en `docs/notas/cera_regimen.md`, `docs/notas/metodologia_paneles.md`, `docs/Papers/Project_Proposal.docx` y los textos ordenados regulatorios del BCRA.

---

## 1. Pregunta de investigación

En una economía donde la regulación macroprudencial impone un **matching formal entre la moneda del fondeo y la moneda del destino del crédito**, ¿cómo es el bank lending channel? Concretamente, para un peso de fondeo USD adicional que llega al balance de un banco, ¿cómo se asigna entre:

1. Crédito en USD a destinos elegibles (exportadores y sectores transables);
2. Rebalanceo de portafolio hacia Tesoro USD, paper del BCRA y conversión spot;
3. Crédito en pesos vía canales indirectos de balance;
4. Outcomes reales — empleo, exportaciones, salarios — a nivel sector × provincia.

El objeto de interés se denomina el **export-biased lending channel**: un bank lending channel cuya pass-through está, por construcción regulatoria, sesgada hacia exportadores y el sector transable. La pregunta empírica es a través de cuál de tres configuraciones se realiza ese sesgo:

- **Canal de destino regulado**: el fondeo USD se aplica efectivamente al crédito a exportadores como pretende la regulación.
- **Canal de sustitución de balance**: el fondeo libera capital y liquidez que el banco reasigna al crédito en pesos, derramándose a sectores no elegibles.
- **Canal de absorción financiera**: el destino regulado absorbe poco y el fondeo se recicla a Tesoro USD, paper del BCRA o conversión spot.

Cada configuración corresponde a una región distinta del espacio de parámetros y produce outcomes reales con patrón espacial-sectorial distinguible.

## 2. Variación cuasi-experimental: el blanqueo de 2024 (Ley 27.743)

### Contexto

El gobierno argentino sancionó en julio 2024 la **Ley 27.743 (Medidas Fiscales Paliativas y Relevantes)**. El Título II crea un Régimen de Regularización de Activos ("blanqueo") que permitió a residentes argentinos declarar tenencias de moneda extranjera no registradas previamente.

Se declararon **aproximadamente USD 22.000 millones** durante la Etapa 1 del régimen (jul-2024 a oct-2024), de los cuales unos **USD 20.000 millones se canalizaron al sistema bancario** vía un instrumento ad hoc: las Cuentas Especiales de Regularización de Activos (CERA).

El régimen se estructuró en tres etapas con alícuotas crecientes del impuesto especial de regularización:

| Etapa | Adhesión | Indisponibilidad original | Cierre efectivo (con prórrogas) | Alícuota |
|---|---|---|---|---|
| 1 | jul-2024 | hasta 30-sep-2024 | hasta 31-oct-2024 | 5% sobre excedente USD 100.000 |
| 2 | nov-2024 | hasta 31-dic-2024 | hasta 28-feb-2025 | 10% |
| 3 | mar-2025 | hasta 31-mar-2025 | hasta 31-jul-2025 | 15% |

**Fecha clave**: hasta el **31-dic-2025**, los fondos pueden permanecer en CERA o aplicarse a destinos autorizados sin ningún costo. El retiro a una cuenta no monitoreada antes de esa fecha dispara una **retención del 5%**, salvo dos excepciones:

1. Importes regularizados ≤ USD 100.000: el titular puede retirar antes del cierre de Etapa 1 si declara que lo aplicará a operaciones onerosas documentadas (consumo, inversión real comprobable).
2. Aplicación a destinos de inversión autorizados: bonos públicos, FCIs productivos, ON, financiamiento MiPyME, construcción CECON.Ar.

### Las cuatro cuentas CERA en el plan contable del BCRA

Por Comunicación "A" 8071 del 23-jul-2024, el BCRA dio de alta cuatro cuentas en el plan contable, todas dentro del capítulo 310000 (Pasivo / Depósitos):

| Código | Capítulo madre | Moneda | Residencia | Significado |
|---|---|---|---|---|
| **311793** | 311 — Depósitos pesos residentes país | ARS | País | Pesos de residentes argentinos |
| **312183** | 312 — Depósitos pesos residentes exterior | ARS | Exterior | Pesos de no residentes |
| **315794** ★ | 315 — Depósitos USD residentes país | USD | País | **Cuenta dominante** (96.6% del peak) |
| **316147** | 316 — Depósitos USD residentes exterior | USD | Exterior | USD de no residentes |

Convención contable BCRA: pasivos con signo negativo. Los saldos económicos son `abs(saldo)`.

## 3. Marco regulatorio relevante

Cuatro restricciones regulatorias actúan simultáneamente sobre el balance del banco que recibe CERA. Todas son **pre-existentes al blanqueo** y aplican a cualquier depósito ME del sistema, no sólo a CERA.

### 3.1 Régimen de Aplicación de Recursos en Moneda Extranjera

Texto ordenado: **Política de Crédito** del BCRA, sección 2 (Com. "A" 8202, vigencia 21/02/2025).

> "La capacidad de préstamo de los depósitos en moneda extranjera deberá aplicarse, en la correspondiente moneda de captación, en forma indistinta, a los siguientes destinos:" (sec. 2.1)

Menú cerrado de destinos. Las categorías más relevantes:

- **2.1.1** Prefinanciación y financiación de exportaciones.
- **2.1.2** Otras financiaciones a exportadores con flujo futuro en ME.
- **2.1.3** Productores, procesadores o acopiadores de bienes con contratos firmes en ME.
- **2.1.10** Préstamos interfinancieros.
- **2.1.11** Letras y Notas del BCRA en USD.
- **2.1.12** Inversiones directas en el exterior.
- **2.1.13** Proyectos energéticos con contratos en ME.
- **2.1.14** Tesoro Nacional en ME, **hasta un tercio del total de aplicaciones** (kink regulatorio).
- **2.1.15** Ganadería bovina, hasta 5% de los depósitos ME.
- **2.1.16** Importadores del exterior.
- **2.1.17** Residentes del país garantizados por cartas de crédito de bancos investment grade del exterior.

**Importante**: los depósitos ME no pueden fondear activos en pesos. Vender los USD recibidos para quedarse en pesos viola el régimen.

En el plan contable del BCRA, los destinos del menú se reflejan en cuatro grandes capítulos del activo:

| Capítulo | Concepto | Rol en el menú |
|---|---|---|
| 115 | Efectivo y depósitos en bancos en ME | Encaje BCRA + efectivo |
| 125 | Títulos públicos en ME | Tesoro USD + Letras BCRA en ME |
| 135 | Préstamos al SPNF en ME | Crédito a exportadores y destinos elegibles |
| 136 | Operaciones interbancarias en ME | Pases activos al BCRA, call entre EEFF |

### 3.2 Posición Global Neta en Moneda Extranjera (PGNME)

Texto ordenado: **PGNME** (Com. "A" 8360, vigencia 10/12/2025).

Definición: la PGNME computa la totalidad de activos, pasivos, compromisos e instrumentos en ME — incluyendo operaciones a término y derivados.

Topes regulatorios:

- **Posición global neta negativa** (banco corto en USD): hasta **−30%** de la Responsabilidad Patrimonial Computable (RPC).
- **Posición global neta positiva** (banco largo en USD): hasta **+5%** de la RPC.

Exclusiones (sección 1.2):

```
1.2.1. Activos deducibles para determinar la RPC.
1.2.2. Conceptos en sucursales en el exterior.
1.2.3. Títulos públicos nacionales en pesos con rendimiento en moneda dual.
1.2.4. Saldos correspondientes a "Cuentas especiales para titulares con
       actividad agrícola" y "Cuentas especiales para exportadores".
1.2.5. LEDIV.
1.2.6. Títulos públicos y privados en pesos ajustables por tipo de cambio.
```

**Las cuentas CERA NO están excluidas de la PGNME.** Las exclusiones de 1.2.4 corresponden a las cuentas 311791 (agrícola), 311792 y 315791 (exportadores) — distintas conceptual y operativamente de CERA.

**Implicancia**: recibir CERA aumenta el pasivo ME del banco sin contraparte inmediata en activo ME, **empujando el ratio PGNME hacia el piso de −30% RPC**. El banco debe expandir activos ME (los del menú de aplicación) o reducir otros pasivos ME para no quedar en infracción.

### 3.3 Efectivo Mínimo (encaje)

Texto ordenado: **Efectivo Mínimo** (Com. "A" 8397, vigencia 06/02/2026).

La sección 7.5 establece:

> "Los depósitos en la 'Cuenta Especial de Regularización de Activos' –punto 3.16. del TO sobre Depósitos de Ahorro, Cuenta Sueldo y Especiales– **serán considerados como depósitos a la vista a los efectos de la exigencia de efectivo mínimo –punto 1.3.2.–**."

La sección 1.3.2.2 fija para depósitos a la vista en moneda extranjera una tasa de encaje del **25%**, igual para Grupo A y restantes entidades.

**Las cuentas CERA tienen encaje del 25%**, no 0%. El encaje 0% que existe en la sec. 1.3.15.2 ("Cuentas especiales para acreditar financiación de exportaciones", USD 0%) aplica a la cuenta 315791, no a las CERA Ley 27.743.

**Implicancia**: por cada USD adicional de depósito CERA, el banco debe inmovilizar mecánicamente 25 centavos en cuenta corriente del BCRA en ME (cuenta 115015 del balance). Es un componente del activo ME que NO es discrecional del banco.

### 3.4 Capitales Mínimos / RPC

Texto ordenado: Capitales Mínimos. La RPC define el numerador del ratio Basilea y el denominador de los topes PGNME y Tesoro USD.

Para nuestros fines, lo relevante es que **la RPC limita el descalce ME**: cuanto más capital tiene el banco, más holgada es la PGNME en valor absoluto. Bancos con menos capital están más restringidos en cuánto pueden expandir activos ME.

### 3.5 La regla del umbral USD 100.000

Regla específica de la CERA establecida por la Comunicación "A" 8110 del BCRA:

- Declarantes con regularización ≤ USD 100.000: exentos del impuesto especial. Pueden retirar antes del cierre de Etapa 1 si destinan los fondos a operaciones onerosas documentadas. **Funcionalmente, son depósitos de corta duración.**
- Declarantes con regularización > USD 100.000: los fondos deben permanecer en CERA o aplicarse a los destinos autorizados hasta el 31-dic-2025 para evitar la retención del 5%. **Funcionalmente, son depósitos atados de larga duración.**

Los bancos ven dos flujos cualitativamente distintos según el tamaño del declarante.

## 4. Hallazgos empíricos preliminares

Toda la sección está basada en panel mensual del BCRA (`bal_hist`), 2020-2026, panel pro-forma con consolidación Macro+BMA. Convertido a USD al tipo de cambio mayorista A-3500 de fin de mes.

**Convención de ventanas usada en esta sección.** Los hechos descriptivos que sólo dependen del peak (composición CERA, distribución entre bancos) son insensibles al horizonte. La asignación del shock dentro del balance, en cambio, depende del horizonte elegido y se reporta en dos ventanas con interpretación distinta:

- **Ventana corta** ago-2024 → mar-2025 (≈8 meses): primer mes completo post-shock hasta el último mes pre-salida del cepo (14-abr-2025). Ventana en la que la asignación del activo ME se puede leer mayormente como respuesta del banco al fondeo CERA bajo restricciones binding (encaje 25%, PGNME, menú 2.1). Es la ventana relevante para la identificación del Paso 1 (γ̂_b).
- **Ventana larga** jun-2024 → ene-2026 (≈19 meses): pre-shock hasta último dato disponible. Mezcla la respuesta inicial al shock con la reasignación posterior bajo el régimen Milei (salida cepo abr-2025, apreciación real, disinflación, baja de tasas en pesos). Útil como descriptivo de la persistencia y del estado terminal del balance, no como evidencia causal del shock CERA.

### 4.1 Magnitud y dinámica del shock administrativo

Saldo total en las cuatro cuentas CERA del plan contable BCRA, en miles de millones de USD:

| Mes | Bancos con saldo | Saldo total CERA (USD B) |
|---|---:|---:|
| jul-2024 | 4 | 0.0 |
| ago-2024 | 26 | 0.6 |
| sep-2024 | 42 | 12.1 |
| **oct-2024 (peak)** | **44** | **12.3** |
| nov-2024 | 39 | 7.7 |
| dic-2024 | 38 | 5.8 |
| jun-2025 | 37 | 3.0 |
| dic-2025 | 35 | 2.3 |
| ene-2026 | 15 | 0.6 |

Composición en el peak: **96.6%** corresponde a la cuenta 315794 (USD residentes país); 3.4% a la cuenta 311793 (ARS residentes país); el resto es marginal.

Esto es lo que la regulación "ve" como CERA stricto sensu. Es un hecho administrativo, no una medida del shock económico: las cuentas se vacían 95% entre oct-2024 y ene-2026, pero los fondos no salen del sistema (ver §4.2).

### 4.2 La verdadera variable de tratamiento: depósitos USD totales del SPNF

Las cuentas CERA caen 95% entre el peak y enero 2026. Pero el stock total de depósitos USD del SPNF (capítulos 315+316) **no cae** — sigue creciendo:

| Mes | CERA (USD B) | Resto USD (USD B) | Total depósitos USD (USD B) |
|---|---:|---:|---:|
| jun-2024 (pre) | 0.0 | 20.0 | **20.0** |
| sep-2024 | 11.7 | 22.1 | 33.8 |
| oct-2024 | 11.9 | 25.1 | 37.0 |
| dic-2024 | 5.8 | 28.3 | 34.1 |
| jun-2025 | 3.0 | 30.6 | 33.7 |
| dic-2025 | 2.3 | 37.7 | 40.0 |
| ene-2026 | 0.6 | 40.8 | **41.4** |

Mientras CERA cae de USD 11.7B a USD 0.6B, los depósitos USD "no-CERA" suben de USD 22.1B a USD 40.8B. **Los dólares no salen del sistema bancario; se reclasifican** dentro del mismo balance del banco, de la cuenta CERA específica a cuentas USD regulares (cajas de ahorro ME, plazos fijos ME, cuentas corrientes ME).

Económicamente: una vez vencidas las restricciones de indisponibilidad y especialmente después del 31-dic-2025 (fecha de liberación sin retención del 5%), los titulares mueven los fondos de la cuenta CERA a una cuenta USD regular del mismo banco. La transferencia entre cuentas del mismo titular dentro del mismo banco no dispara retención.

**El stock USD del sistema se duplica (USD 20B → USD 41B) entre pre-shock y ene-2026.** El shock es persistente, no transitorio.

Para el modelo: la variable de tratamiento relevante no es el saldo CERA sino el aumento de depósitos USD totales por encima del contrafactual. CERA es el nombre administrativo del flujo inicial; lo que importa económicamente es la masa total de depósitos USD adicionales que el banco debe aplicar dentro del menú regulatorio.

Crucialmente, **la reclasificación CERA → depósito USD regular no cambia las exigencias regulatorias**: ambos son depósitos a la vista en ME, encajan al 25% y entran en PGNME. La continuidad del tratamiento prudencial es lo que sostiene la persistencia del efecto sobre la asignación del activo ME del banco.

### 4.3 Distribución entre entidades

44 bancos recibieron flujo CERA. Concentración moderada:

- HHI (mes peak): 1,462 (apenas debajo del umbral de 1,500 = "concentración baja").
- Share top-3: 58.5%, top-5: 76.9%, top-10: 92.0%.
- Top 5 (con sus shares CERA): Galicia 24%, Santander 22%, BBVA 12%, Macro 11%, Nación 7%.

La correlación entre la participación del banco en depósitos USD pre-shock (jun-2024) y la participación en CERA peak es muy alta: **Pearson 0.876, Spearman 0.891**. Los bancos que recibieron más CERA son esencialmente los mismos que ya tenían más depósitos USD antes del blanqueo. No hay sorpresa: los depositantes regularizan sus tenencias en el banco con el que ya operan.

Esta tabla es invariante al horizonte porque los shares se calculan sobre el peak (oct-2024) y la composición pre-shock se calcula sobre jun-2024 — ambas fechas anteriores a cualquier macro-evento contaminante.

### 4.4 Asignación del shock dentro del balance — ventana corta (ago-2024 → mar-2025)

Esta es la ventana de interés para la identificación: pre-cepo, con el grueso del flujo CERA ya asignado y antes de que la salida del cepo (14-abr-2025) y la apreciación real cambien las decisiones de cartera por razones ajenas al shock.

**TODO — recomputar en `code/analisis/01_Shock_Analysis.ipynb`** con corte en mar-2025 (último mes pre-cepo). Tabla esperada (suma sistema, USD B):

| Canal | Δ (USD B) | % del Δ depósitos USD |
|---|---:|---:|
| Crédito a SPNF en ME (cap. 135) | TODO | TODO |
| Efectivo y BCRA en ME (cap. 115, encaje) | TODO | TODO |
| Títulos públicos en ME (cap. 125) | TODO | TODO |
| Interbancario ME (cap. 136) | TODO | TODO |

Métricas adicionales a recomputar para esta ventana: identidad de balance (cobertura % de los cuatro canales), descomposición del componente mecánico del encaje (25% × Δ depósitos vista ME) vs el residuo discrecional, share del Δ que va al menú 2.1 sin Tesoro USD vs con Tesoro USD.

**Lectura esperada bajo cada uno de los tres canales del proyecto** (ver §1):
- Si domina el **canal de destino regulado**: peso fuerte de cap. 135, especialmente sub-aperturas 135199/135499/135799 (prefinanciación de exportaciones).
- Si domina el **canal de absorción financiera**: peso fuerte de cap. 125 (Tesoro USD) hasta tope 1/3, después spillover a cap. 136 (interbancario ME) o piso PGNME.
- Si domina el **canal de sustitución de balance**: la asignación dentro del activo ME es residual/baja, y se observa expansión de crédito en pesos en bancos con más slack de capital ex-ante (no captado en esta tabla, requiere análisis por moneda cruzado).

### 4.5 Evolución bajo el nuevo régimen cambiario — ventana larga (jun-2024 → ene-2026)

Δ acumulado a 19 meses, suma de todos los bancos. **Esta tabla es descriptiva, no causal sobre el shock CERA**: el período incluye salida del cepo (14-abr-2025), apreciación real, disinflación y baja de tasas en pesos, todos eventos que reasignan cartera independientemente del shock CERA.

| Canal | Δ (USD B) | % del Δ depósitos USD |
|---|---:|---:|
| Crédito a SPNF en ME (cap. 135) | **+13.8** | **+64.6%** |
| Efectivo y BCRA en ME (cap. 115, encaje) | **+9.2** | **+43.0%** |
| Títulos públicos en ME (cap. 125) | −3.1 | −14.5% |
| Interbancario ME (cap. 136) | −0.3 | −1.3% |

Identidad de balance: Δ depósitos USD del SPNF = USD 21.4 B; suma de Δ en los cuatro canales del activo ME = USD 19.7 B. Cobertura del 91.8%.

**Descomposición regulatoria del +43% en encaje** (válida en cualquier ventana, porque la regla del 25% es mecánica):
- 25% del Δ depósitos vista ME va obligatoriamente a encaje BCRA en ME. Sobre Δ = USD 21.4 B son USD 5.35 B.
- El residuo de USD 3.86 B (≈18% del Δ) es voluntario o por encaje sobre otros depósitos USD que también crecieron en el período.

**Lectura del estado terminal**: 19 meses después del shock, el sistema bancario terminó con el +65% del Δ depósitos USD aplicado a crédito ME al SPNF y −14.5% en Tesoro USD. Es consistente con un equilibrio en el que (i) el banco trató el fondeo como persistente (ver §4.2), (ii) el tope 1/3 sobre Tesoro USD se volvió más binding al crecer la masa total de aplicaciones, y (iii) la demanda de crédito ME del sector transable estuvo activa durante el período. Pero **no es identificación**: cualquiera de esos resultados puede deberse al shock CERA o a la combinación cepo-cero/apreciación/disinflación que cambió precios relativos. Para separar las dos cosas, ver §4.4 (ventana corta) y §5 (estrategia formal).

### 4.6 Caveat de identificación: contaminación cross-section por el régimen Milei

La preocupación principal con la ventana larga no es un confounder agregado — eso se controlaría con efectos fijos de tiempo. Es que los macro-eventos post-cepo cargan **diferencialmente sobre los bancos** según las mismas características que determinaron quién recibió más CERA:

- Bancos con más clientela exportadora ex-ante: más expuestos a la apreciación real (margen de exportación cae) **y** receptores naturales de CERA (clientela de mayor patrimonio USD).
- Bancos con más posición en USD ex-ante: más expuestos a la unificación cambiaria parcial **y** correlación 0.88 con shares CERA peak.
- Bancos con más fondeo mayorista vs minorista: más sensibles a la baja de tasas en pesos **y** distinta capacidad de sustitución cross-currency.

Es decir, el confounder macro carga sobre el tratamiento por el mismo eje que el tratamiento mismo. No se arregla con FE de tiempo: requiere FE de tiempo × característica del banco, o cortar la ventana antes del 14-abr-2025. Por eso §4.4 corta en mar-2025 y §5 usa la misma ventana corta para el Paso 1.

Eventos Milei a controlar/evitar dentro de la ventana del paper:
- 14-abr-2025: salida del cepo cambiario para personas humanas; régimen de bandas para empresas.
- 2024-Q4 a 2025-Q3: trayectoria de disinflación rápida (CPI mensual de >12% a <2%).
- 2025: apreciación real fuerte del peso (>30% según métricas estándar).
- 2024-2025: caída sostenida de tasas en pesos (BADLAR, plazos fijos minoristas).
- ago-2023: cambio LELIQ → LEFI (anterior al shock pero relevante para cualquier especificación que use deuda BCRA en pesos como variable de control).

## 5. Diseño de identificación

El proyecto sigue el approach de Greenstone, Mas & Nguyen (2020) y Gutierrez, Jaume & Tobal (2023) en dos pasos:

### Paso 1 — γ̂_b idiosincrático

Descomposición demanda-oferta en el cross-section banco × provincia × tiempo de la variación del crédito pre-post blanqueo, con efectos fijos de provincia y banco. El residuo idiosincrático γ̂_b recoge el componente de oferta del shock USD a cada banco una vez descontada la demanda local.

### Paso 2 — Bartik provincial

Z_p = Σ_b s_{b,p,2023} · γ̂_b

donde s_{b,p,2023} es la participación del banco b en el crédito de la provincia p al 31-diciembre 2023 (predeterminada respecto del shock de jul-2024).

### Outcomes a nivel real

Differences-in-differences con intensidad Bartik Z_p a nivel sector × provincia × tiempo, interactuada con dummy de sector transable-exportador e indicador post-agosto 2024. Outcomes:

- **Empleo registrado** sector × provincia (SIPA, mensual desde 2007).
- **Exportaciones por origen provincial** (INDEC OPEX).
- **Crédito por actividad económica × provincia** (BCRA Préstamos por actividad).

El test clave es si Z_p tiene efecto positivo sobre empleo y exportaciones **fuera del menú regulatorio de aplicaciones USD**. Un coeficiente nulo en sectores no elegibles es evidencia de canal de destino regulado puro; un coeficiente positivo y comparable al del sector elegible es evidencia de canal de sustitución de balance con spillovers reales.

### Cuestiones de exogeneidad

La correlación 0.88 entre share pre-shock y share CERA implica que la dosis es proporcional al tamaño preexistente del banco en USD. Esto **no genera endogeneidad** sino baja variación cross-section en intensidad relativa. La identificación del shock es válida porque:

1. El shock total al sistema es exógeno (la ley es nacional, ningún banco lo causa).
2. La asignación entre bancos es predecible desde shares pre-shock (controlables como observable).
3. La variación residual en intensidad relativa (dosis / tamaño) provee γ̂_b explotable.

El riesgo principal es que la heterogeneidad explotable cross-section sea pequeña. La identificación se complementa con:

- **Within-bank event study** (Khwaja-Mian estilo): cada banco como su propio control, comparar evolución del balance pre/post.
- **Heterogeneidad por constraints regulatorios ex-ante**: bancos cerca de los pisos/topes binding responden distinto al mismo shock proporcional.

## 6. El problema del banco — ingredientes para un modelo

Lo que sigue es una enumeración informal de los elementos que el modelo teórico debería incorporar. No es un modelo, es una lista de chequeo.

### 6.1 Variables de estado del banco

- Patrimonio neto / RPC (capital regulatorio).
- Stock de depósitos en pesos.
- Stock de depósitos en ME, dividido en CERA y no-CERA (relevante por la dinámica de retiro).
- Stock de activos en pesos: crédito al SPNF en pesos, Tesoro pesos, Letras BCRA en pesos, encaje en pesos, interbancario en pesos.
- Stock de activos en ME: crédito al SPNF en ME, Tesoro USD, encaje BCRA en ME, interbancario ME.

### 6.2 Restricciones binding simultáneas

Cuatro restricciones macroprudenciales activas al mismo tiempo:

1. **Encaje 25%** sobre depósitos ME (mecánico).
2. **PGNME ∈ [−30%, +5%] · RPC** (descalce máximo ME). Las CERA entran en este cómputo.
3. **Tesoro USD ≤ 1/3 de aplicaciones ME** (kink en cantidades).
4. **Régimen de Aplicación de Recursos en ME** (menú cerrado de destinos para depósitos ME).

Adicionalmente, restricciones del lado peso:
- Encaje sobre depósitos en pesos.
- Capital regulatorio (Basilea local).
- Liquidez exigida sobre depósitos en pesos.

### 6.3 Funciones objetivo y fricciones

El banco maximiza beneficios o utilidad de los accionistas sujeto a:

- Tasas activas y pasivas exógenas (o endógenas en equilibrio parcial).
- Costos de fricción al traspasar entre canales (por ejemplo, aumentar crédito tiene costos de screening; aumentar Tesoro tiene costos de transacción acotados).
- Riesgo de crédito (default rate sobre crédito a SPNF, función de la composición sectorial).
- **Riesgo de retiro de depósitos**, a la Diamond-Dybvig.

### 6.4 La dimensión Diamond-Dybvig

Hipótesis alternativa testeable: los depósitos CERA tienen **mayor probabilidad de retiro** que los depósitos USD orgánicos.

Razones: el depositante CERA tiene motivos no transaccionales para mantener el depósito (regularización fiscal cumplida, sin necesidad de movimiento operativo); es sensible a la fecha 31-dic-2025; viene de tenencias previamente no declaradas (sugiere preferencias de portafolio distintas, posiblemente más volátiles).

Si el banco internaliza esto, su asignación óptima debería:

- Mantener mayor buffer de liquidez (encaje voluntario por encima del 25% obligatorio, posición spot).
- Privilegiar activos ME de **menor duración** (interbancario corto, Tesoro USD de corto plazo) sobre crédito de mayor duración (préstamos a exportadores típicamente >1 año).

Esta hipótesis es separable empíricamente del mecanismo del proposal original (heterogeneidad por slack de constraints regulatorios) usando la variable: ratio CERA / depósitos USD totales del banco × duración promedio del activo ME post-shock.

Predicción: bancos con ratio CERA/USD-total más alto deberían tener mayor share de activos ME de corto plazo, controlando por slack de capital y otros observables.

### 6.5 La dinámica de transformación CERA → depósito regular

Una pieza importante para el modelo: la transición no es "los fondos salen" sino "los fondos cambian de etiqueta dentro del mismo balance". El banco no pierde el fondeo cuando la CERA se vacía hacia depósitos USD regulares — solo cambia su régimen de tratamiento por parte del depositante.

Esto sugiere que la elección óptima de duración del activo no debería responder mucho a la dinámica de la CERA per se, sino a la expectativa del banco sobre la **persistencia conjunta de CERA + depósitos USD regulares derivados**. Si el banco anticipa que los fondos van a quedarse (reclasificados pero presentes), puede tomarlos como fondeo estable y prestarlos a largo plazo.

Los datos muestran exactamente eso ex-post: 65% del shock fue a crédito ME, sugiriendo que los bancos efectivamente trataron el flujo como persistente.

### 6.6 Heterogeneidad bank-level explotable

Variables observables por banco que pueden generar respuestas heterogéneas ante el mismo shock proporcional:

- **Slack de capital regulatorio ex-ante** (RPC / mínimo). Bancos con más slack pueden expandir más balance en pesos vía sustitución cross-currency.
- **Exposición exportadora ex-ante de la cartera ME** (share de capítulo 135 sobre total activos ME, especialmente sub-aperturas 135199/135499/135799). Bancos con cartera más concentrada en exportadores enfrentan retornos decrecientes al expandir más.
- **Distancia al piso de PGNME** (PGNME ex-ante / −30% RPC). Los más cerca del piso tienen menos margen para absorber CERA sin cumplir el matching ME activo / ME pasivo.
- **Distancia al tope de Tesoro USD** (Tesoro USD ex-ante / 1/3 de aplicaciones ME). Los más cerca del tope tienen menos margen para absorber CERA vía Tesoro.
- **Estructura de fondeo mayorista vs minorista**. Bancos más dependientes de mayorista tienen restricción de capital más binding al margen del negocio en pesos.
- **Ratio CERA / depósitos USD totales** del banco. Variable nueva propuesta para capturar la hipótesis Diamond-Dybvig.

## 7. Convenciones de medición

Para que el modelo y la empírica conversen sin ambigüedad:

- **Saldos del balance BCRA**: convención contable. Pasivos con signo negativo. Magnitud económica = `abs(saldo)`.
- **Saldos en ME**: reportados en pesos al tipo de cambio contable (≈ A-3500 de fin de mes). Para magnitudes USD reales, dividir por A-3500.
- **PGNME**: el ratio "ME negativo / RPC" se calcula con signo. Estar "en el piso de −30%" significa que pasivos ME superan activos ME en hasta 30% del PN.
- **El "shock" del paper**: de junio 2024 a enero 2026, depósitos USD del SPNF subieron de USD 20B a USD 41B. Aumento incremental sobre tendencia: ≈USD 21B. La cuenta específica CERA capturó USD 12B en el peak, gran parte luego reclasificada.
- **Período de análisis**: ventana ±12 a ±18 meses alrededor de agosto 2024 para event study; ene-2024 a ene-2026 para descripciones.
- **Robustez**: blanqueo Macri 2016-17 (Ley 27.260) como contrafactual descriptivo. Códigos de cuenta en el plan contable: 311781, 311782, 311783, 315781, 315782, 315783.

## 8. Datos disponibles

Todos ya bajados y procesados en el repo del proyecto.

### Panel principal a nivel banco

- `panel_balance_mensual_proforma.parquet`: ~1.35M filas, 73 entidades, 2020-01 a 2026-01. Una fila por (banco, mes, código de cuenta) con saldo en pesos. Pro-forma consolida Macro+BMA.
- Versión as-is sin pro-forma también disponible para robustez.
- Versión pre-2020 (1994-2019, moneda corriente, ruptura NIIF documentada) para análisis del blanqueo Macri.

### Otros paneles

- Panel banco × provincia × trimestre de préstamos y depósitos (`panel_distribgeo`).
- Panel sector × provincia × trimestre de financiaciones por actividad (datos BCRA).
- Panel banco × trimestre de indicadores CAMELS (40 ratios prudenciales).
- Panel banco × trimestre de morosidad por situación (esd).
- Panel banco × dump de empleados, clientes, cuentas (inf_adi).
- Series diarias del BCRA: A-3500, CER, UVA, BADLAR, reservas, base monetaria.
- Series mensuales: IPC INDEC nacional, SIPA empleo provincia × CIIU.
- Cotizaciones diarias: oficial, blue, MEP, CCL.
- Histórico OPEX 1993-2018; pendiente 2019-2025.

### Crosswalks

- Cuenta BCRA → categoría económica (CERA, crédito ME SPNF, deuda BCRA pesos unificando LELIQ+LEFI, etc.).
- Fusiones bancarias con flag de aplicación pro-forma.
- Provincias con códigos ISO 3166-2:AR.

## 9. Referencias clave

### Empíricas

- Khwaja & Mian (2008). "Tracing the Impact of Bank Liquidity Shocks: Evidence from an Emerging Market". *AER*.
- Chodorow-Reich (2014). "The Employment Effects of Credit Market Disruptions". *QJE*.
- Paravisini, Rappoport, Schnabl & Wolfenzon (2015). "Dissecting the Effect of Credit Supply on Trade". *RES*.
- Greenstone, Mas & Nguyen (2020). "Do Credit Market Shocks Affect the Real Economy?". *AEJ Applied*.
- Jiménez, Ongena, Peydró & Saurina (2017). "Macroprudential Policy, Countercyclical Bank Capital Buffers, and Credit Supply". *JPE*.
- Gutiérrez, Jaume & Tobal (2023). "Do Credit Supply Shocks Affect Employment in Middle-Income Countries?". *AEJ Macro*.
- Borusyak, Hull & Jaravel (2025). "A Practical Guide to Shift-Share Instruments".

### Teóricas

- Diamond & Dybvig (1983). "Bank Runs, Deposit Insurance, and Liquidity". *JPE*.
- Bianchi (2011). "Overborrowing and Systemic Externalities in the Business Cycle". *AER*.
- Bianchi & Bigio (2022). "Banks, Liquidity Management, and Monetary Policy". *Econometrica*.
- Korinek (2018). "Regulating Capital Flows to Emerging Markets". *AER P&P*.
- Ize & Levy Yeyati (2003). "Financial Dollarization". *JIE*.

### Normativa argentina central

- Ley 27.743 (Medidas Fiscales Paliativas y Relevantes), Título II — Régimen de Regularización de Activos.
- Decreto 608/2024 — reglamentación; Decreto 864/2024 — prórroga Etapa 1.
- BCRA Comunicación "A" 8062 (15-jul-2024) — creación CERA.
- BCRA Comunicación "A" 8071 (23-jul-2024) — alta de las cuatro cuentas en el plan contable.
- BCRA Comunicación "A" 8110 — umbral USD 100.000 y operaciones onerosas.
- TO BCRA Política de Crédito (Com. A 8202) — Aplicación de Recursos en ME.
- TO BCRA PGNME (Com. A 8360).
- TO BCRA Efectivo Mínimo (Com. A 8397).
- Resolución 590/2024 Ministerio de Economía — destinos permitidos para fondos CERA.
