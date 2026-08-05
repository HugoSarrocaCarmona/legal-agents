# 🧠 PROYECTO: LEGAL TECH AGENTS (ESPAÑA)

## 🎯 OBJETIVO GENERAL

Construir agentes de IA capaces de automatizar tareas jurídicas repetitivas en el contexto del derecho español, priorizando:

1. Resumen estructurado de sentencias
2. Análisis de contratos (riesgos, cláusulas, faltantes)

El sistema debe producir resultados útiles, consistentes y reutilizables en entornos profesionales.

---

## 📚 ÍNDICE DE ESTÁNDARES

Este archivo contiene **solo los principios comunes** a todos los tipos de documento. Las
reglas concretas de cada tipo —esquema JSON, reglas por campo y contrato de validación— viven
en un archivo por estándar, y **no se repiten en ningún otro sitio**:

| Estándar | Archivo | Estado |
|---|---|---|
| Sentencias, autos y resoluciones judiciales | [`standards/sentencias.md`](standards/sentencias.md) | vigente (v2), medido sobre 35 documentos |
| Contratos civiles y mercantiles | [`standards/contratos.md`](standards/contratos.md) | escrito, sin ejercitar |

**Antes de procesar un documento hay que leer el estándar que le corresponde.** Estos archivos
no se cargan solos.

Ante cualquier discrepancia entre un estándar y los principios de este archivo, prevalecen los
principios de este archivo.

---

## ⚖️ PRINCIPIOS FUNDAMENTALES

Este sistema realiza extracción estructurada de documentos jurídicos.

Reglas absolutas:

1. No inventar información bajo ninguna circunstancia
2. No inferir identificadores ni fechas
3. Separar SIEMPRE:
   - datos extraídos literalmente
   - datos interpretados
4. Priorizar consistencia interna sobre completitud
5. Si hay conflicto entre secciones del documento:
   → usar la cabecera como fuente primaria
6. JSON final debe ser válido y cumplir el contrato de validación de su estándar
7. En caso de duda:
   → preferir null antes que inferencia

---

## 🧾 TIPOS DE DOCUMENTOS SOPORTADOS

- Sentencias judiciales
- Autos
- Resoluciones administrativas
- Contratos civiles y mercantiles básicos

---

## 📤 FORMATO DE SALIDA (OBLIGATORIO)

Todas las respuestas deben ser JSON válido.

Nunca devolver texto libre.

---

## ⚠️ GESTIÓN DE ERRORES

Si hay:

- contradicciones
- fechas imposibles
- múltiples versiones

→ usar la cabecera como referencia
→ registrar la anomalía en los campos que cada estándar destina a ello

Si una duda se despeja con el propio documento, resolverla y no escalarla.

---

## 🚫 LIMITACIONES

El sistema NO debe:

- emitir conclusiones legales definitivas
- sustituir asesoramiento profesional
- afirmar validez jurídica sin contexto completo

---

## 🔄 MEJORA CONTINUA

El sistema debe:

- detectar errores recurrentes
- mejorar consistencia
- reducir ruido en outputs
- adaptarse progresivamente

---

## 🧩 COMPORTAMIENTO DEL AGENTE

- Priorizar precisión sobre creatividad
- Mantener outputs reutilizables
- Minimizar redundancia
- No improvisar estructura

---

## 📁 ORGANIZACIÓN

- Outputs en JSON
- Nombres consistentes
- Estructura estable

---

## 🎯 OBJETIVO FINAL

Crear una base sólida para:

- automatización legal real
- reducción de tiempo
- estandarización jurídica
- futuros productos legal tech
