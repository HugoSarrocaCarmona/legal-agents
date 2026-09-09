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

## 📦 Fase 2 — Analizador de riesgo de ejecución de pliegos (ACTUAL)

> **Reorientada el 09/09/2026.** Deja de ser un «Contract Analyzer» genérico sobre tres
> regímenes y pasa a ser una sola cosa: **estimar qué riesgos de ejecución asume un licitador
> que gana un contrato público español.** El razonamiento de mercado que lo motiva está en
> [`research/02-oportunidad-mercado-espanol.md`](../research/02-oportunidad-mercado-espanol.md);
> aquí solo constan las consecuencias operativas.

**Por qué este giro y no otro.** Es el único frente donde coinciden las cuatro cosas: corpus
**abierto y reutilizable** (PLACSP, frente a un CENDOJ que prohíbe descarga masiva y uso
comercial), **volumen real** (más de 201.000 expedientes en 2025), **destinatario que paga**
—la empresa licitadora, no el abogado— y **ausencia de secreto profesional y de datos de
cliente**, que es lo que mantiene el proyecto fuera del Anexo III del Reglamento de IA y de las
obligaciones de encargo de tratamiento de la Circular 3/2026 del CGAE.

Orden estricto: cada paso depende del anterior. La métrica va primero **a propósito**: en la
fase 1 el esquema se diseñó antes de saber cómo se iba a medir, y los campos sustantivos —los
que aportan el valor real— se quedaron sin evaluación de contenido. Aquí casi todo el esquema
es sustantivo, así que ese error saldría mucho más caro.

- [x] **1. Métrica de campos sustantivos.** [`corpus/metrica.md`](../corpus/metrica.md).
      **Cierra el bloqueo que tenía parada la fase.** La decisión que lo desatasca: `risk_flags`
      no es un campo homogéneo, sino dos —`normativo`, comprobable contra la LCSP, y
      `valorativo`, que es juicio— y cada clase lleva su propia métrica, reportada por separado.
      Fija además unidad de medida (la cláusula), regla de emparejamiento (`id` + ancla),
      tratamiento de `severity`, fallos duros y tamaño mínimo con cifra
- [x] **2. Alcance del corpus.** [`corpus/alcance.md`](../corpus/alcance.md) — criterios de
      inclusión y exclusión por vía, escritos **antes** de descargar nada. Este paso se saltó en
      la iteración anterior y produjo la depuración a posteriori
- [x] **3. Esquema.** `standards/contratos.md` **v2**: ámbito operativo estrechado a
      `regimen = administrativo`; `risk_flags` incorpora `clase`, `base_normativa`,
      `clausula_ref` y `materia`; `missing_clauses` pasa a exigir `base_normativa`; vocabulario
      cerrado de 16 materias con su ancla en la LCSP verificada contra el BOE
- [ ] **4. Rúbrica de riesgos LCSP** (`corpus/rubrica-riesgos-lcsp.md`). **Siguiente tarea.**
      Catálogo **cerrado** —no una guía— con un `id` por flag, su clase, su materia, y según la
      clase: `base_normativa` verificada o `criterio`. Con ejemplo de cláusula real tomado de
      `pliego-01` a `03`. **Redactar antes de anotar ningún documento**, porque la métrica del
      paso 1 empareja por `id`: sin vocabulario cerrado no hay medición posible
- [ ] **5. `validate_contratos.ps1`.** Comprobación mecánica: `id` dentro del catálogo,
      coherencia `clase` ↔ `base_normativa`, coincidencia de `regimen`, vocabulario de
      `consecuencia_juridica` por régimen, y `base_normativa` presente en todo `missing_clauses`
- [ ] **6. `pliego_agent`.** Definición del agente, remitiendo a `standards/contratos.md` y a la
      rúbrica sin duplicar reglas, como hace `sentencia_agent`
- [ ] **7. Gold.** Ficheros de referencia anotados a mano contra la rúbrica. Contrastar cada
      valor con el documento antes de darlo por bueno: en el Gold de sentencias, 6 de las 8
      discrepancias de la primera evaluación del test eran errores del Gold, no del agente
- [ ] **8. Evaluación.** Primera medición sobre ciego-1, registrada en
      [`corpus/evaluaciones.md`](../corpus/evaluaciones.md) **antes** de mirar el resultado.
      Recordatorio del compromiso del paso 1: la clase valorativa es orientativa hasta los ~100
      flags por partición y no decide entre versiones; la normativa sí, desde 40
- [ ] **9. Scripts de PLACSP.** Solo cuando 1–8 estén cerrados: descarga del ZIP mensual de
      sindicación, parseo ATOM/CODICE, filtrado por CPV e importe, comprobación de
      extractabilidad **antes** de muestrear, muestreo con semilla fija, `pdftotext -layout`, y
      partición ciego-1 / ciego-2

### Alcance del corpus tras el giro

| Vía | Estado tras el 09/09/2026 | Función |
|---|---|---|
| **A — Administrativa** (PLACSP) | **Única vía de evaluación** | Corpus, Gold y métrica. Es el producto |
| **B — Mercantil negociada** (CNMV) | **Cerrada en esta iteración** | Ninguna. Ya no es «diferida»: no se abre |
| **C — Condiciones generales** | **Degradada a fuente de criterios** | Las 9 resoluciones aportan los *criterios* valorativos transferibles. **Deja de ser corpus anotable** |

**El cambio real es el de la vía C.** El plan anterior extraía la rúbrica de las 9 resoluciones
de consumo. Eso era correcto para un analizador de condiciones generales y es **inadecuado para
un pliego**: el control de abusividad del TRLGDCU es valorativo casi por entero, mientras que el
riesgo administrativo tiene anclas numéricas en la propia LCSP. **La fuente primaria de la
rúbrica pasa a ser la LCSP**; las resoluciones quedan solo como origen de los cinco criterios
valorativos ya recogidos en `standards/contratos.md`.

Los 8 documentos de adhesión (`adhesion-01` a `08`) **no se anotan**. No se depuran ni se
borran —siguen en disco y en el inventario— pero salen del camino crítico.

**Corpus descargado ≠ corpus anotado.** La vía A escala a cientos en la descarga; el corpus
*anotado* será de decenas. El cuello de botella es la anotación, no la obtención: no confundir
ambas cifras al reportar tamaño. Objetivo fijado en `corpus/metrica.md`: **30–40 pliegos
anotados en total**, 15–20 por partición.

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

> **Matización del 09/09/2026, tras el giro a pliegos.** El razonamiento de arriba sigue siendo
> correcto —lo que faltaba era una fuente de verdad externa, no contratos bilaterales— pero
> **la fuente de verdad ha cambiado**. Para el régimen administrativo la fuente primaria es la
> **LCSP**, que fija umbrales numéricos donde el TRLGDCU solo ofrece un estándar valorativo.
> Las 9 resoluciones conservan una función más estrecha: aportan los **cinco criterios
> valorativos transferibles**, no el catálogo de flags. Los 8 de adhesión dejan de ser material
> anotable en esta iteración. Ninguno de los 30 documentos se depura por esto: cambian de
> función, no de estado.

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

> ✅ **El tamaño de muestra queda cerrado.** Lo resuelve `corpus/metrica.md`: se mide por
> cláusula y no por documento, con intervalos remuestreados por documento para no inflar la
> confianza; mínimos fijados en 40 flags por partición para medir y ~100 valorativos para
> comparar versiones; y compromiso escrito de que la clase valorativa es orientativa hasta
> alcanzarlos. El riesgo no desaparece —se acota y se declara.

> ✅ **El régimen de las 9 resoluciones deja de ser bloqueante.** Al pasar la vía C de corpus
> anotable a fuente de criterios, ya no hace falta clasificar cada resolución como consumo o
> adherente empresario para poder anotar: de ellas solo se extraen los cinco criterios
> valorativos, que son transferibles entre regímenes por definición. La verificación sigue
> siendo necesaria **si algún día se reabre la vía C como corpus**, no ahora.

> ⚠️ **Riesgo nuevo introducido por el giro: la `base_normativa` inventada.** Un flag
> `normativo` que cite un artículo de la LCSP que no dice lo que se le atribuye es la versión
> contractual de la sentencia inventada, y es peor que no emitir el flag. `corpus/metrica.md` lo
> trata como **fallo duro con cero tolerancia**: un solo caso bloquea la versión. Mitigación
> obligatoria en la rúbrica: cada `base_normativa` se transcribe del texto consolidado del BOE
> al redactar el catálogo, no se cita de memoria.

> ⚠️ **Riesgo de sesgo por órgano de contratación.** Los pliegos se redactan sobre plantillas
> de cada órgano. Un corpus concentrado en pocos órganos mide rendimiento sobre sus plantillas,
> no sobre la contratación pública española. El inventario ya registra el órgano; falta
> **estratificar por él al muestrear** y no dar por generalizable una medición que no lo haga.

**Corpus de arranque, no definitivo.** Hay recopilación de contratos nuevos pendiente, y los
actuales no son intocables. Toda incorporación pasa por `corpus/alcance.md` **antes** de
descargarse, y se registra en el inventario con su URL y fecha en el momento de la descarga.

---

## 📦 Fase 3 — Vigilancia normativa (estrecha, transversal)

> **Reclasificada el 09/09/2026: deja de ser una fase posterior y pasa a correr en paralelo,
> porque es lo que sostiene el criterio jurídico del que depende la fase 2.** El precio de que
> funcione es que sea **estrecha**. Un recopilador de «IA + legaltech + noticias globales +
> regulación» es inmantenible por una persona y no aporta ventaja; uno acotado a la materia del
> proyecto, sí.

Ámbito cerrado — nada fuera de esta lista:

- [ ] **LCSP y doctrina de contratación pública.** Resoluciones del TACRC y de los tribunales
      administrativos autonómicos, y modificaciones de la Ley 9/2017. Es la materia prima de la
      rúbrica: cada resolución relevante es un candidato a flag nuevo
- [ ] **Reglamento de IA y su calendario.** Anexo III, aplazamiento del Reglamento Ómnibus
      (UE) 2026/1744 al 02/12/2027, actos de ejecución
- [ ] **Gobernanza de IA en España.** Proyecto de Ley Orgánica en trámite, AESIA, régimen
      sancionador
- [ ] **Deontología y uso de IA en la abogacía.** Circulares del CGAE —la 3/2026 en particular—
      y resoluciones sancionadoras por citas inventadas

---

## 📦 Fase 4 — Agente Universidad (consumo interno)

> **Degradado a propósito.** Es una herramienta personal, no una línea del proyecto: no lleva
> estándar, ni corpus, ni métrica, y no compite por tiempo con la fase 2. Se construye simple y
> no se documenta más allá de esto.

- [ ] Resúmenes de apuntes · esquemas · planificación · Q&A

---

## 📦 Fase 5 — Sistema de Automejora
- [ ] Feedback loop
- [ ] Evaluación outputs
- [ ] Ajuste automático de prompts

---

## 🗄️ Congelado

**Fase 1 — Sentencia Analyzer.** Funciona y se queda como está. Sus dos bloqueos —test gastado
y campos sustantivos sin evaluación de contenido— **siguen abiertos y salen del camino
crítico**: no se retoman hasta que la fase 2 tenga una medición registrada.

Razón: el corpus de sentencias depende del CENDOJ, cuyo aviso legal prohíbe la descarga masiva
y el uso comercial y que ha desplegado CAPTCHA. Ampliar ese corpus para volver a medir es
trabajo cuyo resultado no es explotable. El pipeline conserva todo su valor como **banco de
pruebas del método** —esquema, validador, 35 Gold, ciclo DEBUG/IMPROVE— y como demostración de
la disciplina que se aplica ahora a pliegos.

**Lo que sí se conserva de la fase 1 para reutilizar en la 2:** la separación entre control de
forma y evaluación de contenido, la regla de no mirar el conjunto de test, y el hallazgo de que
6 de las 8 discrepancias de la primera evaluación eran errores del Gold y no del agente — que
es la razón de anotar contrastando contra el documento, no de memoria.