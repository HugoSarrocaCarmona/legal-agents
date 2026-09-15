# 📍 ESTADO DEL PROYECTO

**Punto de entrada. Leer esto primero, antes que cualquier otro documento del repo.**
Actualizado: 09/09/2026.

Este fichero se mantiene **corto a propósito**: es lo que se carga al empezar cualquier
conversación, y si crece deja de cumplir su función. Los detalles viven en los ficheros que
enlaza. Si algo se puede consultar cuando haga falta, no va aquí.

---

## El proyecto tiene una sola línea activa

**Analizador de riesgo de ejecución de pliegos (LCSP).** Responde una pregunta concreta desde
la posición del licitador: *¿qué me puede costar dinero si gano este contrato público?*

Reorientado el 09/09/2026. Antes era un analizador de contratos genérico sobre tres regímenes.
El motivo del giro está en
[`research/02-oportunidad-mercado-espanol.md`](../research/02-oportunidad-mercado-espanol.md) y
se resume en cuatro condiciones que solo coinciden aquí: corpus **abierto** (PLACSP, frente a un
CENDOJ que prohíbe descarga masiva y uso comercial), **volumen real**, un **destinatario que
paga** que no es abogado, y **ausencia de datos de cliente** — lo que mantiene el proyecto fuera
del Anexo III del Reglamento de IA y de las obligaciones de la Circular 3/2026 del CGAE.

| Línea | Estado | Referencia |
|---|---|---|
| **Pliegos** (fase 2) | **Activa** — esquema v2 y métrica cerrados | [`standards/contratos.md`](../standards/contratos.md) · [`corpus/metrica.md`](../corpus/metrica.md) |
| **Sentencias** (fase 1) | **Aparcada**, no bloqueada — ver corrección abajo | [`standards/sentencias.md`](../standards/sentencias.md) |
| **Vigilancia normativa** (fase 3) | Transversal, ámbito cerrado | [`ROADMAP.md`](ROADMAP.md) |

---

## Lo que se decidió el 09/09/2026

**1. La métrica, que era el bloqueo de la fase.** `risk_flags` no es un campo homogéneo: son
dos. Los flags **`normativo`** afirman una divergencia respecto de la LCSP y se comprueban
contra la ley —métrica exacta, umbral F1 ≥ 0,95—. Los **`valorativo`** afirman desproporción
dentro de lo legal y son juicio —precisión y exhaustividad con F₂, que pondera doble no
omitir—. **Se reportan por separado; agregarlos está prohibido.** Detalle, unidad de medida,
regla de emparejamiento y tamaños mínimos en [`corpus/metrica.md`](../corpus/metrica.md).

**2. El esquema v2.** `risk_flags` incorpora `clase`, `base_normativa`, `clausula_ref` y
`materia`; `missing_clauses` solo admite ausencias que alguna norma exija; y hay un vocabulario
cerrado de **16 materias** con su ancla en la LCSP verificada contra el BOE.

---

## Siguiente tarea: bajar PLACSP y responder una pregunta con los datos

> **Reordenada el 15/09/2026 por el veredicto del consejo**
> ([`research/04-veredicto-consejo.md`](../research/04-veredicto-consejo.md)). Antes la tarea
> siguiente era escribir la rúbrica. No lo es: la rúbrica es el paso 2 y no se puede escribir
> bien sin el paso 1.

**Paso 1 — una tarde, y es software, no un documento.** Descargar los datos abiertos de PLACSP y
responder con ellos **por qué quedaron desiertos los 9.819 concursos de 2025**.

Hace dos cosas a la vez, y por eso va primero:

1. **Verifica la premisa sobre la que se apoya toda la línea activa.** El informe 2 dio por
   «causa identificada» que las pymes no pueden con la complejidad de los pliegos. Eso era una
   inferencia de fuente secundaria, no un dato. PLACSP publica el motivo de cada desierto,
   desistimiento y renuncia. **Si el motivo mayoritario es precio inviable o falta de
   financiación, la tesis del producto cae** — y conviene saberlo en un día, no en dos años.
2. **Produce el corpus.** Tres pliegos no son un corpus. Bajar 200 PCAP es una tarde de script.

**Paso 2 — la rúbrica, con el orden invertido.** `corpus/rubrica-riesgos-lcsp.md` sigue siendo un
catálogo **cerrado** —la métrica empareja por `id`— pero **se induce, no se deduce**: leer diez
pliegos a mano, anotar todo riesgo que aparezca, y **solo entonces** anclar cada uno a su
artículo de la LCSP verificado contra el BOE.

> Un catálogo deducido de la ley recoge lo que la ley regula. Uno inducido de documentos recoge
> **lo que los pliegos hacen**. Solo el segundo sirve para medir nada.

---

## Tres bloqueos abiertos

**0. La premisa de la línea activa está sin verificar.** *(Abierto el 15/09/2026.)* Todo el giro
descansa en que los concursos quedan desiertos **porque** las pymes no pueden con la complejidad
del pliego. Eso nunca se comprobó: se tomó de una fuente secundaria y se escribió como «causa
identificada». Es el bloqueo más grave porque invalidaría los otros dos si cae, y es el más
barato de cerrar — lo cierra el paso 1 de la tarea siguiente.

**1. La `base_normativa` inventada.** Es el riesgo que introduce el giro y el más grave del
proyecto: un flag que cite un artículo de la LCSP que no dice lo que se le atribuye es la
versión contractual de la sentencia inventada. Tratado como **fallo duro con cero tolerancia**
—un solo caso bloquea la versión—. La mitigación es de proceso: cada `base_normativa` se
transcribe del texto consolidado del BOE al redactar la rúbrica, nunca de memoria.

**2. El sesgo por órgano de contratación.** Los pliegos se redactan sobre plantillas de cada
órgano. Un corpus concentrado en pocos órganos mide rendimiento sobre sus plantillas, no sobre
la contratación pública española. El inventario ya registra el órgano; falta estratificar por él
al muestrear.

---

## Alcance del corpus tras el giro

- **Vía A — PLACSP.** Única vía de evaluación. Es el producto. Objetivo: **30–40 pliegos
  anotados**, 15–20 por partición ciego-1 / ciego-2.
- **Vía B — CNMV.** **Cerrada en esta iteración.** Ya no es «diferida».
- **Vía C — condiciones generales.** Degradada a **fuente de criterios valorativos**. Las 9
  resoluciones aportan los cinco criterios transferibles; los 8 documentos de adhesión dejan de
  ser material anotable.

Ningún documento se depura por el giro: cambian de función, no de estado. Criterios de inclusión
en [`corpus/alcance.md`](../corpus/alcance.md); inventario con hashes en
[`corpus/inventario-contratos.csv`](../corpus/inventario-contratos.csv).

> **Corrección del 15/09/2026 — el TACRC es un corpus abierto.** El informe 2 dio por cerrada
> «la ley» como fuente de datos sin distinguir jurisdicción de doctrina administrativa. Las
> resoluciones del **Tribunal Administrativo Central de Recursos Contractuales** y de los
> tribunales autonómicos **se publican sin las restricciones del CENDOJ y sin prohibición de uso
> comercial**, y tratan exactamente de qué cláusulas de pliego se anulan. Eso es una fuente de
> verdad para los flags `valorativo` mucho mejor que las 9 resoluciones de consumo: en vez de
> opinar que una cláusula es desproporcionada, se cita que cláusulas de esa forma fueron
> anuladas. **Incorporar al redactar la rúbrica.**

---

## Corrección sobre la línea de sentencias

Se congeló el 09/09 con el argumento de que el CENDOJ hace inexplotable ampliar su corpus. **El
argumento estaba mal aplicado.** El aviso legal prohíbe la **descarga masiva y el uso
comercial**; no prohíbe leer. Medir generalización exige veinte o treinta sentencias leídas a
mano, que es precisamente lo permitido.

Consecuencia: el bloqueo histórico —el conjunto de test gastado— **sigue siendo reparable con
trabajo manual**. La línea se aparca por prioridad, no porque sea imposible medirla. Decir lo
contrario fue una racionalización cómoda y queda corregido aquí.

---

## La advertencia que condiciona todo el diseño

**`risk_flags` tiene que ser consciente del régimen.** El control de abusividad (arts. 82 y ss.
TRLGDCU) es derecho de **consumo** y solo opera frente a consumidores. Un adherente empresario
(Ley 7/1998) solo tiene control de incorporación y transparencia. Y nada de eso rige en un
contrato administrativo (LCSP).

**Una cláusula declarada abusiva por un juez no es una etiqueta transferible a un pliego.** De
la jurisprudencia se transfieren los *criterios* (desequilibrio, falta de reciprocidad,
opacidad, desproporción de la penalización, facultades unilaterales), nunca las
*calificaciones*. Por eso `risk_flags` lleva `regimen`, y por eso importar vocabulario de
consumo a un pliego es fallo duro.

**Corolario propio del régimen administrativo:** la desigualdad entre las partes no es un
defecto, es el régimen. La Administración tiene prerrogativas que la ley le atribuye. Señalar su
mera existencia como riesgo sería no entender el contrato.

---

## Regla operativa del corpus

**Nada se borra.** Todo documento excluido se mueve a `Inputs/_depurados/` con su motivo en el
inventario. `Inputs/` está en `.gitignore` y seguirá estándolo: contiene datos personales reales
que no deben entrar en un histórico inmutable. La protección es la copia externa (`robocopy` a
OneDrive) más los `sha256` del inventario.
