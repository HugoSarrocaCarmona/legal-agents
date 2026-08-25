# 📍 ESTADO DEL PROYECTO

**Punto de entrada. Leer esto primero, antes que cualquier otro documento del repo.**
Actualizado: 25/08/2026.

Este fichero se mantiene **corto a propósito**: es lo que se carga al empezar cualquier
conversación, y si crece deja de cumplir su función. Los detalles viven en los ficheros que
enlaza. Si algo se puede consultar cuando haga falta, no va aquí.

---

## Dos pipelines, en fases distintas

| Pipeline | Estado | Esquema | Medición |
|---|---|---|---|
| **Sentencias** | Funcionando | v2, 16 campos ([`standards/sentencias.md`](../standards/sentencias.md)) | 315/315 en 9 campos de cabecera — **no extrapolable** |
| **Contratos** | En diseño | v1, sin ejercitar ([`standards/contratos.md`](../standards/contratos.md)) | Ninguna |

No comparten esquema, ni validador, ni métricas. Son contratos de datos distintos.

---

## Dos bloqueos abiertos

**1. El test de sentencias está gastado.** Los 13 documentos de `sentencia23`–`sentencia35` se
evaluaron una vez a ciegas (313/315) y después se corrigieron dos reglas *mirando esos fallos*.
El 315/315 confirma que las reglas funcionan; **no mide generalización**. Cualquier medición
honesta exige un corpus nuevo, reservado y no mirado. Detalle en [`ROADMAP.md`](ROADMAP.md).

**2. Los campos sustantivos no tienen evaluación de contenido.** `facts`, `applied_rules`,
`ratio_summary` y `holding` solo tienen control de forma: un output puede pasar las dos
comprobaciones y contener un razonamiento equivocado. En contratos casi todo el esquema es
sustantivo, así que el problema es mayor. Detalle en [`IDEAS.md`](IDEAS.md).

---

## Alcance decidido del corpus de contratos

Tres vías, **con corpus y métricas separados** — no se agregan en una sola tabla de precisión:

- **Vía A — administrativa (principal).** Pliegos de PLACSP. Volumen y datos reales.
- **Vía B — mercantil negociada (secundaria, diferida).** CNMV. Clausulado genuinamente negociado.
- **Vía C — condiciones generales (soporte).** Clausulado de adhesión y la jurisprudencia que lo controla.

Criterios de inclusión y exclusión: [`corpus/alcance.md`](../corpus/alcance.md).
Inventario con hashes: [`corpus/inventario-contratos.csv`](../corpus/inventario-contratos.csv).

**Corpus actual: 23 activos, 7 depurados.** Es corpus de arranque, no definitivo: hay
recopilación de contratos nuevos pendiente, y los actuales no son intocables.

---

## La advertencia que condiciona todo el diseño de contratos

**`risk_flags` tiene que ser consciente del régimen.** El control de abusividad (arts. 82 y ss.
TRLGDCU) es derecho de **consumo** y solo opera frente a consumidores. Un adherente empresario
(Ley 7/1998) solo tiene control de incorporación y transparencia. Y nada de eso rige en un
contrato administrativo (LCSP).

Consecuencia práctica: **una cláusula declarada abusiva por un juez no es una etiqueta
transferible a un pliego administrativo.** De la jurisprudencia se transfieren los *criterios*
(desequilibrio, falta de reciprocidad, opacidad, desproporción de la penalización, facultades
unilaterales), nunca las *calificaciones*. Por eso `risk_flags` lleva campo `regimen`.

---

## Regla operativa del corpus

**Nada se borra.** Todo documento excluido se mueve a `Inputs/_depurados/` con su motivo en el
inventario. `Inputs/` está en `.gitignore` y seguirá estándolo: contiene datos personales
reales que no deben entrar en un histórico inmutable. La protección es la copia externa
(`robocopy` a OneDrive) más los `sha256` del inventario.
