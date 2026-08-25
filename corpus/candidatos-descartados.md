# Candidatos valorados y descartados

Instantánea: **25/08/2026**, posterior a la reestructuración por vías.

Este archivo existe porque el criterio de inclusión del corpus no era reproducible: la tabla
del roadmap contaba los documentos que entraron, pero no cuántos se llegaron a valorar ni por
qué se rechazaron los demás. Sin eso, nadie —incluido el autor dentro de seis meses— puede
repetir el cribado ni juzgar si estuvo bien hecho.

Los criterios que rigen a partir de ahora están en [`alcance.md`](alcance.md), escritos antes
de descargar nada. Este fichero documenta el cribado **anterior** a esa regla.

## Reconciliación

| Población | N | Verificable |
|---|---|---|
| Documentos valorados antes de descargar | **~20 (estimado)** | ❌ No |
| Documentos en disco | **30** | ✅ Sí |
| — activos en `Inputs/corpus/via-{a,b,c}/` | 23 | ✅ Sí |
| — depurados en `Inputs/_depurados/` | 7 | ✅ Sí |

> ⚠️ **La estimación y el disco no cuadran.** El autor recuerda haber valorado unos 20
> documentos, pero en disco hay 30. La discrepancia (~10) queda declarada, no resuelta: no
> existe registro de las búsquedas ni de las descargas, porque `Inputs/` nunca estuvo
> versionado. Cualquier cifra más precisa sería inventada.

## Origen de los documentos

Búsquedas sueltas, sin protocolo registrado, en tres fuentes:

- **Condiciones generales de contratación** publicadas por empresas (banca, telecomunicaciones,
  energía, seguros, seguridad). Es el origen de todo el material de adhesión de la vía C.
- **BOE y boletines oficiales**: convenios administrativos y pliegos de contratación pública.
- **Plantillas comerciales y modelos colegiales** de acceso libre.

No se conserva el listado de consultas ni las URL de descarga. **Para futuras incorporaciones,
registrar la URL y la fecha en el momento de la descarga**, en `inventario-contratos.csv`.

## El vuelco del cribado anterior

La depuración del 06/08/2026 apartó como «descartados» 13 documentos por no ser contratos. Esa
decisión se ha revertido casi entera, y el motivo está en la corrección del blocker de
`risk_flags`: **anotar riesgos no exige datos reales de las partes, exige una fuente de verdad
externa sobre qué constituye riesgo.**

Con ese criterio, 12 de los 13 «descartados» son el corpus, no su descarte:

| Documentos | Estado anterior | Estado nuevo |
|---|---|---|
| 3 pliegos de contratación | Descartados | **Núcleo de la vía A** — son exactamente el tipo documental objetivo |
| 9 resoluciones judiciales | Descartadas (solo 3 «posible cantera») | **Fuente de la rúbrica de `risk_flags`** (vía C) |
| 1 comentario doctrinal | Descartado | Sigue depurado: fuente secundaria |

Se verificó por recuento de términos que **las nueve** resoluciones tratan de abusividad o
condiciones generales, no solo las tres identificadas antes. La redacción anterior infravaloraba
seis documentos válidos. `resolucion-05` es la más rica (44 menciones a abusividad, 22 a
condiciones generales, 49 a transparencia); `resolucion-03` la más marginal (2 menciones).

## Los 7 depurados que quedan

### Fuera de alcance (3)

Los tres caen por el mismo criterio de [`alcance.md`](alcance.md): **un documento que obligue a
crear referencias nuevas para poder analizarse no entra en esta iteración.**

- `laboral-representante-comercio` — relación laboral especial (RD 1438/1985). Exigiría un
  cuarto régimen y una rúbrica de riesgos propia.
- `convenio-subvencion` — convenio administrativo de subvención. No es un contrato; exigiría
  una categoría propia en el inventario.
- `comentario-doctrinal` — fuente secundaria sobre la STS 671/2018. No transcribe clausulado
  original, así que no sirve como cantera de cláusulas anotables.

### Redundantes (3)

`arrendamiento-redundante-01` a `03` — arrendamientos de vivienda casi intercambiables. Se
conserva `via-b/plantilla-01` por mayor cobertura de cláusulas (408 líneas) y por usar
placeholders nombrados (`[Nombre del propietario]`) en lugar de guiones bajos anónimos, que
identifican qué campo va en cada hueco. Redundancia no es cobertura.

### Fichero corrupto (1)

`truncado-arrendamiento` — 35 bytes, solo la línea `CONTRATO DE ARRENDAMIENTO TEMPORADA`. Resto
de una descarga fallida. Estaba en el directorio de contratos sin figurar en la tabla del
roadmap, que es la razón por la que el directorio mostraba 14 ficheros donde la tabla contaba 13.

## Pérdida no recuperable

El antiguo **nº 16** (modelo de sociedad de capital e industria, derecho argentino, Ley 19.550)
se **borró** el 06/08/2026 en lugar de moverse. `Inputs/` figura en `.gitignore`, así que no
existe copia en el histórico. El autor lo da por perdido de forma deliberada: era material
fuera del alcance del proyecto. Queda registrado como precedente — **el borrado de aquel
documento es lo que motivó la regla de que nada se elimina, solo se mueve a
`Inputs/_depurados/`.**

## Lo que el cribado no resuelve

El corpus actual es de **arranque**, no definitivo. Tiene tres vías cubiertas de forma muy
desigual: 3 documentos en la A, 3 en la B —y sin un solo dato real— y 17 en la C. Hay
recopilación de contratos nuevos pendiente, y los actuales no son intocables.

Toda incorporación futura pasa por [`alcance.md`](alcance.md) **antes** de descargarse. Esa es
la vacuna contra volver a depurar a posteriori, que es lo que ha costado esta sesión entera.
