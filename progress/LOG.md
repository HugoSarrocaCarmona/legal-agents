# 📜 Project Log

## [06/09/2026] — 🔧 Alcance a dos regímenes, `severity` derivada y encaje regulatorio

Segunda sesión del día. La primera cerró la métrica y subió el esquema a v2; esta poda el
alcance, rehace el eje de régimen y añade la nota regulatoria pendiente. **Sigue sin existir
ningún output de contratos**, que es justamente cuando cambiar el esquema es gratis.

### ✅ Hecho
- **Vía B eliminada del alcance**, y con ella el régimen `mercantil`. No diferida: eliminada
- **Eje de régimen rehecho** (`contratos` v3): `administrativo | condiciones_generales`, uno por
  vía viva. El eje anterior mezclaba la fuente del control con su consecuencia
- **Columna `condicion_adherente` en el inventario**, donde se registra la verificación
  consumidor/empresario documento a documento
- **`severity` pasa a ser derivada** de `severity_driver` (enum de 4) y `desproporcion` (enum de
  4), con tabla de derivación de 6 filas
- **`criterio` pasa a enum cerrado** de 5 valores, los criterios que se transfieren entre
  regímenes
- **Se descarta reportar la variante estricta de ContractEval.** Dos cómputos por evaluación
  para un número que responde a otra tarea
- **`docs/encaje-regulatorio.md`** — Instrucción 2/2026 CGPJ, Circular 3/2026 CGAE y Reglamento
  (UE) 2024/1689, con la calidad de cada fuente declarada y las preguntas abiertas señaladas
- **Bug preexistente del inventario arreglado**: dos filas tenían una coma sin comillas dentro
  de `motivo` y parseaban con 14 campos en vez de 13. El fichero no era CSV válido

### ❌ Problemas encontrados
- **Borrar `mercantil` a secas habría dejado `adhesion-05` sin clasificación.** Es clausulado de
  adhesión de vía C dirigido a clientes profesionales, y estaba marcado `regimen: mercantil`. El
  eje viejo lo obligaba a elegir entre su procedencia y su control
- **Las 9 resoluciones estaban marcadas `consumo` por defecto**: una suposición presentada como
  dato. Ahora son `por_verificar`, que es la verdad
- **Los 3 documentos de vía B no se pueden reclasificar a vía C**: son plantillas sin
  predisponente identificable ni datos reales, y no cumplen su criterio de inclusión
- **No se pueden mover ficheros de `Inputs/`** desde esta sesión. Quedan `pendiente_depurar`, un
  estado nuevo, en vez de mentir poniéndolos `depurado`

### 💡 Aprendizajes
- **Podar el alcance mejoró el diseño en vez de solo reducirlo.** Al quitar `mercantil` quedó a
  la vista que `consumo` tampoco era un régimen: era la consecuencia de quién se adhiere. El eje
  correcto —fuente del control por un lado, condición del adherente por otro— solo se vio al
  quitar el tercer valor
- **El corpus valida el esquema antes que ningún test.** `adhesion-05` existía desde agosto y era
  la prueba de que el eje estaba mal; nadie la leyó como tal hasta que hubo que tocar el eje
- **Un campo subjetivo se arregla aislando el juicio, no eliminándolo.** `severity` era una
  opinión no falsable. Ahora tres de los cuatro drivers son deterministas y el juicio vive en una
  casilla con una pregunta escrita — y cuando Gold y agente discrepen, el desacuerdo dirá si el
  fallo es de lectura o de criterio
- **Un inventario que no parsea no es auditable, por muy bien redactado que esté.** El bug de la
  coma llevaba desde el 06/08 y ninguna revisión a ojo lo vio

### 🔜 Siguiente paso
- **Paso 4: la rúbrica de `risk_flags`.** Único bloqueo. Ahora con dos regímenes en vez de tres,
  y con `criterio` y `severity_driver` como ejes ya cerrados que la rúbrica solo tiene que
  poblar
- **Manual, fuera de esta sesión**: mover `Inputs/corpus/via-b/plantilla-0{1,2,3}.txt` a
  `Inputs/_depurados/` y pasar su `estado` a `depurado`

---

## [06/09/2026] — 📐 Métrica de contratos y esquema v2

Se cierra el paso 1 de la fase 2, que llevaba bloqueando la rúbrica, el Gold y la evaluación, y
se aplican al esquema los cambios que la métrica exige. Todo, antes de anotar el primer
documento a propósito.

Origen: la investigación de mercado del 03/09 (`research/mercado-legaltech-2026.md`).

### ✅ Hecho
- **`corpus/metrica-contratos.md`** — qué significa que un output de contratos sea correcto.
  Adopta el esquema de **ContractEval** (arXiv 2508.03080) con dos desviaciones documentadas, en
  vez de diseñar una métrica propia
- **Tres niveles que no se agregan**: mecánicos por igualdad exacta, detección por
  F1/F2/Jaccard/pereza, texto libre fuera de la métrica
- **Unidad de medida: el criterio anotado, no el documento.** Es lo que hace medible un corpus
  de decenas
- **F2 como métrica principal** — pondera la exhaustividad, que es la respuesta a «¿penalizan
  los falsos positivos?»
- **`severity` se mide aparte de la detección**, con matriz de confusión 3×3
- **`standards/contratos.md` v2** — `standard_version`, `cita` verbatim + `localizador` en
  `key_clauses` y `risk_flags`, `condicion_adherente`, anclajes de `severity`,
  `risk_flags[].id` como vocabulario cerrado, y semántica de `missing_clauses` por lista de
  referencia. v1 nunca produjo output: nada que migrar
- **Protocolo de acuerdo consigo mismo**: 5 documentos, dos semanas de reposo, reanotación a
  ciegas, umbral F1 < 0,75
- Actualizados `ESTADO.md`, `ROADMAP.md`, `IDEAS.md`, `alcance.md`, `CLAUDE.md` y `README.md`

### ❌ Problemas encontrados
- **`missing_clauses` no tenía semántica.** «Falta una cláusula» solo significa algo contra una
  lista de referencia, y v1 no decía cuál. Dos anotadores habrían marcado cosas distintas sin
  forma de decir quién acierta
- **`control_aplicable` dependía de un dato que no era campo.** La tabla lo hacía depender de la
  condición del adherente, que el anotador tenía que inferir y no quedaba registrada — justo lo
  que prohíbe el principio 3 de `CLAUDE.md`
- **Nada estaba anclado al texto.** Sin `cita` no hay métrica de solapamiento, no hay
  verificación sin releer el contrato entero, y no hay trazabilidad
- **No hay `pwsh` en el entorno de la sesión**, así que `validate_contratos.ps1` no se ha
  escrito: un validador sin ejecutar ni una vez no es un validador

### 💡 Aprendizajes
- **La métrica antes del Gold no era una preferencia de orden, era una dependencia.** Al fijar
  la métrica aparecieron cuatro carencias del esquema que solo se ven cuando intentas calcular
  algo con él
- **Adoptar una métrica publicada gana más que diseñar una propia.** No solo por tiempo: un
  resultado calculado con el mismo esquema que la literatura es comparable, uno casero solo se
  compara consigo mismo
- **El problema del tamaño muestral no se resolvió con más documentos, sino cambiando la unidad
  de medida.** ~23 documentos siguen siendo ~23 documentos; como criterios anotados son varios
  centenares
- **Un 100 % en campos mecánicos no dice nada de los sustantivos, y ahora hay evidencia externa:**
  ContractEval mide F1 ≈ 0,9 en cláusulas frecuentes y cerca de cero en las raras de alto riesgo,
  con el mismo modelo y el mismo documento
- **Separar lo que se mide de lo que no.** `why_it_matters` y `suggested_fix` quedan fuera de la
  métrica a propósito: dos redacciones distintas pueden ser correctas, y puntuarlas daría una
  cifra falsa sobre campos que no deciden nada

### 🔜 Siguiente paso
- **Paso 4: la rúbrica de `risk_flags`** (`corpus/rubrica-riskflags.md`). Es ahora el único
  bloqueo: el esquema v2 exige que `risk_flags[].id` exista en la rúbrica, así que sin ella el
  estándar no es aplicable. Los criterios salen de las 9 resoluciones de la vía C, verificando en
  cada una si juzga a un consumidor o a un adherente empresario
- Después: listas de referencia de `missing_clauses`, y `validate_contratos.ps1`

---

## [25/08/2026] — 🧹 Reconstrucción del corpus de contratos

Sesión dedicada a que el corpus sea auditable antes de construir nada encima.

### ✅ Hecho
- **Inventario desde el disco**, no desde la tabla anterior: `corpus/inventario-contratos.csv`,
  30 filas con `sha256`. Instantánea declarada y suma reconciliada (23 activos + 7 depurados)
- **Reestructuración por vías**: `Inputs/corpus/via-{a,b,c}/` y `Inputs/_depurados/`.
  El renombrado no alteró ningún byte — los 30 hashes son idénticos a los previos
- **Dos ejes separados** en el inventario: `via` (procedencia) y `funcion` (para qué sirve)
- `corpus/alcance.md` — criterios de inclusión y exclusión por vía, escritos antes de descargar
- `corpus/evaluaciones.md` — registro de ejecuciones, para no repetir el gasto del test
- `corpus/candidatos-descartados.md` — población valorada y motivo de cada descarte
- `progress/ESTADO.md` — punto de entrada corto, enlazado desde `CLAUDE.md`
- `standards/contratos.md` v1: `risk_flags` con `regimen` y `control_aplicable`
- Copia externa del corpus a OneDrive, verificada por hash

### ❌ Problemas encontrados
- **Se perdió un documento.** El modelo argentino (nº 16) se borró el 06/08 en vez de moverse, y
  `Inputs/` está en `.gitignore`: no hay copia. Dado por perdido
- **La tabla anterior no cuadraba**: el resumen decía 9 documentos de adhesión donde la tabla
  tenía 8. Error de suma, no de depuración
- **Un fichero truncado** de 35 bytes ocupaba plaza en el corpus sin figurar en la tabla
- **Colisión de nombres**: `contrato1` significaba dos documentos distintos según la carpeta
- **Las vías A/B/C no estaban definidas en ningún sitio del repo**, solo en un documento externo

### 💡 Aprendizajes
- **Una tabla de composición sin instantánea declarada no es auditable.** Dentro de un mes no se
  puede saber qué contaba
- **Un corpus se depura moviendo, nunca borrando.** El único documento perdido lo demuestra
- **`risk_flags` no necesita datos reales de las partes.** El riesgo está en el texto y las
  cifras de la cláusula, no en quién firma. Confundirlo hizo descartar 12 documentos que eran
  justamente el corpus
- **Definir las vías por su fuente y asignarlas por su función son dos cosas distintas.**
  Mezclarlas en una columna bloqueó el inventario hasta desdoblarla en dos

### 🔜 Siguiente paso
- Paso 1 de la fase 2: decidir la métrica de campos sustantivos. Bloquea rúbrica, Gold y evaluación

---

## [06/08/2026] — 🏁 Cierre del módulo de sentencias

Fase 1 cerrada. El pipeline de extracción de sentencias está completo, medido y documentado.

### 📊 Métricas finales

| | Resultado |
|---|---|
| `eval_gold.ps1` | **315/315 (100 %)** — 35 documentos × 9 campos de cabecera, sin discrepancias |
| `validate_v2.ps1` | 35 archivos, **0 FAIL**, 9 avisos, exit 0 |
| Medición ciega (05/08) | **313/315 (99,4 %)** — dev 198/198, test-Supremo 45/45, test-otros órganos 70/72 |

Los nueve campos —`ecli`, `roj`, `resolution_number`, `appeal_number`, `id_cendoj`,
`decision_date`, `court_or_body`, `ponente`, `document_type`— al 100 %.

### 📦 Corpus

35 resoluciones del orden civil del CENDOJ: 27 del Tribunal Supremo (Sala de lo Civil) y 8 de
otros órganos —Tribunal de Instancia (Mercantil y Civil y de Instrucción), Tribunal Superior
de Justicia y Juzgado de lo Mercantil—, con **5 autos** entre ellas. Los 8 documentos fuera
del Supremo son los que ejercitaron las tres reglas del estándar v2 por primera vez.

### 🏗️ Arquitectura final

- `CLAUDE.md`: principios comunes e índice. Ni una regla de campo.
- `standards/sentencias.md`: fuente única del pipeline, el esquema de 16 campos, las reglas por
  campo y el contrato de validación.
- `standards/contratos.md`: borrador, sin ejercitar.
- `.claude/agents/sentencia_agent.md`: 40 líneas, sin duplicar ninguna regla.
- `validate_v2.ps1` (forma) + `eval_gold.ps1` (verdad) + `Gold/` de 35 ficheros.

### ⚠️ Lo que este 100 % no dice

- **No mide contenido.** `facts`, `applied_rules`, `ratio_summary` y `holding` solo tienen
  control de forma. Un output puede pasar las dos comprobaciones y contener un razonamiento
  equivocado. Los 9 campos medidos son los más mecánicos del esquema.
- **No mide generalización.** El conjunto de test **está gastado**: se evaluó el 05/08/2026,
  dio 313/315, y después se corrigieron dos reglas mirando esos dos fallos y se reprocesaron
  los documentos afectados. El 315/315 confirma que las reglas nuevas funcionan, nada más.
  Dev y test miden ya lo mismo: documentos que el estándar ha visto.
- **No cubre otros órdenes.** Todo el corpus es del orden civil.

### 🔜 Siguiente

Fase 2, Contract Analyzer. Ver `ROADMAP.md`. El primer paso no es escribir el esquema sino
**decidir cómo se evalúan campos sustantivos**: la comparación exacta que da el 100 % en
`ecli` o `decision_date` no sirve para `risk_flags` ni `missing_clauses`.

---

## [05-06/08/2026] — Test set procesado: 313/315 y el conjunto ciego se agota

### ✅ Hecho
- Estándar v2, tres cambios: `document_type` como enum cerrado leído del campo
  `Tipo de Resolución:`, `court_or_body` con niveles opcionales, regla de sección ambigua
- `validate_v2.ps1`: `document_type` que no coincide con la cabecera del input pasa de WARN a
  FAIL. Es la única comprobación que mira fuera del JSON
- Gold ampliado a 35 documentos; `document_type` entra como noveno campo evaluado
- Muestra de dev reprocesada (1, 3, 7, 9, 12, 14) y **los 13 documentos de test procesados**,
  un subagente por documento
- **313/315 (99,4 %)**: dev 198/198, test-Supremo 45/45, test-otros órganos 70/72
- `role: null` admitido en `parties`: pasa de FAIL a WARN en el validador
- Reglas nuevas de `ponente` (capitalización y acentos) y `ecli` (prefijo `ECLI:`), y
  `sentencia29` y `sentencia35` reprocesados con ellas: **315/315 (100 %)**

> **El 315/315 no es una medición de generalización.** Las dos reglas se escribieron mirando
> esos dos fallos concretos y después se reprocesaron esos dos documentos: el resultado
> confirma que las reglas hacen lo que tienen que hacer, y no dice nada sobre el rendimiento
> ante una cabecera nueva. La única cifra que mide generalización es el **313/315** de la
> primera pasada sobre test, cuando el conjunto todavía era ciego.

### ❌ Problemas encontrados
- **6 valores mal transcritos en el Gold del test**, detectados al contrastarlos con la
  cabecera: una fecha con el año cambiado, un número de sección, dos ponentes sin acentuar,
  dos sedes con paréntesis prohibidos por el propio estándar y un `null` escrito como cadena
  `"null"`. Todos eran errores del Gold, no del agente
- Los 13 agentes de la primera tanda cayeron por límite de sesión; 10 alcanzaron a escribir
- Dos errores reales del agente, ambos de transcripción de cabecera: ponente en mayúsculas sin
  acentos (`sentencia29`) y ECLI sin prefijo (`sentencia35`). Corregidos en el estándar y en
  los outputs, al precio de gastar el conjunto de test

### 💡 Aprendizajes
- Un Gold anotado a mano tiene la misma tasa de error que el sistema que pretende medir. Seis
  de las ocho discrepancias de la primera evaluación de test eran del Gold. Contrastar cada
  discrepancia contra la cabecera antes de atribuirla al agente no es opcional
- El estándar puede contradecirse a sí mismo sin que se note hasta que un documento lo fuerza:
  la sede `Palmas de Gran Canaria (Las)` chocaba con la prohibición de paréntesis en
  `court_or_body`, y el conflicto solo apareció al salir del Tribunal Supremo
- Una regla escrita mirando una cabecera no está probada hasta que se ejecuta contra ella: las
  tres del v2 pasaron 22 documentos de dev sin dispararse una sola vez
- `null` frente a rellenar: cuando el encabezamiento nombra a alguien sin rol, forzar
  `{name, role}` completo obliga a inferir justo lo que el estándar prohíbe

### 🔜 Siguiente paso
- Corpus nuevo: ya no queda conjunto ciego con el que medir generalización
- Evaluación de contenido para `facts`, `applied_rules`, `ratio_summary` y `holding`, que
  siguen sin más control que el formal

---

## [03/08/2026] — Migración a esquema v2 y control de versiones

### ✅ Hecho
- Esquema v2 (16 campos) como estándar único: `CLAUDE.md` + copia versionada `CLAUDE.v2.md`
- Campos nuevos: `case_id`, `decision_date`, `ponente`, `parties`, `cited_by_parties`, `document_quality_notes`
- Estructuras fijadas: `facts` array 5–15, `parties {name, role}`, `applied_rules {type, ref, note}`
- `validate_v2.ps1`: 12 bloques de comprobación, distingue FAIL de WARN, exit code encadenable
- Dataset completo reprocesado a v2 (6/6 validan, exit code 0)
- README técnico con pipeline, esquema y comandos
- `git init` y primer commit

### ❌ Problemas encontrados
- 5 de 6 agentes de reprocesado cayeron por límite de sesión; 4 alcanzaron a escribir su archivo
- `sentencia2.v2.json` no lo generó el agente: se construyó manualmente. Pendiente regenerarlo con el agente y comparar
- Tres specs legacy en `Agents/` contradecían el estándar vigente (esquema muerto, regla «No especificado» frente a `null`) → archivados

### 💡 Aprendizajes
- Los identificadores (ECLI, Roj, nº resolución) son extracción determinista de cabecera; dejarlos al criterio del modelo produjo 8 de 24 huecos en v1
- Separar `uncertainties` de `document_quality_notes` elimina el ruido estructural que repetían los 6 outputs
- Un validador solo sirve si distingue lo que incumple el contrato de lo que merece revisión humana

### 🔜 Siguiente paso
- Métricas de calidad (`METRICS.md` sigue vacío)
- Contract Analyzer

---

## [01/08/2026] — Inicio sistema documentación

### ✅ Hecho
- Implementado sistema de resumen de sentencias automatizado
- Creación de estructura de agentes
- Primera versión funcional del pipeline

### ⚙️ En progreso
- Mejora del CLAUDE.v2.md
- Estandarización de outputs JSON

### ❌ Problemas encontrados
- Inconsistencia en algunos outputs
- Falta de validación estructural fuerte

### 💡 Aprendizajes
- Importancia de definir schemas desde el inicio
- Claude responde mejor con instrucciones estructuradas

### 🔜 Siguiente paso
- Crear Contract Analyzer