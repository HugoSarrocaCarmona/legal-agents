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

## Campo `formation` (pendiente)

**Problema detectado:** sentencia7 tiene "Sección: 991" en cabecera y "PLENO" en el
cuerpo. El agente conserva el literal 991 (correcto según la regla actual), pero se
pierde la información de que es una sentencia de Pleno.

**Por qué importa:** las sentencias de Pleno tienen distinto valor a efectos de
doctrina jurisprudencial. Es un criterio de filtrado útil para el futuro módulo
de búsqueda de jurisprudencia.

**Decisión:** campo nuevo en vez de mapear dentro de `court_or_body`. Evita que
un mismo campo acumule órgano + sala + sección + sede + composición, y mantiene
el principio de extracción literal.

**Implementación:**
- Añadir al esquema JSON: `"formation": ""`
- Valores permitidos: "pleno" | "seccion" | null
- Regla en CLAUDE.md: extraer "pleno" si la cabecera indica Sección 991
  o el cuerpo menciona expresamente PLENO. En cualquier otro caso, "seccion".
  Si no hay indicio, null.
- Añadir el campo a eval_gold.ps1 y al Gold de las 22 (+13 de test).

**Cuándo:** después de cerrar la tirada de las 22. No tocar el esquema a mitad
de evaluación.

**Coste:** revisar 22 documentos para rellenar el campo en el Gold.

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