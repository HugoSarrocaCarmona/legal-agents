# 📜 Project Log

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