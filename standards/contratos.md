# 📄 ESTÁNDAR: CONTRATOS

Fuente única de las reglas de análisis de contratos civiles y mercantiles básicos.
`CLAUDE.md` recoge los principios comunes a todos los tipos de documento y remite aquí.

Ante una discrepancia entre este archivo y los principios de `CLAUDE.md`, prevalece
`CLAUDE.md`.

> **Estado: sin ejercitar.** No hay ni un solo contrato en el corpus, ni ficheros de
> referencia, ni validador mecánico equivalente a `validate_v2.ps1`. Este estándar está
> escrito pero no medido.

---

## 📦 ESQUEMA JSON

```json
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
```

---

## 📏 REGLAS

- Identificar el tipo de contrato.
- Detectar las cláusulas estándar.
- Detectar las ausencias relevantes.
- Priorizar los riesgos jurídicos.
- Explicar los riesgos con claridad.
