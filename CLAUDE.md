# 🧠 PROYECTO: LEGAL TECH AGENTS (ESPAÑA)

## 🎯 OBJETIVO GENERAL

Construir agentes de IA capaces de automatizar tareas jurídicas repetitivas en el contexto del derecho español, priorizando:

1. Resumen estructurado de sentencias
2. Análisis de contratos (riesgos, cláusulas, faltantes)

El sistema debe producir resultados útiles, consistentes y reutilizables en entornos profesionales.

---

## ⚖️ PRINCIPIOS FUNDAMENTALES

Este sistema realiza extracción estructurada de documentos jurídicos.

Reglas absolutas:

1. No inventar información bajo ninguna circunstancia
2. No inferir identificadores ni fechas
3. Separar SIEMPRE:
   - datos extraídos literalmente
   - datos interpretados
4. Priorizar consistencia interna sobre completitud
5. Si hay conflicto entre secciones del documento:
   → usar la cabecera como fuente primaria
6. JSON final debe ser válido y cumplir el contrato de validación
7. En caso de duda:
   → preferir null antes que inferencia

---

## 🔁 PIPELINE OBLIGATORIO (SENTENCIAS)

Orden de ejecución estricto:

1. Extraer cabecera
2. Extraer identificadores (case_id)
3. Extraer fecha (decision_date)
4. Identificar tribunal (court_or_body)
5. Identificar partes
6. Separar hechos vs procedimiento
7. Identificar cuestiones jurídicas
8. Detectar normas aplicadas
9. Extraer fallo (holding)
10. Construir ratio_summary
11. Detectar uncertainties
12. Detectar document_quality_notes
13. Validar JSON

---

## 🧾 TIPOS DE DOCUMENTOS SOPORTADOS

- Sentencias judiciales
- Autos
- Resoluciones administrativas
- Contratos civiles y mercantiles básicos

---

## 📤 FORMATO DE SALIDA (OBLIGATORIO)

Todas las respuestas deben ser JSON válido.

Nunca devolver texto libre.

---

# ================================
# 📚 ESTÁNDAR: SENTENCIAS
# ================================

## 📦 ESQUEMA JSON

{
  "document_type": "sentencia",
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

---

## 📏 REGLAS POR CAMPO

### case_id
- Extraer SOLO de cabecera
- Prioridad:
  1. ROJ
  2. ECLI
  3. Nº resolución
  4. Nº recurso
  5. ID CENDOJ
- No reconstruir
- Si no existe → null

---

### decision_date
- Fuente: campo "Fecha"
- Formato: YYYY-MM-DD
- Ignorar otras fechas procesales

---

### court_or_body
- Extraer limpio
- Mantener jerarquía
- Eliminar nombres de jueces
- FORMATO NORMALIZADO OBLIGATORIO:
- "Órgano. Sala. Sección N. Sede: Ciudad"
- Ejemplo: "Tribunal Supremo. Sala de lo Civil. Sección 1. Sede: Madrid"
- Separador entre niveles: punto y espacio
- Sección en número arábigo sin ordinal (1, no 1.ª)
- Sede siempre al final como "Sede: Ciudad"
- Nunca usar comas ni paréntesis en este campo

---

### ponente
- Extraer si aparece
- Sin "D.", "D.ª"
- Si no existe → null

---

### parties
- ESTRUCTURA OBLIGATORIA: array de objetos `{ "name": "", "role": "" }`
- Extraer explícitamente
- No inferir roles: transcribirlos del encabezamiento
- Mantener anonimización

---

### facts
- ESTRUCTURA OBLIGATORIA: array de strings (NO string)
- Un elemento = un hecho. No agrupar varios hechos en un mismo elemento
- Entre 5 y 15 elementos
- SOLO hechos materiales, extraprocesales
- NO incluir procedimiento

---

### procedural_posture
- Historia procesal completa
- Incluir:
  - demanda
  - recursos
  - instancias

---

### legal_issues
- Lista de problemas jurídicos
- Claros y separados

---

### applied_rules
- ESTRUCTURA OBLIGATORIA: array de objetos `{ "type": "", "ref": "", "note": "" }`
- `type` ∈ {"norma", "jurisprudencia", "doctrina"}
- SOLO normas usadas por el tribunal como fundamento de su decisión
- No incluir doctrina irrelevante

---

### cited_by_parties
- Normas citadas pero NO adoptadas

---

### holding
- Decisión final
- Clara y directa

---

### ratio_summary
- Array obligatorio
- 3–8 elementos
- Cada elemento:
  - una idea jurídica
  - ≤ 400 caracteres

---

### uncertainties
- SOLO incertidumbres reales del caso
- No incluir errores de OCR
- No incluir campos vacíos estándar

---

### document_quality_notes
- Problemas del documento:
  - OCR
  - fechas imposibles
  - inconsistencias internas

---

### next_review_questions
- 3–8 preguntas útiles
- Para completar o verificar datos

---

## ✅ VALIDACIÓN OBLIGATORIA

Un JSON es válido SOLO si:

- Todos los campos existen, en el orden del esquema
- case_id tiene al menos un identificador
- facts es ARRAY de 5–15 elementos
- facts ≠ procedural_posture (ni solapamiento de contenido)
- parties es array de objetos {name, role}, con al menos un elemento
- applied_rules es array de objetos {type, ref, note}, con type válido
- applied_rules ∩ cited_by_parties = ∅
- ratio_summary es array de 3–8 elementos, cada uno ≤ 400 caracteres
- next_review_questions tiene entre 3 y 8 elementos
- No hay contradicciones internas
- Longitudes respetadas

Si falla:
→ añadir en uncertainties

La comprobación mecánica se ejecuta con `validate_v2.ps1` (ver README.md).

---

# ================================
# 📄 ESTÁNDAR: CONTRATOS
# ================================

## 📦 ESQUEMA JSON

{
  "document_type": "",
  "governing_law": "",
  "parties": [],
  "key_clauses": [],
  "missing_clauses": [],
  "risk_flags": [
    {
      "issue": "",
      "severity": "low|medium|high",
      "why_it_matters": "",
      "suggested_fix": ""
    }
  ],
  "plain_language_summary": "",
  "review_notes": []
}

---

## 📏 REGLAS

- Identificar tipo de contrato
- Detectar cláusulas estándar
- Detectar ausencias relevantes
- Priorizar riesgos jurídicos
- Explicar riesgos claramente

---

# ⚠️ GESTIÓN DE ERRORES

Si hay:

- contradicciones
- fechas imposibles
- múltiples versiones

→ usar cabecera como referencia  
→ registrar en:
  - uncertainties
  - document_quality_notes

---

# 🚫 LIMITACIONES

El sistema NO debe:

- emitir conclusiones legales definitivas
- sustituir asesoramiento profesional
- afirmar validez jurídica sin contexto completo

---

# 🔄 MEJORA CONTINUA

El sistema debe:

- detectar errores recurrentes
- mejorar consistencia
- reducir ruido en outputs
- adaptarse progresivamente

---

# 🧩 COMPORTAMIENTO DEL AGENTE

- Priorizar precisión sobre creatividad
- Mantener outputs reutilizables
- Minimizar redundancia
- No improvisar estructura

---

# 📁 ORGANIZACIÓN

- Outputs en JSON
- Nombres consistentes
- Estructura estable

---

# 🎯 OBJETIVO FINAL

Crear una base sólida para:

- automatización legal real
- reducción de tiempo
- estandarización jurídica
- futuros productos legal tech