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

## Campo `sentencia agent` (riesgo pendiente)
Si el agente no carga standards/, produce JSON plausible con reglas recordadas y ninguno de los dos scripts lo detecta: seguirían dando verde.


## MCP de legislación española (candidato, fase jurisprudencia)

**Origen:** repositorio github.com/Sistemasansvar/leyespañola-mcp (sin verificar).

**Problema que resolvería:** el fallo más grave de la IA jurídica son las citas
inventadas — normas o sentencias plausibles que no existen. Un MCP que consulte
legislación consolidada permite verificar cada referencia contra la fuente en
lugar de confiar en la memoria del modelo.

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

## Evaluación de campos sustantivos (bloqueante para contratos)

**Problema:** eval_gold.ps1 compara por igualdad exacta. Funciona con ecli o
decision_date porque tienen una única respuesta correcta. No sirve para
risk_flags ni missing_clauses: son campos donde la respuesta es más o menos
completa, no correcta o incorrecta.

**Consecuencia:** el 315/315 de la fase 1 no es extrapolable. Se midieron los
9 campos más mecánicos del esquema. Los sustantivos (facts, applied_rules,
ratio_summary, holding) siguen sin evaluación de contenido.

**A decidir antes de construir el Gold de contratos:**
- Qué significa que un riesgo esté bien detectado
- Métrica: precisión/recall sobre conjunto de riesgos, no igualdad exacta
- Umbral de severidad: ¿un riesgo detectado con severity distinta cuenta como acierto?
- Falsos positivos: ¿penalizan? En revisión contractual, señalar de más es menos
  grave que omitir, y la métrica debería reflejarlo

**Orden:** decidir la métrica ANTES de rellenar el Gold. Si se rellena primero
y se decide después, el Gold no servirá.