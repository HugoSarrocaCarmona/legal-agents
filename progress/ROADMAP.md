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

- [ ] **1. Decidir la métrica de evaluación para campos sustantivos.** Qué significa que un
      riesgo esté bien detectado, que falte una cláusula o que un resumen sea correcto. La
      comparación exacta que da el 100 % en `ecli` o `decision_date` no sirve para
      `risk_flags`, `key_clauses` ni `missing_clauses`. Opciones a valorar: solapamiento sobre
      conjuntos anotados (precisión/exhaustividad por cláusula), rúbrica con revisión humana
      muestreada, o juicio por modelo con criterios fijos. **Sin esto, los pasos 2 y 4 se
      diseñan a ciegas**
- [x] **2. Alcance del corpus.** [`corpus/alcance.md`](../corpus/alcance.md) — criterios de
      inclusión y exclusión por vía, escritos **antes** de descargar nada. Este paso se saltó en
      la iteración anterior y produjo la depuración a posteriori
- [x] **3. Esquema con régimen.** `standards/contratos.md` v1: `risk_flags` lleva `regimen` y
      `control_aplicable`. Pendiente el `validate_contratos.ps1` y la revisión contra la métrica
      del paso 1
- [ ] **4. Rúbrica de `risk_flags`** (`corpus/rubrica-riskflags.md`). Cada flag con
      identificador, criterio, régimen aplicable, consecuencia jurídica y ejemplo de cláusula.
      Los criterios se extraen de las 9 resoluciones de la vía C. **Redactar antes de anotar
      ningún documento**
- [ ] **5. `contrato_agent`.** Definición del agente, remitiendo a `standards/contratos.md` sin
      duplicar reglas, como hace `sentencia_agent`
- [ ] **6. Gold.** Ficheros de referencia anotados a mano contra la rúbrica. Contrastar cada
      valor con el documento antes de darlo por bueno: en el Gold de sentencias, 6 de las 8
      discrepancias de la primera evaluación del test eran errores del Gold, no del agente
- [ ] **7. Evaluación.** Primera medición con la métrica del paso 1, sobre ciego-1 y registrada
      en [`corpus/evaluaciones.md`](../corpus/evaluaciones.md)
- [ ] **8. Scripts de PLACSP.** Solo cuando 1–7 estén cerrados: descarga del ZIP mensual de
      sindicación, parseo ATOM/CODICE, filtrado por CPV e importe, muestreo con semilla fija,
      `pdftotext -layout`, y partición ciego-1 / ciego-2

### Alcance del corpus: tres vías, métricas separadas

Corpora y métricas **separados**. No se agregan en una sola tabla de precisión.

| Vía | Fuente | Función | Volumen esperado |
|---|---|---|---|
| **A — Administrativa** (principal) | PLACSP: sindicación ATOM + pliegos PCAP/PPT | Volumen, datos reales de ambas partes, medida del pipeline mecánico | Cientos, escalable |
| **B — Mercantil negociada** (**diferida**) | CNMV: registros oficiales con contrato anexo | Clausulado genuinamente negociado: covenants, reps & warranties, MAC, indemnidades | Decenas |
| **C — Condiciones generales** (soporte) | Clausulado de adhesión + resoluciones de CENDOJ | Material anotable **y** fuente de verdad de la rúbrica | Decenas |

**Corpus descargado ≠ corpus anotado.** La vía A escala a cientos en la descarga, pero el
corpus *anotado* seguirá siendo de decenas. El cuello de botella es la anotación, no la
obtención: no confundir ambas cifras al reportar tamaño.

> **La vía B queda diferida, no paralela.** Los contratos íntegros anexados a la CNMV son
> raros —lo habitual es el resumen— y los que hay son de M&A y financiación, con clausulado
> muy alejado del resto. Declararla "en paralelo" con todo lo demás pendiente equivale a que no
> ocurra. Se abre cuando A y C estén cerradas.

### Composición del corpus

> **Instantánea: 25/08/2026, posterior a la reestructuración por vías.** Total en disco:
> **30**. Activos: **23**. Depurados: **7**. 23 + 7 = 30. Inventario con hashes en
> [`corpus/inventario-contratos.csv`](../corpus/inventario-contratos.csv); criterio de cribado
> en [`corpus/candidatos-descartados.md`](../corpus/candidatos-descartados.md).

| Vía | Función | Documentos | N |
|---|---|---|---|
| A | evaluación | `pliego-01` a `03` — servicios, concesión demanial, obras | 3 |
| B | vocabulario | `plantilla-01` a `03` — arrendamiento, sociedad civil, servicios | 3 |
| C | evaluación | `adhesion-01` a `08` — banca, telecos, energía, seguros, seguridad | 8 |
| C | rúbrica | `resolucion-01` a `09` — 4 casación, 3 apelación, 1 ordinario, 1 auto | 9 |
| — | depurado | fuera de alcance (3), redundantes (3), truncado (1) | 7 |

**El inventario lleva dos columnas, `via` y `funcion`, a propósito.** `via` es la
**procedencia** —y es el eje por el que se separan las métricas—; `funcion` es **para qué
sirve** el documento dentro de su vía. Mezclarlas en una sola columna fue lo que bloqueó el
inventario: un contrato de Orange y una STS sobre revolving comparten función pero no
procedencia, y no se pueden agregar en la misma medición.

**Estructura en disco:** `Inputs/corpus/via-{a,b,c}/` y `Inputs/_depurados/`. El renombrado del
25/08/2026 no alteró ningún contenido —los 30 `sha256` son idénticos a los previos— y el
inventario conserva el nombre anterior en `archivo_origen`.

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

> ⚠️ **El tamaño no da para lo que se quiere medir.** Corpus anotado de decenas, partido en
> ciego-1 y ciego-2, deja ~20 documentos por partición. Para un campo multietiqueta como
> `risk_flags`, los intervalos de confianza serán tan anchos que casi cualquier diferencia
> entre versiones será indistinguible del ruido. **Fijar el tamaño mínimo por partición antes
> de anotar**, o asumir por escrito que la primera medición es orientativa.

> ⚠️ **Régimen de las resoluciones sin verificar.** Las 9 están marcadas `consumo` por defecto.
> Algunas pueden ser de adherente empresario (Ley 7/1998, solo control de incorporación y
> transparencia). Confirmar documento a documento al redactar la rúbrica: son dos niveles de
> control distintos, no un mismo régimen atenuado.

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