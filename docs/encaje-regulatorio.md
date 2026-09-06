# ⚖️ Encaje regulatorio del proyecto

**Fijado: 06/09/2026.** Posición del proyecto frente a la normativa vigente sobre uso de IA en
el ámbito jurídico español.

---

## Qué es este documento y qué no

**Es** la posición razonada del proyecto: dónde encaja lo que hace, qué fronteras no cruza, y
qué obligaciones le afectarían si dejara de ser académico. Existe para que esas decisiones estén
escritas antes de que haga falta invocarlas, y no reconstruidas después.

**No es** asesoramiento jurídico, ni una evaluación de conformidad, ni una afirmación de que el
proyecto cumple nada. `CLAUDE.md` prohíbe al sistema emitir conclusiones jurídicas definitivas y
esa prohibición vale también para este archivo: lo que aquí hay son lecturas de normas, con su
grado de certeza declarado y sus preguntas abiertas señaladas como tales.

**Calidad de las fuentes**, porque no todas son iguales:

| Norma | Fuente usada | Fiabilidad |
|---|---|---|
| Instrucción 2/2026 CGPJ | Texto publicado en el BOE (`BOE-A-2026-2205`) | Alta — fuente oficial |
| Circular 3/2026 CGAE | Prensa jurídica especializada y comentarios doctrinales | **Media — no se ha leído el texto íntegro.** Verificar antes de apoyarse en ella |
| Reglamento (UE) 2024/1689 | Conocimiento general del texto y fuentes secundarias | Media — el Anexo III **no** se ha verificado literalmente |

---

## 1. Instrucción 2/2026 del CGPJ

Aprobada por el Pleno del CGPJ el 28 de enero de 2026 y publicada en el BOE el 30 de enero.
Regula el uso de sistemas de IA **por jueces y magistrados en el ejercicio de la actividad
jurisdiccional**.

### Qué permite y qué prohíbe

| Usos permitidos | Prohibiciones expresas |
|---|---|
| Búsqueda y localización de información jurídica, incluida la identificación de normativa y jurisprudencia | Automatizar decisiones judiciales |
| Análisis y clasificación de documentos procesales | Condicionar la independencia judicial |
| **Elaboración de esquemas o resúmenes internos** | Incorporar contenido sin validación crítica personal |
| Tareas organizativas auxiliares | Usar datos personales especialmente protegidos sin autorización |
| | **Perfilado, predicción de comportamientos o clasificación de sujetos** |
| | Utilizar sistemas no facilitados por las administraciones competentes |

Los borradores de resolución exigen validación personal, completa y crítica del magistrado.

### Dónde encaja este proyecto

**Primero, una precisión que evita una confusión fácil: esta Instrucción no se dirige a este
proyecto.** Su destinatario es el juez o magistrado en el ejercicio de la función
jurisdiccional. Un estudiante o un abogado que analiza documentos no está sujeto a ella.

Dicho eso, **sirve como el mejor mapa disponible de qué usos de la IA se consideran aceptables
sobre material judicial en España**, y por eso conviene contrastar el pipeline contra ella:

| Lo que hace el pipeline de sentencias | Encaje |
|---|---|
| Localizar identificadores, órgano, fecha y ponente en la cabecera | Localización de información jurídica |
| Clasificar el tipo de resolución | Análisis y clasificación de documentos |
| Producir `facts`, `ratio_summary`, `holding` estructurados | **Elaboración de esquemas o resúmenes** |
| Registrar `uncertainties` y `document_quality_notes` en vez de resolverlas | Coherente con la validación crítica: el sistema señala, no decide |

**Y no hace nada de lo prohibido.** No hay perfilado, no hay predicción de comportamiento, no hay
clasificación de sujetos, no se automatiza ninguna decisión.

### La frontera que el proyecto no va a cruzar

**Predicción de resultado judicial.** Es comercialmente atractiva y aparece en varias hojas de
ruta del sector, pero:

1. En el ámbito jurisdiccional está **expresamente prohibida** por esta Instrucción —perfilado y
   predicción de comportamientos—, lo que marca con claridad la posición del regulador español.
2. Exigiría exactamente el tipo de evaluación de contenido que este proyecto todavía no tiene: un
   sistema que predice sin estar medido es un generador de opiniones con apariencia de dato.

**Decisión: fuera de alcance, y no por falta de medios.** Si en el futuro se reconsidera, esta
entrada tiene que reabrirse explícitamente, no ignorarse.

---

## 2. Circular 3/2026 del CGAE

Aprobada por el Consejo General de la Abogacía Española el 10 de abril de 2026, al amparo del
art. 23 de la LO 5/2024 del Derecho de Defensa. Es la norma **directamente aplicable** al uso
profesional que este proyecto persigue.

> ⚠️ **No se ha leído el texto íntegro de la Circular**, solo comentarios y prensa
> especializada. Lo que sigue es una lectura de segunda mano y hay que verificarla contra el
> texto antes de apoyar ninguna decisión seria en ella.

### Lo esencial

**No prohíbe la IA generativa.** La concibe como herramienta auxiliar sujeta a supervisión
humana. Su aportación es elevar el **deber de verificación y control** a categoría dogmática,
anclándolo en la doctrina de la *actio libera in causa*: el abogado que delega en un sistema sin
verificar responde de lo que el sistema produce, porque la decisión de delegar fue suya. No cabe
alegar la opacidad de la herramienta como excusa.

### El punto con consecuencias técnicas

Usar **versiones de consumo** de modelos fundacionales, cuyos términos generales prevén la
reutilización de las entradas para entrenamiento, vulnera:

- el principio de **limitación de la finalidad**, art. 5.1.b RGPD; y
- el **deber de secreto profesional**, art. 542.3 LOPJ.

Requisitos exigibles a la herramienta, para uso profesional:

1. Garantía contractual explícita de **no entrenamiento sobre las entradas**.
2. **Residencia del dato en la UE**.
3. **Cifrado** adecuado.
4. **Contrato de encargo del tratamiento**, art. 28 RGPD.

### Qué significa esto para este repositorio, hoy

**Mientras el proyecto sea académico y el corpus venga de fuentes públicas, el riesgo es bajo.**
Las sentencias son del CENDOJ y los pliegos son de PLACSP: información pública, publicada por
quien tiene el deber de publicarla, y ya anonimizada en origen en el caso del CENDOJ.

**Pero `Inputs/` contiene datos personales reales** —nombres de cliente, protocolo notarial,
NIF—, según consta en `ROADMAP.md`. Sobre eso:

> **El `.gitignore` es necesario y no es suficiente.** Protege el histórico de git de contener
> datos personales, que es un problema real y está bien resuelto. Pero **no regula qué se envía
> al modelo**, que es exactamente lo que mira la Circular. Son dos riesgos distintos y solo uno
> está cubierto.

**Tres medidas, por orden de coste:**

1. **Priorizar fuentes públicas** en el corpus. Coste cero, y es lo que ya se decidió por otras
   razones: las vías A y C son PLACSP y CENDOJ.
2. **Anonimizar antes de procesar.** Es el patrón de Legalfly —un modelo local que sustituye los
   identificadores antes de que el documento llegue al LLM—. Para este proyecto bastaría una
   versión mucho más simple aplicada a los documentos con datos reales.
3. **Verificar las condiciones contractuales** de la herramienta concreta que se use, contra los
   cuatro requisitos de arriba, antes de procesar cualquier documento de un cliente real.

**La 3 es la que hay que hacer antes de que entre el primer documento de cliente**, y no
después.

---

## 3. Reglamento (UE) 2024/1689 de Inteligencia Artificial

Los sistemas de IA destinados a ser utilizados **por la Administración de Justicia** para
interpretar hechos o aplicar el Derecho son de **alto riesgo** (Anexo III), con obligaciones de
documentación técnica, marcado CE, registro en base de datos europea, evaluación de impacto en
derechos fundamentales (FRIA, art. 27) y supervisión humana efectiva. Desde agosto de 2026 el
incumplimiento puede alcanzar los 35 M€ o el 7 % de la facturación mundial. El CGPJ actúa como
autoridad de vigilancia del mercado para estos sistemas.

### ⚠️ Pregunta abierta, y es la que más consecuencias tiene

**¿Alcanza el Anexo III a una herramienta que usa un abogado sobre sus propios documentos?**

La lectura razonable es que **no**: el supuesto se refiere a sistemas destinados a ser utilizados
*por una autoridad judicial o en su nombre*, y una herramienta de análisis documental en manos de
un profesional privado no encaja ahí por esa vía.

**Esa lectura NO está verificada contra el texto del Anexo III y no debe darse por buena.**

Importa mucho porque decide si aplican o no el marcado CE y la FRIA, que es la diferencia entre
un proyecto viable para una persona sola y uno que no lo es.

**Qué hay que hacer para cerrarla**, por orden:

1. Leer el literal del Anexo III, punto relativo a administración de justicia y procesos
   democráticos, y anotar aquí su redacción exacta.
2. Comprobar si el uso previsto encaja además en algún otro punto del Anexo III.
3. Revisar el art. 6 y sus excepciones, que modulan cuándo un sistema del Anexo III se considera
   efectivamente de alto riesgo.
4. Determinar el **rol**: quien desarrolla un sistema para uso propio no está en la misma
   posición que un proveedor que lo comercializa. Si el proyecto llegara a distribuirse, cambia.

**Hasta que estén los cuatro puntos, la posición del proyecto es: pregunta abierta, y no se
afirma cumplimiento de nada.**

---

## 4. Resumen operativo

Lo que se sigue de todo lo anterior, en cinco líneas:

1. **El pipeline de sentencias hace lo permitido y nada de lo prohibido** por la Instrucción
   2/2026, que no le es aplicable pero es el mejor mapa disponible.
2. **La predicción de resultado judicial queda fuera de alcance**, por decisión y no por
   omisión.
3. **El deber de verificación es del profesional, no de la herramienta.** El diseño lo acompaña:
   el estándar prefiere `null` a la inferencia, exige cita verbatim para cada riesgo y obliga a
   registrar la duda en vez de resolverla.
4. **Con corpus público el riesgo es bajo; con documentos de cliente cambia todo**, y las
   condiciones contractuales de la herramienta hay que verificarlas antes, no después.
5. **El alcance del Reglamento de IA sobre este proyecto está sin resolver**, con cuatro pasos
   concretos escritos para resolverlo.

---

## 5. Pendiente

- [ ] Leer el texto íntegro de la Circular 3/2026 y corregir aquí lo que haga falta.
- [ ] Verificar el literal del Anexo III del Reglamento (UE) 2024/1689, con los cuatro pasos de
      la sección 3.
- [ ] Comprobar las condiciones contractuales de la herramienta usada contra los cuatro
      requisitos del CGAE. **Antes de procesar el primer documento de un cliente real.**
- [ ] Decidir si se implementa anonimización previa, y con qué alcance.
