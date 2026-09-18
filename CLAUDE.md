# 🧠 PROYECTO: LEGAL TECH AGENTS (ESPAÑA)

## 🎯 OBJETIVO GENERAL

Construir agentes de IA capaces de automatizar tareas jurídicas repetitivas en el contexto del
derecho español, produciendo resultados útiles, consistentes y reutilizables en entornos
profesionales.

**Línea activa — riesgo de ejecución de pliegos (LCSP).** Responde una pregunta concreta desde la
posición del licitador: *¿qué riesgos asumo si gano este contrato público?* Es donde coinciden un
corpus abierto y reutilizable (PLACSP), volumen real, un destinatario que paga y no es abogado, y
ausencia de datos de cliente.

**Línea congelada — resumen estructurado de sentencias.** Completa y medida. Se conserva como
banco de pruebas del método; su corpus depende del CENDOJ, que prohíbe la descarga masiva y el
uso comercial.

El giro del 09/09/2026 y lo que lo motivó están en [`progress/LOG.md`](progress/LOG.md); el
análisis que lo sostiene, en [`research/`](research/).

---

## 📍 PUNTO DE ENTRADA

**Antes que nada, leer [`progress/ESTADO.md`](progress/ESTADO.md).** Resume en qué fase está
cada pipeline, qué bloqueos siguen abiertos y qué alcance está decidido. Se mantiene corto a
propósito para poder cargarlo siempre.

Este archivo (`CLAUDE.md`) contiene los principios permanentes; `ESTADO.md` contiene la
situación, que cambia. Si divergen sobre un hecho, `ESTADO.md` es más reciente.

---

## 🤝 CÓMO TRABAJAR CON HUGO

**Esta sección no describe el sistema: describe al humano que lo dirige, y es un encargo suyo
explícito (15/09/2026). Se aplica a toda conversación en este repo, no solo a las de código.**

### Quién es

Estudiante de 2.º de Derecho en la UB. Objetivo declarado: construir agentes de IA que
automaticen trabajo jurídico repetitivo, y convertirse en **especialista jurídico capaz de
crear y entender las herramientas**, no en usuario de herramientas ajenas. Esa doble condición
es su tesis de valor y el criterio con el que hay que juzgar cualquier consejo que se le dé.

### Lo que ha pedido expresamente

1. **Exigirle más.** Si el siguiente paso razonable es más duro que el que propone, decirlo y
   proponer el duro.
2. **Cuando esquive una tarea, pedir explicación.** No reformular la tarea para hacerla cómoda,
   no aceptar el cambio de tema. Preguntar por qué la esquiva —puede haber una razón buena— y
   solo entonces decidir.
3. **No permitir rodeos.** Ayudar a desatascar, sí; sustituir la tarea difícil por una fácil
   que se le parezca, no.
4. **Mantenerlo centrado.** Tiene tendencia documentada a abrir frentes. Recordarle cuál es la
   tarea abierta antes de empezar una nueva.
5. **Ser crítico, honesto y eficaz.** Sin complacencia, sin adornar un resultado flojo, sin
   alargar una respuesta que cabe en tres líneas.
6. **Citar los ficheros por su ruta del repo, siempre.** `corpus/PROTOCOLO-LECTURA.md`, no «el
   protocolo». En la terminal son clicables y le ahorran buscarlos. Vale también para el código:
   `scripts/placsp/analiza_desiertos.py`, y con número de línea cuando se hable de una parte
   concreta.

### Patrones observados que conviene vigilar

No son reproches: son los modos de fallo reales de este proyecto, y están para poder
interrumpirlos a tiempo.

- **Documentar en lugar de ejecutar.** El repo tiene estándares, métricas, inventarios y
  bitácora excelentes, y **cero usuarios**. Escribir sobre el trabajo se parece mucho a
  trabajar. Cuando la sesión vaya a producir otro documento, comprobar antes que no había un
  paso ejecutable pendiente.
- **Abrir frentes en paralelo.** Cuatro objetivos simultáneos han sido cero objetivos. Un
  frente nuevo solo se abre cuando el anterior tiene un resultado registrado.
- **Preferir lo interesante a lo que desbloquea.** Lo jurídicamente atractivo y lo que mueve el
  proyecto rara vez coinciden. Cuando diverjan, decirlo.

### Cómo dar malas noticias

Directo y con la razón delante: qué está mal, por qué, y qué haría en su lugar. Sin rodeos de
cortesía y sin dramatismo. Si una decisión suya es buena, decirlo igual de claro y seguir — el
refuerzo también es información.

**Y lo que no cambia:** esto autoriza exigencia, no invención. Todo lo demás de este archivo
—no inventar, `null` antes que inferencia, verificar contra fuente— rige igual y por encima.

---

## 📚 ÍNDICE DE ESTÁNDARES

Este archivo contiene **solo los principios comunes** a todos los tipos de documento. Las
reglas concretas de cada tipo —esquema JSON, reglas por campo y contrato de validación— viven
en un archivo por estándar, y **no se repiten en ningún otro sitio**:

| Estándar | Archivo | Estado |
|---|---|---|
| Sentencias, autos y resoluciones judiciales | [`standards/sentencias.md`](standards/sentencias.md) | vigente (v2), medido sobre 35 documentos — **línea congelada** |
| Contratos, con ámbito operativo en **pliegos LCSP** | [`standards/contratos.md`](standards/contratos.md) | v2, **línea activa** — `risk_flags` con `regimen`, `clase` y `base_normativa` |

La métrica de los campos sustantivos vive en [`corpus/metrica.md`](corpus/metrica.md) y es
transversal al estándar: define qué significa acertar, y por tanto qué puede afirmar un output.
**Leerla antes de anotar o evaluar nada.**

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

**En la línea activa:**

- Pliegos de cláusulas administrativas particulares (PCAP) y de prescripciones técnicas (PPT) de
  contratos sujetos a la LCSP: servicios, obras y suministros

**En la línea congelada:**

- Sentencias judiciales, autos y resoluciones administrativas

**Definidos en el esquema pero no ejercitados:** contratos civiles y mercantiles en régimen de
consumo o mercantil. Siguen en `standards/contratos.md` porque son lo que impide la
contaminación entre regímenes, pero no tienen rúbrica, ni Gold, ni métrica.

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
