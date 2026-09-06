# 📄 ESTÁNDAR: CONTRATOS (v3)

Fuente única de las reglas de análisis de contratos administrativos y de clausulado sometido a
condiciones generales de la contratación. `CLAUDE.md` recoge los principios comunes a todos los
tipos de documento y remite aquí.

Ante una discrepancia entre este archivo y los principios de `CLAUDE.md`, prevalece
`CLAUDE.md`. Sobre **cómo se mide** un campo, prevalece
[`corpus/metrica-contratos.md`](../corpus/metrica-contratos.md).

> **Estado: esquema v3, sin ejercitar.** No hay ficheros de referencia ni validador mecánico
> equivalente a `validate_v2.ps1`. Este estándar está escrito y **no medido**.
>
> **Es un esquema propio, no una variante del de sentencias.** Son contratos de datos distintos:
> no comparten campos, ni validador, ni métricas. La coincidencia de números de versión entre
> ambos es casual y no significa nada.

---

## 🎯 ALCANCE: DOS REGÍMENES, NO TRES

**Este estándar cubre dos regímenes y solo dos**, que se corresponden con las dos vías vivas del
corpus:

| Régimen | Vía del corpus | Qué es |
|---|---|---|
| `administrativo` | **A** | Contrato del sector público sometido a la LCSP (Ley 9/2017). Pliegos PCAP/PPT |
| `condiciones_generales` | **C** | Clausulado predispuesto por una parte al que la otra se adhiere, sometido a la Ley 7/1998 y —si el adherente es consumidor— al TRLGDCU |

**El régimen mercantil negociado queda fuera del alcance**, y con él la vía B. Un contrato
libremente negociado entre partes simétricas no tiene control de contenido ni lista de
referencia defendible: lo que «debería» estar en él es una preferencia de negociación, no una
exigencia jurídica. Anotarlo sería registrar la opinión del anotador y llamarlo dato.

> **`condiciones_generales` no es lo mismo que «consumo».** Es el eje correcto porque nombra la
> **fuente del problema** —clausulado predispuesto, no negociado— en lugar de una de sus dos
> consecuencias. Quién sea el adherente (`condicion_adherente`) es lo que decide **qué control**
> se aplica, y es un dato distinto del régimen.
>
> Esta separación no es teórica: el corpus tiene ya un contrato de adhesión de servicios de
> inversión dirigido a **clientes profesionales** (`adhesion-05`). Con un eje que confundiera
> régimen y condición del adherente, ese documento no tendría clasificación posible.

**Límite conocido del eje, y por qué se acepta.** La Ley 7/1998 exige que el clausulado esté
predispuesto **para una pluralidad de contratos**; el control de contenido del art. 82 TRLGDCU
alcanza a toda cláusula **no negociada individualmente** en contrato con consumidor, aunque sea
de un contrato único. Los dos conjuntos se solapan casi por completo en el clausulado de
adhesión masiva, que es lo que contiene la vía C. Una cláusula no negociada de un contrato de
consumo aislado quedaría fuera de la definición estricta de condición general: **no hay ninguna
en el corpus, y si aparece se registra en `review_notes` en lugar de forzar el eje.**

---

## 🔀 QUÉ CAMBIA RESPECTO DE v2

Ninguna versión anterior produjo output. **No hay nada que migrar, y no lo habrá una vez exista
el primer Gold**: el momento de cambiar el esquema es exactamente este.

| Cambio | Por qué |
|---|---|
| `regimen` pasa de `consumo\|administrativo\|mercantil` a `administrativo\|condiciones_generales` | El eje anterior mezclaba la fuente del control con su consecuencia, y `mercantil` agrupaba dos cosas incompatibles: contrato negociado (sin adherente) y adhesión con adherente empresario |
| Fuera el régimen mercantil negociado | Sin lista de referencia defendible y sin control de contenido. Ver alcance |
| `severity` pasa a ser **derivado** de `severity_driver` y `desproporcion` | Tres niveles subjetivos son el campo que más destroza el acuerdo entre anotadores. Ahora el juicio vive en un solo campo, acotado y nombrado |
| `criterio` pasa a enum cerrado | Era texto libre, y sin vocabulario cerrado no es medible ni comparable |

---

## ⚖️ REGLA QUE CONDICIONA TODO EL ESQUEMA

**`risk_flags` es consciente del régimen jurídico.** Sin eso, el esquema mezcla regímenes y las
métricas no significan nada.

El control de **contenido** —la declaración de abusividad, arts. 82 y ss. TRLGDCU— es derecho
de consumo y opera **solo frente a consumidores**. Un adherente **empresario**, bajo la Ley
7/1998 de Condiciones Generales de la Contratación, dispone únicamente de control de
**incorporación y transparencia**, no de control de abusividad. Son dos niveles distintos, no
un mismo régimen atenuado. Y nada de ello rige en un contrato administrativo sometido a la LCSP.

**Consecuencia directa: una cláusula declarada abusiva por un juez no es una etiqueta
transferible a un pliego administrativo.** Copiar esas etiquetas importa un régimen que allí no
rige, y la evaluación mediría algo que no existe.

De la jurisprudencia se transfieren los **criterios**, nunca las **calificaciones**. La
*consecuencia jurídica* (nulidad por abusividad) solo en consumo; el criterio sustantivo, en
cualquier régimen.

**Riesgos propios del régimen administrativo**, que no derivan de la doctrina de consumo:
penalidades por demora, régimen de garantías, revisión de precios, modificación unilateral
(*ius variandi*), causas de resolución, subcontratación, cesión, confidencialidad y plazos de
pago.

---

## 📦 ESQUEMA JSON (12 campos, en este orden)

```json
{
  "standard_version": "contratos-v3",
  "document_type": "",
  "governing_law": "",
  "regimen": "administrativo|condiciones_generales",
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
      "criterio": "desequilibrio|falta_reciprocidad|falta_transparencia|desproporcion_penalizacion|facultad_unilateral",
      "regimen": "administrativo|condiciones_generales",
      "consecuencia_juridica": "",
      "severity_driver": "perdida_prestacion|restriccion_defensa|coste_economico|sin_efecto_economico",
      "desproporcion": "si|no|indeterminado|n_a",
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

- **Valor literal y obligatorio: `"contratos-v3"`.** Este valor se define aquí y **solo** aquí.
- No se deduce, no se recuerda y no se infiere del nombre del fichero.
- **Para qué sirve.** Si el agente no lee este archivo y trabaja de memoria, produce un JSON
  plausible con reglas recordadas que ningún control detecta. Un valor que solo puede conocerse
  leyendo este fichero convierte ese fallo silencioso en un fallo visible.
- No demuestra que las reglas se hayan aplicado bien; demuestra que el estándar se abrió. Es el
  mínimo, y es mucho más que nada.

### document_type

- Tipo contractual, en minúscula y en la denominación que use el propio documento
  (`"contrato de suministro de energía"`, `"pliego de cláusulas administrativas particulares"`).
- No inferirlo del nombre del archivo.

### governing_law

- Ley aplicable **solo si el documento la declara**. Si no la declara → `null`.
- No deducirla de la lengua, del domicilio de las partes ni del tipo de contrato.

### regimen

- **ENUM CERRADO**: `"administrativo"` | `"condiciones_generales"`.
- Se determina por la **naturaleza de las partes y del contrato**, no por su contenido.
- `administrativo`: una de las partes es un poder adjudicador y el contrato se somete a la LCSP.
- `condiciones_generales`: el clausulado lo predispone una parte y la otra se adhiere sin
  negociarlo.
- Un documento que no encaje en ninguno de los dos **está fuera del alcance de este estándar**:
  `null`, y registrarlo en `review_notes`. No forzarlo.

> ⚠️ **Un `regimen` equivocado contamina todos los `risk_flags` del documento**, porque cambia
> qué control es aplicable y qué consecuencia jurídica puede afirmarse. Por eso la métrica trata
> un documento con `regimen` incorrecto como **contaminado** y lo excluye del cómputo de
> detección en vez de promediarlo.

### condicion_adherente

- **ENUM CERRADO**: `"consumidor"` | `"empresario"` | `"n_a"`.
- Condición de quien **se adhiere** al clausulado predispuesto por la otra parte.
- `"n_a"` **solo** en régimen administrativo: el contratista acepta el pliego, pero el aparato de
  control aplicable es el de la LCSP y no el de condiciones generales.
- Es un campo **extraído**, no interpretado: se toma de cómo el documento identifica al
  adherente y a qué público se dirige. Un contrato de servicios de inversión dirigido a
  «clientes profesionales y contrapartes elegibles» declara a su adherente. Si el documento no
  permite determinarlo → `null`.

### control_aplicable

- **ENUM CERRADO**, y **derivado** de los dos campos anteriores. No es una valoración libre:

| `regimen` | `condicion_adherente` | `control_aplicable` |
|---|---|---|
| `condiciones_generales` | `consumidor` | `contenido_y_transparencia` |
| `condiciones_generales` | `empresario` | `solo_incorporacion_y_transparencia` |
| `administrativo` | `n_a` | `n_a` |

- **`n_a` significa que no rige el control de condiciones generales, no que no haya control.**
  En un contrato administrativo el control existe y es el de la LCSP; opera por otra vía y con
  otras consecuencias.
- Si `regimen` o `condicion_adherente` es `null`, `control_aplicable` es `null`.

**Las tres filas son exhaustivas. Cualquier otra combinación es una contradicción, no un caso
raro:**

- `administrativo` con `condicion_adherente` distinto de `n_a`.
- `condiciones_generales` con `condicion_adherente` = `n_a` — si no hay adherente, no hay
  condiciones generales.

Ante cualquiera de las dos: revisar `regimen`, que es el campo que manda, y registrar la
anomalía en `review_notes`.

### parties

- **Estructura obligatoria**: array de objetos `{nombre, rol}`.
- `rol` tomado literalmente del documento (`"órgano de contratación"`, `"predisponente"`,
  `"adherente"`, `"tomador"`). No inferirlo: si el documento nombra a alguien sin asignarle rol
  → `rol: null`. `nombre` nunca es `null`.
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
| `condiciones_generales` | Se deriva de la rúbrica, a partir de las 9 resoluciones de la vía C | **Pendiente de redactar** |

**Mientras la lista de un régimen no esté escrita, `missing_clauses` va vacío en ese régimen y
no se mide.** Es preferible un campo vacío a un campo relleno con criterio implícito: la métrica
distingue el vacío declarado del no medido, y el segundo no puntúa.

### risk_flags

Campo central del esquema.

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

**`criterio`** — **ENUM CERRADO.** El criterio sustantivo que hace de esto un riesgo **en
Derecho**. Es lo que se transfiere entre regímenes, y es la razón de que la jurisprudencia de
consumo sirva para leer un pliego:

| Valor | Qué señala |
|---|---|
| `desequilibrio` | Desequilibrio importante entre las prestaciones de las partes |
| `falta_reciprocidad` | Una carga, plazo o remedio que solo opera en un sentido |
| `falta_transparencia` | Redacción que impide comprender la carga económica o jurídica real |
| `desproporcion_penalizacion` | La consecuencia del incumplimiento excede lo que el incumplimiento justifica |
| `facultad_unilateral` | Atribución a una parte de interpretar, modificar o resolver por sí sola |

**`regimen`** — Debe coincidir con el `regimen` del documento. Un flag cuyo régimen no coincida
es un error de anotación, no una observación válida.

**`consecuencia_juridica`** — La consecuencia **dentro de su régimen y su control**:

| `control_aplicable` | Consecuencias invocables |
|---|---|
| `contenido_y_transparencia` | Nulidad por abusividad (arts. 82 y ss. TRLGDCU), no incorporación, falta de transparencia |
| `solo_incorporacion_y_transparencia` | No incorporación y falta de transparencia (Ley 7/1998). **Nunca abusividad** |
| `n_a` (administrativo) | El efecto que corresponda en la LCSP, o `null` si no hay consecuencia típica |

### severity: por qué es derivada, y de qué

**`severity` no se puntúa a ojo. Se deriva de dos campos anteriores.**

La razón es la misma por la que `control_aplicable` se deriva: una escala subjetiva de tres
niveles es el campo que más destruye el acuerdo entre anotadores, y sin acuerdo entre anotadores
no hay Gold fiable ni métrica que signifique nada. En tareas jurídicas subjetivas, el acuerdo
entre juristas titulados se queda en torno a κ = 0,3-0,6. Un `high` sin justificar es una
opinión no falsable: no se puede comprobar, no se puede discutir y no se puede medir.

La solución no es eliminar la gravedad —es información útil, y es por lo que un revisor ordena
su trabajo— sino **aislar el juicio en un solo campo, acotado y nombrado**, y derivar el resto.

**`severity_driver`** — **ENUM CERRADO.** Qué es lo peor que esa cláusula **puede hacer**, según
su propio texto:

| Valor | Qué significa |
|---|---|
| `perdida_prestacion` | Puede privar a la contraparte de aquello por lo que contrató: resolución unilateral, pérdida de lo entregado, decaimiento del derecho |
| `restriccion_defensa` | Cierra o encarece una vía de defensa o reclamación: sumisión, renuncia de acciones, inversión de la carga de la prueba, limitación de medios de prueba |
| `coste_economico` | Traslada un coste cuantificable: penalidad, interés, comisión, garantía, indemnización |
| `sin_efecto_economico` | Defecto de transparencia, incorporación o forma, sin efecto económico directo identificable en el texto |

**Regla de desempate:** si una cláusula encaja en más de uno, se toma el **primero de la tabla**.
El driver nombra lo más grave que la cláusula puede hacer, no todo lo que hace.

**`desproporcion`** — **El único campo del esquema que es un juicio, y está acotado a un caso.**
Solo se aplica cuando `severity_driver` es `coste_economico`; en cualquier otro caso vale `n_a`.

Pregunta exacta: *¿el coste que impone esta cláusula excede lo que justifica el incumplimiento o
la contraprestación que lo desencadena, **según las cifras del propio contrato**?*

| Valor | Cuándo |
|---|---|
| `si` | El contrato da la cifra o el umbral, y excede |
| `no` | El contrato da la cifra o el umbral, y no excede |
| `indeterminado` | **El contrato no da la cifra o el umbral necesarios para juzgarlo** |
| `n_a` | El driver no es `coste_economico` |

**`indeterminado` no es un fallo de anotación: es la respuesta correcta cuando el documento no
da la cifra.** Es la aplicación del principio 7 de `CLAUDE.md` —preferir `null` antes que
inferencia— a un campo que no admite `null`, y tiene una consecuencia mecánica: deriva `medium`,
nunca `high`. En caso de duda, la gravedad baja.

**`severity`** — **DERIVADA. No se decide, se calcula:**

| `severity_driver` | `desproporcion` | `severity` |
|---|---|---|
| `perdida_prestacion` | `n_a` | `high` |
| `restriccion_defensa` | `n_a` | `high` |
| `coste_economico` | `si` | `high` |
| `coste_economico` | `no` | `medium` |
| `coste_economico` | `indeterminado` | `medium` |
| `sin_efecto_economico` | `n_a` | `low` |

La tabla es exhaustiva: seis filas cubren todas las combinaciones válidas. Cualquier otra es un
error de validación.

> **Qué se gana con esto.** De «puntúa cada riesgo del 1 al 3» se pasa a «di qué puede hacer la
> cláusula, y solo si es económica, di si la cifra es desproporcionada». Tres de los cuatro
> drivers son deterministas. El juicio queda en una casilla, con una pregunta escrita y una
> regla de empate. Y cuando el Gold y el agente discrepen, **el desacuerdo dirá en qué**: si en
> el driver, es un problema de lectura de la cláusula; si en `desproporcion`, es un problema de
> criterio. Con un `severity` suelto, las dos cosas se veían igual.

**`why_it_matters`** y **`suggested_fix`** — Texto libre. **No entran en la métrica**: dos
redacciones distintas pueden ser ambas correctas, y puntuarlas con igualdad exacta daría un
número falso. Se revisan cualitativamente sobre muestra.

### plain_language_summary

- String. Qué hace el contrato y a qué obliga a cada parte, sin jerga.
- Fuera de la métrica.

### review_notes

- Array. Defectos del soporte y anomalías del análisis: documento truncado, clausulado remitido
  a un anexo que no consta, contradicciones internas, combinaciones contradictorias de `regimen`
  y `condicion_adherente`, y documentos que no encajan en ninguno de los dos regímenes.
- Fuera de la métrica.

---

## 📏 REGLAS GENERALES

- Identificar el régimen **antes** que nada: condiciona todo lo demás.
- Detectar las cláusulas presentes y anclarlas al texto.
- Detectar las ausencias relevantes **solo** contra una lista de referencia escrita.
- Priorizar los riesgos jurídicos.
- Explicar los riesgos con claridad.
- En caso de duda sobre el régimen: `null`, nunca inferencia.

---

## ✅ CONTRATO DE VALIDACIÓN

El JSON es válido **solo si**:

- Existen los 12 campos, en el orden del esquema.
- `standard_version` es exactamente `"contratos-v3"`.
- `regimen` ∈ `{"administrativo", "condiciones_generales"}` o `null`.
- `condicion_adherente` ∈ `{"consumidor", "empresario", "n_a"}` o `null`.
- `control_aplicable` **se deriva** de `regimen` y `condicion_adherente` según su tabla, o es
  `null` si alguno de los dos lo es.
- No se da ninguna de las dos combinaciones contradictorias: `administrativo` con
  `condicion_adherente` ≠ `n_a`, ni `condiciones_generales` con `condicion_adherente` = `n_a`.
- `parties` es array de objetos `{nombre, rol}` con al menos un elemento; `nombre` no vacío,
  `rol` puede ser `null`.
- `key_clauses` es array de objetos `{tipo, cita, localizador}`; ninguno de los tres vacío.
- Toda `cita`, en `key_clauses` y en `risk_flags`, aparece **verbatim** en el documento de
  origen.
- `missing_clauses` es array de objetos `{ref_id, lista_referencia, nota}`, y está **vacío** si
  el régimen del documento no tiene lista de referencia escrita.
- `risk_flags` es array de objetos con los doce subcampos del esquema.
- Todo `risk_flags[].id` existe en `corpus/rubrica-riskflags.md`.
- Todo `risk_flags[].regimen` coincide con el `regimen` del documento.
- `criterio` ∈ el enum de cinco valores.
- `severity_driver` ∈ el enum de cuatro valores.
- `desproporcion` es `"n_a"` **si y solo si** `severity_driver` ≠ `"coste_economico"`.
- `severity` **se deriva** de `severity_driver` y `desproporcion` según su tabla de seis filas.
- `consecuencia_juridica` no invoca la abusividad cuando `control_aplicable` ≠
  `contenido_y_transparencia`.
- No hay contradicciones internas.

Si algo falla → registrarlo en `review_notes` con explicación técnica.

> **La comprobación mecánica no existe todavía.** `validate_contratos.ps1`, equivalente a
> `validate_v2.ps1`, está pendiente. Hasta entonces este contrato se comprueba a mano, y eso
> significa que se incumple sola: es la primera pieza a construir cuando exista la rúbrica.
>
> Cinco de estas comprobaciones son puramente mecánicas y van a atrapar la mayor parte de los
> errores: la cita verbatim, las dos derivaciones (`control_aplicable` y `severity`), la
> exclusividad de `desproporcion`, y la pertenencia de `id` a la rúbrica.

---

## ⏳ PENDIENTE

Por orden de dependencia:

1. **Rúbrica de `risk_flags`** (`corpus/rubrica-riskflags.md`): cada criterio con identificador,
   definición, régimen aplicable, `criterio` y `severity_driver` típicos, consecuencia jurídica
   y ejemplo de cláusula. Se extrae de las 9 resoluciones de la vía C. **Redactar antes de
   anotar ningún documento** — sin ella, `risk_flags[].id` no tiene vocabulario y el esquema no
   es aplicable.
2. **Listas de referencia de `missing_clauses`**, una por régimen, según su tabla.
3. **`validate_contratos.ps1`**, con las comprobaciones del contrato de validación.

---

## 💾 FORMATO Y GUARDADO

JSON válido, sin texto libre fuera de la estructura.

Guardar en `Outputs/` con el nombre base del input y sufijo `.contrato.json`
(p. ej. `Inputs/corpus/via-a/pliego-01.txt` → `Outputs/pliego-01.contrato.json`).

El sufijo es distinto del `.v2.json` de sentencias a propósito: son dos contratos de datos
distintos y `validate_v2.ps1` no debe recogerlos.
