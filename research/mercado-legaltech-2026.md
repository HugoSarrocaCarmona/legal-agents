# 🔍 Investigación de mercado: automatización legal 2026

**Fecha de la investigación:** 03/09/2026
**Encargo:** mapear las empresas pioneras en automatización jurídica a nivel mundial y en España,
entender cómo funcionan por dentro, y extraer lo aprovechable para este proyecto.
**Estado:** documento de investigación. No modifica ningún estándar ni el `ROADMAP.md`; las
propuestas de la sección 10 son eso, propuestas, y no se han aplicado.

---

## 0. Cómo leer esto y qué fiabilidad tiene

Esta investigación se ha hecho con fuentes **secundarias y públicas**: webs de producto, prensa
especializada del sector (*Artificial Lawyer*, *Legal IT Insider*, *LawSites*, *Global Legal
Post*), notas de prensa corporativas, papers de arXiv y normativa oficial (BOE).

Tres advertencias que condicionan la lectura:

1. **Las webs de producto no son fuentes neutrales.** Cuando una empresa dice que su arquitectura
   "elimina las alucinaciones", eso es marketing hasta que un tercero lo mide. Se señala en cada
   caso quién afirma qué.
2. **Buena parte de los rankings de "mejores IA jurídicas de España" están publicados por las
   propias herramientas rankeadas.** El ranking de `prudencia.ai` sitúa a Prudencia.ai en el
   primer puesto; el listado de Lefebvre es de Lefebvre. Se usan como **inventario de actores**,
   nunca como evaluación comparativa.
3. **Las cifras de mercado agregadas son poco fiables.** Los datos de financiación global de
   legaltech en 2026 (~4.300 M$ en 356 operaciones) proceden de blogs de posicionamiento, no de
   una fuente primaria verificada. Se dan como orden de magnitud.

Lo único que aquí puede tratarse como **hecho firme** es: la normativa (BOE), los papers
académicos, y los hechos corporativos confirmados por varias cabeceras del sector.

---

## 1. Resumen ejecutivo

**El mercado se ha estructurado en tres capas** que compiten por moats distintos: los editores de
contenido jurídico (moat = el corpus), las plataformas horizontales de IA (moat = flujo de
trabajo y confianza empresarial) y las verticales de un solo caso de uso (moat = ejecutar un
proceso de punta a punta).

**La arquitectura agéntica se ha commoditizado en 2025-2026.** Harvey —la referencia del sector,
valorada en miles de millones— decidió explícitamente **no construir su propia librería de
agentes** y adoptar el SDK de OpenAI. Si el líder no considera que orquestar agentes sea su
ventaja competitiva, no lo es para nadie. Lo que sí sigue siendo diferencial es el corpus
evaluado, el conocimiento de dominio y la distribución.

**La evaluación es el verdadero campo de batalla técnico.** El estudio de Stanford RegLab (2024)
demostró que herramientas comerciales que se anunciaban como libres de alucinaciones fallaban
entre el 17 % y el 34 % de las veces. Desde entonces, los actores serios publican benchmarks
propios: Harvey tiene su *Legal Agent Benchmark* (1.200 tareas, 75.000 criterios de rúbrica),
Legora su *Benchmark for Agentic Reasoning*, y existe un evaluador independiente (Vals AI).

**España tiene un actor de talla mundial y un mercado dominado por editoriales.** vLex, fundada
en Barcelona en 2000, fue comprada por Clio por 1.000 M$ en 2025 — la mayor operación de la
historia del sector y uno de los pocos unicornios tecnológicos nacidos en España. Por debajo, el
mercado lo ocupan las IA de las editoriales jurídicas (Aranzadi, Lefebvre, Tirant, Sepín), cuyo
argumento no es la tecnología sino su fondo documental.

**Hay un hueco real y es exactamente donde está este proyecto.** No existe ningún benchmark
público de análisis contractual en derecho español. CUAD es de contratos M&A estadounidenses en
inglés; LegalBench es de derecho estadounidense; Multi-Legal-Bench cubre seis jurisdicciones
europeas civilistas —Ucrania, Francia, Países Bajos, Polonia, Chequia y Lituania— y **excluye
España expresamente**. Nadie ha publicado un corpus anotado y medido de contratos españoles.

---

## 2. Mapa del mercado: las tres capas

| Capa | Quién | Moat real | Vulnerabilidad |
|---|---|---|---|
| **Contenido** | Thomson Reuters (CoCounsel/Westlaw), LexisNexis (Protégé), vLex, Aranzadi, Lefebvre, Tirant, Sepín, C.H. Beck | El fondo documental propietario y las licencias | Su IA es tan buena como su contenido; tecnológicamente van a remolque |
| **Plataforma horizontal** | Harvey, Legora, Luminance, Legalfly, Noxtua, Vecflow | Integración empresarial, gobernanza, confianza del despacho grande | No poseen el contenido; dependen de licenciarlo o del corpus del cliente |
| **Vertical de un caso de uso** | Ivo, Spellbook, LegalOn, DraftWise, Definely (contratos); EvenUp, Eve, Supio, Alexi (litigación); Garfield (reclamaciones) | Hacer un proceso entero, mejor que nadie | Si el proceso se absorbe en una plataforma más grande, desaparecen |

**Las capas se están fusionando por compra**, no por desarrollo. Clio (gestión de despacho)
compró vLex (contenido + IA). Litera compró Kira. Docusign compró Lexion. Workday compró Evisort.
Thomson Reuters compró Casetext. Nadie construye la capa que le falta: la adquiere.

### El caso de fracaso que más enseña: Robin AI

Robin AI (Londres, 2019) era una de las referencias del análisis contractual con IA: 71,7 M$
levantados, Serie B de 26 M$ liderada por Temasek en 2024, arquitectura híbrida de LLMs de
Anthropic más modelos propios y un equipo interno de juristas revisando salidas
(*human-in-the-loop*). Modelo aparentemente sólido.

**A finales de 2025 colapsó.** Una ronda de 50 M$ se cayó, HMRC presentó una petición de
liquidación y la empresa entró en administración concursal. En diciembre de 2025, Scissero
compró su división de servicios gestionados (~75 personas). En enero de 2026, Microsoft
absorbió al equipo de ingeniería —incluidos su CTO y su directora de IA— para reforzar las
capacidades legales de Word.

**Tres lecciones.** Primera: el análisis contractual horizontal, sin contenido propio ni canal de
distribución, es un negocio frágil aunque tenga buena tecnología. Segunda: el destino del equipo
—el equipo de Word de Microsoft— señala dónde cree Microsoft que se juega la partida: en el
procesador de textos donde el abogado ya trabaja, no en una herramienta aparte. Tercera: el
modelo de "juristas internos revisando cada salida" es caro y no escala; es coste de servicios
disfrazado de margen de software.

---

## 3. Fichas de los actores globales

### 3.1 Harvey — la referencia, y la más documentada arquitectónicamente

**Qué resuelve:** asistente jurídico general para grandes despachos y departamentos legales, con
constructor de flujos de trabajo propio.

**Arquitectura (documentada con detalle poco habitual):**

- Adoptaron el **SDK de Agentes de OpenAI** en lugar de construir orquestación propia. Decisión
  deliberada: querían trabajar *con* las capacidades del modelo, no construir sistemas híbridos.
- Todo se organiza en **"Tool Bundles"**: paquetes de capacidades que agrupan varias herramientas
  más sus instrucciones asociadas. Ejemplos: un *bundle* de sistema de ficheros (búsqueda tipo
  `grep`, apertura de archivos, búsqueda semántica), un *bundle* de redacción (herramienta de
  edición más subagente de redacción), integración con LexisNexis.
- **Regla organizativa dura:** toda función nueva del Asistente debe implementarse como Tool
  Bundle, y toda interfaz de hilo de primer nivel debe ser un agente. Es una restricción
  impuesta a propósito, para forzar a los equipos a no salirse del patrón.
- Cada Tool Bundle tiene **control parcial del prompt de sistema**: los equipos de producto
  inyectan instrucciones de dominio sin aprobación central.
- **Puertas de validación *leave-one-out***: cada Tool Bundle mantiene su propio conjunto de
  datos y sus evaluadores, y todo cambio debe demostrar que no degrada las capacidades
  existentes.

**Su propia evaluación — el *Legal Agent Benchmark* (LAB):** más de 1.200 tareas en 24 áreas de
práctica, evaluadas contra más de 75.000 criterios de rúbrica escritos por expertos. Cada tarea
tiene cuatro componentes: instrucción breve (~50 palabras, formulada como encargo de socio a
asociado), entorno (un asunto con sus documentos, universo cerrado), salida (un producto de
trabajo revisable) y verificación (rúbricas de formato, hechos y análisis). **Las rúbricas se
descomponen en criterios atómicos binarios de aprobado/suspenso**, y la puntuación es de tipo
*all-pass*: detectar 8 de 10 riesgos puntúa cero.

**Hoja de ruta declarada:** agentes en segundo plano con tareas de larga duración ("configurar y
olvidar"), análisis profundo combinando web pública, documentos del despacho y bases de datos
jurídicas en un solo hilo de razonamiento, y orquestación de varios modelos fundacionales en
lugar de depender de un proveedor único. Su *Workflow Builder* se describe como "una plataforma
tipo Zapier"; se han construido en él unos 25.000 agentes personalizados.

**Punto débil declarado por ellos mismos:** la gestión de contexto es un problema abierto —a
medida que los Tool Bundles acumulan salidas más ricas, mantener el rendimiento dentro de los
límites de contexto "requiere atención continua"—, y no tienen resuelto cómo testear la
complejidad combinatoria de varios bundles interactuando. Su conclusión más citada: *"lo difícil
de adoptar agentes no es escribir el código: es aprender, como organización de ingeniería, a
compartir la propiedad de un único cerebro."*

### 3.2 Legora — el competidor europeo directo

**Qué resuelve:** plataforma jurídica agéntica; su producto insignia es **Tabular Review**, una
hoja de cálculo generada por IA sobre conjuntos grandes de documentos — una fila por documento,
una columna por pregunta, **y cada celda enlazada a su fuente**.

**Arquitectura:** lo llaman *agentic operating system* (aOS). Flujos multi-paso construidos en
lenguaje natural que combinan redacción, revisión tabular, investigación, traducción y consultas
a bases de datos.

**Su tesis para 2026:** el paso de chatbots asistivos a agentes que completan trabajo jurídico de
punta a punta. Sus salvaguardas declaradas: contexto completo del asunto como base de toda acción
del agente, puntos de revisión humana en decisiones críticas, **rastro de auditoría completo de
cada acción del agente**, y herramientas específicamente jurídicas (revisión tabular, integración
con el gestor documental, *redlining*). Su formulación es buena y vale la pena retenerla: *"un
modelo potente y una plataforma jurídica específica son dos cosas distintas."*

**Datos:** Serie D de 550 M$ en marzo de 2026. En junio de 2026 movieron su nivel Agent Pro a
precio por consumo — señal de que el trabajo agéntico de larga duración tiene un coste variable
que ya no cabe en una licencia por usuario.

### 3.3 Luminance — verificación en la capa del modelo

**Qué resuelve:** ciclo completo del contrato — generación, negociación y análisis posterior a la
firma.

**Arquitectura:** su **LPT** (*Legal Pre-Trained Transformer*) se entrena solo con documentos
jurídicos verificados; afirman exposición a más de 150 millones de documentos. Su mecanismo
distintivo es el **"Panel of Judges"**: combinan un conjunto diverso de modelos fundacionales,
propietarios y afinados, de modo que la verificación queda incorporada *en la capa del modelo* en
lugar de ser una comprobación posterior.

En enero de 2026 lanzaron su mayor actualización en una década, cuya novedad es la **memoria
institucional**: una arquitectura que retiene el historial de negociación y el razonamiento
jurídico a través de todo el histórico de contratos de la organización, combinando memoria a
corto plazo con conocimiento institucional a largo plazo. Toda salida lleva citas a nivel de
fuente que trazan directamente hasta la cláusula subyacente.

**Cautela:** "Panel of Judges" y "Legal-Grade AI" son marcas registradas y material de marketing.
La idea subyacente —verificación por consenso multi-modelo— es sólida y está bien documentada en
la literatura de ML; la afirmación de que resuelve "la mayor objeción a la IA en derecho" no está
verificada por terceros.

### 3.4 LegalOn — el enfoque más transferible a este proyecto

**Qué resuelve:** revisión contractual dentro de Word, para equipos jurídicos internos. Más de
7.000 clientes.

**Por qué importa aquí:** su método no es "encontrar riesgos" sino **comparar contra un
*playbook* redactado por abogados**. Ofrecen más de 50 playbooks preescritos, más la posibilidad
de crear los propios. En abril de 2026 lanzaron **International Playbooks**: estándares de
revisión para NDAs y contratos comerciales comunes en **23 países**, elaborados por su equipo
jurídico interno y revisados por abogados de cada jurisdicción.

Esto es la validación comercial más clara de una tesis central de este proyecto: **el estándar de
revisión es dependiente de la jurisdicción y hay que escribirlo antes de aplicarlo**. LegalOn
gasta dinero en abogados locales redactando criterios país por país porque no hay atajo.

Serie E de 50 M$ liderada por Goldman Sachs, con un despacho japonés (Mori Hamada & Matsumoto)
entre los inversores.

### 3.5 Ivo, Spellbook, DraftWise, Definely — las verticales de contratos

- **Ivo**: revisión, *redlining* y extracción para equipos internos; genera y exporta listas de
  incidencias, verifica documentos contra requisitos y contra playbooks. Serie B de 55 M$ en enero
  de 2026, con ARR multiplicado por seis en nueve meses.
- **Spellbook**: redacción y revisión nativas en Word. En 2026 lanzaron *Autonomous Contract
  Management*, que cubre admisión, revisión e insight — es decir, están invadiendo el territorio
  de los CLM desde abajo. Su estrategia de distribución es notable: programa de socios de canal,
  acuerdo con el Colegio de Abogados canadiense, programa académico en más de 50 facultades.
- **DraftWise / Definely**: redacción asistida a partir del precedente propio del despacho y
  navegación de definiciones y referencias cruzadas dentro del documento.

**Patrón común:** todas viven **dentro de Word**. La lección de la absorción del equipo de Robin
por Microsoft es que ese territorio va a ser disputado por el propio Microsoft.

### 3.6 CLM empresarial: Sirion, Icertis, Ironclad, Evisort

Gestión del ciclo de vida contractual para grandes empresas. Sirion se define como CLM nativo de
IA construido sobre arquitectura agéntica. Los cuatro hacen extracción de cláusulas y obligaciones
con LLMs.

**Relevancia para este proyecto:** poca en producto, mucha en concepto. El CLM demuestra que el
valor económico del análisis contractual no está en analizar *un* contrato, sino en **consultar
una cartera entera**: obligaciones que vencen, cláusulas que se desvían del estándar, exposición
agregada. Un extractor que produce JSON consistente es precisamente lo que hace posible esa
consulta agregada — que es exactamente la apuesta arquitectónica de este proyecto.

### 3.7 Los incumbentes: Thomson Reuters y LexisNexis

**CoCounsel Legal** (Thomson Reuters, lanzado agosto 2025) unifica investigación jurídica,
automatización de flujos, búsqueda documental inteligente y asistencia con IA. Su **Deep
Research** se presenta como la primera capacidad agéntica de investigación jurídica de grado
profesional: razona, planifica y entrega resultados fundamentados en Westlaw y Practical Law. En
junio de 2026 añadieron *Deep Research Verify* e investigación jurídica internacional.

**Su jugada estratégica más inteligente es educativa:** en enero de 2026 dieron acceso a CoCounsel
y Deep Research a más de 120.000 estudiantes de derecho en más de 200 facultades estadounidenses.
Es captura de mercado a diez años vista: el abogado que se forma con Westlaw compra Westlaw.

**LexisNexis** persigue la misma estrategia con Protégé.

**Su diferenciador declarado frente a Harvey o Legora:** las salidas están fundamentadas en
contenido propietario con citas verificables. **Su problema:** son precisamente estos productos
los que peor salieron en el estudio de Stanford (sección 7).

### 3.8 Litigación estadounidense: EvenUp, Eve, Supio, Alexi

Vertical de demandante en daños personales. EvenUp (Serie E de 150 M$, valoración de 2.000 M$) se
centra en el trabajo previo al litigio y en cartas de reclamación, con datos de valoración
detrás de la cifra reclamada. Eve superó los 1.000 M$ de valoración. Supio cubre el caso entero
—desde la admisión hasta el veredicto— y su argumento diferencial es que **aprende del histórico
del propio despacho**: casos previos, plantillas y resoluciones.

**Lección transferible:** la vertical más rentable de la IA jurídica estadounidense no es la que
razona mejor, sino la que ha encontrado un proceso repetitivo, de alto volumen y con salida
estandarizada. La cronología médica y la carta de reclamación son formularios caros. **La
pregunta equivalente para este proyecto: ¿cuál es el "formulario caro" del derecho español?**

### 3.9 Despachos nativos de IA: Garfield, Lawhive, Crosby

En mayo de 2025, la **SRA** británica autorizó a **Garfield.Law Ltd** como primer despacho
habilitado para prestar servicios jurídicos íntegramente mediante IA — reclamación de deudas en
juicios de escasa cuantía, hasta 10.000 £. Las condiciones impuestas por el regulador son el dato
más interesante: confidencialidad, ausencia de conflictos, **aprobación del usuario en cada
fase**, y —crucialmente— **prohibición de que la IA proponga jurisprudencia**, precisamente para
prevenir alucinaciones.

Lawhive compró un despacho tradicional británico en septiembre de 2025; Crosby levantó 5,8 M$ de
Sequoia y Bain Capital Ventures.

**Lo relevante no es la tecnología sino la forma regulatoria:** el regulador no autorizó "IA que
ejerce la abogacía", autorizó un despacho con supervisión humana, en un ámbito acotado y de bajo
riesgo, con la capacidad más peligrosa (citar jurisprudencia) expresamente desactivada. Es un
modelo de gradualismo regulatorio que conviene tener presente.

### 3.10 Europa soberana: Noxtua, Legalfly, Vecflow

- **Noxtua** (Berlín, antes Xayn): 80,7 M€ de Serie B para "la primera IA jurídica soberana de
  Europa". Modelos propios entrenados **exclusivamente con datos jurídicos europeos**. Inversores
  estratégicos reveladores: C.H. Beck (editorial jurídica alemana, que aporta acceso a más de 55
  millones de documentos), CMS y Dentons. Desde febrero de 2026 ofrecen la primera licencia
  europea transfronteriza que da acceso a contenido de varias editoriales y jurisdicciones en una
  sola plataforma.
- **Legalfly** (Bélgica): más de una docena de agentes especializados. **Su diferenciador es
  directamente aplicable a este proyecto: anonimizan todo documento *antes* de que llegue al LLM**,
  mediante un modelo afinado que se ejecuta en local. Afirman ser los únicos que lo hacen de forma
  sistemática. Tienen contrato con la Dirección General de RRHH de la Comisión Europea.
- **Vecflow** (Oliver): agente construido sobre Llama 3.1 405B, evaluado independientemente en el
  informe de Vals AI.

**Patrón europeo:** el argumento de venta no es la capacidad, es la **soberanía del dato**
—modelos entrenados en Europa, datos que no salen, anonimización previa—. Es una respuesta
comercial directa a lo que en España impone la Circular 3/2026 del CGAE (sección 8).

---

## 4. España

### 4.1 vLex — el caso de éxito español

Fundada en **Barcelona en 2000** por los hermanos Lluís Faus (CEO) y Ángel Faus (CTO). Plataforma
global de investigación jurídica con **Vincent AI** como capa generativa: análisis multimodal de
audio y vídeo, validación de argumentos jurídicos y flujos de trabajo personalizados.

**Clio la adquirió por 1.000 M$** (efectivo y acciones). Anunciado el 30 de junio de 2025,
aprobación regulatoria española a finales de octubre, cierre en noviembre de 2025, acompañado de
una Serie G de 500 M$ a una valoración de 5.000 M$. Es la mayor compra de la historia del sector
y convierte a vLex en uno de los pocos unicornios tecnológicos nacidos en España.

**La tesis de la fusión** es la más interesante estratégicamente: unir el sistema operativo de
gestión de Clio (más de 200.000 profesionales) con la inteligencia jurídica de vLex para pasar de
un *sistema de registro* a un *sistema de acción* — una IA que entiende tanto la mecánica del
trabajo jurídico como su contenido.

**Dato de calidad contrastado:** Vincent AI fue uno de los cuatro productos evaluados en el primer
*Vals Legal AI Report* (febrero 2025), junto a CoCounsel, Harvey Assistant y Oliver de Vecflow.
Es de los pocos productos con evaluación independiente publicada.

### 4.2 Las IA de las editoriales: el verdadero mercado español

| Producto | Editorial | Base documental | Nota |
|---|---|---|---|
| **Allegra** / Aranzadi Fusión | Aranzadi LA LEY (Wolters Kluwer) | ~10 millones de documentos; la mayor base privada de jurisprudencia de España | Lanzado marzo 2026 |
| **GenIA-L** | Lefebvre | Integrado con los Mementos y el contenido editorial | Considerado por varias fuentes la referencia de 2026 |
| **SOFIA 3.0** | Tirant lo Blanch (Valencia) | Legislación, jurisprudencia, doctrina, formularios y fondo bibliográfico | |
| **Helena** | Sepín | Especializada en civil, familia y arrendamientos | Nicho por materia |

**Arquitectura declarada (Allegra, la mejor documentada):** algoritmos propios combinados con LLMs
comerciales del mercado (mencionan Azure/OpenAI), desplegados en entorno controlado y alineado con
el Reglamento europeo de IA; garantizan que los datos y consultas del cliente permanecen cifrados
y **no se usan para entrenar modelos externos**. Todas las plataformas españolas declaran
explícitamente el principio de *human in the loop*.

**Lectura crítica:** ninguna afirma tener modelo propio. Todas son, esencialmente, **RAG sobre su
fondo documental con un LLM comercial detrás**. Su ventaja competitiva es la licencia del
contenido, no la ingeniería. Esto tiene dos consecuencias: (a) su calidad de razonamiento está
acotada por el modelo base que licencien, igual que la de cualquiera; (b) su foso es
inexpugnable para un tercero en investigación jurídica — y **completamente irrelevante en análisis
de documentos aportados por el cliente**, que es donde está este proyecto.

### 4.3 Otros actores españoles

- **Prudencia.ai**: copiloto jurídico (análisis, redacción, investigación, revisión de contratos,
  gestión de expedientes) que se posiciona sobre trazabilidad de respuestas y flujos de trabajo.
- **Lexroom**: legaltech italiana con más de 20 M€ levantados que entró en España en febrero de
  2026. Señal de que el mercado español se percibe como atacable desde fuera.
- **Councilbox**: gobierno corporativo digital — actas, votaciones y certificación de acuerdos.
- **Absia Legaltech**, **Axioma**, **LexFlow**: capa de herramientas para despacho pequeño y
  mediano, poco documentadas técnicamente.
- **Contratación pública**: nicho con actores propios — **PliegoBot** (redacción de PPT y PCAP
  alineada con la LCSP), **LICAI** de Eivor, **Tendios**, **LicitaBot**. Casi todos están del
  **lado del licitador** (encontrar licitaciones, preparar ofertas, verificar cumplimiento formal),
  no del lado del análisis crítico del pliego.
- **Despachos**: Garrigues y Cuatrecasas lideran el mercado legal español; Cuatrecasas mantiene un
  programa de aceleración de startups legaltech. La inversión en startups de IA en España superó
  los 800 M€ en 2025, con España en quinto puesto europeo por número de startups de IA.

**Diagnóstico del mercado español:** dominado por editoriales que compiten en profundidad
documental, con un único campeón global (vLex) ya absorbido por una empresa canadiense, y un tejido
de startups pequeño y poco diferenciado tecnológicamente. **El análisis riguroso de pliegos
administrativos desde el lado del análisis jurídico —no del lado de ganar la licitación— no lo
está haciendo nadie de forma medible.**

---

## 5. Patrones arquitectónicos transferibles

Seis patrones que aparecen repetidamente y que este proyecto puede adoptar.

### Patrón 1 — El *playbook* como fuente de verdad, no el modelo

El sector **no** implementa "pídele al modelo que encuentre riesgos". Implementa: *compara el
contrato contra un documento de referencia escrito por abogados*. Ese documento —el playbook—
contiene posición preferente, posiciones de repliegue (*fallbacks*) aceptables, términos
inaceptables, ejemplos de cláusula, reglas de escalado y justificación de negocio. La IA detecta
**desviaciones respecto de la referencia**, gradúa el riesgo y propone lenguaje aprobado.

**Consecuencia para este proyecto:** la `rubrica-riskflags.md` pendiente en el paso 4 de la fase 2
**es exactamente un playbook**. Es el patrón dominante del sector y el orden correcto —redactarla
antes de anotar— coincide con lo que ya está escrito en el `ROADMAP.md`.

### Patrón 2 — Anclaje al texto fuente, siempre

Legora: cada celda de la revisión tabular enlaza a su fuente. Luminance: toda salida lleva citas a
nivel de fuente que trazan hasta la cláusula subyacente. ContractEval: la tarea *es* extracción de
espans exactos. CGPJ (Instrucción 2/2026): trazabilidad obligatoria.

Sin un ancla al texto, una afirmación de riesgo no es verificable, no es medible por solapamiento,
y no cumple la expectativa regulatoria.

### Patrón 3 — La capacidad como unidad de evaluación

Harvey encapsula cada capacidad en un Tool Bundle **con su propio conjunto de datos y sus propios
evaluadores**, y exige puertas *leave-one-out*: ningún cambio entra si degrada capacidades
existentes. Es regresión de software aplicada a comportamiento de modelo.

### Patrón 4 — Verificación por consenso, con modelos distintos

El "Panel of Judges" de Luminance combina modelos fundacionales, propietarios y afinados. La
literatura sobre LLM-as-judge coincide: la fiabilidad mejora cuando el evaluador es distinto del
evaluado.

### Patrón 5 — Anonimización antes del modelo

Legalfly anonimiza en local, con un modelo afinado, **antes** de que el documento llegue al LLM.
Es la respuesta arquitectónica a la obligación de secreto profesional.

### Patrón 6 — Memoria institucional

Luminance retiene historial de negociación y razonamiento a través de todo el histórico
contractual; Supio aprende del histórico del propio despacho; Legora habla de memoria de
preferencias del cliente entre sesiones. El valor compuesto no está en analizar un documento, sino
en que el análisis número 500 sea mejor por haber hecho los 499 anteriores.

---

## 6. Lo que el sector hace mal

Un inventario honesto de debilidades es tan útil como el de fortalezas.

1. **Se anuncian garantías que no se cumplen.** Los proveedores presentaron el RAG como
   eliminación de alucinaciones. Stanford demostró que no (sección 7). Es la debilidad estructural
   del sector: incentivo comercial a exagerar fiabilidad en un dominio donde el error es caro.
2. **Los benchmarks propios son juez y parte.** Harvey publica el benchmark en el que Harvey sale
   bien; Legora, el suyo; Vecflow titula una entrada "Vecflow queda primero en el Legal Benchmark".
   Solo Vals AI opera como evaluador independiente, y su cobertura es reducida.
3. **Sesgo anglosajón masivo.** CUAD, LegalBench, VLAIR: derecho estadounidense. Multi-Legal-Bench
   cubre seis jurisdicciones civilistas europeas y **excluye España**. El civil law está
   infra-evaluado, y el derecho español, casi no evaluado.
4. **Las capacidades sustantivas están mucho menos resueltas de lo que parece.** ContractEval mide
   F1 ~0.9 en cláusulas frecuentes como "Governing Law" y **cerca de cero** en cláusulas raras y de
   alto riesgo como "Uncapped Liability" o "Joint IP Ownership". Justo las que importan.
5. **La "pereza" del modelo es un modo de fallo real y poco reportado.** ContractEval mide la tasa
   de "no hay cláusula relacionada" falsos: hasta un 30 % en modelos abiertos frente a un 1-7 % en
   propietarios. Un modelo que dice "no encuentro nada" parece prudente y en realidad está fallando.
6. **El modelo de negocio no está resuelto.** El colapso de Robin AI y el giro de Legora a precio
   por consumo apuntan a lo mismo: el trabajo agéntico de larga duración tiene coste variable alto
   y no encaja bien en licencias por usuario.

---

## 7. Cómo mide el sector la calidad — la sección más útil para este proyecto

Esto responde directamente al **paso 1 de la fase 2** del `ROADMAP.md`, que sigue abierto.

### 7.1 El estudio que cambió el debate: Stanford RegLab (2024)

Primera evaluación empírica preregistrada de herramientas comerciales de investigación jurídica
con IA: Lexis+ AI, Westlaw AI-Assisted Research y Ask Practical Law AI, sobre 202 consultas
jurídicas puntuadas a mano por expertos. **Alucinaban entre el 17 % y el 34 % de las veces**
(Lexis más del 17 %, Westlaw más del 34 %).

**Su aportación conceptual más importante es la distinción entre dos tipos de error:**

- **Fabricación**: la IA inventa un caso que no existe. Es lo que todo el mundo entiende por
  alucinación, y es el error *fácil* — se detecta comprobando que la referencia existe.
- **Desanclaje (*misgrounding*)**: la IA describe el derecho correctamente, cita un caso que
  existe de verdad, **pero el caso citado no sostiene la afirmación que se le atribuye**.

El desanclaje es más sutil y más peligroso, y **es invisible para cualquier validador de forma**.

> **Aplicación directa a este proyecto.** El riesgo pendiente registrado en `IDEAS.md` sobre el
> MCP de legislación española está bien identificado pero apunta solo a la mitad del problema: un
> MCP que verifique que la norma existe resuelve la fabricación, **no el desanclaje**. Que el art.
> 1124 CC exista no significa que sea el que aplica el tribunal en ese fundamento. La verificación
> de que `applied_rules` está correctamente anclada es un problema distinto y más difícil que
> comprobar que la cita es real.

### 7.2 Vals Legal AI Report (VLAIR) — evaluación independiente

Primer informe en febrero de 2025: cuatro herramientas (CoCounsel, Vincent AI, Harvey Assistant,
Oliver) en siete tareas — extracción de datos, Q&A documental, resumen, *redlining*, análisis de
transcripciones, generación de cronologías e investigación en EDGAR.

**Hallazgo con la forma exacta del problema de este proyecto:** las herramientas rindieron bien en
Q&A, resumen y **extracción de datos**, superando a menudo a la referencia humana; y **flojearon
en investigación en EDGAR y en *redlining* contractual**. Es decir: bien en lo mecánico y
estructurado, mal en lo sustantivo y valorativo.

Seguimiento de octubre de 2025 sobre investigación jurídica: 200 preguntas, productos jurídicos
específicos entre 78-81 % de exactitud y ChatGPT en 80 %. La conclusión incómoda para el sector es
que **el modelo generalista igualaba a los productos verticales** en esa tarea concreta.

### 7.3 CUAD y ContractEval — la métrica más directamente adoptable

**CUAD** (*Contract Understanding Atticus Dataset*): más de 13.000 etiquetas en 510 contratos
comerciales extraídos de EDGAR, sobre **41 tipos de cláusula** relevantes en *due diligence* de
M&A. El conjunto de test tiene 4.128 puntos de datos sobre 102 contratos. **Las anotaciones las
hicieron estudiantes de Derecho con 70-100 horas de formación específica, bajo supervisión de
abogados con experiencia.**

> Este dato merece subrayarse: el conjunto de datos de referencia del análisis contractual con IA
> lo anotaron estudiantes de Derecho formados y supervisados. La anotación por un estudiante de
> segundo no es un atajo, es **exactamente la metodología estándar** — siempre que haya rúbrica
> previa y formación registrada.

**ContractEval** (2025) construye sobre CUAD la evaluación de identificación de riesgo a nivel de
cláusula, y su esquema de métricas es lo más aprovechable de toda esta investigación:

**Definición de la tarea:** dado un contrato y una pregunta dirigida, extraer el/los *span* exactos
que la responden, o responder "no hay cláusula relacionada". Distribución del conjunto: **30 %
casos positivos, 70 % negativos.**

**Métrica 1 — Corrección (F1 y F2).** Clasificación:

| | Etiqueta no vacía | Etiqueta vacía |
|---|---|---|
| **Predice cláusula** | **TP** si cubre completamente el span etiquetado; **FN** si lo cubre parcialmente | **FP** |
| **Dice "no hay cláusula"** | **FN** | **TN** |

```
F1 = 2 · (P · R) / (P + R)
F2 = 5 · (P · R) / (4 · P + R)
```

**F2 pondera la exhaustividad por encima de la precisión**, penalizando más los falsos negativos —
justificado explícitamente porque en contexto jurídico omitir es más grave que señalar de más.

> **Esto responde una pregunta abierta literal de `IDEAS.md`:** *"Falsos positivos: ¿penalizan? En
> revisión contractual, señalar de más es menos grave que omitir, y la métrica debería reflejarlo."*
> La respuesta del estado del arte es sí, y el instrumento es **F2**, que es F-beta con β=2. La
> intuición ya registrada en el repositorio era correcta y tiene nombre, fórmula y precedente.

**Métrica 2 — Efectividad de la salida (similitud de Jaccard).** Solo sobre casos positivos:

```
J(A,B) = |A ∩ B| / |A ∪ B|
```

sobre los conjuntos de tokens del span predicho y el real. Mide **concisión**: penaliza tanto
quedarse corto como pasarse. El criterio declarado es el del abogado sénior: "exacto pero no
excesivamente verboso".

**Métrica 3 — Pereza.** Proporción de casos en que el modelo responde "no hay cláusula relacionada"
existiendo etiqueta. Es un subconjunto de los falsos negativos, aislado a propósito porque
diagnostica evasión, no error.

**Tratamiento de coincidencias parciales:** una predicción solo cuenta como TP si **cubre
completamente** el span etiquetado. Las coincidencias parciales son falsos negativos en F1/F2, y
su calidad se recoge por separado en Jaccard. Es una decisión de diseño defendible y explícita:
dos métricas complementarias en lugar de una métrica difusa.

**Hallazgos:** GPT-4.1 lidera con F1 ~0.64; mejores modelos abiertos ~0.54. El modo "thinking"
**mejora Jaccard pero empeora F1** — sobrecomplica tareas simples y aumenta la verbosidad. Y el
hallazgo estructural ya citado: F1 ~0.9 en categorías frecuentes, cerca de cero en cláusulas raras
de alto riesgo.

### 7.4 LegalBench y el benchmark de agentes de Harvey

**LegalBench**: 162 tareas en seis categorías de razonamiento — detección de cuestiones, recuerdo
de reglas, interpretación, aplicación, conclusión y retórica. Lectura resumida del estado del
arte: CUAD indica que la clasificación de cláusulas en contratos de M&A está prácticamente
resuelta; LegalBench indica que un modelo frontera detecta cuestiones aproximadamente al nivel de
un asociado de primer año sobre supuestos aislados.

**Harvey LAB**: rúbricas descompuestas en **criterios atómicos binarios** —hechos, citas,
calificaciones de gravedad, recomendaciones, formato— con puntuación *all-pass*. Una tarea de
cambio de control tiene 57 criterios sobre nueve cuestiones jurídicas.

> **Este es el patrón que resuelve el problema de tamaño muestral registrado en `IDEAS.md`.** El
> problema anotado era: ~20 documentos por partición dan intervalos de confianza inutilizables
> para un campo multietiqueta. La solución del sector es **medir por criterio, no por documento**:
> Harvey tiene 1.200 tareas y 75.000 criterios, unos 62 criterios por tarea. Con 23 documentos y
> 15-25 unidades anotadas cada uno, la N efectiva pasa de decenas a varios centenares.
>
> **Con la salvedad que ya está correctamente anotada en `IDEAS.md`:** las cláusulas de un mismo
> documento no son independientes. La consecuencia práctica no es descartar la métrica por
> criterio, es **no calcular intervalos de confianza como si lo fueran** — hay que agrupar por
> documento, o declarar por escrito que la medición es diagnóstica y no inferencial. Un desglose
> por identificador de flag ("el flag `PENAL-01` falla en 7 de 9 apariciones") es diagnóstico puro
> y no necesita potencia estadística para ser accionable.
>
> **La puntuación *all-pass* de Harvey no es adoptable aquí.** Con 23 documentos, exigir que todos
> los criterios acierten produciría casi con seguridad un cero y ninguna señal de mejora. Tiene
> sentido con 1.200 tareas y para comunicar a clientes empresariales; no para iterar.

### 7.5 LLM como juez: qué dice la literatura sobre su fiabilidad

Dado que la opción "juicio por modelo con criterios fijos" está sobre la mesa en el `ROADMAP.md`:

- El acuerdo entre anotadores **humanos** en tareas subjetivas de generación de lenguaje se sitúa
  típicamente en **κ = 0,3-0,6**. En un estudio jurídico con nueve expertos titulados, el acuerdo
  sobre "satisfacción" fue κ = 0,344; sobre consenso, 0,529; sobre riesgo de litigio, 0,613.
- **Con una rúbrica bien construida, el acuerdo sube sustancialmente**: LexRubric reporta α de
  Krippendorff = 0,759.
- Los jueces LLM alcanzan acuerdos altos pero **por debajo de la consistencia humana**, con más
  variabilidad entre modelos. Tienden a ser **más estrictos** que los humanos: marcan como
  incorrectas respuestas fácticamente correctas pero poco específicas.

> **Tres conclusiones operativas.** (1) La decisión ya tomada de escribir la rúbrica antes de
> anotar tiene respaldo empírico medible: es la diferencia entre κ≈0,4 y α≈0,76. (2) Existe un
> techo: ni siquiera juristas titulados coinciden perfectamente en juicios sustantivos, así que
> **no hay que perseguir el 100 % en `risk_flags`** — el 315/315 de sentencias no tiene equivalente
> posible aquí, y esperarlo llevaría a diseñar mal la rúbrica para forzarlo. (3) Antes de fiarse
> del Gold conviene **medir el propio acuerdo consigo mismo**: anotar 5 documentos, dejarlos
> reposar dos semanas, reanotarlos a ciegas y calcular la coincidencia. Si es baja, el problema es
> la rúbrica, no el agente — y se descubre antes de anotar los 23.

---

## 8. Marco regulatorio español y europeo — novedades de 2026

Esto ha cambiado sustancialmente desde la última actualización del repositorio y afecta al
proyecto.

### 8.1 Instrucción 2/2026 del CGPJ (BOE, 30/01/2026)

Aprobada por el Pleno del CGPJ el 28 de enero de 2026, regula el uso de sistemas de IA por jueces
y magistrados en el ejercicio de la actividad jurisdiccional. Nueve principios: control humano
efectivo, no sustitución, responsabilidad judicial exclusiva, independencia, derechos
fundamentales, confidencialidad y seguridad, prevención de sesgos, proporcionalidad y formación.

**Usos permitidos:** búsqueda y localización de información jurídica —incluida la identificación
de normativa y jurisprudencia—, análisis y clasificación de documentos procesales, **elaboración
de esquemas o resúmenes internos**, y tareas organizativas auxiliares. Los borradores de sentencia
exigen validación personal, completa y crítica del magistrado.

**Prohibiciones:** automatizar decisiones judiciales, condicionar la independencia, incorporar
contenido sin validación crítica personal, usar datos especialmente protegidos sin autorización,
**perfilado, predicción de comportamientos o clasificación de sujetos**, y utilizar sistemas no
facilitados por las administraciones competentes.

> **Lectura para este proyecto:** el pipeline de sentencias hace exactamente lo que la Instrucción
> permite —localizar información jurídica, clasificar documentos, elaborar resúmenes estructurados—
> y **nada** de lo que prohíbe. No hay perfilado, no hay predicción de resultados, no hay
> clasificación de sujetos. Es un argumento de posicionamiento sólido y conviene tenerlo escrito.
> La prohibición de predicción de comportamientos, además, delimita una frontera que este proyecto
> no debería cruzar: la "predicción de resultado judicial" es un producto atractivo comercialmente
> y explícitamente vetado en el ámbito jurisdiccional español.

### 8.2 Circular 3/2026 del CGAE (10 de abril de 2026)

Dictada al amparo del art. 23 de la LO 5/2024 del Derecho de Defensa. **No prohíbe** la IA
generativa: la concibe como herramienta auxiliar sujeta a supervisión humana. Su aportación es
elevar el **deber de verificación y control** a categoría dogmática, anclándolo en la doctrina de
la *actio libera in causa* — desplazando cualquier intento de irresponsabilidad tecnológica del
abogado. En abril de 2026 el CGAE aprobó además directrices específicas sobre el uso de IA en
escritos jurídicos.

**El punto con consecuencias técnicas directas:** usar versiones de consumo de modelos
fundacionales, cuyos términos generales prevén la reutilización de las entradas para
entrenamiento, constituye una vulneración directa del principio de limitación de la finalidad
(art. 5.1.b RGPD) y del deber de secreto (art. 542.3 LOPJ). La orientación práctica es exigir:
**garantía contractual explícita de no entrenamiento sobre las entradas, residencia del dato en la
UE, cifrado adecuado y contrato de encargo del art. 28 RGPD.**

> **Esto interpela directamente al repositorio.** `Inputs/` contiene datos personales reales
> —nombres de cliente, protocolo notarial, NIF— según consta en `ROADMAP.md`. La decisión de
> mantenerlo en `.gitignore` es correcta y necesaria, pero **no es suficiente** desde la
> perspectiva de la Circular: el `.gitignore` protege el histórico de git, no regula qué se envía
> al modelo. Mientras el proyecto sea académico y los documentos procedan de fuentes públicas
> (PLACSP, CENDOJ) el riesgo es bajo; en el momento en que entre un documento de un cliente real,
> la Circular 3/2026 es de aplicación plena.
>
> Aquí encaja el patrón 5 (Legalfly): **anonimizar antes de procesar**. Y para el corpus actual,
> hay una medida más simple y de coste casi nulo: priorizar las vías A y C, que son documentos
> públicos, sobre cualquier documento privado con datos reales — que es, de hecho, lo que ya se
> decidió por otras razones.

### 8.3 Reglamento de IA (UE) 2024/1689

Los sistemas de IA usados **por la Administración de Justicia** para interpretar hechos o aplicar
el Derecho son **alto riesgo** (Anexo III), con obligaciones de documentación técnica, marcado CE,
registro en base de datos europea, evaluación de impacto en derechos fundamentales (FRIA, art. 27)
y supervisión humana efectiva. Desde agosto de 2026 el incumplimiento puede alcanzar 35 M€ o el
7 % de la facturación mundial. El CGPJ actúa como autoridad de vigilancia del mercado para estos
sistemas.

> **Matiz importante y no resuelto:** la calificación de alto riesgo del Anexo III se refiere a
> sistemas destinados a ser utilizados **por una autoridad judicial o en su nombre**. Una
> herramienta que usa un abogado para analizar sus propios documentos no encaja en ese supuesto y,
> en principio, no sería de alto riesgo por esa vía. **No es una conclusión firme y no debe darse
> por buena sin verificar el texto del Anexo III.** Pero es una distinción que conviene resolver
> por escrito antes de que el proyecto se acerque a cualquier uso real, porque determina si aplican
> o no las obligaciones de marcado CE y FRIA — que son la diferencia entre un proyecto viable y uno
> inviable para un desarrollador individual.

---

## 9. Diagnóstico: este proyecto frente al mercado

### 9.1 Lo que este proyecto hace mejor que el mercado

**1. Rigor de evaluación por encima de la media del sector.** Es una afirmación fuerte pero
sostenible. Este repositorio contiene algo que la mayoría de productos comerciales no tiene: un
conjunto Gold anotado, un validador mecánico, un histórico de métricas y —lo más raro— **una
advertencia escrita de que su propia medición del 100 % no es extrapolable**. El sector entero
tiene el problema opuesto: publica el 100 % y omite la advertencia. La nota de `ESTADO.md` sobre
el test gastado es, metodológicamente, mejor práctica que la de varios productos con financiación
de nueve cifras.

**2. La consciencia del régimen no la tiene nadie.** No he encontrado ningún producto, español o
internacional, que distinga estructuralmente entre control de contenido (consumo, arts. 82 y ss.
TRLGDCU), control de incorporación y transparencia (adherente empresario, Ley 7/1998) y régimen
administrativo (LCSP). Lo más cercano son los *International Playbooks* de LegalOn —estándares por
país— y los modelos por jurisdicción de Noxtua. Pero eso es granularidad **geográfica**; el campo
`regimen` es granularidad **de nivel de control dentro de un mismo ordenamiento**, que es más
fina y jurídicamente más correcta.

Y la advertencia central de `ESTADO.md` —que una cláusula declarada abusiva no es una etiqueta
transferible a un pliego administrativo, y que de la jurisprudencia se transfieren los criterios y
nunca las calificaciones— es el tipo de precisión que un producto construido por ingenieros no
suele alcanzar. **Es la ventaja competitiva real de este proyecto, y viene de la formación
jurídica, no de la técnica.**

**3. Separación de corpus y métricas por vía.** Que las vías A, B y C tengan métricas separadas y
no se agreguen en una sola tabla de precisión es correcto y poco habitual. Los productos
comerciales publican una cifra global de "precisión" que mezcla tareas heterogéneas.

**4. La disciplina documental.** `CLAUDE.md` como principios permanentes, `ESTADO.md` como
situación cambiante, un estándar por tipo de documento y la regla de no duplicar reglas es,
esencialmente, el patrón de Tool Bundles de Harvey aplicado a documentación: una fuente única por
capacidad, con instrucciones propias. Se llegó a la misma solución de forma independiente.

### 9.2 Lo que el mercado hace mejor y aquí falta

**1. Anclaje al texto fuente.** El esquema v1 de `standards/contratos.md` **no tiene ningún campo
que localice la cláusula en el documento**. Ni `key_clauses` ni `risk_flags` llevan cita literal,
offset, número de cláusula o página. Es la carencia más importante que he encontrado, porque
bloquea tres cosas a la vez: no se puede calcular Jaccard ni cobertura de span (sección 7.3), no
se puede verificar una anotación sin releer el contrato entero, y no se cumple la expectativa de
trazabilidad de la Instrucción 2/2026 y de todo el sector.

**2. `missing_clauses` no tiene referencia definida.** Una cláusula "falta" solo respecto de una
lista de referencia. El estándar no define cuál es esa lista, y esa lista **es necesariamente
dependiente del régimen**: en un pliego LCSP el contenido mínimo lo fija la ley; en un contrato de
adhesión de consumo la referencia es distinta; en un mercantil negociado casi no hay referencia
objetiva. Sin resolverlo, dos anotaciones del mismo documento diferirán y no habrá forma de decir
cuál es correcta. Es el mismo hallazgo que en el patrón 1: `missing_clauses` es un campo de
*playbook*, y sin playbook no tiene semántica.

**3. `severity` sin anclajes.** Tres niveles (`low`/`medium`/`high`) sin definición operativa es la
receta estándar para destrozar el acuerdo entre anotadores. La literatura de la sección 7.5 lo
predice: los juicios subjetivos sin rúbrica se quedan en κ≈0,3-0,4. La regla escrita —"nunca
inferir gravedad de la mera presencia de una cláusula"— es correcta pero es una prohibición, no un
criterio positivo.

**4. `control_aplicable` depende de un dato que no es campo.** La tabla del estándar hace depender
`control_aplicable` de `regimen` **y de la condición del adherente**, pero la condición del
adherente no existe como campo en el esquema. Un anotador tiene que inferirla y no queda
registrada, que es exactamente lo que `CLAUDE.md` prohíbe en su principio 3 (separar lo extraído
de lo interpretado).

**5. No hay forma de detectar que el estándar no se cargó.** El riesgo está registrado en
`IDEAS.md` —"si el agente no carga standards/, produce JSON plausible con reglas recordadas y
ninguno de los dos scripts lo detecta"— y sigue sin mitigación. Harvey lo resuelve por
construcción: las instrucciones del Tool Bundle se inyectan en el prompt de sistema, no dependen
de que el agente decida leerlas.

**6. Nada de memoria institucional.** Cada documento se procesa de cero. Es razonable en esta fase
—no tiene sentido construir memoria antes de tener métrica— pero es la dirección hacia la que va
todo el sector (patrón 6) y conviene que el esquema no la imposibilite.

### 9.3 El posicionamiento real

Este proyecto **no puede competir** con Aranzadi o vLex en investigación jurídica: su foso es la
licencia del fondo documental y es inexpugnable. **No debería intentarlo.**

Sí puede ocupar un espacio que ahora mismo está vacío: **análisis estructurado de documentos que
aporta el usuario, en derecho español, con consciencia de régimen y con evaluación publicada.** El
fondo documental es irrelevante para ese caso de uso, porque el documento lo trae el cliente.

Y hay una asimetría a favor que conviene ver con claridad: **la arquitectura agéntica se ha
commoditizado y el corpus evaluado no.** Harvey usa el SDK de OpenAI. Cualquiera puede montar un
agente. Lo que nadie tiene es un corpus de contratos españoles anotado contra una rúbrica escrita,
con métricas publicadas y particiones ciegas reservadas. **El activo de este proyecto no es el
agente: es el corpus y la rúbrica.** Y el `ROADMAP.md` ya está ordenado de esa manera, aunque
quizá por otras razones.

---

## 10. Conclusiones y recomendaciones

Ordenadas por lo que desbloquean. Son propuestas: no se ha modificado ningún estándar.

### Prioridad 1 — Cerrar el paso 1 adoptando una métrica existente, no inventando una

El paso 1 de la fase 2 lleva bloqueando la rúbrica, el Gold y la evaluación. **Se puede cerrar
adoptando el esquema de ContractEval**, que ya está diseñado, publicado y validado para
exactamente esta tarea:

- **Corrección** por F1 **y F2**, con las definiciones de TP/FP/FN/TN de la sección 7.3. F2 como
  métrica principal, porque pondera la exhaustividad — que es la respuesta que `IDEAS.md` ya
  intuía a la pregunta sobre falsos positivos.
- **Jaccard** sobre los spans, solo en positivos, para medir concisión.
- **Tasa de pereza**: proporción de "no detectado" cuando sí hay etiqueta. Diagnóstico de evasión.
- **Coincidencia parcial = falso negativo** en F1/F2, con la calidad parcial recogida aparte en
  Jaccard. Es una decisión explícita y defendible, mejor que un umbral de solapamiento arbitrario.
- **Unidad de medida: el criterio anotado, no el documento**, para elevar la N efectiva — con la
  advertencia de no independencia ya registrada, y declarando por escrito que la primera medición
  es diagnóstica.
- Sobre `severity`: medirla **por separado** de la detección. Un flag detectado con gravedad
  distinta es un acierto de detección y un fallo de calibración, y mezclarlos oculta cuál de los
  dos falla. Esto responde a otra pregunta abierta literal de `IDEAS.md`.

**Por qué adoptar en vez de diseñar:** no es solo ahorro de tiempo. Es que los resultados serán
**comparables** con la literatura publicada, lo que convierte una medición interna en un dato
citable — y eso importa mucho si esto acaba siendo un trabajo académico.

### Prioridad 2 — Añadir anclaje al texto en el esquema v1, antes de anotar nada

Cambio de esquema pequeño, consecuencias grandes. Cada `risk_flag` y cada `key_clause` debería
llevar la cita literal del texto que la sostiene, más su localizador (número de cláusula, o página
y párrafo).

Habilita: métrica de span, verificación de anotaciones sin releer el documento, cumplimiento de la
expectativa de trazabilidad, y detección de desanclaje — que la sección 7.1 identifica como el
error peligroso y que sin cita literal es indetectable.

**Hay que hacerlo antes de anotar el Gold**, porque añadirlo después obliga a reanotar.

### Prioridad 3 — Resolver la semántica de `missing_clauses` antes de la rúbrica

Decidir y escribir cuál es la lista de referencia por régimen. En la vía A (administrativa) hay una
respuesta objetiva y disponible: el contenido mínimo del PCAP según la LCSP. Es el régimen con la
referencia más sólida y probablemente el mejor sitio para empezar.

Si no hay referencia defendible para un régimen, la alternativa honesta es **dejar
`missing_clauses` vacío en ese régimen y no medirlo**, en lugar de anotarlo con criterio
implícito. Es coherente con el principio 7 de `CLAUDE.md`: preferir `null` antes que inferencia.

### Prioridad 4 — Cerrar dos huecos de esquema detectados

- Añadir `condicion_adherente` (o equivalente) como campo, para que `control_aplicable` sea
  derivable de datos registrados y no de una inferencia no anotada.
- Añadir anclajes operativos a `severity`: qué hace que un riesgo sea `high` y no `medium`, con
  ejemplo. Sin esto, la métrica de gravedad no será estable ni consigo misma.

### Prioridad 5 — Hacer verificable la carga del estándar

Mitigación barata para el riesgo abierto en `IDEAS.md`: que el estándar defina un campo de versión
—por ejemplo `standard_version: "contratos-v1"`— cuyo valor **solo pueda conocerse leyendo el
fichero del estándar**, y que el validador lo compruebe. No garantiza que el agente aplicara las
reglas, pero convierte "no cargó el estándar" de fallo silencioso en fallo detectable. Es la
versión mínima y viable del patrón de Harvey.

### Prioridad 6 — Antes de anotar los 23, medir el acuerdo consigo mismo

Anotar 5 documentos contra la rúbrica, dejarlos dos semanas, reanotarlos sin mirar la primera
versión, y calcular la coincidencia. Si es baja, el problema está en la rúbrica y se descubre
habiendo gastado 5 documentos en vez de 23.

Es barato, es la práctica estándar en construcción de conjuntos anotados, y da además una cifra
que contextualiza cualquier resultado posterior: si el acuerdo humano consigo mismo es 0,75,
ningún agente debería esperar más.

### Prioridad 7 — Escribir la nota de encaje regulatorio

Una página en el repositorio: por qué el pipeline de sentencias encaja en los usos permitidos de la
Instrucción 2/2026 y no en los prohibidos; qué exige la Circular 3/2026 sobre entradas al modelo y
secreto profesional; y la cuestión abierta sobre si el Anexo III del Reglamento de IA alcanza o no
a una herramienta usada por un abogado sobre sus propios documentos.

No es burocracia. Es la clase de documento que en un proyecto de un estudiante de Derecho vale
tanto como el código, y **es exactamente el terreno donde este proyecto tiene ventaja sobre uno
construido por ingenieros**.

### Lo que NO recomiendo

- **No construir orquestación agéntica propia.** Harvey decidió no hacerlo. La `sentencia_agent`
  actual, con un fichero de estándar detrás, es el patrón correcto y suficiente.
- **No abrir la fase 3 ni la 4 ahora.** Las fases 3 (universidad) y 4 (noticias) son atractivas y
  fáciles de empezar, precisamente porque no exigen resolver la evaluación. Empezarlas ahora
  significaría abandonar la fase 2 en el punto donde está su dificultad real y su valor
  diferencial. La disciplina del `ROADMAP.md` en este punto es correcta.
- **No perseguir el 100 % en `risk_flags`.** El 315/315 de sentencias fue posible porque los
  campos de cabecera tienen una única respuesta correcta. Los campos sustantivos no la tienen —ni
  entre juristas titulados—. Un objetivo de 100 % en `risk_flags` llevaría a diseñar la rúbrica
  para que sea fácil, en vez de para que sea útil.
- **No añadir el MCP de legislación todavía**, y cuando se añada, no venderlo como solución a las
  alucinaciones: resuelve la fabricación, no el desanclaje (sección 7.1).
- **No tocar predicción de resultado judicial.** Es atractivo comercialmente y está expresamente
  prohibido en el ámbito jurisdiccional por la Instrucción 2/2026. Además exigiría exactamente el
  tipo de evaluación que este proyecto aún no tiene.

---

## 11. Fuentes

**Arquitectura y producto**
- ZenML LLMOps Database — [Scaling Agent-Based Architecture for Legal AI Assistant (Harvey)](https://www.zenml.io/llmops-database/scaling-agent-based-architecture-for-legal-ai-assistant)
- Harvey — [Introducing Harvey's Legal Agent Benchmark](https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark) · [The Year Legal AI Becomes Core Infrastructure](https://www.harvey.ai/blog/the-year-legal-ai-becomes-core-infrastructure)
- Legora — [2026: The Year of Agents in Legal AI](https://legora.com/blog/2026-the-year-of-agents-in-legal-ai) · [Tabular Review](https://legora.com/product/tabular-review) · [Benchmark for Agentic Reasoning](https://legora.com/bar)
- Luminance — [The Next Frontier for Contract Work](https://www.luminance.com/resources/blog/the-next-frontier-for-contract-work-legal-grade-ai-that-understands-the-bigger-picture/) · Tech.eu — [Luminance unveils its biggest platform upgrade in a decade](https://tech.eu/2026/01/27/legaltech-luminance-unveils-its-biggest-platform-upgrade-in-a-decade/)
- LegalOn — [Contract Playbooks](https://www.legalontech.com/contract-playbooks) · [Expands Global Contracting Capabilities](https://www.legalontech.com/press-releases/legalon-expands-global-contracting-capabilities-for-in-house-legal-teams) · LawSites — [Custom Playbooks](https://www.lawnext.com/2025/01/legalon-expands-ai-contract-review-platform-with-feature-to-create-custom-playbooks.html)
- Thomson Reuters — [Launches CoCounsel Legal: Agentic AI and Deep Research](https://www.thomsonreuters.com/en/press-releases/2025/august/thomson-reuters-launches-cocounsel-legal-transforming-legal-work-with-agentic-ai-and-deep-research) · [Agentic AI to Over 200 Law Schools](https://www.thomsonreuters.com/en/press-releases/2026/january/thomson-reuters-brings-agentic-ai-to-over-200-law-schools)
- LEGALFLY — [Secures €15M to set security standard](https://www.legalfly.com/post/legalfly-secures-eu15-million-to-set-security-standard-in-ai-legal-services) · nonbillable — [LegalFly is all-in on AI for in-house teams](https://www.nonbillable.co.uk/news/legalfly-ruben-miessen-interview)
- Noxtua — [Cross-border legal AI license (Tech.eu)](https://tech.eu/2026/02/18/noxtua-launches-europes-first-cross-border-legal-ai-license/) · Sifted — [€80m Series B for sovereign legal AI](https://sifted.eu/articles/noxtua-sovereign-ai-series-b)
- Ivo — [Raises $55M Series B](https://www.ivo.ai/blog/ivo-raises-55m-to-bring-ai-contract-intelligence-to-every-in-house-legal-team) · Legal IT Insider — [Contract review platform Ivo raises $55m](https://legaltechnology.com/2026/01/20/contract-review-platform-ivo-raises-55m-series-b/)
- National Law Review — [Spellbook launches Autonomous Contract Management](https://natlawreview.com/article/spellbook-builds-its-ai-foundation-launch-autonomous-contract-management)
- Sirion — [Gartner Leaders: Sirion vs Ironclad vs Icertis](https://www.sirion.ai/library/contract-insights/gartner-leaders-sirion-vs-ironclad-vs-icertis-clm/)
- Artificial Lawyer — [Plaintiff Bar AI Takes Off: EvenUp Bags $150m](https://www.artificiallawyer.com/2025/10/07/plaintiff-bar-ai-takes-off-evenup-bags-150m/)
- GC AI — [Build a Custom AI Contract Playbook](https://gc.ai/blog/ai-contract-playbook) · ScaleFirm — [What Is a Contract Playbook](https://scalefirm.com/post/what-is-a-contract-playbook-and-why-it-matters-for-ai-contract-review/)

**El caso Robin AI**
- Legal IT Insider — [Microsoft hires raft of Robin AI engineers](https://legaltechnology.com/2026/01/12/microsoft-hires-raft-of-robin-ai-engineers-to-bolster-its-word-team/)
- Artificial Lawyer — [Microsoft 'To Acqui-Hire Robin AI Tech Team'](https://www.artificiallawyer.com/2026/01/09/microsoft-to-acqui-hire-robin-ai-tech-team/)
- Global Legal Post — [Scissero buys managed services team of rival Robin AI](https://www.globallegalpost.com/news/scissero-buys-managed-services-team-of-rival-robin-ai-264599795)

**España**
- LawSites — [Clio Completes Historic $1 Billion vLex Acquisition](https://www.lawnext.com/2025/11/clio-completes-historic-1-billion-vlex-acquisition-announces-500-million-series-g-at-5-billion-valuation-plus-exclusive-interview-with-ceo-and-cfo.html) · [In A Mega Deal, Clio Buys vLex for $1 Billion](https://www.lawnext.com/2025/06/in-a-mega-deal-clio-buys-vlex-for-1-billion-merging-ai-research-and-practice-management.html)
- vLex — [Clio firma acuerdo para adquirir vLex](https://vlex.es/news/clio-firma-acuerdo-para-adquirir-vlex)
- Legal Today — [Aranzadi LA LEY lanza Allegra](https://www.legaltoday.com/actualidad-juridica/noticias-de-derecho/aranzadi-la-ley-lanza-allegra-la-ia-que-convierte-el-mejor-fondo-juridico-en-decisiones-agiles-y-seguras-2026-03-26/)
- Prudencia.ai — [Las 10 mejores IA jurídicas de España en 2026](https://prudencia.ai/blog/mejores-ia-juridicas-espana-2026/) *(fuente interesada: la publica una de las herramientas rankeadas)*
- Lefebvre — [Top 10 IA Jurídicas 2026 en España](https://lefebvre.es/genia-l/blog/asistente-juridico-con-ia/10-ias-juridicas-potentes-mercado-2026/) *(idem)*
- El Español / Invertia — [La legaltech italiana Lexroom entra en España](https://www.elespanol.com/invertia/disruptores/ecosistema-startup/startups/20260227/legaltech-italiana-lexroom-entra-espana-acumular-millones-rondas-financiacion/1003744147221_0.html)
- Cuatrecasas — [Innovando con startups Legaltech: la IA generativa](https://www.cuatrecasas.com/es/spain/art/innovando-con-startups-legaltech-la-ia-generativa)
- [PliegoBot — Redacción de Pliegos de Licitación con IA (LCSP)](https://www.pliegobot.com/) · [LICAI — Gestión de Licitaciones con IA](https://eivor.es/solucion/automatizaciones-con-ia/gestion-de-licitaciones-en-espana/)

**Evaluación y benchmarks**
- Magesh et al. — [Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools](https://onlinelibrary.wiley.com/doi/full/10.1111/jels.12413) (*Journal of Empirical Legal Studies*) · [Stanford RegLab](https://reglab.stanford.edu/publications/hallucination-free-assessing-the-reliability-of-leading-ai-legal-research-tools/)
- Vals AI — [Vals Legal AI Report (VLAIR)](https://www.vals.ai/industry-reports/vlair-2-27-25) · [VLAIR — Legal Research](https://www.vals.ai/industry-reports/vlair-10-14-25) · LawSites — [Legal and General AI Now Outperform Lawyers in Legal Research Accuracy](https://www.lawnext.com/2025/10/vals-ais-latest-benchmark-finds-legal-and-general-ai-now-outperform-lawyers-in-legal-research-accuracy.html)
- [ContractEval: Benchmarking LLMs for Clause-Level Legal Risk Identification in Commercial Contracts](https://arxiv.org/html/2508.03080) (arXiv 2508.03080)
- [LegalBench: a collaboratively built benchmark for measuring legal reasoning in LLMs](https://arxiv.org/pdf/2308.11462) (arXiv 2308.11462)
- [Multi-Legal-Bench: Evaluating LLMs on Legal Reasoning Across Jurisdictions, Languages, and Legal Traditions](https://arxiv.org/html/2605.29738v1) (arXiv 2605.29738)
- [LexRubric: A Rubric-Guided Diagnostic Benchmark for Open-Ended Legal Tasks](https://arxiv.org/pdf/2606.09389) · [The Coin Flip Judge? Reliability and Bias in LLM-as-a-Judge Evaluation](https://arxiv.org/pdf/2606.13685) · [Simulating Dispute Mediation with LLM-Based Agents for Legal Research](https://arxiv.org/pdf/2509.06586)

**Regulación**
- BOE — [Instrucción 2/2026 del CGPJ sobre utilización de sistemas de IA en el ejercicio de la actividad jurisdiccional](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-2205)
- Confilegal — [La Circular 3/2026 del CGAE sobre el uso de IA en la Abogacía](https://confilegal.com/20260516-circular-3-2026-cgae-ia-abogacia-proteccion-datos-secreto-profesional/)
- Blog José Carlos Fernández Rozas — [La Abogacía Española aprueba nuevas directrices sobre el uso de IA en escritos jurídicos](https://fernandezrozas.com/2026/05/26/la-abogacia-espanola-aprueba-nuevas-directrices-sobre-el-uso-de-ia-en-escritos-juridicos-10-abril-2026/)
- SRA — [SRA approves first AI-driven law firm (Garfield)](https://news.sra.org.uk/news/news/press/2025-press-releases/garfield-ai-authorised/) · IBA — [The AI-native law firm: regulatory innovation](https://www.ibanet.org/AI-native-law-firm-regulatory-innovation-and-fundamental-restructuring-of-legal-service-delivery)
