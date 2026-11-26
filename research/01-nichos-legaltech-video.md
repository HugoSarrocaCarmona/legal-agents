# 📹 INFORME 1 — Los nichos del legaltech según el mercado global

**Fuente:** *«Understand the Legal AI market in 40 mins.»* — Mags Chilaev (41:21).
https://youtu.be/WtWs-BtKECE
Transcripción íntegra en [`transcripcion-video-legal-ai-market.txt`](transcripcion-video-legal-ai-market.txt).

> Los nombres de empresa se han reconstruido a partir de subtítulos automáticos. Donde la
> transcripción era fonéticamente ambigua se marca con `(?)`. Las cifras de financiación son
> las que da el autor, no verificadas de forma independiente.

---

## La tesis del vídeo, en tres frases

El autor revisó más de mil empresas que dicen «hacer IA para derecho» y encontró que **casi
todas sirven uno o varios de los mismos 32 casos de uso**, y que esos 32 casos caben en **8
categorías de producto que el legaltech ya tenía antes de la IA generativa**.

Su conclusión: **la IA apenas ha creado categorías nuevas; ha vertido capacidades nuevas en
categorías viejas.** Solo una cosa es genuinamente nueva (el despacho nativo de IA).

Y su explicación de por qué esas categorías son tan estables es la parte realmente útil:

> *«Cada herramienta vale exactamente lo que vale el cuerpo de información sobre el que puede
> razonar.»*

---

## 🔑 EL MARCO QUE IMPORTA: las 5 fuentes de datos

Esta es la aportación aprovechable del vídeo. Todo producto legaltech razona sobre una de estas
cinco fuentes, y **la fuente determina la dificultad, el foso competitivo y quién puede
construirlo**:

| # | Fuente de datos | Qué es | Quién la controla |
|---|---|---|---|
| 1 | **La ley misma** | Legislación, jurisprudencia, regulación | Editoriales / Estado |
| 2 | **El conocimiento del despacho** | Precedentes, playbooks, contratos firmados | El propio despacho |
| 3 | **La prueba de un caso concreto** | Documentos, correos, testimonios de un litigio | El cliente |
| 4 | **Los datos operativos del despacho** | Expedientes, plazos, horas, facturas | El propio despacho |
| 5 | **Internet abierto** | Registros públicos, dockets, quejas, filings | Nadie / abierto |

**Por qué esto es la clave del informe 2:** la fuente de datos no es un detalle técnico, es la
barrera de entrada. Un producto sobre la fuente 1 en España es casi imposible de construir
desde cero; uno sobre la fuente 5 es viable para una persona sola.

---

## 🗂️ LAS 8 CATEGORÍAS Y LOS 32 CASOS DE USO

`A` = *augment* (la IA asiste, el humano decide) · `AUT` = *automate* (corre solo) ·
`A/AUT` = a caballo.

### 1. Ciclo de vida del contrato (CLM) — 4 casos

| Caso de uso | Qué hace la IA | Fuente | A/AUT | Referente |
|---|---|---|---|---|
| Redacción de contratos | Primer borrador competente en minutos, anclado al precedente y estilo del despacho | 2 | A | Spellbook (~$120M) |
| Revisión y *redline* | Lee el borrador de la otra parte, marca cláusulas fuera de mercado, propone cambios contra el *playbook* | 2 | A | Luminance (~$165M) |
| CLM como sistema | Repositorio central, extracción de términos, enrutado a aprobadores, alertas de vencimiento | 4 | **AUT** | Ironclad (~$333M) |
| Inteligencia contractual / *benchmarking* | Compara una cláusula contra millones de acuerdos reales: ¿es estándar, agresiva o anómala? | 1 (corpus de mercado) | A | SimpleDocs / Law Insider (20M cláusulas) |

**Observación del autor:** la IA produce el lenguaje, pero no puede cargar con el juicio de si
esos términos son los correctos *para este cliente, este negocio y este nivel de riesgo*.

### 2. Investigación jurídica — 5 casos

| Caso de uso | Qué hace la IA | Fuente | A/AUT | Referente |
|---|---|---|---|---|
| Pregunta–respuesta | Respondes en lenguaje natural con citas a las fuentes reales | 1 | A | Legora (~$866M) |
| *Litigation sourcing* | Rastrea quejas de consumo, filings SEC y dockets buscando patrones que señalen una infracción litigable, y vende el caso montado a despachos de demandante | **5** | A | Darrow (~$60M, rentable) |
| Analítica judicial | Predice cómo irá un caso: cómo falla ese juez, cuánto tardan asuntos así, qué hace el letrado contrario | 1 (registros judiciales) | A | Lex Machina (LexisNexis) |
| Arbitraje internacional | Mapea conceptos entre idiomas y jurisdicciones: buscas en inglés y aflora un laudo en francés | 1 | A | Jus Mundi (~$33M) |
| Investigación fiscal | Responde preguntas fiscales duras sobre legislación densa y por capas | 1 | A | Blue J (~$133M) |

**Punto crítico del autor:** aquí acertar importa más que en ningún otro sitio, porque *un
modelo abandonado a su memoria inventa con facilidad un caso que suena plausible y perfecto y
que sencillamente no existe*. Todas las buenas herramientas de esta categoría compiten en lo
mismo: **atar cada respuesta a una fuente real**.

### 3. Litigación — 6 casos

Aquí la fuente cambia: ya no es la ley, es **la prueba del caso concreto**. Es la parte más
saturada del mapa porque combina volúmenes enormes, mucho en juego y un corpus cerrado.

| Caso de uso | Qué hace la IA | Fuente | A/AUT | Referente |
|---|---|---|---|---|
| *eDiscovery* / revisión documental | Ordena por relevancia millones de correos y archivos, aflora el puñado que importa | 3 | A/AUT | aiR by Relativity (~$3.000M, saliendo a bolsa) |
| Inteligencia de hechos | No busca documentos: reconstruye **qué pasó**. Cronologías y contradicciones, cada afirmación enlazada a su fuente | 3 | A | Wexler (~$6,7M) |
| Redacción procesal | Escribe escritos que se presentan al juzgado, verifica cada cita contra el expediente, formatea según las reglas locales | 1 + 3 | A | Clearbrief (~$8M) |
| Análisis de declaraciones | Transcribe con vocabulario jurídico y resume horas de testimonio hasta los momentos clave | 3 | A | Parrot (~$15M, adquirida por Filevine) |
| Revisión de historiales médicos | Digiere cientos de miles de páginas y monta cronología clínica con enlace a página fuente | 3 | A | Medchron / Filevine (~$400M en 2025) |
| Generación de *demand packets* | Monta la reclamación al asegurador y **pone cifra a la lesión** usando el histórico de veredictos y acuerdos | 3 + 1 | A | EvenUp (~$385M) |

### 4. *Due diligence* — 2 casos

| Caso de uso | Qué hace la IA | Fuente | A/AUT | Referente |
|---|---|---|---|---|
| *Data room* | Interrogas todo el *data room* de golpe («marca todo contrato con cláusula de cambio de control») en vez de leer documento a documento | 3 | A | Harvey (cientos de millones) |
| Inteligencia de operaciones | Convierte el histórico de operaciones cerradas en activo consultable: «¿cómo tratamos este *covenant* en las últimas 100 operaciones?» | 2 | A | Centari (~$14M, la mitad del AmLaw 10) |

### 5. Propiedad industrial y patentes — 3 casos

Categoría aparte porque **exige razonamiento técnico, no solo jurídico**: para juzgar si una
invención es nueva hay que buscar en todo el corpus de publicación técnica humana.

| Caso de uso | Qué hace la IA | Fuente | A/AUT | Referente |
|---|---|---|---|---|
| Redacción de patentes | Redacta la solicitud desde la memoria de invención, incluso en química, biología y física | 1 + 3 | A | DeepIP (~$40M, 400+ despachos) |
| Búsqueda y analítica de patentes | Estado de la técnica: ¿es novedoso? ¿infringe? ¿dónde están los huecos de la cartera? | 1 | A | Patlytics (~$65M) |
| Litigación de PI | Genera *claim charts* mapeando elemento por elemento la reivindicación contra el producto o el estado de la técnica | 1 + 3 | A | &AI (YC, ~$6,5M) |

### 6. Conocimiento y búsqueda — 3 casos

Mira hacia dentro: el conocimiento acumulado de la propia organización.

| Caso de uso | Qué hace la IA | Fuente | A/AUT | Referente |
|---|---|---|---|---|
| Búsqueda interna | «¿Hemos defendido esta pretensión antes? ¿Cómo nos fue?» sobre todo el repositorio propio | 2 | A | iManage |
| Gestión de experiencia | No *qué* hemos escrito sino **quién** de los nuestros ha hecho esto y con qué resultado (para *pitches* y RFPs) | 2 + 4 | A | Litera |
| Anonimización y tachado | Detecta y oculta datos sensibles: nombres y PII en texto, **caras, matrículas y voces** en vídeo y audio, siguiendo el objeto fotograma a fotograma | 3 | **AUT** (con revisión) | Veritone Redact (?) |

### 7. *Compliance* — 3 casos

| Caso de uso | Qué hace la IA | Fuente | A/AUT | Referente |
|---|---|---|---|---|
| Mapeo de obligaciones regulatorias | Convierte la norma en **árbol de decisión ejecutable** que un agente corre contra la actividad ordinaria del negocio | 1 | A/AUT | Norm Ai (~$140M) |
| Gobernanza de IA | Inventaría qué IA usa la empresa, clasifica su riesgo frente al RIA y genera documentación lista para auditoría | 1 + 4 | A | Trustible (~$6M) |
| Conflictos e intake | Busca conflictos de interés incluyendo matrices, filiales y contrapartes históricas; triaje en «hay/no hay/dudoso» + sanciones y titularidad real | 4 | A | Intapp |

**Nota del autor:** la gobernanza de IA *es un trabajo que hace tres años no existía*.

### 8. Operaciones jurídicas (*legal ops*) — 6 casos

No hay razonamiento jurídico, pero **determina si el despacho gana dinero**.

| Caso de uso | Qué hace la IA | Fuente | A/AUT | Referente |
|---|---|---|---|---|
| Automatización de flujos | Encadena triaje → documentos → aprobaciones → informe sin que nadie persiga cada paso | 4 | A | BRYTER · *(el autor sitúa aquí Claude for Legal como «la fontanería» que orquesta entre sistemas)* |
| Intake, triaje y chatbots | Puerta única de entrada al departamento legal: enruta lo valioso al abogado, resuelve solo lo rutinario | 4 + 2 | A/AUT | Checkbox (~$23M) |
| Gestión de expedientes | La IA no sustituye el sistema: **empuja el trabajo** — crea la cita desde el documento, resume el asunto dormido, señala el expediente que se atasca | 4 | A | Clio |
| Imputación de horas | Reconstruye el día facturable pasivamente en vez de que el abogado lo recuerde el viernes, y redacta la narrativa de factura | 4 | **AUT** | Laurel (~$130M) |
| Revisión de facturación externa | Lee línea a línea las facturas de los despachos externos contra las *billing guidelines* antes de autorizar el pago | 4 | A/AUT | BrightFlag (adq. Wolters Kluwer) |
| Extranjería de extremo a extremo | Ingiere documentos, hace la investigación del caso, redacta escritos y anexos y devuelve un PDF listo | 3 + 1 | A | Caselink (?) (~$2,5M) |

---

## 🆕 LO ÚNICO GENUINAMENTE NUEVO: el despacho nativo de IA

Todo lo anterior son **herramientas que un despacho compra**. Esto es otra cosa: un **negocio
regulado construido desde cero con la IA como mecanismo de entrega**, no un despacho normal que
le atornilla IA encima. Un número pequeño de humanos responsables supervisa y responde, pero el
servicio jurídico lo presta la IA.

El autor identifica **dos condiciones habilitantes**, y ambas son regulatorias y económicas, no
tecnológicas:

1. **El regulador abre la puerta** deliberadamente, para promover el acceso a la justicia.
2. **La economía solo cuadra en volumen alto y valor bajo**: reclamaciones demasiado pequeñas
   para que a un abogado le compense mirarlas.

### Variante consumo / pyme

Trabajo que **nunca habría llegado a un abogado**. Te deben unos miles de euros; contratar
letrado cuesta más que la deuda; la deuda se cancela contablemente. *Ese descuadre, repetido a
lo largo de millones de facturas impagadas, es el hueco.*

- **Garfield AI** — primer despacho nativo de IA plenamente autorizado por la **SRA** (Inglaterra
  y Gales). Lleva la reclamación de deuda mercantil de principio a fin: lee la factura, redacta
  la carta de requerimiento, el *letter before action*, el formulario de demanda, y prepara el
  expediente y los argumentos esquemáticos. **Desde 2 £ la carta inicial.** Reporta ~500.000 £
  recuperadas en 600+ casos, y en mayo de 2026 se le atribuyó la primera victoria en juicio
  contradictorio de un despacho nativo de IA. Un *barrister* humano hace la vista.
- **Legal OS** — el mismo modelo en extranjería: dos docenas de agentes especializados redactan
  una petición de visado con patrones aprendidos de 12.000 expedientes exitosos, anticipando
  las objeciones del examinador. Petición lista en 48 h, firmada por abogado colegiado.

### Variante enterprise

Apuesta distinta: que este modelo puede **ganar trabajo jurídico complejo compitiendo en precio
y velocidad**. Toman capital riesgo, usan **estructuras de propiedad liberalizadas que permiten
socios no letrados**, y crecen **comprando proveedores tradicionales** y envolviéndolos en IA.

El discurso al cliente corporativo no es «aquí tienes una herramienta para tu equipo interno»,
sino **«danos el trabajo: nuestra IA más humanos lo hará más barato y mejor que tu abogado
externo»**. Dejan de ser proveedor de software para ser **el prestador del servicio**.

- **Eudia** (~$105M) — gastó buena parte del capital comprando ALSPs y levantó un despacho
  regulado bajo las reglas de propiedad liberalizada de **Arizona**.
- **Manifest** (~$60M) — lo mismo desde el otro lado: arrancó en un vertical y se expande a
  despacho nativo de IA multi-área.

---

## 📌 Las cinco conclusiones que hay que llevarse

1. **La IA no ha inventado categorías; ha rellenado las que ya existían.** Buscar «la categoría
   nueva» es perseguir un fantasma: 31 de 32 casos de uso son trabajos que ya se hacían.
2. **La fuente de datos es la barrera de entrada**, no el modelo. El modelo es una *commodity*;
   el corpus, no.
3. **Casi todo es *augment*, no *automate*.** Lo que se automatiza de verdad comparte tres
   rasgos: **datos estructurados, apuestas bajas y volumen inhumano** (CLM, imputación de
   horas, tachado, cribado de facturas). Donde hay juicio jurídico, sigue habiendo humano.
4. **La verificación contra fuente real es el campo de batalla** de todo lo que toca la ley. No
   es un extra de calidad: es *la* función del producto.
5. **La única novedad real —el despacho nativo de IA— no es un avance técnico sino
   regulatorio.** Existe porque la SRA y Arizona lo permitieron. Donde el regulador no abre esa
   puerta, ese modelo sencillamente no existe.

> El punto 5 es el que decide el informe 2, porque **España no ha abierto esa puerta**.
