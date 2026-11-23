# 📍 ESTADO DEL PROYECTO

**Punto de entrada. Leer esto primero, antes que cualquier otro documento del repo.**
Actualizado: 23/11/2026.

Se mantiene corto a propósito: es lo que se carga al empezar cualquier conversación. Lo que pasó
y por qué está en [`LOG.md`](LOG.md); el plan por fases, en [`ROADMAP.md`](ROADMAP.md). Si este
fichero pasa de unas 80 líneas, algo de lo que contiene ya es historia y va al `LOG.md`.

## Línea activa: riesgo de pliegos (LCSP)

Analizador de riesgo de pliegos de contratación pública, desde la posición del licitador. Es
donde coinciden un corpus abierto (PLACSP), volumen real, un destinatario que paga y no es
abogado, y ausencia de datos de cliente. El porqué del giro, en `LOG.md` (09/09/2026) y
[`research/02-oportunidad-mercado-espanol.md`](../research/02-oportunidad-mercado-espanol.md).

**El encuadre está abierto y lo decide Hugo.** Se enunció como riesgo de *ejecución* («¿qué
asumo si gano?»). Los datos de PLACSP (`LOG.md`, 17/09) y las anotaciones apuntan a riesgo de
*admisión* («¿por qué han tirado mi oferta?»). Se decide contando la columna `momento` al
terminar los diez pliegos, no antes.

| Línea | Estado | Referencia |
|---|---|---|
| **Pliegos** (fase 2) | **Activa** — paso 5, lectura de diez pliegos | [`standards/contratos.md`](../standards/contratos.md) · [`corpus/metrica.md`](../corpus/metrica.md) · [`corpus/PROTOCOLO-LECTURA.md`](../corpus/PROTOCOLO-LECTURA.md) |
| **Sentencias** (fase 1) | **Aparcada**, no bloqueada: el test gastado se repara con 20–30 sentencias leídas a mano | [`standards/sentencias.md`](../standards/sentencias.md) |
| **Vigilancia normativa** (fase 3) | Transversal, ámbito cerrado, sin empezar | [`ROADMAP.md`](ROADMAP.md) |

## Tarea abierta: los diez pliegos, y son de Hugo

**Avance: 5 de 10** — pliegos 1, 6, 9, 10 y 2, con 61 filas en
[`corpus/anotaciones-pliegos.csv`](../corpus/anotaciones-pliegos.csv). Leídas 207 de las 700
páginas de PCAP; quedan 493. Detalle de cada pliego en `LOG.md`.

**Siguiente: pliego 7** (Junta de Castilla y León, obras, 65 págs.). Después el 3 y el 8, y al
final los dos largos: el 4 (115 págs.) y el 5 (158).

**La señal, con n = 5:** `momento` da 39 de admisión, 21 de ejecución y 1 de valoración. De las
39 de admisión, 17 caen entre la propuesta de adjudicación y la formalización: requisitos que
solo se descubren al ganar. Con la cautela de recuento del pliego 9, la admisión baja a 35 de 57.

**Para los cinco que quedan, las filas las escribe Hugo enteras**, y Claude las revisa después
dejando constancia en `notas`. En los pliegos 9, 10 y 2 Claude redactó o reescribió parte de las
filas, y la rúbrica va a salir de ellas.

## Después de los diez pliegos

1. **Contar `momento`** y decidir el encuadre.
2. **Si sale admisión, un esquema v3 antes que la rúbrica.** Las 16 materias cerradas de
   `standards/contratos.md` son todas de ejecución, y unas 32 de las 39 filas de admisión no
   caben en ninguna ([`research/05-harness-2027-y-situacion.md`](../research/05-harness-2027-y-situacion.md), §3).
3. **Rúbrica inducida, validador, `pliego_agent`, Gold de 30–40 pliegos nuevos y evaluación.**
   Orden y detalle en `ROADMAP.md`, fase 2.

## Bloqueos abiertos

1. **La `base_normativa` inventada.** Un flag que cite un artículo de la LCSP que no dice lo que
   se le atribuye es fallo duro con cero tolerancia. Cada `base_normativa` se transcribe del
   texto consolidado del BOE al redactar la rúbrica, nunca de memoria.
2. **El sesgo por órgano de contratación.** Los pliegos salen de plantillas de cada órgano. Se
   muestrea un pliego por órgano, y no se da por generalizable una medición que no lo haga.

**Pendiente fuera del repo:** ninguna conversación todavía con alguien del sector. El consejo
fijó el umbral de reversión en la primera conversación útil
([`research/04-veredicto-consejo.md`](../research/04-veredicto-consejo.md)).

## Corpus y regla operativa

**Vía A — PLACSP**, única vía de evaluación. La vía B (CNMV) está cerrada; la C queda como fuente
de criterios valorativos. Criterios en [`corpus/alcance.md`](../corpus/alcance.md); inventario
con hashes en [`corpus/inventario-contratos.csv`](../corpus/inventario-contratos.csv).

**Nada se borra.** Todo documento excluido se mueve a `Inputs/_depurados/` con su motivo en el
inventario. `Inputs/` está fuera de git porque contiene datos personales reales. Lo protegen la
copia externa (`robocopy` a OneDrive), los `sha256` del inventario y las reglas `deny` de
`.claude/settings.json`: Claude no puede borrar, crear ni sobrescribir nada dentro, y mover a
`_depurados/` pide confirmación.
