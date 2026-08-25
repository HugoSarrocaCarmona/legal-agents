# Registro de evaluaciones

**Una línea por ejecución, escrita ANTES de mirar el resultado.**

Este fichero existe porque el corpus de test de sentencias se gastó por reevaluación repetida:
se midió, se corrigieron reglas mirando los fallos, y se volvió a medir sobre los mismos
documentos. El 315/315 resultante confirma que las reglas funcionan, pero no mide
generalización, y no hay forma de recuperar esa medición perdida.

La regla que lo evita es simple y está en [`alcance.md`](alcance.md): **una ejecución por
versión del pipeline sobre ciego-1; ciego-2 no se abre hasta la siguiente release mayor.** Una
regla sin registro se incumple sola, casi siempre sin mala fe: por eso este fichero.

## Cómo usarlo

Antes de lanzar una evaluación, añade la fila. Después, rellena el resultado. Si vas a evaluar
una partición que ya aparece con la misma versión del pipeline, **para**: eso es gastar el
conjunto ciego, y hay que subir versión o abrir la partición siguiente.

| Fecha | Pipeline | Versión | Vía | Partición | Nº docs | Resultado | Notas |
|---|---|---|---|---|---|---|---|
| 05/08/2026 | sentencias | v2 | — | test (`sentencia23`–`35`) | 13 | 313/315 | Única medición ciega que existe |
| 05/08/2026 | sentencias | v2 | — | test (mismos documentos) | 13 | 315/315 | ⚠️ **Conjunto gastado.** Reevaluación tras corregir dos reglas mirando los fallos anteriores. No mide generalización |

*Sin evaluaciones de contratos: el pipeline aún no existe.*

---

## Pre-registros

Criterios de éxito escritos **antes** de ejecutar la evaluación. Se registran aquí para que el
resultado no pueda racionalizarse después: si el umbral se fija al ver los números, deja de ser
un umbral.

### Generalización de dominio en sentencias — registrado el 17/08/2026

> «En esta evaluación se van a recoger sentencias de materias diversas con tal de medir
> generalización de dominio. Considero aceptable un total del 30 % de acierto y me haría
> replanteármelo un total del 7 %, solo si hay algún indicio de potencial mejora a mi alcance
> estaré dispuesto a continuar con el modelo.»

**Estado: pendiente de ejecutar.** El corpus de materias diversas no está recogido.

Dos cosas a revisar antes de correrla, porque afectan a si el umbral significa lo que parece:

- **Los umbrales conviven con un 315/315 en los 9 campos de cabecera.** Si el 30 % se refiere a
  los mismos campos, es una caída enorme y conviene explicitar por qué se espera; si se refiere
  a los campos sustantivos, entonces es otra métrica y debería nombrarse como tal.
- **Sobre qué campos se mide.** Un porcentaje global mezcla campos mecánicos y sustantivos, y el
  resultado se vuelve difícil de interpretar. Conviene fijar el desglose antes, no después.

Ninguna de las dos invalida el pre-registro: lo que no debe cambiarse al ver los números son los
umbrales, no su redacción previa.
