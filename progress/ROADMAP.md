# 🧭 Roadmap del Proyecto

## 🎯 Objetivo principal
Sistema de agentes legales autónomos que:
- Analicen documentos jurídicos
- Se automejoren
- Generen outputs estructurados
- Reduzcan tiempo dedicado a tareas repetitivas

---

## 📦 Fase 1 — Sentencia Analyzer
- [x] Lectura de inputs
- [x] Generación de resumen
- [x] Output JSON
- [x] Validación automática (`validate_v2.ps1`)
- [x] Métricas de calidad (`eval_gold.ps1`, Gold de 35 documentos, 9 campos de cabecera)
- [ ] Evaluación de **contenido**: `facts`, `applied_rules`, `ratio_summary` y `holding` solo
      tienen control de forma. Un output puede pasar las dos comprobaciones y contener un
      razonamiento equivocado
- [ ] Corpus nuevo con el que volver a medir

> ⚠️ **El conjunto de test está gastado.** Los 13 documentos de `sentencia23`–`sentencia35` se
> evaluaron el 05/08/2026 y dieron **313/315 (99,4 %)**, la única medición ciega que existe.
> Después se corrigieron dos reglas del estándar —acentos en `ponente`, prefijo en `ecli`—
> **mirando esos fallos**, y se reprocesaron los dos documentos afectados hasta 315/315. Ese
> 100 % confirma que las reglas funcionan; no mide generalización.
>
> A partir de aquí, dev y test miden lo mismo: rendimiento sobre documentos que el estándar ya
> ha visto. **Cualquier medición honesta de generalización exige un corpus nuevo**, y conviene
> reservarlo sin mirarlo antes de la siguiente ronda de ajustes.

---

## 📦 Fase 2 — Contract Analyzer (ACTUAL)

En este orden. La métrica va primero **a propósito**: en la fase 1 el esquema se diseñó antes
de saber cómo se iba a medir, y el resultado es que los campos sustantivos —los que aportan el
valor real— se quedaron sin evaluación de contenido. En contratos, casi todo el esquema es
sustantivo, así que ese error saldría mucho más caro.

- [ ] **1. Decidir la métrica de evaluación para campos sustantivos.** Qué significa que un
      riesgo esté bien detectado, que falte una cláusula o que un resumen sea correcto. La
      comparación exacta que da el 100 % en `ecli` o `decision_date` no sirve para
      `risk_flags`, `key_clauses` ni `missing_clauses`. Opciones a valorar: solapamiento sobre
      conjuntos anotados (precisión/exhaustividad por cláusula), rúbrica con revisión humana
      muestreada, o juicio por modelo con criterios fijos. **Sin esto, los pasos 2 y 4 se
      diseñan a ciegas**
- [ ] **2. Esquema.** `standards/contratos.md` existe con un borrador de 8 campos escrito sin
      un solo contrato delante. Revisarlo contra documentos reales y contra la métrica del
      paso 1: reglas por campo, contrato de validación y un `validate_contratos.ps1`
      equivalente al de sentencias
- [ ] **3. `contrato_agent`.** Definición del agente, remitiendo a `standards/contratos.md` sin
      duplicar reglas, como hace `sentencia_agent`
- [ ] **4. Gold.** Ficheros de referencia anotados a mano. Contrastar cada valor con el
      documento antes de darlo por bueno: en el Gold de sentencias, 6 de las 8 discrepancias
      de la primera evaluación del test eran errores del Gold, no del agente
- [ ] **5. Evaluación.** Primera medición con la métrica del paso 1

**Prerrequisito transversal: el corpus.** Los pasos 2, 4 y 5 necesitan contratos reales
anonimizados, con variedad de tipo (arrendamiento, compraventa, prestación de servicios, NDA).
Separar dev y test **desde el principio** y no mirar test hasta el final — la fase 1 terminó
sin conjunto ciego y esa lección conviene no repetirla.

### Composición de `Inputs/contratos/` (13 documentos, medido el 06/08/2026)

| # | Tipo contractual | Categoría | Datos |
|---|---|---|---|
| 1 | Servicio de agregación de posiciones (CaixaBank–CWML) | Adhesión | Solo predisponente (CIF A08663619); cliente sin rellenar |
| 2 | Representante de comercio (laboral especial, RD 1438/1985) | **Mixto** ⁽¹⁾ | Empresa con placeholders `[EMPRESA]`/`[NIF]`, trabajador con datos reales |
| 3 | Contrato multicanal de banca a distancia (BBVA) | Adhesión | Solo predisponente (A-48265169); cabecera en blanco (`En , a de de`) |
| 4 | Servicio de alarma y seguridad (Movistar Prosegur) | Adhesión | Solo predisponente (A-82018474, B87222006) |
| 5 | Servicio de telecomunicaciones (Orange Espagne) | Adhesión | Solo predisponente (A82009812) |
| 6 | Contrato marco RTO de renta fija, clientes profesionales (CaixaBank) | Adhesión | Solo predisponente (A08663619) |
| 7 | Póliza de seguro de automóviles (MAPFRE) | Adhesión | Solo condiciones generales; sin condiciones particulares |
| 8 | Contrato general de seguridad + orden de domiciliación (Movistar Prosegur) | Adhesión | Solo predisponente (A-82018474, B87222006) |
| 9 | Suministro de energía eléctrica (Endesa Energía) | Adhesión | Solo predisponente (A81948077, B09732520) |
| 10 | Convenio administrativo de subvención (Mº Transportes–Generalitat) | **No es contrato** | **Datos reales completos** (partes, cargos, fecha) |
| 11 | Arrendamiento de vivienda | Negociado (plantilla) | Placeholders `[lugar]`, `[Nombre del propietario]`… (62) |
| 15 | Constitución de sociedad civil | Negociado (plantilla) | Placeholders `.........` |
| 17 | Prestación de servicios (Colegio de Graduados Sociales) | Negociado (plantilla) | Campos en blanco; modelo `de 200_` |

⁽¹⁾ **`contrato2` no admite la clasificación binaria y se queda en categoría propia.** Tiene
forma negociada —comparecientes identificados, REUNIDOS, ESTIPULACIONES en ordinales, dos
ejemplares firmados— sobre un clausulado íntegramente predispuesto por la empresa que el
trabajador no negoció. En el eje de los datos también está partido: una parte anonimizada con
placeholders y la otra con datos reales. Forzarlo a "adhesión" o a "negociado" perdería
justamente lo que lo hace interesante como caso de prueba.

**Resumen:** 9 de adhesión con datos reales solo del predisponente · 3 plantillas negociadas
sin ningún dato · 1 mixto (nº 2) · 1 que no es contrato (nº 10). **Cero contratos negociados
con datos reales de ambas partes.**

**Depuración aplicada el 06/08/2026:** eliminado el antiguo nº 16 (sociedad de capital e
industria) por ser de **derecho argentino** —Ley 19.550, importes en pesos—, fuera del alcance
del proyecto. De los cuatro arrendamientos de vivienda casi intercambiables (11–14) se
conserva solo el **nº 11**, el de mayor cobertura de cláusulas (408 líneas) y con placeholders
nombrados —`[Nombre del propietario]`— que identifican qué campo va en cada hueco, frente a
los guiones bajos anónimos de los otros. Los nº 12, 13 y 14 quedan en `Inputs/apartados/`:
redundancia no es cobertura. La numeración conserva los huecos a propósito, para que las
referencias anteriores del LOG sigan resolviendo.

> ⚠️ **El corpus actual no permite evaluar `risk_flags` ni extracción de datos concretos.**
> Falta material negociado con datos reales antes de construir el Gold.

**Dónde queda material aprovechable.** `Inputs/descartados-contratos/` son 13 documentos que
no son contratos —9 sentencias, 1 comentario doctrinal, 3 pliegos de contratación pública—,
pero **6 de ellos sí transcriben cláusulas con datos concretos** y son la fuente más cercana
a lo que falta: los 3 pliegos (nº 1, 11 y 14) traen importes, plazos y penalidades reales de
un órgano de contratación real, y 3 sentencias de condiciones generales (nº 2, 3 y 12)
transcriben literalmente cláusulas de préstamo y de tarjeta revolving con sus cifras. Ninguno
sirve tal cual como contrato, pero sí como cantera de cláusulas anotables.

---

## 📦 Fase 3 — Agente Universidad
- [ ] Resúmenes de apuntes
- [ ] Generador de esquemas
- [ ] Planificador de estudio
- [ ] Q&A automático

---

## 📦 Fase 4 — Legal Intelligence Agent
- [ ] Noticias jurídicas
- [ ] Legal tech
- [ ] Tendencias
- [ ] Alertas personalizadas

---

## 📦 Fase 5 — Sistema de Automejora
- [ ] Feedback loop
- [ ] Evaluación outputs
- [ ] Ajuste automático de prompts