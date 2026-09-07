# 📋 Metodología: Redacción de la Rúbrica de `risk_flags`

**Versión: 07/09/2026 | Responsabilidad: Anotador manual**

---

## 🎯 Objetivo

Redactar `corpus/rubrica-riskflags.md`: documento que define cada posible `risk_flag.id` con:
- Definición clara y jurídicamente ancla
- Régimen aplicable
- Criterio sustantivo (`desequilibrio`, `falta_reciprocidad`, etc.)
- `severity_driver` típico
- Consecuencia jurídica
- Ejemplos de cláusulas reales del corpus

**Por qué:** El esquema v3 exige que `risk_flags[].id` exista en la rúbrica. Sin ella, el estándar no es aplicable y no se puede anotar ni un documento.

---

## 📚 Fuente de Verdad

Las 9 resoluciones de la vía C en `Inputs/corpus/via-c/`:

| Archivo | Tipo | Descripción |
|---------|------|-------------|
| `resolucion-01.txt` | Auto judicial | AJPI 1/2025 Cartagena. 28 menciones a abusividad |
| `resolucion-02.txt` | STS Casación | STS 3413/2026. 29 menciones a transparencia |
| `resolucion-03.txt` | STS Casación | STS 3399/2026. Marginal: solo 2 menciones a abusividad |
| `resolucion-04.txt` | STS Casación | STS 3171/2026 |
| `resolucion-05.txt` | Casación TS | Casacion 2697/2014 TS. El más rico: 44 abusividad / 22 cond.grales / 49 transparencia |
| `resolucion-06.txt` | AP Apelación | AP Barcelona seccion 15 |
| `resolucion-07.txt` | SAP Apelación | SAP B 4988/2026 |
| `resolucion-08.txt` | SAP Apelación | SAP B 4973/2026 |
| `resolucion-09.txt` | SJM Ordinario | SJM C 3188/2018 Mercantil A Coruna |

**Todas tratan de abusividad o condiciones generales, pero algunas pueden juzgar a un adherente empresario (Ley 7/1998, solo control de incorporación y transparencia).**

---

## 🔍 PASO 1: Verificar `condicion_adherente` de cada resolución

**Esta es la tarea crítica que debe hacerse antes de extraer risk_flags.**

Para cada una de las 9 resoluciones, lee el documento y decide:

- **`consumidor`**: La resolución trata de un consumidor (definición TRLGDCU: persona física que actúa con propósito ajeno a su actividad profesional o comercial).
- **`empresario`**: La resolución trata de un adherente empresario bajo Ley 7/1998 (persona física o jurídica que actúa en el ejercicio de actividad profesional, comercial o industrial).

**Cómo identificarlo:**
- Busca en el encabezado del documento: "Se demanda a...", "Demandado...", tipo de personas
- Busca en los hechos: ¿qué tipo de sujeto es el adherente?
- Busca en el razonamiento: menciones explícitas a consumidor/empresario/profesional

**Registro:**
- Anota en la fila correspondiente de `plantilla-rubrica.csv`, columna `condicion_adherente_verificada`
- Si no se puede determinar claramente → `indeterminado` (no dejar en blanco)

---

## 🚩 PASO 2: Extraer `risk_flags` de cada resolución

Para cada resolución, busca **cláusulas o prácticas criticadas por el juez** que encajen en los criterios permitidos:

| Criterio | Definición | Ejemplos de doctrinal |
|---|---|---|
| `desequilibrio` | Diferencia notable y no justificada entre derechos y obligaciones de las partes | Cláusula que exonera a predisponente pero no a adherente; límite de responsabilidad asimétrico |
| `falta_reciprocidad` | Obligación que recae en una sola parte cuando ambas están vinculadas al contrato | Penalidad solo para adherente; derecho de resolución unilateral del predisponente |
| `falta_transparencia` | Cláusula redactada de forma que dificulta su comprensión por el adherente | Remisión circular; términos técnicos sin explicación; ubicación oculta en el documento |
| `desproporcion_penalizacion` | Penalidad contractual manifiestamente desproporcionada respecto del daño que dice compensar | Multa por demora 10× el precio diario; penalidad fija muy superior al perjuicio típico |
| `facultad_unilateral` | Derecho del predisponente a modificar términos clave sin consentimiento del adherente | Derecho a cambiar precio; rescisión discrecional; cambio de objeto del contrato |

**No todos los criterios aparecerán en todas las resoluciones.** Algunos pueden no encontrarse en el corpus.

---

## 📝 PASO 3: Estructura de cada risk_flag

Para cada cláusula o práctica que extraigas, rellena estos campos:

### Campos obligatorios:

1. **`id`** (identifier único)
   - Formato: `snake_case`, descriptivo
   - Ejemplos: `penalidad_asimetrica`, `cambio_precio_unilateral`, `exoneracion_predisponente`
   - Debe ser **único** en la rúbrica

2. **`criterio`** (enum cerrado)
   - Uno de: `desequilibrio`, `falta_reciprocidad`, `falta_transparencia`, `desproporcion_penalizacion`, `facultad_unilateral`
   - Solo **uno** por risk_flag

3. **`regimen`** (enum cerrado)
   - Uno de: `administrativo`, `condiciones_generales`
   - Todas en esta rúbrica serán `condiciones_generales` (porque provienen de resoluciones sobre vía C)

4. **`condicion_adherente_aplicable`** (enum cerrado)
   - `consumidor` | `empresario` | `ambos`
   - ¿A cuál tipo de adherente le aplica este riesgo?
   - Si solo aparece juzgado en el corpus en sentencias contra consumidores → `consumidor`
   - Si aparece en sentencias contra empresarios → `empresario`
   - Si aparece en ambos tipos → `ambos`

5. **`severity_driver_tipico`** (enum cerrado)
   - El más común en el corpus para este riesgo
   - Uno de: `perdida_prestacion`, `restriccion_defensa`, `coste_economico`, `sin_efecto_economico`

6. **`definicion`** (texto libre, 1-2 párrafos)
   - Qué es este riesgo, por qué importa, cuándo se activa
   - Escribir como abogado escribiría una cláusula de cuidado: clara, específica, basada en jurisprudencia

7. **`consecuencia_juridica`** (texto libre)
   - ¿Qué ocurre si este riesgo se materializa?
   - Régimen consumo: nulidad (art. 82 TRLGDCU), etc.
   - Régimen empresario: control de incorporación y transparencia (Ley 7/1998)
   - NO deducir; tomar de las sentencias

8. **`cita_doctrinal`** (referencia a resoluciones)
   - STS, AP, etc.
   - Ejemplo: "STS 3413/2026, FJ 3" o "Casacion 2697/2014, FJ 15"
   - Una o dos referencias máximo

9. **`ejemplo_clausula_reales`** (texto literal del corpus)
   - Copia literal de una o dos cláusulas reales del corpus que encajen en este riesgo
   - No inventar ni parafrasear
   - Formato: `«clausula literal» (Fuente: adhesion-02.txt, línea 45)` o similar

---

## 📋 PASO 4: Trabajar con el template CSV

Usa el archivo `corpus/plantilla-rubrica.csv` con estas columnas:

```
id | criterio | regimen | condicion_adherente_aplicable | severity_driver_tipico | definicion | consecuencia_juridica | cita_doctrinal | ejemplo_clausula_reales
```

**Cómo hacerlo óptimamente:**

1. **Abre el CSV en Excel o LibreOffice Calc**, no en un editor de texto
   - Facilita llenar campos largos sin romper comillas
   - Puedes filtrar y ordenar mientras trabajas

2. **Rellena fila por fila**, una resolución a la vez
   - Lee resolución 1 → extrae todos sus risk_flags → pasa a resolución 2
   - Es más eficiente que ir saltando

3. **Mantén el corpus abierto en otra ventana**
   - Consulta permanentemente: el ejemplo de cláusula debe ser literal
   - Verifica la línea exacta para referenciarla

4. **Al terminar la primera resolución, tómate una pausa corta**
   - Estos documentos son densos
   - Descansa 10 min antes de pasar a la siguiente
   - Evita burnout de lectura jurídica

5. **No intentes "completar" risk_flags que no estén en el corpus**
   - Si una cláusula de penalidad no aparece en ninguna resolución, no la crees
   - El criterio es: **lo que el corpus tiene, eso medimos**

6. **Cuando dudes si un risk_flag ya existe bajo otro ID**
   - Busca en las filas anteriores
   - Si es la misma práctica juzgada por dos sentecias → mismo `id`
   - Si es variante distinta → `id` nuevo

---

## 📊 PASO 5: Validación antes de finalizar

Antes de dar por terminada la rúbrica, revisa:

- [ ] **9 resoluciones procesadas** (columna `resolucion_origen` tiene 9 valores únicos)
- [ ] **IDs únicos** (no hay dos filas con el mismo `id`)
- [ ] **Criterios válidos** (todos en el enum permitido)
- [ ] **Ejemplos literales** (copias directas del corpus, no paráfrasis)
- [ ] **Citas doctrinales** (referencias reales, no inventadas)
- [ ] **Coherencia régimen/condición**: Si `condicion_adherente_aplicable` = consumidor, ¿tiene sentido jurídico en consumo?

---

## ⏱️ Estimación de tiempo

- **Lectura inicial de 9 resoluciones**: 3-5 horas (depende de densidad)
- **Extracción de risk_flags en CSV**: 2-4 horas
- **Revisión y validación**: 1-2 horas
- **Total estimado**: 6-11 horas de trabajo concentrado

**Recomendación:** Hazlo en sesiones de máximo 2 horas para mantener la precisión.

---

## 🚨 Riesgos comunes

| Riesgo | Cómo evitarlo |
|--------|---|
| Confundir "criterio" con "consecuencia" | Lee las definiciones 3 veces. Criterio = qué está mal. Consecuencia = qué ocurre |
| Crear risk_flags "genéricos" que no están en el corpus | Anchura: cada fila debe referir a una cláusula real o práctica real. Si no, no va |
| Perder la "voz" jurídica | Escribe como si redactaras la sección de "Riesgos" de un informe de M&A. Formal, específico, defensible |
| Mezclar consumidor y empresario | Verifica en cada resolución: ¿a quién juzga? Registra en `condicion_adherente_verificada`. Luego transfiere a `condicion_adherente_aplicable` |
| Duplicar ejemplos de cláusula | Usa cláusulas distintas para risk_flags distintos cuando sea posible. Si la misma cláusula encaja en dos riesgos, vale; pero evita repetirla |

---

## 📌 Archivo de salida esperado

Cuando termines, tendrás:

**`corpus/rubrica-riskflags.md`** (Markdown)
- Versión legible y citable de la rúbrica
- Se genera a partir del CSV
- Formato: tabla + descripción de cada risk_flag

**`corpus/plantilla-rubrica.csv`** (CSV relleno)
- Datos estructurados
- Validable por máquina
- Se importa en el agente

---

## 🔗 Enlaces de referencia

- Estándar de contratos: `standards/contratos.md` (campos de risk_flags)
- Métricas: `corpus/metrica-contratos.md` (cómo se medirán)
- Inventario: `corpus/inventario-contratos.csv` (referencias a resoluciones)
- Alcance: `corpus/alcance.md` (criterios de inclusión/exclusión)

---

## ✅ Checklist final antes de entregar

- [ ] He leído las 9 resoluciones completamente
- [ ] He verificado `condicion_adherente` de cada una (consumidor o empresario)
- [ ] He extractado todos los risk_flags que encuentro, sin añadir inventados
- [ ] Cada fila del CSV tiene ejemplo literal de cláusula del corpus
- [ ] He validado que no hay IDs duplicados
- [ ] He revisado coherencia: criterio-consecuencia-severidad
- [ ] He comprobado que todas las citas doctrinales existen en las resoluciones

**Cuando todo esté ✓, avísame y convertiré el CSV a Markdown + cargaré en el repositorio.**
