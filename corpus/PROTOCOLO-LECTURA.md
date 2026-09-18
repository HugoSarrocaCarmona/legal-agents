# 📖 Protocolo de lectura de los diez pliegos

**Paso 5 de la fase 2. Es trabajo de Hugo, no de Claude.** De aquí sale
`corpus/rubrica-riesgos-lcsp.md`, y de la rúbrica depende todo lo que viene después: el
validador, el agente, el Gold y la evaluación.

Corpus: [`pliegos-a-leer.csv`](pliegos-a-leer.csv) — diez expedientes de la población **«un solo
licitador, y fue excluido»**, diez órganos distintos. Por qué esa población y no otra, en
[`../scripts/placsp/selecciona_pliegos.py`](../scripts/placsp/selecciona_pliegos.py).

---

## La regla que hace que esto funcione

> **Durante la lectura no se cita ni un solo artículo de la LCSP.**

Es contraintuitivo y es el punto entero del protocolo. Si al leer la cláusula 12 se anota «art.
107 LCSP», lo que se está haciendo es **reconocer** lo que ya se sabe de la ley, y el catálogo
acaba siendo el índice de la LCSP con otro nombre. Anclar va en la fase 2, con el texto
consolidado del BOE delante y ya sabiendo qué hay que anclar.

Un catálogo deducido de la ley recoge lo que la ley regula. Uno inducido de documentos recoge
**lo que los pliegos hacen**. Solo el segundo sirve para medir.

---

## La pregunta única

A cada cláusula se le hace **una sola pregunta**:

> **¿Qué exige esto, y cómo se falla?**

No «¿es esto legal?» ni «¿es esto abusivo?». La primera ya la contestó el órgano y la segunda es
la fase 2. Lo que se busca es el punto donde un licitador razonable, con prisa y sin abogado,
mete la pata.

**Ayuda saber que estos diez pliegos ya se cobraron una víctima cada uno.** En los diez se
presentó exactamente una empresa y la excluyeron. Mientras lees, la pregunta de fondo es: *¿fue
por esta cláusula?*

---

## Cómo conseguir los PDF

No hay que abrirlos a mano. El XML de la sindicación lleva la URL de descarga directa de cada
documento, y [`documentos-pliegos.csv`](documentos-pliegos.csv) ya las tiene todas — 69
documentos de los 10 expedientes, con el número de páginas de los que son PCAP o PPT.

```bash
python3 scripts/placsp/extrae_documentos.py /ruta/raw/placsp_2025*.zip \
        --expedientes corpus/pliegos-a-leer.csv \
        -o corpus/documentos-pliegos.csv \
        --descargar Inputs/pliegos --solo-pliegos
```

**Comprobado el 18/09/2026: los 20 PDF (PCAP + PPT de los diez) llevan texto extraíble; ninguno
está escaneado.** No hará falta OCR en ningún punto de la fase.

---

## El procedimiento, pliego a pliego

**Presupuesto realista: entre 45 y 100 minutos por pliego, según tamaño.** Los diez PCAP suman
**700 páginas**, y están muy mal repartidas:

| Páginas del PCAP | Pliegos |
|---|---|
| 25 – 49 | 4 (los pliegos 1, 6, 9, 10) |
| 61 – 85 | 4 |
| 115 y 158 | 2 |

En total, **entre 12 y 15 horas de lectura**, no siete. Buena parte de un PCAP es articulado de
formulario que se lee en diagonal, pero la cifra honesta es esa y conviene saberla antes de
empezar en vez de descubrirla en el pliego 4.

> **Empieza por los cortos —1, 6, 9, 10—.** Se calibra el criterio de anotación con cuatro
> pliegos de 25 a 49 páginas, y solo después se entra en los de 115 y 158. Al revés, el criterio
> se fija leyendo el caso más atípico del corpus.

**El PPT no se lee entero.** Solo se abre si el PCAP remite a él para un requisito de admisión.
El PPT del pliego 7 son **905 páginas** —es el proyecto de obra— y leerlo no entra en esta fase.

1. **Abrir el PCAP.** El PPT solo si el PCAP remite a él para un requisito de admisión.
2. **Leer entero y del tirón, sin anotar.** Anotar mientras se lee produce veinte notas sobre
   la primera mitad y ninguna sobre la segunda.
3. **Segunda pasada, anotando.** Ahora sí, rellenando
   [`anotaciones-pliegos.csv`](anotaciones-pliegos.csv), una fila por riesgo.
4. **Entre 8 y 20 filas por pliego.** Menos de 8 es lectura superficial. Más de 20 es estar
   anotando el pliego entero en vez de sus riesgos.
5. **Marcar en `pliegos-a-leer.csv`** las columnas `pcap_descargado` y `riesgos_anotados`.

**No leas los diez seguidos.** Tras el tercero, para y revisa: si las filas del pliego 3 no se
parecen en nada a las del 1, o el criterio de anotación ha cambiado por el camino, corrígelo
ahora — no después de diez.

---

## Las columnas, y qué se juega cada una

| Columna | Qué va |
|---|---|
| `pliego` | El `orden` de `pliegos-a-leer.csv`, 1 a 10 |
| `documento` | `PCAP`, `PPT` o `anexo` |
| `clausula` | Cláusula, apartado y página. **Tiene que permitir volver al sitio exacto** |
| `cita` | Transcripción **literal**, máximo dos líneas. Literal significa literal |
| `que_exige` | Una frase, en tus palabras, sin jerga |
| `como_se_falla` | El error concreto. No «incumplimiento de solvencia» sino «aporta el certificado de una obra similar pero de menor importe que el mínimo exigido» |
| `momento` | `admision`, `valoracion` o `ejecucion`. **Ver abajo** |
| `quien_controla` | `licitador`, `organo` o `tercero` |
| `severidad_intuitiva` | `baja` / `media` / `alta`. Sin pensarlo mucho: es una primera señal, no una calificación |
| `notas` | Lo que no cabe en las otras |

### `momento` es la columna que decide el rumbo del proyecto

Las otras nueve columnas construyen la rúbrica. **Esta contesta una pregunta abierta de
`ESTADO.md`**: si el producto es *riesgo de admisión* («¿por qué han tirado mi oferta?») o
*riesgo de ejecución* («¿qué asumo si gano?»).

- **`admision`** — se falla **antes** de que valoren tu oferta. Solvencia, clasificación,
  documentación, modelos obligatorios, plazos, forma de presentación, declaración responsable.
  Te quedas fuera sin que nadie llegue a leer lo que ofrecías.
- **`valoracion`** — tu oferta entra pero puntúa mal, o cae por baja anormal.
- **`ejecucion`** — no te afecta hasta que ganas: penalidades, revisión de precios,
  modificaciones, plazos de pago, garantías, subcontratación, condiciones especiales.

**Al terminar los diez, se cuenta esta columna.** Si la mayoría de los riesgos anotados son
`admision`, el proyecto está mal enunciado y hay que decirlo en voz alta. Si son `ejecucion`, el
enunciado actual se confirma con datos propios.

> Esa cuenta es el resultado del paso 5, tanto como la rúbrica. **No la decidas antes de
> contarla, y no ajustes la anotación para que salga lo que esperas.** Si te descubres dudando
> entre dos valores, pon el que corresponda al momento en que el licitador **pierde el
> contrato**, no al momento en que aparece la cláusula en el documento.

---

## Cuándo NO se anota una fila

- **La cláusula solo repite la ley** sin añadir exigencia propia. «El contratista deberá cumplir
  la normativa laboral vigente» no es un riesgo: es un recordatorio.
- **La prerrogativa de la Administración por sí sola.** Que el órgano pueda interpretar el
  contrato o modificarlo dentro de la ley no es un riesgo, es el régimen administrativo. Lo que
  sí se anota es **hasta dónde** llega en este pliego concreto.
- **Lo que no puede salirle mal a nadie.** Si no se te ocurre cómo se falla, no hay `como_se_falla`
  y no hay fila.

---

## Qué pasa después (fase 2, ya con la LCSP delante)

1. **Agrupar** las ~120 filas por similitud. Salen entre 25 y 45 grupos.
2. **Un `id` por grupo**, del vocabulario cerrado — la métrica empareja por `id`, así que un
   catálogo abierto la deja inservible.
3. **Anclar cada grupo**: `normativo` si diverge de un umbral o requisito concreto de la LCSP,
   con la `base_normativa` **transcrita del texto consolidado del BOE, nunca de memoria**;
   `valorativo` si es desproporción dentro de lo legal, y entonces el criterio se apoya en
   resoluciones del **TACRC**, que son abiertas y sin prohibición de uso comercial.
4. **Contar la columna `momento`** y resolver la pregunta de rumbo.

Reglas de campo y vocabulario de materias en
[`../standards/contratos.md`](../standards/contratos.md); qué significa acertar, en
[`metrica.md`](metrica.md).
