# 🧭 Roadmap del Proyecto

## 🎯 Objetivo principal
Sistema de agentes legales autónomos que:
- Analicen documentos jurídicos
- Se automejoren
- Generen outputs estructurados
- Reduzcan tiempo dedicado a tareas repetitivas

---

## 📦 Fase 1 — Sentencia Analyzer
- [x] Lectura de inputs
- [x] Generación de resumen
- [x] Output JSON
- [x] Validación automática (`validate_v2.ps1`)
- [x] Métricas de calidad (`eval_gold.ps1`, Gold de 35 documentos, 9 campos de cabecera)
- [ ] Evaluación de **contenido**: `facts`, `applied_rules`, `ratio_summary` y `holding` solo
      tienen control de forma. Un output puede pasar las dos comprobaciones y contener un
      razonamiento equivocado
- [ ] Corpus nuevo con el que volver a medir

> ⚠️ **El conjunto de test está gastado.** Los 13 documentos de `sentencia23`–`sentencia35` se
> evaluaron el 05/08/2026 y dieron **313/315 (99,4 %)**, la única medición ciega que existe.
> Después se corrigieron dos reglas del estándar —acentos en `ponente`, prefijo en `ecli`—
> **mirando esos fallos**, y se reprocesaron los dos documentos afectados hasta 315/315. Ese
> 100 % confirma que las reglas funcionan; no mide generalización.
>
> A partir de aquí, dev y test miden lo mismo: rendimiento sobre documentos que el estándar ya
> ha visto. **Cualquier medición honesta de generalización exige un corpus nuevo**, y conviene
> reservarlo sin mirarlo antes de la siguiente ronda de ajustes.

---

## 📦 Fase 2 — Contract Analyzer (ACTUAL)

Orden estricto: el paso 2 depende del 1, y el 5 del 4. La métrica va primero **a propósito**:
en la fase 1 el esquema se diseñó antes de saber cómo se iba a medir, y los campos sustantivos
—los que aportan el valor real— se quedaron sin evaluación de contenido. En contratos casi todo
el esquema es sustantivo, así que ese error saldría mucho más caro.

- [x] **1. Métrica de evaluación para campos sustantivos.**
      [`corpus/metrica-contratos.md`](../corpus/metrica-contratos.md) — decidida el 06/09/2026,
      antes de anotar ningún documento. Adopta el esquema de **ContractEval** (arXiv 2508.03080)
      con dos desviaciones documentadas, en vez de diseñar una métrica propia: el problema ya
      estaba resuelto y así los resultados son comparables con la literatura. Tres niveles que
      **no se agregan** —mecánicos por igualdad exacta, detección por F1/F2/Jaccard/pereza,
      texto libre fuera de la métrica—; unidad de medida el **criterio anotado**, no el
      documento; **F2** como métrica principal porque pondera la exhaustividad; y `severity`
      medida **aparte** de la detección
- [x] **2. Alcance del corpus.** [`corpus/alcance.md`](../corpus/alcance.md) — criterios de
      inclusión y exclusión por vía, escritos **antes** de descargar nada. Este paso se saltó en
      la iteración anterior y produjo la depuración a posteriori
- [x] **3. Esquema con régimen.** `standards/contratos.md` **v3** (06/09/2026), revisado contra
      la métrica del paso 1. Frente al v1: `standard_version` verificable; anclaje al texto
      (`cita` verbatim + `localizador`) en `key_clauses` y `risk_flags`; `condicion_adherente`,
      del que `control_aplicable` pasa a ser derivable; `risk_flags[].id` y `criterio` como
      vocabularios cerrados; y semántica de `missing_clauses` por lista de referencia.
      **El eje de régimen se rehízo en v3**: `administrativo | condiciones_generales`, uno por
      vía viva, en lugar de `consumo | administrativo | mercantil`, que mezclaba la fuente del
      control con su consecuencia. **`severity` pasa a ser derivada** de `severity_driver` y
      `desproporcion`, dejando el juicio en una sola casilla acotada. Ninguna versión anterior
      produjo output: no hay nada que migrar. **Pendiente el `validate_contratos.ps1`**
- [ ] **4. Rúbrica de `risk_flags`** (`corpus/rubrica-riskflags.md`) — **siguiente paso, y el
      único que bloquea todo lo demás**. Cada flag con identificador, definición, régimen
      aplicable, su `criterio` y su `severity_driver` típicos, consecuencia jurídica y ejemplo de
      cláusula. Se extrae de las 9 resoluciones de la vía C, verificando en cada una si juzga a
      un consumidor o a un adherente empresario —lo que se registra en la columna
      `condicion_adherente` del inventario—. **Redactar antes de anotar ningún documento**: el
      esquema v3 exige que `risk_flags[].id` exista en la rúbrica, así que sin ella el estándar
      no es aplicable. Incluye también las **listas de referencia de `missing_clauses`** por
      régimen
- [ ] **5. `contrato_agent`.** Definición del agente, remitiendo a `standards/contratos.md` sin
      duplicar reglas, como hace `sentencia_agent`
- [ ] **6. Gold.** Ficheros de referencia anotados a mano contra la rúbrica. Contrastar cada
      valor con el documento antes de darlo por bueno: en el Gold de sentencias, 6 de las 8
      discrepancias de la primera evaluación del test eran errores del Gold, no del agente.
      **Antes de anotar los 23, anotar 5 y medir el acuerdo consigo mismo** (protocolo en
      `metrica-contratos.md`): dos semanas de reposo, reanotación a ciegas, y F1 < 0,75
      significa que el problema está en la rúbrica. Cuesta 5 documentos descubrirlo; descubrirlo
      al final cuesta 23
- [ ] **7. Evaluación.** Primera medición con la métrica del paso 1, sobre ciego-1 y registrada
      en [`corpus/evaluaciones.md`](../corpus/evaluaciones.md)
- [ ] **8. Scripts de PLACSP.** Solo cuando 1–7 estén cerrados: descarga del ZIP mensual de
      sindicación, parseo ATOM/CODICE, filtrado por CPV e importe, muestreo con semilla fija,
      `pdftotext -layout`, y partición ciego-1 / ciego-2

### Alcance del corpus: dos vías, un régimen cada una, métricas separadas

Corpora y métricas **separados**. No se agregan en una sola tabla de precisión.

| Vía | Régimen | Fuente | Función | Volumen esperado |
|---|---|---|---|---|
| **A — Administrativa** (principal) | `administrativo` | PLACSP: sindicación ATOM + pliegos PCAP/PPT | Volumen, datos reales de ambas partes, medida del pipeline mecánico | Cientos, escalable |
| **C — Condiciones generales** (soporte) | `condiciones_generales` | Clausulado de adhesión + resoluciones de CENDOJ | Material anotable **y** fuente de verdad de la rúbrica | Decenas |

**Corpus descargado ≠ corpus anotado.** La vía A escala a cientos en la descarga, pero el
corpus *anotado* seguirá siendo de decenas. El cuello de botella es la anotación, no la
obtención: no confundir ambas cifras al reportar tamaño.

> **La vía B queda eliminada (06/09/2026), no diferida.** El régimen mercantil negociado sale
> del estándar: un contrato libremente negociado no tiene control de contenido ni lista de
> referencia defendible, así que `missing_clauses` registraría la opinión del anotador y
> `risk_flags` produciría hallazgos sin consecuencia jurídica a la que referirlos. Se suma el
> motivo ya registrado el 25/08 —los contratos íntegros de la CNMV son raros y su clausulado
> está muy alejado del resto—. Una vía diferida durante meses y de obtención dudosa no es una
> vía, es una intención. Detalle en [`corpus/alcance.md`](../corpus/alcance.md).

> **Dentro de la vía C conviven dos controles, y eso no la parte en dos vías.** `condicion_adherente`
> distingue al consumidor (control de contenido y transparencia, TRLGDCU) del empresario (solo
> incorporación y transparencia, Ley 7/1998). El corpus ya tiene un caso de adherente empresario,
> `adhesion-05`. La procedencia es la misma, así que la vía es la misma; el desglose por control
> se reporta dentro de ella.

### Composición del corpus

> **Instantánea: 06/09/2026, posterior a la eliminación de la vía B.** Total en disco: **30**.
> Activos: **20**. Pendientes de depurar: **3**. Depurados: **7**. 20 + 3 + 7 = 30. Inventario
> con hashes en [`corpus/inventario-contratos.csv`](../corpus/inventario-contratos.csv);
> criterio de cribado en
> [`corpus/candidatos-descartados.md`](../corpus/candidatos-descartados.md).

| Vía | Función | Documentos | N |
|---|---|---|---|
| A | evaluación | `pliego-01` a `03` — servicios, concesión demanial, obras | 3 |
| C | evaluación | `adhesion-01` a `08` — banca, telecos, energía, seguros, seguridad. `05` es el único de adherente empresario | 8 |
| C | rúbrica | `resolucion-01` a `09` — 4 casación, 3 apelación, 1 ordinario, 1 auto | 9 |
| B | **pendiente de depurar** | `plantilla-01` a `03` — vía eliminada del alcance | 3 |
| — | depurado | fuera de alcance (3), redundantes (3), truncado (1) | 7 |

> ⚠️ **Paso manual pendiente.** Los 3 de `plantilla-*` siguen físicamente en
> `Inputs/corpus/via-b/`. Están como `pendiente_depurar` y no como `depurado` para que el
> inventario no afirme algo que el disco no confirma. Al moverlos a `Inputs/_depurados/` hay que
> actualizar su columna `archivo` y su `estado`.

**El inventario lleva dos columnas, `via` y `funcion`, a propósito.** `via` es la
**procedencia** —y es el eje por el que se separan las métricas—; `funcion` es **para qué
sirve** el documento dentro de su vía. Mezclarlas en una sola columna fue lo que bloqueó el
inventario: un contrato de Orange y una STS sobre revolving comparten función pero no
procedencia, y no se pueden agregar en la misma medición.

**Estructura en disco:** `Inputs/corpus/via-{a,b,c}/` y `Inputs/_depurados/`. El renombrado del
25/08/2026 no alteró ningún contenido —los 30 `sha256` son idénticos a los previos— y el
inventario conserva el nombre anterior en `archivo_origen`. La reclasificación del 06/09/2026
tampoco tocó ningún byte: solo columnas del inventario, y los 30 hashes siguen siendo los mismos.

**El inventario gana la columna `condicion_adherente`**, que es donde se registra la
verificación consumidor/empresario documento a documento. Las 9 resoluciones están
`por_verificar`: es trabajo de la rúbrica, y ahora está visible fila a fila en vez de en una nota
al pie.

### Corrección del blocker de `risk_flags`

**Redacción anterior (incorrecta):** *«Cero contratos negociados con datos reales de ambas
partes, que es justo lo que hace falta para anotar `risk_flags`.»*

El corpus fusionaba dos necesidades independientes. La **extracción** de partes, importes,
fechas y plazos sí exige documentos con datos reales; la **anotación de `risk_flags` no**. El
riesgo de una cláusula depende de su texto y sus cifras, no de la identidad de quien firma: un
contrato de adhesión con el adherente anonimizado es plenamente anotable. Lo que faltaba no
eran contratos bilaterales con datos reales — era una **fuente de verdad externa** sobre qué
constituye riesgo y por qué. Esa fuente son las 9 resoluciones de la vía C.

Consecuencia: los documentos que la iteración anterior daba por descartables **son el corpus**.
Los 3 pliegos pasan a ser el núcleo de la vía A; las 9 resoluciones, la fuente de la rúbrica;
los 8 de adhesión, material anotable. Se verificó que **las nueve** tratan de abusividad o
condiciones generales — la redacción anterior solo reconocía tres, e infravaloraba seis
documentos válidos. La más rica es `resolucion-05` (44 menciones a abusividad, 22 a condiciones
generales, 49 a transparencia); la más marginal, `resolucion-03`.

### Depuración

**Regla: nada se elimina.** Todo documento excluido se mueve a `Inputs/_depurados/` con su
motivo en el inventario. El precedente que la motivó: el antiguo nº 16 (sociedad de capital e
industria, **derecho argentino**, Ley 19.550) se **borró** el 06/08/2026 en vez de apartarse, y
como `Inputs/` está en `.gitignore` no hay copia recuperable. Se da por perdido.

Los 7 depurados actuales, por motivo:

- **Fuera de alcance (3).** `laboral-representante-comercio` (relación laboral especial,
  RD 1438/1985: exigiría un cuarto régimen y una rúbrica propia), `convenio-subvencion` (es un
  convenio administrativo, no un contrato) y `comentario-doctrinal` (fuente secundaria, no
  transcribe clausulado original). Los tres se excluyen por el mismo criterio: **un documento
  que obligue a crear referencias nuevas para poder analizarse no entra en esta iteración.**
- **Redundantes (3).** De cuatro arrendamientos de vivienda casi intercambiables se conserva
  `plantilla-01`, el de mayor cobertura (408 líneas) y con placeholders nombrados que
  identifican qué campo va en cada hueco. Redundancia no es cobertura.
- **Truncado (1).** 35 bytes, solo el título.

> El corpus **no está versionado** y seguirá sin estarlo: contiene datos personales reales
> (nombres de cliente, protocolo notarial, NIF) que no deben entrar en un histórico inmutable.
> La protección es doble: copia externa con `robocopy` tras cada depuración, y los `sha256` del
> inventario, que convierten cualquier pérdida silenciosa en una detectable.

### Riesgos abiertos de esta fase

> ⚠️ **El muestreo se rompe si se filtra después.** Parte de los pliegos de PLACSP son PDF
> escaneados sin capa de texto. Descartarlos *después* de muestrear sesga la muestra hacia los
> órganos con mejor ofimática. Comprobar extractabilidad **antes** de muestrear.

> ✅ **El tamaño: resuelto en el paso 1, no por tener más documentos.** La unidad de medida
> pasa a ser el **criterio anotado** en vez del documento, y ~23 documentos × 15-25 unidades dan
> varios centenares de unidades en vez de decenas. Como las unidades de un mismo documento **no
> son independientes**, no se calculan intervalos de confianza sobre ellas: para comparar
> versiones se usa la **regla del documento único** —si quitar cualquier documento invierte el
> resultado, la comparación no vale—, y queda escrito que **la primera medición es
> orientativa**. Detalle en [`corpus/metrica-contratos.md`](../corpus/metrica-contratos.md).

> ⚠️ **Condición del adherente de las 9 resoluciones, sin verificar.** Todas tratan de
> abusividad, pero algunas pueden juzgar a un adherente **empresario** (Ley 7/1998, solo control
> de incorporación y transparencia). Confirmar documento a documento al redactar la rúbrica: son
> dos niveles de control distintos, no un mismo régimen atenuado.
>
> Desde el 06/09/2026 están marcadas `condicion_adherente: por_verificar` en el inventario, en
> lugar de `consumo` por defecto — que era una suposición presentada como dato. El trabajo
> pendiente queda visible fila a fila en vez de en una nota al pie.

**Corpus de arranque, no definitivo.** Hay recopilación de contratos nuevos pendiente, y los
actuales no son intocables. Toda incorporación pasa por `corpus/alcance.md` **antes** de
descargarse, y se registra en el inventario con su URL y fecha en el momento de la descarga.

---

## 📦 Fase 3 — Agente Universidad
- [ ] Resúmenes de apuntes
- [ ] Generador de esquemas
- [ ] Planificador de estudio
- [ ] Q&A automático

---

## 📦 Fase 4 — Legal Intelligence Agent
- [ ] Noticias jurídicas
- [ ] Legal tech
- [ ] Tendencias
- [ ] Alertas personalizadas

---

## 📦 Fase 5 — Sistema de Automejora
- [ ] Feedback loop
- [ ] Evaluación outputs
- [ ] Ajuste automático de prompts