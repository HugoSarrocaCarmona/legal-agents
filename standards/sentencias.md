# 📚 ESTÁNDAR: SENTENCIAS (v2)

Fuente única de las reglas de extracción de sentencias, autos y resoluciones judiciales
españolas. Ningún otro archivo del repositorio repite estas reglas: `CLAUDE.md` recoge los
principios comunes a todos los tipos de documento y remite aquí, y
`.claude/agents/sentencia_agent.md` remite aquí también.

Ante una discrepancia entre este archivo y los principios de `CLAUDE.md`, prevalece
`CLAUDE.md`.

---

## 🔁 PIPELINE OBLIGATORIO

Orden de ejecución estricto:

1. Leer el archivo indicado desde `Inputs/`.
2. Extraer la cabecera (primeras ~15 líneas).
3. Extraer el tipo de resolución → `document_type`.
4. Extraer identificadores → `case_id`.
5. Extraer la fecha → `decision_date`.
6. Identificar el tribunal → `court_or_body`, y el ponente → `ponente`.
7. Identificar las partes → `parties`.
8. Separar hechos materiales de historia procesal → `facts` / `procedural_posture`.
9. Identificar las cuestiones jurídicas → `legal_issues`.
10. Detectar las normas aplicadas por el tribunal → `applied_rules`, y las invocadas
    por las partes pero no adoptadas → `cited_by_parties`.
11. Extraer el fallo → `holding`.
12. Construir el `ratio_summary`.
13. Detectar incertidumbres jurídicas → `uncertainties`.
14. Detectar defectos del soporte documental → `document_quality_notes`.
15. Formular preguntas de revisión → `next_review_questions`.
16. Validar el JSON contra el contrato de validación.
17. Guardar en `Outputs/` con el nombre base del archivo de entrada y sufijo `.v2.json`.

---

## 📦 ESQUEMA JSON (16 campos, en este orden)

```json
{
  "document_type": "sentencia|auto",
  "case_id": {
    "ecli": "",
    "roj": "",
    "resolution_number": "",
    "appeal_number": "",
    "id_cendoj": ""
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

---

## 📏 REGLAS POR CAMPO

### document_type

- **ENUM CERRADO**: `"sentencia"` | `"auto"`.
- Fuente **única**: el campo `Tipo de Resolución:` de la cabecera, en minúscula
  (`Sentencia` → `"sentencia"`, `Auto` → `"auto"`).
- No inferirlo del nombre del archivo ni del cuerpo del documento: un archivo llamado
  `sentenciaN.txt` puede contener un auto.
- Si el campo falta o su valor no es ninguno de los dos → `null`, y registrarlo en
  `document_quality_notes`.

### case_id

- Extracción literal de la cabecera, nunca reconstruida.
- Prioridad: ROJ, ECLI, nº resolución, nº recurso, Id Cendoj.
- Subcampo ausente en el documento → `null`.
- **`ecli` conserva el prefijo `ECLI:`** tal y como figura en la cabecera:
  - Correcto: `"ECLI:ES:TICI:2025:2A"`
  - Incorrecto: `"ES:TICI:2025:2A"`

### decision_date

- Fuente: el campo `Fecha:` de la cabecera.
- Formato `YYYY-MM-DD`.
- Ignorar las demás fechas: votación y fallo, vista, resoluciones de instancia.

### court_or_body

- Órgano, sala, sección y sede. Sin nombres de magistrados.
- **Formato normalizado con niveles opcionales**: incluir solo los niveles presentes en el
  documento, separados por punto y espacio, en este orden:
  `"Órgano. Sala. Sección N. Sede: Ciudad"`.
- **Omitir el nivel ausente; nunca rellenarlo ni inferirlo.** Ejemplos:
  - `"Tribunal Supremo. Sala de lo Civil. Sección 1. Sede: Madrid"` (cuatro niveles)
  - `"Juzgado de lo Mercantil N.º 3. Sede: Valencia"` (sin Sala ni Sección)
- Separador entre niveles: punto y espacio.
- Sección en número arábigo sin ordinal (`1`, no `1.ª`).
- Sede siempre al final, como `Sede: Ciudad`.
- **Nunca comas ni paréntesis en este campo.** Una sede en forma invertida se endereza:
  `Palmas de Gran Canaria (Las)` → `Las Palmas de Gran Canaria`.

#### Sección ambigua

- Si la cabecera contiene **varias** líneas `Sección:`, usar la **numérica**.
- Si ninguna de ellas es numérica, **omitir** el nivel Sección.
- En ambos casos, registrar la ambigüedad en `document_quality_notes`.

### ponente

- Nombre sin tratamiento honorífico (`D.`, `D.ª`, `Excmo. Sr.`).
- **Restituir capitalización y acentos**: la cabecera lo escribe en mayúsculas y sin
  acentuar, y no se transcribe así.
  - `RAQUEL BLAZQUEZ MARTIN` → `"Raquel Blázquez Martín"`
  - Si el cuerpo del documento trae la grafía acentuada, esa es la fuente.
- `null` si no consta.

### parties

- **Estructura obligatoria**: array de objetos `{name, role}`.
- Roles tomados literalmente del encabezamiento; no inferirlos.
- Si el documento nombra a alguien sin asignarle rol → `role: null`. «No inferir» prevalece
  sobre «rellenar el campo». `name` nunca es `null`.
- Mantener la anonimización del documento.

### facts

- **Array de strings** de 5 a 15 elementos. Nunca un string.
- Un elemento = un hecho. No agrupar varios en uno.
- Solo hechos materiales, extraprocesales.
- **Prohibido** narrar la historia procesal.

### procedural_posture

- String. Cronología procesal completa: demanda, instancias, recursos, admisión, vista, fallo.

### legal_issues

- Array. Cuestiones formuladas como tales (`"Si ..."`, `"Cuál ..."`), claras y separadas.

### applied_rules

- **Estructura obligatoria**: array de objetos `{type, ref, note}`.
- `type` ∈ `{"norma", "jurisprudencia", "doctrina"}`.
- **Solo lo que el tribunal usa como fundamento de su decisión.** No incluir doctrina
  irrelevante.

### cited_by_parties

- Array de strings. Normas y sentencias invocadas por las partes que el tribunal **no** hace
  suyas. Array vacío si no aplica.

### holding

- String. Decisión final, clara y directa, con su alcance (costas, depósitos).

### ratio_summary

- Array obligatorio de 3 a 8 elementos.
- Cada elemento, una idea jurídica de ≤ 400 caracteres.

### uncertainties

- Array. Solo incertidumbres jurídicas o fácticas **reales del caso**.
- **No incluir** errores de OCR, campos de cabecera vacíos (`Fallo/Acuerdo:`, `Nota:`) ni la
  anonimización del CENDOJ como práctica general.

### document_quality_notes

- Array. Defectos del soporte documental: artefactos de OCR, fechas imposibles, referencias
  huérfanas, inconsistencias internas, anonimización inconsistente.

### next_review_questions

- Array de 3 a 8 preguntas necesarias para completar o verificar el análisis.
- **Excluir** valoración estratégica, impacto como precedente y previsión de recursos futuros.

---

## 🧭 RESOLVER ANTES DE ESCALAR

Si una duda se despeja con el propio documento, resuélvela y no la escales. Ejemplo: un
identificador Roj (`SJPI 162/2019`) y un número de resolución (`sentencia 218/2019`) referidos
a la misma sentencia no son una contradicción, sino dos sistemas de numeración.

Cuando el conflicto es real —contradicciones, fechas imposibles, varias versiones del mismo
dato— la cabecera es la referencia, y la anomalía se registra en `uncertainties` si es del
caso o en `document_quality_notes` si es del soporte.

---

## ✅ CONTRATO DE VALIDACIÓN

El JSON es válido **solo si**:

- Existen los 16 campos, en el orden del esquema.
- `document_type` ∈ `{"sentencia", "auto"}` **y coincide** con el campo `Tipo de Resolución:`
  de la cabecera del documento de origen.
- `case_id` tiene al menos un identificador.
- `facts` es array de 5–15 elementos.
- `facts` ≠ `procedural_posture` y no se solapan en contenido.
- `parties` es array de objetos `{name, role}` con al menos un elemento; `name` no vacío,
  `role` puede ser `null` si el documento no lo consigna.
- `applied_rules` es array de objetos `{type, ref, note}` con `type` válido.
- `applied_rules` ∩ `cited_by_parties` = ∅.
- `ratio_summary` es array de 3–8 elementos, cada uno ≤ 400 caracteres.
- `next_review_questions` tiene entre 3 y 8 entradas.
- No hay contradicciones internas.
- Longitudes respetadas.

Si algo falla → registrarlo en `uncertainties` con explicación técnica.

La comprobación mecánica se ejecuta con `validate_v2.ps1` (ver `README.md`).

---

## 💾 FORMATO Y GUARDADO

JSON válido, sin texto libre fuera de la estructura.

Guardar en `Outputs/` con el nombre base del input y sufijo `.v2.json`
(p. ej. `Inputs/dev/sentencia3.txt` → `Outputs/sentencia3.v2.json`).
