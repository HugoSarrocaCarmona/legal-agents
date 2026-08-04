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