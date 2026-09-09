# 📐 Métrica de evaluación de campos sustantivos

**Paso 1 de la Fase 2. Cierra el bloqueo que impedía diseñar la rúbrica y el Gold.**
Fijado: 09/09/2026.

Este fichero decide **qué significa acertar** en `risk_flags`, `key_clauses` y
`missing_clauses`. Se escribe **antes** de la rúbrica y **antes** del Gold, a propósito: en la
fase 1 el esquema se diseñó sin saber cómo se iba a medir y los campos sustantivos se quedaron
sin evaluación. Aquí el orden se invierte.

Ámbito: **`regimen = administrativo`** (pliegos LCSP). Los demás regímenes siguen definidos en
`standards/contratos.md` pero no se miden en esta iteración.

---

## 🔑 LA DECISIÓN QUE DESBLOQUEA TODO

**`risk_flags` no es un campo homogéneo. Son dos campos con naturalezas distintas metidos en
una misma lista, y por eso no había métrica posible.**

| Clase | Qué afirma el flag | ¿Hay respuesta única? |
|---|---|---|
| **`normativo`** | Que la cláusula **diverge de un umbral o requisito de la LCSP** | **Sí.** Se comprueba contra el texto de la ley |
| **`valorativo`** | Que la cláusula es **desproporcionada o desequilibrada** sin que ninguna norma fije el umbral | **No.** Es juicio |

Esta distinción es el hallazgo operativo del giro hacia pliegos, y no existía mientras el
corpus era de consumo. El control de abusividad del TRLGDCU es **valorativo casi por entero**:
el desequilibrio importante no tiene umbral legal. La LCSP, en cambio, **fija cifras**: 10 % y
50 % en penalidades, 0,60 € por 1.000 € y día, 5 % y 10 % en garantías, 20 % y 50 % en
modificaciones, 30 + 30 días en pagos.

**Consecuencia:** una parte sustancial de `risk_flags` en régimen administrativo es
*mecánicamente comprobable*, y admite exactamente el mismo tipo de métrica que dio 315/315 en
`ecli` o `decision_date`. El problema de medición no desaparece — se reduce a la mitad
valorativa, que es donde de verdad estaba.

> Por eso el esquema incorpora `risk_flags[].clase` y `risk_flags[].base_normativa`. Sin esos
> dos campos, las dos clases se promedian en una sola cifra y la métrica vuelve a no significar
> nada — el mismo error que la agregación de regímenes.

---

## 1 · Unidad de medida

**La unidad es la cláusula anotada, no el documento.**

Un pliego rinde entre 8 y 20 cláusulas con riesgo anotable. Medir por documento tira esa
información y deja N ≈ 20 por partición, que es el tamaño que `alcance.md` ya identificó como
insuficiente.

**Pero las cláusulas de un mismo pliego no son independientes** — comparten órgano, plantilla y
criterio redactor. Contarlas como observaciones independientes infla la confianza
artificialmente. Corrección obligatoria:

> **Las métricas puntuales se calculan por cláusula; los intervalos de confianza se calculan
> remuestreando por documento** (*bootstrap* por conglomerados, el documento es el
> conglomerado). Nunca al revés, y nunca un intervalo calculado sobre cláusulas sueltas.

Esto responde al riesgo abierto de `alcance.md` sin inventar corpus que no existe.

---

## 2 · Regla de emparejamiento

Un flag predicho **empareja** con un flag del Gold si y solo si se cumplen las dos cosas:

1. **Mismo `id`**, tomado del vocabulario cerrado de la rúbrica. No hay emparejamiento por
   parecido de texto.
2. **Anclado a la misma cláusula**: `clausula_ref` coincide o solapa con la del Gold.

No se empareja por similitud de `issue` ni de `why_it_matters`. Un identificador cerrado más un
ancla es lo que hace la comparación mecánica; la prosa libre la haría irreproducible.

**Corolario que condiciona la rúbrica:** si el vocabulario de `id` no es cerrado y exhaustivo,
esta métrica no se puede aplicar. **La rúbrica tiene que ser un catálogo, no una guía.**

---

## 3 · Qué se cuenta

### Clase `normativo` — comparación exacta

Cada flag normativo se evalúa como una afirmación verdadera o falsa contra la LCSP.

- **Acierto (VP):** el flag está en el Gold y el agente lo emite sobre la misma cláusula.
- **Omisión (FN):** está en el Gold y el agente no lo emite.
- **Falso positivo (FP):** el agente lo emite y no está en el Gold.

Métrica: **precisión, exhaustividad y F1**, sin ponderar.

**Exigencia distinta al resto del esquema:** aquí no vale «razonablemente bien». Un flag
normativo mal emitido es una afirmación falsa sobre el contenido de una ley, que es exactamente
el fallo que este proyecto existe para no cometer. Umbral de aceptación: **F1 ≥ 0,95**. Por
debajo, el pipeline no se da por bueno aunque la clase valorativa vaya bien.

### Clase `valorativo` — conjuntos, con asimetría explícita

- Mismo emparejamiento por `id` + ancla.
- Métrica: **precisión y exhaustividad, y como cifra resumen F₂** — que pondera la
  exhaustividad el doble que la precisión.

**Por qué F₂ y no F1.** En revisión contractual, señalar de más cuesta minutos de lectura;
omitir cuesta dinero cuando el riesgo se materializa. La métrica tiene que reflejar esa
asimetría en vez de fingir que los dos errores pesan igual. F₂ la codifica sin necesidad de
ponderaciones ad hoc.

### `missing_clauses` — se mide con la clase normativa

Una cláusula ausente solo es reprochable si **alguna norma la exige**. La ausencia de una
condición especial de ejecución es un incumplimiento del art. 202.1 LCSP; la ausencia de una
cláusula que a uno le gustaría tener, no es nada.

**Regla:** `missing_clauses` solo admite entradas con `base_normativa`. Sin norma que la exija,
la observación va a `review_notes`, no a `missing_clauses`. Se evalúa con la métrica normativa.

### `key_clauses` — cobertura, no acierto

Es un campo de localización, no de juicio: identifica dónde está cada materia en el pliego. Se
mide como **cobertura de las materias de la rúbrica presentes en el documento**, con las mismas
reglas de ancla. No lleva precisión: identificar una cláusula de más no es un error.

---

## 4 · Severidad: métrica secundaria, nunca parte del emparejamiento

`severity` **no interviene** en si un flag empareja o no. Se evalúa aparte, y **solo sobre los
flags ya emparejados**.

Métrica: **acierto exacto** más **error medio con signo** en la escala ordinal
`low < medium < high`, para poder detectar si el agente sobreestima o subestima de forma
sistemática, que es más informativo que un porcentaje de acierto.

Razón de separarlo: si la severidad entrara en el emparejamiento, un riesgo correctamente
detectado con severidad discrepante contaría como omisión **y** como falso positivo a la vez —
penalizado dos veces por un solo desacuerdo, y encima el desacuerdo más opinable de todos.

*(Esto cierra la pregunta abierta en `IDEAS.md`: un riesgo detectado con severidad distinta
cuenta como acierto en el emparejamiento y como fallo en la métrica de severidad.)*

---

## 5 · Fallos duros: no son omisiones, son errores de contrato

Tres situaciones **no se puntúan como fallo de exhaustividad**. Invalidan el documento entero y
se reportan aparte, en recuento absoluto:

| Fallo duro | Detección |
|---|---|
| **Régimen contaminado** — un `risk_flags[].regimen` distinto del `regimen` del documento | Mecánica |
| **Consecuencia jurídica importada** — se afirma nulidad por abusividad en régimen administrativo | Mecánica: `consecuencia_juridica` con vocabulario propio de consumo bajo `regimen=administrativo` |
| **`base_normativa` inexistente o que no dice lo que se le atribuye** | Contra el texto consolidado del BOE |

El tercero es la versión contractual de las sentencias inventadas, y es el fallo que más caro
sale: un informe que cita mal un artículo de la LCSP es peor que un informe que no dice nada.
**Cero tolerancia: un solo caso bloquea la versión.**

---

## 6 · Cómo se reporta

**Nunca una sola cifra.** El reporte mínimo de una evaluación son cuatro bloques:

```
normativo    P / R / F1        + IC bootstrap por documento
valorativo   P / R / F2        + IC bootstrap por documento
severidad    acierto exacto, error medio con signo (solo emparejados)
fallos duros recuento absoluto por tipo
```

Agregar normativo y valorativo en un número medio está **prohibido**: mezclaría una métrica de
verdad-falsedad con una de juicio, y el resultado no sería interpretable — el mismo error de
categoría que agregar regímenes.

---

## 7 · Tamaño mínimo, con cifra

`alcance.md` dejaba esto abierto. Se cierra así:

| Clase | Mínimo para **medir** | Mínimo para **comparar versiones** |
|---|---|---|
| `normativo` | 40 flags anotados por partición | 40 — la clase es casi determinista, no necesita más |
| `valorativo` | 40 flags anotados por partición | **~100 flags** por partición |

Con 8–20 cláusulas anotables por pliego y aproximadamente la mitad valorativas, esos 100 flags
salen de **~15–20 pliegos anotados por partición**, o **30–40 pliegos anotados en total**.

> **Compromiso por escrito, para que no se incumpla solo:** hasta alcanzar los 100 flags
> valorativos por partición, la clase valorativa se reporta como **orientativa** y **no se usa
> para decidir entre versiones del pipeline**. La clase normativa sí es decisoria desde los 40,
> porque es comprobable contra la ley y no depende de tamaño muestral para ser correcta.

Esta es la salida realista al riesgo abierto: no se finge potencia estadística que no hay, y a
la vez el proyecto no se queda paralizado — se avanza con la mitad que sí se puede medir.

---

## 8 · Lo que esta métrica **no** mide

Escrito aquí para que no se dé por medido lo que no lo está:

- **No mide utilidad.** Un pipeline puede acertar todos los flags de la rúbrica y no servirle a
  nadie, porque la rúbrica podría no recoger los riesgos que de verdad cuestan dinero. Eso solo
  lo corrige contrastar la rúbrica con quien licita.
- **No mide `plain_language_summary`.** Queda sin métrica, y se declara así en vez de inventarle
  una.
- **No mide calibración de `severity` frente a impacto económico real.** Solo consistencia con
  el Gold.
- **No mide generalización a otros órganos de contratación.** El sesgo por plantilla del órgano
  es real: si el corpus se concentra en pocos órganos, la métrica mide rendimiento sobre sus
  plantillas. Registrar el órgano en el inventario y estratificar al muestrear —ya previsto en
  `alcance.md`— es la mitigación, no la solución.
