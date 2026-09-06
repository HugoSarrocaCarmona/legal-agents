# 📐 Métrica de evaluación — contratos

**Decidida antes de anotar ningún documento.** Fijada: 06/09/2026.
Cierra el paso 1 de la fase 2 del [`ROADMAP.md`](../progress/ROADMAP.md).

Este fichero define **qué significa que un output de contratos sea correcto**, y por tanto qué
tiene que registrar el Gold. Es anterior al Gold a propósito: en la fase 1 el esquema se diseñó
antes de saber cómo se iba a medir, y los campos sustantivos se quedaron sin evaluación de
contenido. En contratos casi todo el esquema es sustantivo.

Ante una discrepancia entre este archivo y [`standards/contratos.md`](../standards/contratos.md)
sobre la **forma** de un campo, prevalece el estándar. Sobre **cómo se mide**, prevalece este.

---

## Origen: por qué esta métrica y no una propia

Se adopta el esquema de **ContractEval** (arXiv 2508.03080), que evalúa identificación de riesgo
a nivel de cláusula sobre CUAD, con dos adaptaciones documentadas más abajo. No se diseña una
métrica nueva por dos razones:

1. **Está resuelto.** El problema —cómo puntuar un campo multietiqueta donde la respuesta es
   más o menos completa, no correcta o incorrecta— ya tiene una respuesta publicada y usada.
2. **Comparabilidad.** Un resultado calculado con el mismo esquema que la literatura es un dato
   citable. Uno calculado con una métrica casera solo se compara consigo mismo.

De la misma literatura se toman dos decisiones concretas: la ponderación de la exhaustividad
(**F2**, de ContractEval) y la descomposición de la rúbrica en **criterios atómicos binarios**
(del *Legal Agent Benchmark* de Harvey). Detalle en
[`research/mercado-legaltech-2026.md`](../research/mercado-legaltech-2026.md), sección 7.

---

## Tres niveles de medición, que no se agregan

El error a evitar es una cifra global de "precisión" que mezcle campos heterogéneos. El esquema
de contratos tiene tres clases de campo y cada una se mide distinto. **No se suman en un único
porcentaje.**

| Nivel | Campos | Métrica |
|---|---|---|
| **1. Mecánicos** | `standard_version`, `document_type`, `governing_law`, `regimen`, `condicion_adherente`, `control_aplicable`, `parties` | Igualdad exacta |
| **2. Detección** | `risk_flags`, `key_clauses`, `missing_clauses` | F1, F2, Jaccard, pereza |
| **3. Texto libre** | `plain_language_summary`, `review_notes`, y dentro de cada flag: `issue`, `why_it_matters`, `suggested_fix` | **Fuera de la métrica.** Revisión cualitativa muestreada |

### Por qué el nivel 3 queda fuera

`why_it_matters` y `suggested_fix` no admiten comparación exacta ni solapamiento de conjuntos:
dos redacciones distintas pueden ser ambas correctas. Puntuarlas con igualdad exacta daría un
número falso; puntuarlas con juicio por modelo introduciría un evaluador menos consistente que
un humano (ver *Acuerdo esperable* más abajo) para campos que **no deciden nada**: el valor
operativo del output está en detectar el riesgo y anclarlo, no en la prosa que lo explica.

Se revisan cualitativamente sobre una muestra, y esa revisión se registra como observación, no
como cifra. Si una revisión detecta un patrón de error, el sitio para corregirlo es la rúbrica.

---

## Nivel 1 — Campos mecánicos

Igualdad exacta contra el Gold, un acierto por campo y documento. Es la misma métrica que
`eval_gold.ps1` aplica a los campos de cabecera de sentencias, y funciona por la misma razón:
tienen una única respuesta correcta.

**`parties` se compara como conjunto**, sin orden: aciertan los dos campos de todos sus
elementos, o no acierta. Es un campo mecánico pese a ser un array, porque un contrato identifica
a sus partes de forma expresa y cerrada.

**`control_aplicable` se deriva de `regimen` y `condicion_adherente`.** Medirlo como campo
independiente no informa de nada nuevo cuando la derivación es correcta: lo que su fallo detecta
es que el agente no aplicó la tabla del estándar. Se reporta, pero como control de aplicación de
regla, no como acierto sustantivo.

> ⚠️ **Un 100 % aquí no dice nada del resto.** Es exactamente el error que documenta
> `ESTADO.md` sobre el 315/315 de sentencias, y la literatura lo confirma: ContractEval mide
> F1 ≈ 0,9 en cláusulas frecuentes y **cerca de cero** en cláusulas raras de alto riesgo, con el
> mismo modelo y el mismo documento. Reportar el nivel 1 sin el nivel 2 al lado es engañoso.

**`regimen` es especial: un fallo aquí invalida el documento entero.** Un régimen mal asignado
contamina todos los `risk_flags`, porque cambia qué control es aplicable y qué consecuencia
jurídica puede afirmarse. Un documento con `regimen` incorrecto **no puntúa en el nivel 2**: se
cuenta aparte como *documento contaminado* y se reporta su número. Promediarlo con el resto
mediría una detección que se apoya en una premisa falsa.

---

## Nivel 2 — Campos de detección

### Qué es la unidad de medida

**No el documento: el criterio anotado.** Un documento con 15 riesgos anotados aporta 15
unidades, no una.

Esto es lo que hace medible un corpus de decenas. Es el patrón del *Legal Agent Benchmark* de
Harvey (1.200 tareas, 75.000 criterios: unos 62 por tarea). Con 23 documentos activos y del
orden de 15-25 unidades por documento, la N efectiva pasa de decenas a varios centenares.

> ⚠️ **Las unidades de un mismo documento no son independientes.** Un contrato de adhesión
> redactado por un mismo predisponente repite el mismo tipo de desequilibrio en varias
> cláusulas: acertar una hace más probable acertar las demás. La consecuencia **no** es
> descartar la unidad-criterio, es no calcular incertidumbre como si fueran independientes.
> Ver *Qué se puede concluir* al final.

### Qué significa "bien detectado"

**Un riesgo está bien detectado cuando el agente emite un flag con el mismo identificador de
rúbrica que el Gold y anclado en la misma cláusula.** Nada más entra en la detección: ni la
redacción de `issue`, ni `why_it_matters`, ni `suggested_fix`, ni los atributos calificadores
—`criterio`, `severity_driver`, `desproporcion`—, que se miden aparte y por separado.

Esto exige dos cosas del esquema, y por eso la métrica se decide antes que el Gold:

1. Que `risk_flags[].id` sea un **identificador de la rúbrica**, no texto libre. Sin
   vocabulario cerrado no hay emparejamiento posible.
2. Que cada flag lleve **ancla al texto** (`cita` + `localizador`). Sin ancla no se puede saber
   si dos flags con el mismo `id` hablan de la misma cláusula o de dos distintas.

### Emparejamiento

Es un problema de conjuntos, no de igualdad. Para cada documento:

1. Un flag predicho `p` y un flag del Gold `g` son **candidatos** si `p.id == g.id` **y** sus
   anclas se solapan (comparten texto, o el `localizador` apunta a la misma cláusula).
2. Entre los candidatos se emparejan **uno a uno**, tomando primero el par de mayor solapamiento.
3. Par emparejado → **TP**. Predicción sin pareja → **FP**. Gold sin pareja → **FN**.

**El mismo `id` puede aparecer varias veces en un documento** —dos cláusulas distintas pueden
incurrir en el mismo desequilibrio— y por eso el emparejamiento es por instancia, no por
conjunto de identificadores.

No hay TN: en una tarea de detección sobre un documento abierto no existe el conjunto de "no
riesgos". No hace falta — la familia F se calcula solo con TP, FP y FN.

### Corrección: F1 y F2

```
P  = TP / (TP + FP)
R  = TP / (TP + FN)

F1 = 2 · (P · R) / (P + R)
F2 = 5 · (P · R) / (4 · P + R)
```

**La métrica principal es F2.** F2 es F-beta con β = 2: pondera la exhaustividad por encima de
la precisión, penalizando más los falsos negativos que los falsos positivos.

Esto responde a una pregunta que estaba abierta en `IDEAS.md`: *«Falsos positivos: ¿penalizan?
En revisión contractual, señalar de más es menos grave que omitir, y la métrica debería
reflejarlo.»* Sí penalizan, pero menos. La intuición era correcta y el instrumento tiene nombre,
fórmula y precedente: es la elección explícita de ContractEval, por la misma razón.

**Se reportan las dos.** F1 sola escondería la asimetría; F2 sola escondería un agente que
señala de más hasta acertar por saturación. La distancia entre ambas es en sí un diagnóstico:
F2 ≫ F1 significa exceso de falsos positivos.

### Calidad del ancla: Jaccard

Solo sobre los pares emparejados (TP), sobre los conjuntos de tokens de la cita predicha y la
del Gold:

```
J(A, B) = |A ∩ B| / |A ∪ B|
```

Mide **concisión**: penaliza tanto quedarse corto —citar media cláusula— como pasarse —citar
tres cláusulas para señalar una—. El criterio es el del revisor experimentado: exacto pero no
verboso.

### Pereza

Proporción de unidades del Gold para las que el agente **no emitió absolutamente nada** con ese
identificador en ese documento. Es un subconjunto de los FN, aislado a propósito.

Diagnostica evasión, no error. Un agente que omite parece prudente y está fallando: ContractEval
mide hasta un 30 % de falsos «no hay cláusula relacionada» en modelos abiertos, frente a un
1-7 % en propietarios. Un FN por pereza y un FN por haber anclado mal se corrigen de formas
distintas, y agregarlos oculta cuál está ocurriendo.

### Atributos del flag: medidos aparte, nunca dentro de la detección

Solo sobre los pares emparejados (TP). Un flag detectado con un atributo equivocado es **un
acierto de detección y un fallo de calificación**; mezclarlos en una sola cifra oculta cuál de
los dos está fallando, que es la segunda pregunta que `IDEAS.md` dejaba abierta.

El esquema v3 hace esto medible de verdad, porque los tres atributos que importan son enums
cerrados y `severity` ya no es un juicio suelto:

| Atributo | Cómo se mide | Qué diagnostica su fallo |
|---|---|---|
| `criterio` | Coincidencia exacta, y **matriz de confusión 5×5** | El agente ve el riesgo pero lo encuadra en la doctrina equivocada |
| `severity_driver` | Coincidencia exacta, y **matriz de confusión 4×4** | El agente lee mal **qué puede hacer** la cláusula. Es un error de lectura del texto |
| `desproporcion` | Coincidencia exacta, solo sobre los pares con `severity_driver = coste_economico` | Error de **criterio**, no de lectura: es la única casilla de juicio del esquema |
| `severity` | **Comprobación de derivación**, no acierto sustantivo | Si `severity` no se sigue de los dos anteriores, el agente no aplicó la tabla del estándar |

> **Esto es lo que se gana derivando `severity`.** Con una escala de tres niveles suelta, un
> desacuerdo `high`/`medium` era un número y nada más. Ahora el desacuerdo se localiza: si está
> en `severity_driver`, el agente no entendió la cláusula; si está en `desproporcion`, entendió
> la cláusula y discrepa del criterio. Son dos fallos distintos que se corrigen en sitios
> distintos —el segundo, en la rúbrica— y antes se veían iguales.

**No se calcula coincidencia adyacente sobre `severity`.** Con `severity` derivada, «fallar por
un nivel» ya no es una categoría: o la derivación es correcta, o alguno de los dos campos de
origen está mal, y eso ya se mide arriba.

### `key_clauses`

Idéntico a `risk_flags`, emparejando por `tipo` + ancla en lugar de por `id` + ancla.

### `missing_clauses`: la excepción, y por qué

Es el único campo de detección donde **sí existe TN**, porque no se detecta sobre un documento
abierto sino contra una **lista de referencia finita y enumerable**. La unidad es el par
(documento, elemento de la lista de referencia), y cada par es una clasificación binaria:

| | Gold: falta | Gold: está |
|---|---|---|
| **Predice que falta** | TP | FP |
| **No lo predice** | FN | TN |

Se reportan P, R, F1 y F2 igual que arriba.

> ⚠️ **`missing_clauses` solo es medible en los regímenes que tengan lista de referencia
> escrita.** Sin lista, la ausencia no significa nada: dos anotadores marcarían cosas distintas
> y no habría forma de decir cuál acierta. El estándar fija que, sin lista, el campo va vacío y
> **no se mide** — no se anota con criterio implícito. Estado de las listas por régimen: ver
> `standards/contratos.md`.

---

## Métricas separadas por vía

Las dos vías del corpus **no se agregan en una sola tabla**, por la misma razón por la que no
se agregan los tres niveles: miden cosas distintas.

| Vía | Régimen | Qué mide su cifra |
|---|---|---|
| **A — administrativa** | `administrativo` | Pipeline sobre pliegos reales, con el catálogo de riesgos de la LCSP |
| **C — condiciones generales** | `condiciones_generales` | Detección de riesgo sobre clausulado de adhesión, con el catálogo de la rúbrica |

Un F2 global que promediase vía A y vía C sería un número sin referente: el catálogo de riesgos
aplicable no es el mismo.

**Dentro de la vía C se reporta además el desglose por `condicion_adherente`.** No es una tercera
vía —la procedencia es la misma— pero el control aplicable no lo es, y el corpus ya contiene un
documento de adherente empresario (`adhesion-05`). Si el agente rinde peor en ese caso que en
consumo, es un dato que un promedio de la vía C escondería.

---

## Protocolo previo: medir el acuerdo consigo mismo

**Antes de anotar los 23 documentos, anotar 5 y medir la consistencia de la propia anotación.**

1. Anotar 5 documentos contra la rúbrica. Registrar la fecha.
2. Dejarlos reposar **dos semanas sin mirarlos**.
3. Reanotarlos desde cero, sin abrir la primera versión.
4. Calcular F1 de la segunda anotación contra la primera, con el mismo emparejamiento de arriba,
   y la coincidencia de `criterio`, `severity_driver` y `desproporcion` sobre los pares.

> **Mirar `desproporcion` con especial atención.** Es la única casilla de juicio del esquema, así
> que es donde la inconsistencia consigo mismo va a aparecer primero. Si el resto concuerda y esa
> no, el problema no es la rúbrica entera: es la definición de desproporción.

**Umbral: F1 < 0,75 significa que el problema está en la rúbrica, no en el agente.** Un criterio
que el propio autor aplica de dos formas distintas con dos semanas de diferencia no es
anotable, y ningún agente puede superar ese techo.

La referencia empírica: el acuerdo entre anotadores humanos en tareas jurídicas subjetivas se
sitúa típicamente en κ = 0,3-0,6 **sin rúbrica**, y sube a α ≈ 0,76 **con rúbrica bien
construida**. Escribir la rúbrica antes de anotar no es orden burocrático: es la diferencia
entre esos dos números.

Cuesta 5 documentos descubrir que la rúbrica no sirve. Descubrirlo después de anotar 23 cuesta 23.

---

## Acuerdo esperable: no perseguir el 100 %

El 315/315 de sentencias fue posible porque los campos de cabecera tienen **una única respuesta
correcta**. Los campos sustantivos no la tienen, ni siquiera entre juristas titulados: en un
estudio con nueve expertos con la habilitación profesional, el acuerdo sobre juicios sustantivos
fue κ = 0,344 en el criterio más blando y κ = 0,613 en el más duro.

**Fijar como objetivo el 100 % en `risk_flags` llevaría a diseñar la rúbrica para que sea fácil
de acertar, en vez de para que sea útil.** El objetivo es un F2 estable y un diagnóstico que
señale dónde falla, no una cifra redonda.

---

## Qué se puede concluir de una medición, y qué no

**Uso diagnóstico — desde el primer documento, sin mínimo.** El desglose por identificador de
rúbrica —«`PENAL-01` falla en 7 de sus 9 apariciones»— es una observación, no una inferencia. No
necesita potencia estadística para ser accionable, y es el uso principal de esta métrica.

**Uso comparativo — con una regla explícita.** Para decidir que una versión del pipeline es
mejor que otra:

> **Regla del documento único.** Recalcular la comparación quitando un documento cada vez. Si
> quitar *cualquier* documento invierte el resultado, la diferencia está dentro del ruido de un
> solo documento y **la comparación no vale**.

Es una comprobación *leave-one-out*, barata de calcular, y no exige suponer independencia entre
unidades —que es justo lo que aquí no se cumple—. Es también el mismo patrón con el que Harvey
protege sus capacidades de regresiones entre versiones.

**No se calculan intervalos de confianza** sobre las unidades-criterio como si fueran
independientes. Si en algún momento hacen falta, hay que agruparlos por documento.

**La primera medición es orientativa, y queda escrito aquí para que no pueda alegarse después.**

---

## Lo que esta métrica NO adopta, y por qué

Dos desviaciones deliberadas respecto de las fuentes:

**1. La coincidencia parcial no es un fallo de detección.** ContractEval exige que la predicción
**cubra completamente** el span del Gold para contar como TP, y manda las coincidencias parciales
a FN. Aquí no: un par emparejado es TP aunque la cita cubra el 80 % de la cláusula, y esa
imprecisión se recoge en Jaccard.

La razón es que las tareas son distintas. En ContractEval el span *es* la respuesta —se pregunta
por la cláusula y se extrae—. Aquí el span es el **ancla** de un riesgo: señalar el riesgo
correcto en la cláusula correcta citando parte de ella es un acierto de detección con una
imprecisión de cita. Fundirlos sería el mismo error que fundir la calificación y la detección.

**No se calcula además la variante estricta.** Se valoró reportar las dos cifras para conservar
comparabilidad con la literatura, y se descarta: obliga a computar dos veces cada evaluación
para producir un número que responde a una tarea que no es la nuestra. La comparabilidad que
importa se conserva igualmente —la estructura F1/F2, el Jaccard y la tasa de pereza son las de
ContractEval— y donde no se conserva es donde deliberadamente medimos otra cosa.

**Consecuencia, dicha por escrito:** el F1 y el F2 de detección de este proyecto **no son
directamente comparables** con los F1 publicados de ContractEval. El Jaccard y la tasa de pereza
sí lo son. No presentar las cifras de detección como si estuvieran en la misma escala.

**2. No se usa puntuación *all-pass*.** El *Legal Agent Benchmark* de Harvey exige que **todos**
los criterios de una tarea acierten. Con 23 documentos produciría un cero casi seguro y ninguna
señal de mejora entre versiones. Se toma de Harvey la **descomposición en criterios atómicos
binarios**, no su agregación.

---

## Qué tiene que registrar el Gold

Consecuencia directa de todo lo anterior. Para cada documento anotado:

- Los campos del nivel 1, con su valor exacto.
- Cada `risk_flag` con su `id` de rúbrica, su `cita` **literal y verbatim** del documento, su
  `localizador`, y sus tres atributos calificadores: `criterio`, `severity_driver` y
  `desproporcion`. **`severity` no se anota: se deriva.** Anotarla a mano reintroduciría el
  juicio suelto que el esquema v3 elimina, y además permitiría que el Gold se contradijese
  consigo mismo.
- Cada `key_clause` con `tipo`, `cita` y `localizador`.
- `missing_clauses` **solo** si el régimen del documento tiene lista de referencia escrita.

> **Contrastar cada valor con el documento antes de darlo por bueno.** En el Gold de sentencias,
> **6 de las 8 discrepancias** de la primera evaluación del test eran errores del Gold, no del
> agente. Un Gold sin verificar mide el Gold.
