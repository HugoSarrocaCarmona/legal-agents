# Legal Tech Agents (España) — extracción estructurada de sentencias

Convierte sentencias judiciales españolas en JSON estructurado, validable y comparable
entre documentos. Fase actual: sentencias civiles del Tribunal Supremo publicadas por CENDOJ.

---

## Estructura del repositorio

```
CLAUDE.md                       Estándar vigente (v2). Lo carga el harness automáticamente.
validate_v2.ps1                 Validador mecánico del esquema v2.
Inputs/                         Sentencias en texto plano (extracción de PDF de CENDOJ).
Outputs/                        JSON generados, con sufijo .v2.json
Archive/                        Estándares superados (v1, propuesta) y outputs v1.
.claude/agents/sentencia_agent.md   Definición del agente.
.claude/commands/               Recetas invocables como /RUN, /DEBUG, /IMPROVE, /run_once.
```

`CLAUDE.md` es la **fuente de verdad**. Ante cualquier discrepancia con la definición del
agente o con este README, prevalece `CLAUDE.md`.

---

## Pipeline

Orden estricto, definido en `CLAUDE.md` y replicado en el agente:

| # | Paso | Campo que produce |
|---|---|---|
| 1 | Leer el input desde `Inputs/` | — |
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
Usa el agente sentencia_agent para analizar Inputs/sentencia3.txt con el esquema v2
```

El agente escribe `Outputs/sentencia3.v2.json`. Sobrescribe si ya existe.

### Reprocesar el dataset completo

Un agente por sentencia, en paralelo. Es la ruta recomendada: cada documento ocupa entre
28 KB y 136 KB y procesarlos en una sola pasada degrada la calidad de la extracción.

```
Reprocesa todo Inputs/ a v2 con el agente sentencia_agent, un agente por archivo
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

## Limitaciones

- El sistema **no** emite conclusiones legales definitivas ni sustituye asesoramiento
  profesional. Es una herramienta de apoyo.
- El esquema está calibrado sobre la cabecera CENDOJ del Tribunal Supremo. Autos,
  resoluciones administrativas e instancias inferiores están declarados como soportados
  pero **no validados** contra el dataset actual; las reglas de `case_id` y `document_type`
  requerirán revisión con el primer documento de otro tipo.
- El agente no verifica el contenido contra fuentes externas: lo que no consta en el
  documento se escala a `uncertainties` o `next_review_questions`, nunca se completa.
