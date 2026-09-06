# 📍 ESTADO DEL PROYECTO

**Punto de entrada. Leer esto primero, antes que cualquier otro documento del repo.**
Actualizado: 06/09/2026.

Este fichero se mantiene **corto a propósito**: es lo que se carga al empezar cualquier
conversación, y si crece deja de cumplir su función. Los detalles viven en los ficheros que
enlaza. Si algo se puede consultar cuando haga falta, no va aquí.

---

## Dos pipelines, en fases distintas

| Pipeline | Estado | Esquema | Medición |
|---|---|---|---|
| **Sentencias** | Funcionando | v2, 16 campos ([`standards/sentencias.md`](../standards/sentencias.md)) | 315/315 en 9 campos de cabecera — **no extrapolable** |
| **Contratos** | En diseño | v3, 12 campos, sin ejercitar ([`standards/contratos.md`](../standards/contratos.md)) | Métrica decidida ([`corpus/metrica-contratos.md`](../corpus/metrica-contratos.md)), sin ejecutar |

No comparten esquema, ni validador, ni métricas. Son contratos de datos distintos.

---

## Dos bloqueos abiertos

**1. El test de sentencias está gastado.** Los 13 documentos de `sentencia23`–`sentencia35` se
evaluaron una vez a ciegas (313/315) y después se corrigieron dos reglas *mirando esos fallos*.
El 315/315 confirma que las reglas funcionan; **no mide generalización**. Cualquier medición
honesta exige un corpus nuevo, reservado y no mirado. Detalle en [`ROADMAP.md`](ROADMAP.md).

**2. Los campos sustantivos de sentencias no tienen evaluación de contenido.** `facts`,
`applied_rules`, `ratio_summary` y `holding` solo tienen control de forma: un output puede pasar
las dos comprobaciones y contener un razonamiento equivocado. Detalle en [`IDEAS.md`](IDEAS.md).

> **En contratos este bloqueo ya no está abierto.** La métrica se decidió el 06/09/2026, antes
> de anotar nada: [`corpus/metrica-contratos.md`](../corpus/metrica-contratos.md). Lo que
> bloquea ahora la fase 2 es **la rúbrica**, que es trabajo por hacer, no una decisión pendiente.

---

## Lo siguiente: la rúbrica de `risk_flags`

Único paso que bloquea todo lo demás. El esquema v2 exige que `risk_flags[].id` exista en
`corpus/rubrica-riskflags.md`, así que **sin rúbrica el estándar no es aplicable** y no se puede
anotar ni un documento. Los criterios salen de las 9 resoluciones de la vía C, y hay que
verificar en cada una si juzga a un consumidor o a un adherente empresario.

Antes de anotar los 23 documentos, anotar **5** y medir el acuerdo consigo mismo tras dos
semanas de reposo. Protocolo y umbral en la métrica.

---

## Alcance decidido del corpus de contratos

**Dos vías, un régimen cada una**, con corpus y métricas separados — no se agregan en una sola
tabla de precisión:

- **Vía A — administrativa (principal).** Pliegos de PLACSP. Régimen `administrativo` (LCSP).
- **Vía C — condiciones generales (soporte).** Clausulado de adhesión y la jurisprudencia que lo
  controla. Régimen `condiciones_generales`; dentro, `condicion_adherente` decide si el control
  es de contenido (consumidor) o solo de incorporación y transparencia (empresario).

**La vía B —mercantil negociada— se eliminó el 06/09/2026**, y con ella el régimen `mercantil`.
Un contrato libremente negociado no tiene control de contenido ni lista de referencia
defendible: `missing_clauses` registraría la opinión del anotador y `risk_flags` daría hallazgos
sin consecuencia jurídica a la que referirlos.

Criterios de inclusión y exclusión: [`corpus/alcance.md`](../corpus/alcance.md).
Inventario con hashes: [`corpus/inventario-contratos.csv`](../corpus/inventario-contratos.csv).

**Corpus actual: 20 activos, 3 pendientes de depurar, 7 depurados.** Es corpus de arranque, no
definitivo: hay recopilación de contratos nuevos pendiente, y los actuales no son intocables.

---

## La advertencia que condiciona todo el diseño de contratos

**`risk_flags` tiene que ser consciente del régimen.** El control de abusividad (arts. 82 y ss.
TRLGDCU) es derecho de **consumo** y solo opera frente a consumidores. Un adherente empresario
(Ley 7/1998) solo tiene control de incorporación y transparencia. Y nada de eso rige en un
contrato administrativo (LCSP).

Consecuencia práctica: **una cláusula declarada abusiva por un juez no es una etiqueta
transferible a un pliego administrativo.** De la jurisprudencia se transfieren los *criterios*
(desequilibrio, falta de reciprocidad, opacidad, desproporción de la penalización, facultades
unilaterales), nunca las *calificaciones*.

**Cómo lo recoge el esquema v3.** `regimen` nombra la **fuente** del control
(`administrativo` | `condiciones_generales`); `condicion_adherente` nombra **quién** se adhiere;
y `control_aplicable` se **deriva** de los dos. Antes era un solo eje que mezclaba las tres
cosas, y un contrato de adhesión dirigido a clientes profesionales —que el corpus ya tiene— no
tenía clasificación posible.

---

## Regla operativa del corpus

**Nada se borra.** Todo documento excluido se mueve a `Inputs/_depurados/` con su motivo en el
inventario. `Inputs/` está en `.gitignore` y seguirá estándolo: contiene datos personales
reales que no deben entrar en un histórico inmutable. La protección es la copia externa
(`robocopy` a OneDrive) más los `sha256` del inventario.

---

## Contexto de mercado

[`research/mercado-legaltech-2026.md`](../research/mercado-legaltech-2026.md) — investigación
del 03/09/2026 sobre cómo funcionan y cómo se evalúan los sistemas de automatización jurídica
pioneros. De ahí salen la métrica del paso 1 y los cambios del esquema v2. No es documento
operativo: se consulta, no se carga por defecto.

---

## Encaje regulatorio

[`docs/encaje-regulatorio.md`](../docs/encaje-regulatorio.md) — Instrucción 2/2026 del CGPJ,
Circular 3/2026 del CGAE y Reglamento (UE) 2024/1689. Dos cosas que conviene tener presentes sin
abrir el fichero:

- **La predicción de resultado judicial está fuera de alcance por decisión**, no por falta de
  medios.
- **`Inputs/` tiene datos personales reales y el `.gitignore` no cubre ese riesgo**: protege el
  histórico de git, no regula qué se envía al modelo. Con corpus público —PLACSP, CENDOJ— el
  riesgo es bajo; con documentos de cliente, hay que verificar antes las condiciones de la
  herramienta.
