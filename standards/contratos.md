# 📄 ESTÁNDAR: CONTRATOS (v2)

Fuente única de las reglas de análisis de contratos civiles, mercantiles y administrativos.
`CLAUDE.md` recoge los principios comunes a todos los tipos de documento y remite aquí.

Ante una discrepancia entre este archivo y los principios de `CLAUDE.md`, prevalece
`CLAUDE.md`. Sobre **cómo se mide** un campo, prevalece
[`corpus/metrica-contratos.md`](../corpus/metrica-contratos.md).

> **Estado: esquema v2, sin ejercitar.** No hay ficheros de referencia ni validador mecánico
> equivalente a `validate_v2.ps1`. Este estándar está escrito y **no medido**.
>
> **Es un esquema propio, no una variante del v2 de sentencias.** Son contratos de datos
> distintos: no comparten campos, ni validador, ni métricas. La coincidencia del número de
> versión es casual.

---

## 🔀 QUÉ CAMBIA RESPECTO DE v1

v1 nunca produjo ningún output, así que **no hay nada que migrar**. Los cambios responden a
carencias detectadas al fijar la métrica, y todos son anteriores a anotar el primer documento a
propósito: añadirlos después habría obligado a reanotar.

| Cambio | Por qué |
|---|---|
| Campo `standard_version` | v1 no permitía detectar que el estándar no se había cargado: el agente producía JSON plausible de memoria y ningún control lo veía |
| `cita` y `localizador` en `key_clauses` y `risk_flags` | v1 no anclaba nada al texto. Sin ancla no hay métrica de solapamiento, no hay verificación sin releer el contrato entero, y no hay trazabilidad |
| `key_clauses` pasa a array de objetos | Era un array suelto sin estructura declarada |
| `missing_clauses` pasa a array de objetos, con lista de referencia | «Falta una cláusula» solo significa algo respecto de una lista, y v1 no decía cuál |
| Campo `condicion_adherente` | `control_aplicable` dependía de un dato que no era campo: el anotador tenía que inferirlo y no quedaba registrado |
| Anclajes operativos de `severity` | Tres niveles sin definición destrozan el acuerdo entre anotadores |
| `risk_flags[].id` es identificador de rúbrica | Sin vocabulario cerrado no hay emparejamiento posible entre output y Gold |
| `parties` pasa a array de objetos | Consistencia con la estructura `{nombre, rol}` |

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

## 📦 ESQUEMA JSON (12 campos, en este orden)

```json
{
  "standard_version": "contratos-v2",
  "document_type": "",
  "governing_law": "",
  "regimen": "consumo|administrativo|mercantil",
  "condicion_adherente": "consumidor|empresario|n_a",
  "control_aplicable": "contenido_y_transparencia|solo_incorporacion_y_transparencia|n_a",
  "parties": [{ "nombre": "", "rol": "" }],
  "key_clauses": [
    {
      "tipo": "",
      "cita": "",
      "localizador": ""
    }
  ],
  "missing_clauses": [
    {
      "ref_id": "",
      "lista_referencia": "",
      "nota": ""
    }
  ],
  "risk_flags": [
    {
      "id": "",
      "cita": "",
      "localizador": "",
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

### standard_version

- **Valor literal y obligatorio: `"contratos-v2"`.** Este valor se define aquí y **solo** aquí.
- No se deduce, no se recuerda y no se infiere del nombre del fichero.
- **Para qué sirve.** Si el agente no lee este archivo y trabaja de memoria, produce un JSON
  plausible con reglas recordadas que ningún control detecta. Un valor que solo puede conocerse
  leyendo este fichero convierte ese fallo silencioso en un fallo visible.
- No demuestra que las reglas se hayan aplicado bien; demuestra que el estándar se abrió. Es el
  mínimo, y es mucho más que nada.

### document_type

- Tipo contractual, en minúscula y en la denominación que use el propio documento
  (`"arrendamiento de vivienda"`, `"pliego de cláusulas administrativas particulares"`).
- No inferirlo del nombre del archivo.

### governing_law

- Ley aplicable **solo si el documento la declara**. Si no la declara → `null`.
- No deducirla de la lengua, del domicilio de las partes ni del tipo de contrato.

### regimen

- **ENUM CERRADO**: `"consumo"` | `"administrativo"` | `"mercantil"`.
- Se determina por la **naturaleza de las partes y del contrato**, no por su contenido.
- En caso de duda → `null`, nunca inferencia.

> ⚠️ **Un `regimen` equivocado contamina todos los `risk_flags` del documento**, porque cambia
> qué control es aplicable y qué consecuencia jurídica puede afirmarse. Por eso la métrica trata
> un documento con `regimen` incorrecto como **contaminado** y lo excluye del cómputo de
> detección en vez de promediarlo.

### condicion_adherente

- **ENUM CERRADO**: `"consumidor"` | `"empresario"` | `"n_a"`.
- Condición de quien **se adhiere** a un clausulado predispuesto por la otra parte.
- `"n_a"` cuando **no hay adherente**: contrato genuinamente negociado entre partes simétricas,
  o contrato administrativo, donde el régimen de control es el de la LCSP y no el de condiciones
  generales.
- Es un campo **extraído**, no interpretado: se toma de cómo el documento identifica a las
  partes. Si el documento no permite determinarlo → `null`.

### control_aplicable

- **ENUM CERRADO**, y **derivado** de los dos campos anteriores. No es una valoración libre:

| `regimen` | `condicion_adherente` | `control_aplicable` |
|---|---|---|
| `consumo` | `consumidor` | `contenido_y_transparencia` |
| `mercantil` | `empresario` | `solo_incorporacion_y_transparencia` |
| `mercantil` | `n_a` | `n_a` |
| `administrativo` | `n_a` | `n_a` |

- **`n_a` significa que no rige el control de condiciones generales, no que no haya control.**
  En un contrato administrativo el control existe y es el de la LCSP; opera por otra vía y con
  otras consecuencias.
- Si `regimen` o `condicion_adherente` es `null`, `control_aplicable` es `null`.

**Dos combinaciones son contradicciones, no casos raros:**

- `regimen: "consumo"` con `condicion_adherente: "empresario"` — si quien se adhiere es
  empresario, el contrato no es de consumo.
- `regimen: "administrativo"` con `condicion_adherente` distinto de `"n_a"`.

Ante cualquiera de las dos: revisar `regimen`, que es el campo que manda, y registrar la
anomalía en `review_notes`.

### parties

- **Estructura obligatoria**: array de objetos `{nombre, rol}`.
- `rol` tomado literalmente del documento (`"arrendador"`, `"órgano de contratación"`,
  `"predisponente"`). No inferirlo: si el documento nombra a alguien sin asignarle rol →
  `rol: null`. `nombre` nunca es `null`.
- Mantener la anonimización que traiga el documento. No restituir nombres.

### key_clauses

- **Estructura obligatoria**: array de objetos `{tipo, cita, localizador}`.
- `tipo`: la clase de cláusula (`"duración"`, `"penalidades por demora"`, `"jurisdicción"`).
- Solo cláusulas **presentes** en el documento. Una cláusula que falta no va aquí: va en
  `missing_clauses`.

### missing_clauses

- **Estructura obligatoria**: array de objetos `{ref_id, lista_referencia, nota}`.
- `ref_id`: identificador del elemento **dentro de su lista de referencia**.
- `lista_referencia`: nombre de la lista contra la que se comprueba la ausencia.
- `nota`: por qué su ausencia es relevante en ese contrato concreto.

**Una cláusula «falta» solo respecto de una lista de referencia, y la lista depende del
régimen.** Sin lista escrita, la ausencia no significa nada: dos anotadores marcarían cosas
distintas y no habría forma de decir cuál acierta.

| Régimen | Lista de referencia | Estado |
|---|---|---|
| `administrativo` | Contenido mínimo del PCAP, derivado del art. 122 LCSP y su desarrollo reglamentario | **Pendiente de redactar** |
| `consumo` y `mercantil` con adherente | Se deriva de la rúbrica, a partir de las 9 resoluciones de la vía C | **Pendiente de redactar** |
| `mercantil` negociado | **No hay lista defendible** | Decidido: no la habrá |

> **Por qué el mercantil negociado no tendrá lista.** En un contrato libremente negociado, lo
> que «debería» estar es una preferencia de negociación, no una exigencia jurídica. Marcar
> ausencias ahí sería anotar la opinión del anotador y llamarlo dato.

**Mientras la lista de un régimen no esté escrita, `missing_clauses` va vacío en ese régimen y
no se mide.** Es preferible un campo vacío a un campo relleno con criterio implícito: la métrica
distingue el vacío declarado del no medido, y el segundo no puntúa.

### risk_flags

Campo central del esquema. Reglas por subcampo:

**`id`** — Identificador del criterio en `corpus/rubrica-riskflags.md`. **Vocabulario cerrado**:
no es texto libre ni una descripción. Un `id` que no esté en la rúbrica es un error de
anotación, no un hallazgo nuevo — si hace falta un criterio nuevo, se añade primero a la rúbrica.

Sin vocabulario cerrado no hay emparejamiento posible entre output y Gold, y sin emparejamiento
no hay métrica.

**El mismo `id` puede aparecer varias veces en un documento**, anclado en cláusulas distintas.
Dos cláusulas pueden incurrir en el mismo desequilibrio y son dos hallazgos, no uno.

**`cita`** — **Transcripción literal y verbatim** del texto del contrato que sostiene el flag.
No es un resumen, ni una paráfrasis, ni una reconstrucción.

- Debe poder encontrarse **carácter a carácter** en el documento de origen.
- Es la comprobación mecánica más fuerte del esquema: un riesgo inventado no puede producir una
  cita verbatim.
- Cita la cláusula que sostiene el riesgo, no el contrato entero ni media línea suelta.

**`localizador`** — Dónde está la cita, con la referencia que use el propio documento:
`"cláusula 12.3"`, `"estipulación cuarta"`, `"PCAP, cláusula 24, p. 31"`. Si el documento no
numera nada → página y párrafo. Nunca inventarse una numeración.

**`issue`** — Qué ocurre en esa cláusula. Descriptivo, no valorativo.

**`criterio`** — El criterio sustantivo aplicado: desequilibrio, falta de reciprocidad, opacidad,
desproporción de la penalización, atribución unilateral de facultades. Es lo que se transfiere
entre regímenes.

**`regimen`** — Debe coincidir con el `regimen` del documento. Un flag cuyo régimen no coincida
es un error de anotación, no una observación válida.

**`consecuencia_juridica`** — La consecuencia **dentro de su régimen**. Solo en consumo puede ser
la nulidad por abusividad. En administrativo o mercantil, describir el efecto que corresponda, o
`null` si no hay consecuencia típica.

**`severity`** — **ENUM CERRADO**, con estos anclajes:

| Valor | Criterio |
|---|---|
| `high` | La cláusula puede, **por sí sola**, privar a la contraparte de la prestación principal, imponer una consecuencia económica desproporcionada respecto del incumplimiento que la desencadena, o cerrar una vía de defensa o reclamación |
| `medium` | Desplaza coste o riesgo de forma relevante, pero **acotada y cuantificable** con lo que dice el propio contrato |
| `low` | Desviación de transparencia, de incorporación o de forma, **sin efecto económico directo identificable** en el texto |

- **Nunca inferir la gravedad de la mera presencia de una cláusula**: depende de su contenido y
  de sus cifras. Una penalización por demora no es grave por existir; lo es por su cuantía.
- **Si la gravedad depende de una cifra y la cifra no está en el documento → el nivel más bajo
  de los dos que se dudan.** Es la aplicación del principio de preferir `null` antes que
  inferencia a un campo que no admite `null`.

**`why_it_matters`** y **`suggested_fix`** — Texto libre. **No entran en la métrica**: dos
redacciones distintas pueden ser ambas correctas, y puntuarlas con igualdad exacta daría un
número falso. Se revisan cualitativamente sobre muestra.

### plain_language_summary

- String. Qué hace el contrato y a qué obliga a cada parte, sin jerga.
- Fuera de la métrica.

### review_notes

- Array. Defectos del soporte y anomalías del análisis: documento truncado, clausulado
  remitido a un anexo que no consta, contradicciones internas, combinaciones contradictorias de
  `regimen` y `condicion_adherente`.
- Fuera de la métrica.

---

## 📏 REGLAS GENERALES

- Identificar el tipo de contrato y su régimen **antes** que nada: el régimen condiciona todo lo
  demás.
- Detectar las cláusulas presentes y anclarlas.
- Detectar las ausencias relevantes **solo** contra una lista de referencia escrita.
- Priorizar los riesgos jurídicos.
- Explicar los riesgos con claridad.
- En caso de duda sobre el régimen: `null`, nunca inferencia.

---

## ✅ CONTRATO DE VALIDACIÓN

El JSON es válido **solo si**:

- Existen los 12 campos, en el orden del esquema.
- `standard_version` es exactamente `"contratos-v2"`.
- `regimen` ∈ `{"consumo", "administrativo", "mercantil"}` o `null`.
- `condicion_adherente` ∈ `{"consumidor", "empresario", "n_a"}` o `null`.
- `control_aplicable` **se deriva** de `regimen` y `condicion_adherente` según la tabla, o es
  `null` si alguno de los dos lo es.
- No se da ninguna de las dos combinaciones contradictorias: `consumo` + `empresario`, ni
  `administrativo` + `condicion_adherente` ≠ `n_a`.
- `parties` es array de objetos `{nombre, rol}` con al menos un elemento; `nombre` no vacío,
  `rol` puede ser `null`.
- `key_clauses` es array de objetos `{tipo, cita, localizador}`; ninguno de los tres vacío.
- Toda `cita`, en `key_clauses` y en `risk_flags`, aparece **verbatim** en el documento de
  origen.
- `missing_clauses` es array de objetos `{ref_id, lista_referencia, nota}`, y está **vacío** si
  el régimen del documento no tiene lista de referencia escrita.
- `risk_flags` es array de objetos con los diez subcampos del esquema.
- Todo `risk_flags[].id` existe en `corpus/rubrica-riskflags.md`.
- Todo `risk_flags[].regimen` coincide con el `regimen` del documento.
- `severity` ∈ `{"low", "medium", "high"}`.
- No hay contradicciones internas.

Si algo falla → registrarlo en `review_notes` con explicación técnica.

> **La comprobación mecánica no existe todavía.** `validate_contratos.ps1`, equivalente a
> `validate_v2.ps1`, está pendiente. Hasta entonces este contrato se comprueba a mano, y eso
> significa que se incumple sola: es la primera pieza a construir cuando exista la rúbrica.

---

## ⏳ PENDIENTE

Por orden de dependencia:

1. **Rúbrica de `risk_flags`** (`corpus/rubrica-riskflags.md`): cada criterio con identificador,
   definición, régimen aplicable, consecuencia jurídica y ejemplo de cláusula. Los criterios se
   extraen de las 9 resoluciones de la vía C. **Redactar antes de anotar ningún documento** — sin
   ella, `risk_flags[].id` no tiene vocabulario y el esquema no es aplicable.
2. **Listas de referencia de `missing_clauses`**, por régimen, según la tabla de arriba.
3. **`validate_contratos.ps1`**, con las comprobaciones del contrato de validación. La
   verificación verbatim de `cita` contra el input y la derivación de `control_aplicable` son
   las dos que más errores van a atrapar.

---

## 💾 FORMATO Y GUARDADO

JSON válido, sin texto libre fuera de la estructura.

Guardar en `Outputs/` con el nombre base del input y sufijo `.contrato.json`
(p. ej. `Inputs/corpus/via-a/pliego-01.txt` → `Outputs/pliego-01.contrato.json`).

El sufijo es distinto del `.v2.json` de sentencias a propósito: son dos contratos de datos
distintos y `validate_v2.ps1` no debe recogerlos.
