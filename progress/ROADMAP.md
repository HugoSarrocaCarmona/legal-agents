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

En este orden. Cada paso depende del anterior: el estándar se escribe mirando documentos
reales, no al revés, y el Gold no se puede anotar sin un esquema estable.

- [ ] **1. Corpus de contratos.** Reunir contratos civiles y mercantiles reales, anonimizados,
      con variedad de tipo (arrendamiento, compraventa, prestación de servicios, NDA). Separar
      dev y test **desde el principio**, y no tocar test
- [ ] **2. Esquema y estándar.** `standards/contratos.md` existe con un esquema borrador de 8
      campos, escrito sin un solo contrato delante. Revisarlo contra el corpus: reglas por
      campo, contrato de validación y un `validate_contratos.ps1` equivalente al de sentencias
- [ ] **3. `contrato_agent`.** Definición del agente, remitiendo a `standards/contratos.md` sin
      duplicar reglas, como hace `sentencia_agent`
- [ ] **4. Gold.** Ficheros de referencia anotados a mano sobre el conjunto dev. Contrastar
      cada valor con el documento antes de darlo por bueno: en el Gold de sentencias, 6 de las
      8 discrepancias de la primera evaluación eran errores del Gold, no del agente
- [ ] **5. Evaluación.** `eval_gold` adaptado a los campos de contratos y primera medición

Lo que ya se sabe de la fase 1 y aplica aquí: identificación de cláusulas, extracción de
riesgos, resumen estructurado y clasificación jurídica son campos **sustantivos**, no de
cabecera. La evaluación por comparación exacta que funciona con `ecli` o `decision_date` no
sirve para `risk_flags` ni para `missing_clauses`, así que el paso 5 exige decidir antes qué
significa que un riesgo esté bien detectado.

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