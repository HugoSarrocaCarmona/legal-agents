# Alcance del corpus de contratos

**Criterios de inclusión y exclusión, escritos antes de descargar nada.**
Fijado: 25/08/2026.

Este fichero existe porque la iteración anterior descargó primero y depuró después. El
resultado fue un corpus que hubo que reconciliar a mano y del que se perdió un documento. **Un
documento que no cumpla el criterio de su vía no se descarga; si ya está descargado, se mueve a
`Inputs/_depurados/` con su motivo.** Ninguna de las dos cosas se decide sobre la marcha.

---

## Principio general

**El alcance se estrecha a propósito.** Primero hacer bien una variedad pequeña de tipos
contractuales; ampliar después, si el pipeline lo sostiene. En caso de duda sobre si un
documento entra, la respuesta por defecto es **no**.

Dos causas de exclusión automática, sin más análisis:

1. **Documentos a medias** — truncados, sin clausulado completo, o versiones parciales.
2. **Documentos que exigirían crear referencias nuevas** para poder analizarlos: un régimen
   jurídico no contemplado, una categoría nueva en el inventario, o una rúbrica propia.

La segunda es la que más corpus ha depurado, y es deliberada. Cada régimen nuevo obliga a
escribir su rúbrica de riesgos completa antes de poder anotar un solo documento.

---

## Vía A — Administrativa (principal)

**Fuente:** PLACSP, sindicación ATOM + pliegos PCAP/PPT.
**Función:** volumen, datos reales de ambas partes, medida del pipeline mecánico.

| Criterio | Valor |
|---|---|
| Tipo de contrato | Servicios, obras y suministros |
| Importe | Excluidos los **contratos menores** (<15.000 € servicios/suministros, <40.000 € obras) |
| Rango temporal | Adjudicaciones de 2024 en adelante |
| Órgano | Cualquiera, pero registrando el órgano para poder estratificar |
| Longitud mínima | El PCAP debe traer clausulado, no solo cuadro de características |
| Formato | **PDF con capa de texto.** Los escaneados sin OCR quedan fuera |

> ⚠️ **La extractabilidad se comprueba ANTES de muestrear, no después.** Si se descartan los
> PDF no extraíbles una vez hecho el muestreo, la muestra deja de ser aleatoria y se sesga
> hacia los órganos con mejor ofimática. Filtrar primero, muestrear después, semilla registrada.

**Exclusiones:** contratos menores, acuerdos marco sin pliego propio, prórrogas y modificados
que no traigan clausulado nuevo, y expedientes desiertos o desistidos.

---

## Vía B — Mercantil negociada (**cerrada**)

**Fuente:** CNMV, registros oficiales e información relevante con contrato anexo.
**Función:** clausulado genuinamente negociado — covenants, reps & warranties, MAC, indemnidades.

| Criterio | Valor |
|---|---|
| Tipo de anexo | Contratos completos anexados a hechos relevantes; no resúmenes ni notas |
| Rango temporal | 2020 en adelante |
| Volumen esperado | Decenas |

> 🔒 **Cerrada el 09/09/2026, no diferida.** Con el giro a pliegos, el régimen mercantil sale
> del alcance de esta iteración entero: no tendrá rúbrica, ni Gold, ni métrica. Mantenerla como
> "diferida" era una forma educada de tenerla abierta sin trabajarla. Se reabrirá, si acaso,
> como iteración propia y con su propio alcance escrito.
>
> *Redacción anterior, conservada por trazabilidad:* los contratos íntegros anexados a la CNMV
> son raros —lo habitual es el resumen—, y los que hay son de M&A y financiación, con clausulado
> muy alejado del resto del corpus.

Las 3 plantillas negociadas (`plantilla-01` a `03`) permanecen en disco y en el inventario. No
se anotan ni se depuran.

---

## Vía C — Condiciones generales (soporte)

**Fuente:** clausulado de adhesión publicado por empresas, y resoluciones de CENDOJ sobre
cláusulas abusivas.
**Función:** *(revisada el 09/09/2026)* **fuente de criterios valorativos, y nada más.**

> 🔻 **Degradada tras el giro a pliegos.** La función anterior era doble: clausulado de adhesión
> como material **anotable**, y resoluciones como **fuente de verdad** de la rúbrica. Las dos
> cambian.
>
> **La rúbrica ya no se extrae de aquí.** Para el régimen administrativo la fuente primaria es
> la **LCSP**, que fija umbrales numéricos —10 % y 50 % en penalidades, 0,60 € por 1.000 € y
> día, 5 % y 10 % en garantías, 20 % y 50 % en modificaciones, 30 + 30 días en pagos— donde el
> control de abusividad del TRLGDCU solo ofrece un estándar valorativo. Extraer de consumo el
> catálogo de un pliego habría importado un régimen que allí no rige, que es justamente lo que
> `standards/contratos.md` prohíbe.
>
> **Lo que sí se conserva de las 9 resoluciones** son los cinco criterios valorativos
> transferibles: desequilibrio, falta de reciprocidad, opacidad, desproporción de la penalización
> y facultades unilaterales. Son transferibles **por ser criterios**, no calificaciones.
>
> **Los 8 documentos de adhesión dejan de ser material anotable.** Permanecen en disco y en el
> inventario; salen del camino crítico.

Es la única vía heterogénea por diseño, y por eso el inventario lleva dos columnas: `via`
(procedencia) y `funcion` (para qué sirve). Un contrato de Orange y una STS sobre revolving
comparten función pero no procedencia.

| Subconjunto | Criterio |
|---|---|
| Clausulado de adhesión | Condiciones generales completas y vigentes de un predisponente identificable |
| Resoluciones | Materia: condiciones generales, cláusulas abusivas, transparencia. Cualquier instancia |

**Exclusiones:** fuentes secundarias —comentarios doctrinales, notas de jurisprudencia— por no
transcribir clausulado original; y resoluciones cuya materia no sea el control de condiciones
generales.

> **Pendiente al redactar la rúbrica:** confirmar documento a documento si cada resolución
> juzga a un **consumidor** o a un **adherente empresario**. Son dos niveles de control
> distintos (abusividad vs. solo incorporación y transparencia), no un mismo régimen atenuado.
> Ahora mismo las 9 están marcadas `consumo` por defecto y eso está sin verificar.

---

## Fuera de alcance (decidido, no pendiente)

- **Derecho no español.** Precedente: el modelo argentino de sociedad de capital e industria
  (Ley 19.550), que motivó esta sección.
- **Relación laboral**, incluidas las especiales (p. ej. representantes de comercio,
  RD 1438/1985). Exigiría un cuarto régimen y una rúbrica propia.
- **Convenios administrativos** de subvención o colaboración: no son contratos.
- **Redundancia.** Varios documentos casi idénticos aportan un solo caso de prueba. Se conserva
  el de mayor cobertura de cláusulas.

---

## Partición de evaluación

Ortogonal a las vías. Dentro de cada vía, el corpus anotado se parte en **ciego-1**
(evaluación) y **ciego-2** (reserva).

- Se evalúa **solo sobre ciego-1**, y **una única ejecución por versión del pipeline**.
- **Ciego-2 no se abre hasta la siguiente release mayor.**
- Toda ejecución se registra en [`evaluaciones.md`](evaluaciones.md) antes de mirar el resultado.

Esto es la corrección directa del error cometido con el corpus de sentencias, donde el test se
gastó por reevaluación repetida. La regla sin registro se incumple sola: por eso el fichero.

> ✅ **Tamaño mínimo decidido el 09/09/2026** en [`metrica.md`](metrica.md). Se resuelve por dos
> vías a la vez: **se mide por cláusula anotada, no por documento** —lo que multiplica la N
> efectiva— y **los intervalos de confianza se remuestrean por documento**, para no tratar como
> independientes cláusulas que comparten órgano y plantilla.
>
> Mínimos: **40 flags por partición** para medir; **~100 flags valorativos por partición** para
> comparar versiones, lo que equivale a **15–20 pliegos anotados por partición** (30–40 en
> total). Hasta alcanzarlos, la clase valorativa se reporta como orientativa y **no decide entre
> versiones**; la normativa sí, desde 40, porque es comprobable contra la ley y su corrección no
> depende del tamaño muestral.
