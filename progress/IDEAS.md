# 💡 Ideas

## 🔥 Ideas prioritarias
- Sistema de scoring de calidad de resúmenes
- Comparador entre sentencias
- Clasificación automática por materia

---

## 🧪 Experimentos
- Multi-agente colaborativo
- Auto-validación con segundo agente
- Prompt chaining

---

## 🚀 Futuro
- SaaS legal
- API pública
- Integración con bases de datos jurídicas

## El agente que no carga el estándar

Si el agente no carga `standards/`, produce JSON plausible con reglas recordadas y ninguno de
los dos scripts lo detecta: seguirían dando verde.

**Resuelto en contratos, abierto en sentencias.** El esquema v3 de contratos lleva un campo
`standard_version` cuyo valor —`"contratos-v3"`— solo puede conocerse leyendo el fichero del
estándar. Que el valor cambie con cada versión del esquema es intencionado: si no cambiara,
dejaría de identificar qué reglas se aplicaron. No demuestra que las reglas se aplicaran bien; convierte «no cargó el estándar» de
fallo silencioso en fallo detectable, que es el mínimo y es mucho más que nada.

**Por qué no se ha hecho lo mismo en sentencias.** Añadir un campo al esquema v2 de sentencias
rompería el orden de campos que comprueba `validate_v2.ps1`, e invalidaría los 35 outputs y los
35 ficheros del Gold contra el validador actual. Es un cambio con coste real, y hacerlo de
pasada al tocar otra cosa sería exactamente la clase de decisión que este repositorio evita.

Queda como propuesta, con su coste explícito: `standard_version` + `SCHEMA_ORDER` actualizado +
reproceso o migración de los 35 outputs. Decidir aparte, no de rebote.


## MCP de legislación española (candidato, fase jurisprudencia)

**Origen:** repositorio github.com/Sistemasansvar/leyespañola-mcp (sin verificar).

**Problema que resolvería:** el fallo más grave de la IA jurídica son las citas
inventadas — normas o sentencias plausibles que no existen. Un MCP que consulte
legislación consolidada permite verificar cada referencia contra la fuente en
lugar de confiar en la memoria del modelo.

**Resuelve la mitad del problema, y conviene tenerlo claro antes de construirlo.**
El estudio de Stanford RegLab distingue dos errores distintos:

- **Fabricación** — la cita no existe. Es la que un MCP resuelve.
- **Desanclaje** (*misgrounding*) — la norma existe, está bien citada, y **no
  sostiene lo que se le atribuye**. Que el art. 1124 CC exista no significa que sea
  el que aplica el tribunal en ese fundamento.

El desanclaje es el más sutil y el más peligroso, y es invisible tanto para un MCP
como para cualquier validador de forma. Verificar el anclaje de `applied_rules` es
un problema distinto y más difícil. **No presentar el MCP como solución a las
alucinaciones**: resuelve las citas falsas, no las citas mal traídas.

**Encaje:** no es un agente nuevo, es una fuente de datos. Serviría para validar
`applied_rules` y `cited_by_parties` en el módulo de sentencias, y sería
infraestructura necesaria para el futuro módulo de jurisprudencia.

**Verificar antes de usar:**
- Quién lo mantiene y con qué licencia
- De dónde saca los datos: si no es del BOE, no sirve para uso profesional
- Si devuelve texto consolidado y actualizado o una copia congelada
- Qué pasa con normativa autonómica

**Cuándo:** después de cerrar el test set y el módulo de contratos.
No añadir agentes nuevos antes de medir la generalización del extractor actual.

## ✅ Evaluación de campos sustantivos — CERRADO el 06/09/2026

**Problema:** eval_gold.ps1 compara por igualdad exacta. Funciona con ecli o
decision_date porque tienen una única respuesta correcta. No sirve para
risk_flags ni missing_clauses: son campos donde la respuesta es más o menos
completa, no correcta o incorrecta.

**Decidido en [`corpus/metrica-contratos.md`](../corpus/metrica-contratos.md)**, adoptando el
esquema de ContractEval (arXiv 2508.03080) en vez de diseñar uno propio. Las cuatro preguntas
que estaban abiertas, con su respuesta:

- **Qué significa que un riesgo esté bien detectado** → mismo identificador de rúbrica que el
  Gold **y** ancla solapada en la misma cláusula. Ni `issue`, ni `why_it_matters`, ni
  `suggested_fix` entran en la detección.
- **Métrica** → F1 y F2 sobre emparejamiento de conjuntos, más Jaccard sobre las citas y una
  tasa de pereza aislada. Unidad: el criterio anotado, no el documento.
- **Severidad** → se mide **aparte**, sobre los pares ya emparejados, con coincidencia exacta,
  coincidencia adyacente y matriz de confusión 3×3. Un flag detectado con severidad distinta es
  un acierto de detección y un fallo de calibración; fundirlos oculta cuál falla.
- **Falsos positivos** → penalizan, pero **menos**. La intuición era correcta y el instrumento
  es **F2** (F-beta con β=2), que es la elección explícita de ContractEval por la misma razón.

**Sigue abierto para sentencias.** `facts`, `applied_rules`, `ratio_summary` y `holding` siguen
sin evaluación de contenido, y el 315/315 sigue sin ser extrapolable. La métrica de contratos no
es trasladable tal cual: sentencias no tiene rúbrica ni vocabulario cerrado, que es lo que hace
posible el emparejamiento.

## ✅ Tamaño mínimo del conjunto de evaluación — CERRADO el 06/09/2026

**Problema:** el corpus anotado será de decenas aunque el descargado llegue a
cientos. Partido en ciego-1 y ciego-2 quedan ~20 documentos por partición, y para
`risk_flags`, que es multietiqueta, eso da intervalos tan anchos que casi cualquier
diferencia entre versiones sería indistinguible del ruido.

**Se resolvió cambiando la unidad de medida, no consiguiendo más documentos.** De las tres
opciones que estaban planteadas se toman la segunda y la tercera, que no eran excluyentes:

- **Unidad = criterio anotado**, no documento. ~23 documentos × 15-25 unidades dan varios
  centenares de unidades. Es el patrón del *Legal Agent Benchmark* de Harvey: 1.200 tareas,
  75.000 criterios.
- **Sin intervalos de confianza sobre esas unidades**, porque la objeción registrada era
  correcta: las cláusulas de un mismo documento no son independientes.
- Para comparar versiones, **regla del documento único**: recalcular quitando un documento cada
  vez; si quitar cualquiera invierte el resultado, la comparación no vale. Es *leave-one-out*, no
  exige suponer independencia, y es barata de calcular.
- **La primera medición es orientativa, y está escrito** en la métrica para que no pueda
  alegarse después.

Se descarta la primera opción —fijar un mínimo por partición y no evaluar hasta alcanzarlo—
porque bloquearía el uso diagnóstico, que funciona desde el primer documento y es el uso
principal.

## Anotación asistida por modelo (candidato, no decidido)

**Idea:** si el cuello de botella es la anotación manual, usar el modelo para
pre-anotar y que el trabajo humano sea revisar en lugar de escribir.

**Riesgo grave:** si el mismo modelo que se evalúa pre-anota el Gold, el Gold
hereda sus sesgos y la evaluación deja de ser independiente. Mediría consistencia
consigo mismo, no acierto.

**Condición mínima si se hace:** modelo distinto del evaluado, revisión humana de
todas las pre-anotaciones, y registrar qué documentos fueron pre-anotados para
poder medir si difieren de los anotados desde cero.

**Cuándo:** no antes de tener la rúbrica escrita. Sin criterio previo, la
pre-anotación no es revisable.