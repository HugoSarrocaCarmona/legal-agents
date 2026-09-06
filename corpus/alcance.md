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

## Vía B — Mercantil negociada (secundaria, **diferida**)

**Fuente:** CNMV, registros oficiales e información relevante con contrato anexo.
**Función:** clausulado genuinamente negociado — covenants, reps & warranties, MAC, indemnidades.

| Criterio | Valor |
|---|---|
| Tipo de anexo | Contratos completos anexados a hechos relevantes; no resúmenes ni notas |
| Rango temporal | 2020 en adelante |
| Volumen esperado | Decenas |

> ⚠️ **Vía explícitamente diferida, no paralela.** Los contratos íntegros anexados a la CNMV
> son raros —lo habitual es el resumen—, y los que hay son de M&A y financiación, con
> clausulado muy alejado del resto del corpus. Declararla "en paralelo" con todo lo demás
> pendiente equivale a que no ocurra. Se abre cuando A y C estén cerradas.

Mientras tanto, las 3 plantillas negociadas del corpus actual sirven como **vocabulario de
cláusulas** para construir la rúbrica del régimen mercantil, no como corpus de evaluación: no
traen ni un dato real.

---

## Vía C — Condiciones generales (soporte)

**Fuente:** clausulado de adhesión publicado por empresas, y resoluciones de CENDOJ sobre
cláusulas abusivas.
**Función:** doble. El clausulado de adhesión es material **anotable**; las resoluciones son la
**fuente de verdad** de la rúbrica de `risk_flags`.

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
>
> El esquema v2 da dónde registrarlo (`condicion_adherente`) y convierte el descuido en error
> detectable: `regimen: consumo` con `condicion_adherente: empresario` es una contradicción que
> el contrato de validación rechaza.

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
- **Qué se mide y cómo**: [`metrica-contratos.md`](metrica-contratos.md). Las métricas van
  separadas por vía y no se agregan en una sola cifra, por la misma razón por la que los corpus
  van separados.

Esto es la corrección directa del error cometido con el corpus de sentencias, donde el test se
gastó por reevaluación repetida. La regla sin registro se incumple sola: por eso el fichero.

> ✅ **Tamaño mínimo: resuelto el 06/09/2026, cambiando la unidad de medida.** El corpus
> *anotado* sigue siendo de decenas —el cuello de botella es la anotación, no la obtención—,
> pero la unidad pasa a ser el **criterio anotado** en vez del documento, y ~20 documentos por
> partición dan varios centenares de unidades. No se calculan intervalos de confianza sobre
> ellas, porque las de un mismo documento no son independientes; para comparar versiones se usa
> la **regla del documento único**. Y queda escrito que la primera medición es orientativa.
> Detalle en [`metrica-contratos.md`](metrica-contratos.md).
>
> **No se fija un mínimo por partición.** Bloquearía el uso diagnóstico, que funciona desde el
> primer documento y es el uso principal de la métrica.
