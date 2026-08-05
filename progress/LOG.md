# 📜 Project Log

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

### ❌ Problemas encontrados
- **6 valores mal transcritos en el Gold del test**, detectados al contrastarlos con la
  cabecera: una fecha con el año cambiado, un número de sección, dos ponentes sin acentuar,
  dos sedes con paréntesis prohibidos por el propio estándar y un `null` escrito como cadena
  `"null"`. Todos eran errores del Gold, no del agente
- Los 13 agentes de la primera tanda cayeron por límite de sesión; 10 alcanzaron a escribir
- Dos errores reales del agente, ambos de transcripción de cabecera: ponente en mayúsculas sin
  acentos (`sentencia29`) y ECLI sin prefijo (`sentencia35`). Corregidos en el estándar, con
  los outputs **sin reprocesar**

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
- Reprocesar `sentencia29` y `sentencia35` con las reglas nuevas y volver a medir
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