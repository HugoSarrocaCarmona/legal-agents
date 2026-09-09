# 📄 ESTÁNDAR: CONTRATOS

Fuente única de las reglas de análisis de contratos. `CLAUDE.md` recoge los principios comunes a
todos los tipos de documento y remite aquí.

Ante una discrepancia entre este archivo y los principios de `CLAUDE.md`, prevalece `CLAUDE.md`.

> **Estado: esquema v2. Ámbito operativo estrechado a `regimen = administrativo` (pliegos
> LCSP).** Los regímenes de consumo y mercantil siguen definidos —son lo que impide la
> contaminación— pero **no se ejercitan, no tienen rúbrica y no se miden** en esta iteración.
>
> Métrica decidida en [`corpus/metrica.md`](../corpus/metrica.md). Catálogo de flags en
> `corpus/rubrica-riesgos-lcsp.md` *(pendiente)*. Validador `validate_contratos.ps1`
> *(pendiente)*.
>
> **Es un esquema propio, no una variante del v2 de sentencias.** Contratos de datos distintos:
> no comparten campos, ni validador, ni métricas.

---

## ⚖️ REGLA QUE CONDICIONA TODO EL ESQUEMA

**`risk_flags` es consciente del régimen jurídico.** Sin eso, el esquema mezcla regímenes y las
métricas no significan nada.

El control de **contenido** —la declaración de abusividad, arts. 82 y ss. TRLGDCU— es derecho de
consumo y opera **solo frente a consumidores**. Un adherente **empresario**, bajo la Ley 7/1998
de Condiciones Generales de la Contratación, dispone únicamente de control de **incorporación y
transparencia**, no de control de abusividad. Son dos niveles distintos, no un mismo régimen
atenuado. Y nada de ello rige en un contrato administrativo sometido a la LCSP (Ley 9/2017) ni
en un mercantil negociado entre partes simétricas.

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

---

## 🏛️ REGLA PROPIA DEL RÉGIMEN ADMINISTRATIVO

En un pliego, la desigualdad entre las partes **no es un defecto: es el régimen**. La
Administración ostenta prerrogativas —modificar, interpretar, resolver— que la ley le atribuye
expresamente. Señalar como riesgo el mero hecho de que existan sería no entender el contrato.

**Lo que sí es riesgo en un pliego es una de estas tres cosas, y ninguna otra:**

1. **Divergencia de la ley.** El pliego establece algo que la LCSP no permite, o supera un
   umbral que la LCSP fija.
2. **Omisión de lo que la ley exige.** El pliego calla donde la LCSP obliga a pronunciarse.
3. **Desproporción dentro de lo legal.** El pliego se mantiene dentro de la ley pero traslada al
   contratista una carga o un riesgo desmedido respecto de la prestación.

Las dos primeras son **comprobables contra el texto de la ley**. La tercera es **juicio**.

> **Esa frontera es la que parte `risk_flags` en dos clases,** `normativo` y `valorativo`, y es
> lo que hace medible este esquema. El razonamiento completo está en
> [`corpus/metrica.md`](../corpus/metrica.md); aquí solo se recoge la consecuencia sobre los
> campos.

**Y una consecuencia práctica que hay que tener presente al redactar los flags:** el análisis se
hace desde la posición del **licitador que ejecutará el contrato**, no desde la del órgano de
contratación ni desde la de quien impugna la licitación. La pregunta que responde este esquema
es *«¿qué me puede costar dinero si gano esto?»*, no *«¿es impugnable este pliego?»*.

---

## 📦 ESQUEMA JSON (v2)

```json
{
  "document_type": "",
  "governing_law": "",
  "regimen": "consumo|administrativo|mercantil",
  "control_aplicable": "contenido_y_transparencia|solo_incorporacion_y_transparencia|n_a",
  "expediente": {
    "organo_contratacion": "",
    "objeto": "",
    "cpv": [],
    "valor_estimado": null,
    "presupuesto_base_licitacion": null,
    "plazo_ejecucion": ""
  },
  "parties": [],
  "key_clauses": [
    { "materia": "", "clausula_ref": "", "texto_literal": "" }
  ],
  "missing_clauses": [
    { "materia": "", "base_normativa": "", "why_it_matters": "" }
  ],
  "risk_flags": [
    {
      "id": "",
      "clase": "normativo|valorativo",
      "materia": "",
      "clausula_ref": "",
      "texto_literal": "",
      "issue": "",
      "criterio": "",
      "base_normativa": "",
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
partes y del contrato, no por su contenido. En caso de duda: `null`, nunca inferencia. Un
régimen mal asignado contamina todos los `risk_flags` del documento.

**`control_aplicable`** — Depende de `regimen` y de la condición del adherente:

| Situación | Valor |
|---|---|
| `regimen=consumo` y el adherente es consumidor | `contenido_y_transparencia` |
| Adherente **empresario** sobre clausulado predispuesto (Ley 7/1998) | `solo_incorporacion_y_transparencia` |
| `regimen=administrativo` o `mercantil` negociado | `n_a` |

**`expediente`** — Solo en régimen administrativo; `null` en los demás. Se extrae de la carátula
o cuadro de características del PCAP. **No se infiere del clausulado**: si el importe no aparece
como tal, es `null`, aunque se pueda deducir sumando anualidades.

**`key_clauses[].materia`** — Del vocabulario cerrado de materias (más abajo). Localiza dónde
trata el pliego cada materia. **Es un campo de localización, no de juicio**: incluir una materia
sin riesgo asociado es correcto y esperado.

**`key_clauses[].texto_literal`** — Transcripción literal, no paráfrasis. Es lo que permite
auditar el flag sin volver al PDF.

**`missing_clauses[]`** — **Solo admite ausencias que alguna norma exija subsanar.** Una
cláusula que convendría tener pero que ninguna norma impone no es una ausencia reprochable: va a
`review_notes`. Sin `base_normativa`, la entrada es inválida.

**`risk_flags[].id`** — Identificador del catálogo cerrado de la rúbrica. **No se inventan
identificadores.** Un riesgo real que no esté en la rúbrica se anota en `review_notes` con la
propuesta de alta, y la rúbrica se amplía en su propio fichero — nunca sobre la marcha dentro de
un output.

**`risk_flags[].clase`** — Determina cómo se mide el flag y qué se le exige:

| Clase | El flag afirma | Exigencia |
|---|---|---|
| `normativo` | Divergencia u omisión respecto de la LCSP | `base_normativa` **obligatoria** y verificada contra el BOE |
| `valorativo` | Desproporción dentro de lo legal | `base_normativa` **null**, `criterio` obligatorio |

Un flag `normativo` sin `base_normativa`, o con una que no dice lo que se le atribuye, es un
**fallo duro**: invalida el documento, no cuenta como una omisión más. Es la versión contractual
de la sentencia inventada.

**`risk_flags[].base_normativa`** — Artículo y apartado concretos, con la norma citada por su
identificador completo. Formato: `art. 192.1 LCSP`. Nunca un artículo «aproximado» ni una
remisión genérica a la ley.

**`risk_flags[].criterio`** — El criterio sustantivo que se aplica (desequilibrio, falta de
reciprocidad, opacidad, desproporción de la penalización, facultad unilateral…). Es lo que se
transfiere entre regímenes. Obligatorio en los flags `valorativo`; en los `normativo` puede ser
`null`, porque ahí lo que sostiene el flag es la norma, no el criterio.

**`risk_flags[].regimen`** — Debe coincidir con el `regimen` del documento. Un flag cuyo régimen
no coincida es un error de anotación, no una observación válida — y es **fallo duro**.

**`risk_flags[].consecuencia_juridica`** — La consecuencia **dentro de su régimen**. Solo en
consumo puede ser la nulidad por abusividad. En administrativo, describir el efecto que
corresponda —nulidad de la cláusula, inaplicación, causa de impugnación del pliego, derecho
indemnizatorio del contratista— o `null` si no hay consecuencia típica. **Emplear vocabulario de
consumo bajo `regimen=administrativo` es fallo duro.**

**`severity`** — Nunca inferir gravedad de la mera presencia de una cláusula: depende del
contenido y de sus cifras. Una penalidad del 8 % y una del 0,5 % son la misma materia y no la
misma gravedad. No interviene en el emparejamiento de la métrica.

**`suggested_fix`** — En régimen administrativo, el licitador **no negocia el pliego**: lo acepta
o no se presenta. Por eso aquí `suggested_fix` no propone redacción alternativa, sino la
**acción disponible**: cuantificar el riesgo en la oferta económica, pedir aclaración en plazo,
impugnar el pliego, o desistir. Proponer una redacción alternativa sería no entender el régimen.

---

## 🗂️ VOCABULARIO CERRADO DE MATERIAS

Alcance obligatorio de la rúbrica. Cada materia agrupa los flags de ambas clases. Los artículos
citados son el ancla normativa de la materia, verificados contra el texto consolidado del BOE.

| # | Materia | Ancla en la LCSP (Ley 9/2017) |
|---|---|---|
| 1 | Penalidades por incumplimiento parcial o defectuoso | art. 192 |
| 2 | Penalidades por demora | art. 193 |
| 3 | Daños y perjuicios e imposición de penalidades | art. 194 |
| 4 | Garantía definitiva y complementaria | arts. 107–108 |
| 5 | Revisión de precios | arts. 103–104 |
| 6 | Riesgo y ventura | art. 197 |
| 7 | Condiciones especiales de ejecución | art. 202 |
| 8 | Modificación del contrato — prevista y no prevista | arts. 203–205 |
| 9 | Suspensión del contrato | art. 208 |
| 10 | Cumplimiento, recepción y plazo de garantía | art. 210 (general) · **art. 243 en obras** |
| 11 | Causas de resolución | art. 211 |
| 12 | Cesión del contrato | art. 214 |
| 13 | Subcontratación y pago a subcontratistas | arts. 215–216 |
| 14 | Pago del precio y demora de la Administración | art. 198 |
| 15 | Confidencialidad | art. 133 |
| 16 | Protección de datos y encargo de tratamiento | DA 25.ª |

> **Regla de cierre:** una materia que no esté en esta tabla no genera flags. Si aparece un
> riesgo real fuera de ella, va a `review_notes` y la tabla se amplía **aquí**, con su ancla
> verificada, antes de poder anotarlo. Es la misma disciplina que `corpus/alcance.md` aplica al
> corpus: nada entra sobre la marcha.

**El ancla depende del tipo de contrato, no solo de la materia.** El art. 210 es la regla
general de recepción, pero los contratos de **obras** se rigen por el art. 243. Antes de emitir
un flag normativo hay que confirmar que el artículo citado es el aplicable *a ese tipo
contractual*, no solo a la materia. Citar la regla general donde rige la especial es una
`base_normativa` incorrecta, y por tanto **fallo duro**.

> ⚠️ **Cuestión abierta sobre el alcance: las concesiones demaniales.** El corpus actual incluye
> un pliego de concesión demanial (`pliego-02`). Las concesiones sobre bienes de dominio público
> se rigen por la **Ley 33/2003 del Patrimonio de las Administraciones Públicas**, no por la
> LCSP, cuyo art. 9.1 las excluye de su ámbito. Un pliego así **no es anotable con esta rúbrica**
> sin añadir la LPAP como ancla normativa propia — es decir, exactamente el supuesto de exclusión
> automática que fija `corpus/alcance.md`: un documento que obliga a crear referencias nuevas no
> entra en esta iteración. **Verificar el tipo contractual de `pliego-02` y, si se confirma,
> apartarlo antes de anotar.**

---

## 📏 REGLAS GENERALES

- Identificar el tipo de contrato y el régimen antes que nada.
- Localizar cada materia del vocabulario presente en el documento.
- Detectar las ausencias **que alguna norma exija**.
- Priorizar los riesgos por lo que pueden costar en ejecución, no por su vistosidad.
- Explicar los riesgos con claridad, en términos del dinero o del plazo que ponen en juego.
- En caso de duda sobre el régimen: `null`, nunca inferencia.
- En caso de duda sobre una `base_normativa`: **no emitir el flag**. Un flag normativo sin
  respaldo verificado es peor que un flag omitido.

---

## ⏳ PENDIENTE

- **`corpus/rubrica-riesgos-lcsp.md`** — catálogo cerrado de flags. Cada uno con `id`, `clase`,
  materia, criterio o base normativa según su clase, consecuencia jurídica y ejemplo de cláusula
  real. **Redactar antes de anotar ningún documento.** Es el paso siguiente.
- **`validate_contratos.ps1`** — validador mecánico. Debe comprobar, como mínimo: `id` dentro del
  catálogo, coherencia `clase` ↔ `base_normativa`, coincidencia de `regimen`, vocabulario de
  `consecuencia_juridica` por régimen, y que toda entrada de `missing_clauses` lleve
  `base_normativa`.
- **Gold sobre vía A**, anotado contra la rúbrica y partido en ciego-1 / ciego-2.
