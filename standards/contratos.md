# 📄 ESTÁNDAR: CONTRATOS

Fuente única de las reglas de análisis de contratos civiles y mercantiles básicos.
`CLAUDE.md` recoge los principios comunes a todos los tipos de documento y remite aquí.

Ante una discrepancia entre este archivo y los principios de `CLAUDE.md`, prevalece
`CLAUDE.md`.

> **Estado: esquema v1, sin ejercitar.** No hay ficheros de referencia ni validador mecánico
> equivalente a `validate_v2.ps1`. Este estándar está escrito y **no medido**.
>
> **Es un esquema propio, no una variante del v2 de sentencias.** Son contratos de datos
> distintos: no comparten campos, ni validador, ni métricas.

---

## ⚖️ REGLA QUE CONDICIONA TODO EL ESQUEMA

**`risk_flags` es consciente del régimen jurídico.** Sin eso, el esquema mezcla regímenes y las
métricas no significan nada.

El control de **contenido** —la declaración de abusividad, arts. 82 y ss. TRLGDCU— es derecho
de consumo y opera **solo frente a consumidores**. Un adherente **empresario**, bajo la Ley
7/1998 de Condiciones Generales de la Contratación, dispone únicamente de control de
**incorporación y transparencia**, no de control de abusividad. Son dos niveles distintos, no
un mismo régimen atenuado. Y nada de ello rige en un contrato administrativo sometido a la LCSP
(Ley 9/2017) ni en un mercantil negociado entre partes simétricas.

**Consecuencia directa: una cláusula declarada abusiva por un juez no es una etiqueta
transferible a un pliego administrativo.** Copiar esas etiquetas importa un régimen que allí no
rige, y la evaluación mediría algo que no existe.

De la jurisprudencia se transfieren los **criterios**, nunca las **calificaciones**:

- desequilibrio importante entre prestaciones
- falta de reciprocidad
- falta de transparencia y comprensibilidad real
- desproporción de la penalización respecto del incumplimiento
- atribución unilateral de facultades de interpretación, modificación o resolución

Esos criterios son evaluables en cualquier régimen. La *consecuencia jurídica* (nulidad por
abusividad) solo en consumo.

**Riesgos propios del régimen administrativo**, que no derivan de la doctrina de consumo:
penalidades por demora, régimen de garantías, revisión de precios, modificación unilateral
(*ius variandi*), causas de resolución, subcontratación, cesión, confidencialidad y plazos de
pago.

---

## 📦 ESQUEMA JSON (v1)

```json
{
  "document_type": "",
  "governing_law": "",
  "regimen": "consumo|administrativo|mercantil",
  "control_aplicable": "contenido_y_transparencia|solo_incorporacion_y_transparencia|n_a",
  "parties": [],
  "key_clauses": [],
  "missing_clauses": [],
  "risk_flags": [
    {
      "id": "",
      "issue": "",
      "criterio": "",
      "regimen": "consumo|administrativo|mercantil",
      "consecuencia_juridica": "",
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

## 📏 REGLAS POR CAMPO

**`regimen`** — Régimen jurídico del contrato completo. Se determina por la naturaleza de las
partes y del contrato, no por su contenido.

**`control_aplicable`** — Depende de `regimen` y de la condición del adherente:

| Situación | Valor |
|---|---|
| `regimen=consumo` y el adherente es consumidor | `contenido_y_transparencia` |
| Adherente **empresario** sobre clausulado predispuesto (Ley 7/1998) | `solo_incorporacion_y_transparencia` |
| `regimen=administrativo` o `mercantil` negociado | `n_a` |

Esta es la distinción que no puede perderse: determina qué consecuencias jurídicas son
invocables y, por tanto, qué puede afirmar `risk_flags`.

**`risk_flags[].regimen`** — Debe coincidir con el `regimen` del documento. Un flag cuyo
régimen no coincida es un error de anotación, no una observación válida.

**`risk_flags[].criterio`** — El criterio sustantivo que se aplica (desequilibrio, falta de
reciprocidad, opacidad…). Es lo que se transfiere entre regímenes.

**`risk_flags[].consecuencia_juridica`** — La consecuencia **dentro de su régimen**. Solo en
consumo puede ser la nulidad por abusividad. En administrativo o mercantil, describir el efecto
que corresponda, o `null` si no hay consecuencia típica.

**`severity`** — Nunca inferir gravedad de la mera presencia de una cláusula: depende del
contenido y de sus cifras.

---

## 📏 REGLAS GENERALES

- Identificar el tipo de contrato.
- Detectar las cláusulas estándar.
- Detectar las ausencias relevantes.
- Priorizar los riesgos jurídicos.
- Explicar los riesgos con claridad.
- En caso de duda sobre el régimen: `null`, nunca inferencia. Un régimen mal asignado
  contamina todos los `risk_flags` del documento.

---

## ⏳ PENDIENTE

- **Rúbrica de `risk_flags`** (`corpus/rubrica-riskflags.md`): cada flag definido con
  identificador, criterio, régimen aplicable, consecuencia jurídica y ejemplo de cláusula.
  Los criterios se extraen de las 9 resoluciones de la vía C. **Redactar antes de anotar ningún
  documento.**
- **Métrica de campos sustantivos.** `risk_flags`, `key_clauses` y `missing_clauses` no admiten
  comparación exacta. Sin métrica decidida, el esquema y el Gold se diseñan a ciegas.
- **`validate_contratos.ps1`**, equivalente al validador de sentencias.
