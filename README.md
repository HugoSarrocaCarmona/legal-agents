# Legal Tech Agents (España) — extracción estructurada de sentencias

Convierte sentencias judiciales españolas en JSON estructurado, validable y comparable
entre documentos. Fase actual: resoluciones del orden civil publicadas por CENDOJ. Lo ya
procesado y medido es Tribunal Supremo; el corpus reservado incluye además otros órganos.

---

## Estructura del repositorio

```
CLAUDE.md                       Estándar vigente (v2). Lo carga el harness automáticamente.
validate_v2.ps1                 Validador mecánico del esquema v2.
eval_gold.ps1                   Evaluación de precisión contra los ficheros de referencia.
Outputs/                        JSON generados, con sufijo .v2.json
Gold/                           Ficheros de referencia anotados a mano, con sufijo .gold.json
progress/                       Bitácora, métricas históricas y hoja de ruta.
.claude/agents/sentencia_agent.md   Definición del agente.
.claude/commands/               Recetas invocables como /RUN, /DEBUG, /IMPROVE, /run_once.
```

**Los directorios `Inputs/` y `Archive/` no se publican en el repositorio.** El corpus son 35
resoluciones del orden civil, todas descargables desde el buscador de jurisprudencia del CENDOJ
(`poderjudicial.es`) a partir de los identificadores que constan en cada output. No son todas
del Tribunal Supremo: ver [composición del corpus](#división-dev--test).

La exclusión es deliberada, por minimización de datos: este repositorio publica **metadatos de
cabecera y análisis estructurado**, no republica el texto íntegro de las resoluciones. Quien
quiera reproducir el pipeline descarga las sentencias de la fuente oficial y las coloca en
`Inputs/dev/` e `Inputs/test/` con el nombre `sentenciaN.txt`.

`CLAUDE.md` es la **fuente de verdad**. Ante cualquier discrepancia con la definición del
agente o con este README, prevalece `CLAUDE.md`.

---

## Pipeline

Orden estricto, definido en `CLAUDE.md` y replicado en el agente:

| # | Paso | Campo que produce |
|---|---|---|
| 1 | Leer el input desde `Inputs/dev/` o `Inputs/test/` | — |
| 2 | Extraer la cabecera (primeras ~15 líneas) | — |
| 3 | Extraer identificadores | `case_id` |
| 4 | Extraer la fecha | `decision_date` |
| 5 | Identificar tribunal y ponente | `court_or_body`, `ponente` |
| 6 | Identificar las partes | `parties` |
| 7 | Separar hechos materiales de historia procesal | `facts`, `procedural_posture` |
| 8 | Identificar cuestiones jurídicas | `legal_issues` |
| 9 | Separar normas aplicadas de las solo invocadas | `applied_rules`, `cited_by_parties` |
| 10 | Extraer el fallo | `holding` |
| 11 | Construir el razonamiento | `ratio_summary` |
| 12 | Detectar incertidumbres jurídicas | `uncertainties` |
| 13 | Detectar defectos del soporte documental | `document_quality_notes` |
| 14 | Formular preguntas de revisión | `next_review_questions` |
| 15 | Validar contra el contrato | — |
| 16 | Guardar en `Outputs/<base>.v2.json` | — |

**Principios que gobiernan el pipeline:** no inventar; no inferir identificadores ni fechas;
la cabecera es la fuente primaria ante conflictos; `null` antes que inferencia; consistencia
interna por encima de completitud.

---

## Esquema v2 (16 campos)

```json
{
  "document_type": "sentencia",
  "case_id": {
    "ecli": "", "roj": "", "resolution_number": "", "appeal_number": "", "id_cendoj": ""
  },
  "decision_date": "",
  "court_or_body": "",
  "ponente": "",
  "parties": [{ "name": "", "role": "" }],
  "facts": [],
  "procedural_posture": "",
  "legal_issues": [],
  "applied_rules": [{ "type": "", "ref": "", "note": "" }],
  "cited_by_parties": [],
  "holding": "",
  "ratio_summary": [],
  "uncertainties": [],
  "document_quality_notes": [],
  "next_review_questions": []
}
```

| Campo | Tipo | Restricción |
|---|---|---|
| `document_type` | string | `"sentencia"` |
| `case_id` | objeto | 5 subcampos; al menos uno no nulo; extracción literal de cabecera |
| `decision_date` | string | `YYYY-MM-DD`, del campo `Fecha:` de la cabecera |
| `court_or_body` | string | órgano y sección, sin nombres de magistrados |
| `ponente` | string \| null | sin `D.` / `Excmo. Sr.` |
| `parties` | array de objetos | `{name, role}`; roles literales, nunca inferidos |
| `facts` | **array** | 5–15 elementos, un hecho por elemento, solo hechos materiales |
| `procedural_posture` | string | cronología procesal completa |
| `legal_issues` | array | cuestiones formuladas como tales |
| `applied_rules` | array de objetos | `{type, ref, note}`; `type` ∈ norma / jurisprudencia / doctrina |
| `cited_by_parties` | array | invocado por las partes y **no** asumido por la Sala |
| `holding` | string | fallo y su alcance |
| `ratio_summary` | array | 3–8 elementos, ≤ 400 caracteres cada uno |
| `uncertainties` | array | solo dudas jurídicas reales del caso |
| `document_quality_notes` | array | OCR, fechas imposibles, anonimización inconsistente |
| `next_review_questions` | array | 3–8 preguntas para completar o verificar |

### Dos separaciones que definen el estándar

- **`facts` vs `procedural_posture`** — lo que ocurrió antes del litigio frente a lo que
  ocurrió dentro de él. Sin esta separación los campos se duplican.
- **`applied_rules` vs `cited_by_parties`** — lo que la Sala usa como fundamento frente a lo
  que las partes invocan sin éxito. Sin esta separación `applied_rules` deja de ser fiable.

Análoga en espíritu: **`uncertainties` vs `document_quality_notes`** separa las lagunas
jurídicas del caso de los defectos del PDF de origen.

---

## Cómo ejecutar

### Reprocesar una sentencia

Invoca el agente `sentencia_agent` indicando el archivo:

```
Usa el agente sentencia_agent para analizar Inputs/dev/sentencia3.txt con el esquema v2
```

El agente escribe `Outputs/sentencia3.v2.json`. `/RUN` **no sobrescribe outputs existentes**:
procesa solo los que faltan. Para regenerar uno ya producido hay que borrarlo antes, o pedir
la reescritura explícitamente al agente.

### Reprocesar el dataset completo

Un agente por sentencia, en paralelo. Es la ruta recomendada: cada documento ocupa entre
28 KB y 136 KB y procesarlos en una sola pasada degrada la calidad de la extracción.

```
Reprocesa todo Inputs/dev/ a v2 con el agente sentencia_agent, un agente por archivo
```

### Validar

```bash
powershell -ExecutionPolicy Bypass -File validate_v2.ps1
```

Valida todos los `Outputs/*.v2.json`. Para un archivo suelto o una carpeta distinta:

```bash
powershell -ExecutionPolicy Bypass -File validate_v2.ps1 -Path Outputs/sentencia3.v2.json
```

Devuelve exit code `1` si algún archivo tiene un `FAIL`, `0` en caso contrario — encadenable
en un hook o en CI.

**Comprobaciones:** JSON parseable · 16 campos en orden · `case_id` con al menos un
identificador · `decision_date` ISO 8601 · `facts` array de 5–15 · `facts` ≠
`procedural_posture` (identidad y solapamiento literal) · `parties` con `{name, role}` ·
`applied_rules` con `{type, ref, note}` y `type` válido · `applied_rules` ∩
`cited_by_parties` = ∅ · `ratio_summary` 3–8 elementos ≤ 400 caracteres ·
`next_review_questions` 3–8 · campos string obligatorios no vacíos.

Distingue **FAIL** (incumple el contrato) de **WARN** (merece revisión humana, no bloquea):
`case_id` incompleto, `ponente` nulo, marcadores procesales dentro de `facts`.

---

## Evaluación

`validate_v2.ps1` comprueba que el JSON cumple el contrato. No comprueba que **diga la
verdad**. Para eso está `Gold/`.

### Ficheros de referencia

`Gold/` contiene 22 ficheros `sentenciaN.gold.json`, uno por documento del conjunto dev,
rellenados **manualmente leyendo la cabecera** de cada sentencia. Son la referencia contra la
que se mide el agente, no una salida suya: si un identificador no consta en el documento, en el
gold figura `null`, y que el agente lo rellene cuenta como error.

### Ejecutar la evaluación

```bash
powershell -ExecutionPolicy Bypass -File eval_gold.ps1
```

Compara cada `Gold/sentenciaN.gold.json` con su `Outputs/sentenciaN.v2.json` y calcula
**precisión por campo** sobre los 8 campos de cabecera:

`ecli` · `roj` · `resolution_number` · `appeal_number` · `id_cendoj` · `decision_date` ·
`court_or_body` · `ponente`

Cada discrepancia se clasifica: **INVENTADO** (el agente rellena lo que no consta),
**OMITIDO** (el dato existe y no se extrae), **CASE** (solo difiere en capitalización) o
**ERROR** (valores distintos). La distinción importa: inventar y omitir son fallos de
naturaleza opuesta y se corrigen de forma opuesta. `""` y `null` se tratan como el mismo
valor —ausencia de dato—, y cada tirada se anexa a `progress/METRICS.md`.

Exit code `1` si falta algún output, si algún JSON es ilegible o si no se comparó ningún
campo; `0` en caso contrario.

### División dev / test

| Conjunto | Documentos | Gold | Uso |
|---|---|---|---|
| dev | `sentencia1`–`sentencia22` | sí | iterar el estándar y medir |
| test | `sentencia23`–`sentencia35` | no | reservado, **sin evaluar** |

El conjunto de test está intacto a propósito. Cada vuelta de `/DEBUG` → `/IMPROVE` ajusta
`CLAUDE.md` mirando los fallos de dev, y eso hace que la precisión sobre dev deje de ser una
estimación honesta del rendimiento sobre una sentencia nueva: el estándar se ha adaptado a
esos 22 documentos concretos. Test sirve para comprobar, una sola vez y al final, cuánto de
la precisión es método y cuánto es sobreajuste.

**Composición por órgano.** Los dos conjuntos no son homogéneos, y conviene saberlo antes de
leer cualquier número:

| Órgano | dev | test |
|---|---|---|
| Tribunal Supremo, Sala de lo Civil | 22 | 5 |
| Tribunal de Instancia (Mercantil / Civil y de Instrucción) | — | 5 |
| Tribunal Superior de Justicia, Sala de lo Civil y Penal | — | 2 |
| Juzgado de lo Mercantil | — | 1 |
| **Total** | **22** | **13** |

Dev es íntegramente Tribunal Supremo. Test son 5 documentos de Supremo y **8 de otros
órganos**. Es decir, test no mide solo generalización a sentencias nuevas: mide además
generalización a **cabeceras de otro tipo**, y son dos cosas distintas mezcladas en el mismo
conjunto. Los 5 de Supremo permiten separarlas si al evaluar se reportan por separado.

Hay razones concretas para esperar degradación fuera del Supremo. El formato normalizado de
`court_or_body` —`"Órgano. Sala. Sección N. Sede: Ciudad"`— presupone una `Sala` que un
Juzgado de lo Mercantil no tiene; el Tribunal de Instancia es una figura reciente cuyas
cabeceras usan `Sección` con dos sentidos distintos; y la prioridad de identificadores de
`case_id` está calibrada sobre cabeceras del Supremo. Nada de esto está resuelto: está
reservado junto con el conjunto.

### Resultado actual

**176/176 (100 %) sobre dev** — 22 documentos × 8 campos, sin discrepancias.

Es un resultado de una sola vuelta y hay que leerlo con tres reservas. Primera: mide 8 campos
de cabecera, que son los más mecánicos del esquema. Segunda: se ha medido sobre el conjunto en
el que se iteró. Tercera: se ha medido sobre 22 documentos del **mismo órgano y la misma sala**,
con cabeceras casi idénticas entre sí; el 100 % dice que el agente lee bien una plantilla, no
que lea bien una cabecera judicial cualquiera. El número sobre test es desconocido y será igual
o peor.

### Qué NO mide

Los campos sustantivos —**`facts`, `applied_rules`, `ratio_summary`, `holding`**, y con ellos
`legal_issues`, `procedural_posture` y `cited_by_parties`— **no tienen evaluación de
contenido**. De ellos solo se comprueba la **forma** vía `validate_v2.ps1`: que `facts` sea un
array de 5–15 elementos, que no se solape con `procedural_posture`, que `applied_rules` traiga
`{type, ref, note}` y no intersecte con `cited_by_parties`, que `ratio_summary` tenga 3–8
elementos de ≤ 400 caracteres.

Nada de eso verifica que los hechos sean los del caso, que las normas listadas sean las que la
Sala usó como fundamento, ni que el fallo esté bien recogido. Un output puede pasar
`validate_v2.ps1` y `eval_gold.ps1` a la vez y contener un razonamiento equivocado. Esa capa
—gold sustantivo o revisión humana muestreada— está pendiente.

---

## Limitaciones

- El sistema **no** emite conclusiones legales definitivas ni sustituye asesoramiento
  profesional. Es una herramienta de apoyo.
- El esquema está calibrado sobre la cabecera CENDOJ del Tribunal Supremo, Sala de lo Civil:
  es el único órgano presente en el conjunto sobre el que se ha iterado y medido. El corpus
  reservado ya contiene 8 resoluciones de Tribunal de Instancia, Tribunal Superior de Justicia
  y Juzgado de lo Mercantil, **ninguna procesada ni evaluada todavía**. Las reglas de
  `court_or_body` (que presupone `Sala`) y la prioridad de identificadores de `case_id`
  requerirán revisión con esos documentos. Autos y resoluciones administrativas siguen
  declarados como soportados y sin un solo caso en el corpus.
- El agente no verifica el contenido contra fuentes externas: lo que no consta en el
  documento se escala a `uncertainties` o `next_review_questions`, nunca se completa.
