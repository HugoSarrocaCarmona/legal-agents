# 📜 Project Log

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