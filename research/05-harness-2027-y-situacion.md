# 🧭 INFORME 5 — El vídeo de Eric Risco y dónde está legal-agents

**Fecha:** 23/11/2026 · **Pedido por Hugo:** extraer el vídeo, decir qué aplicar y qué no, y hacer
un alto para situar el proyecto: dónde estamos, qué viene después del anotador, a dónde lleva, y
qué otras vías existen.

> ⚠️ **Estado de la fuente: el vídeo NO se ha oído.** YouTube bloquea subtítulos, audio y
> storyboards desde la IP del contenedor (`tools/video/watch_video.py` lo intentó con todos sus
> clientes). Lo mismo con la charla de Lydia Hallie en la que se basa. La sección 1 está
> construida con: el **índice de 16 capítulos y la descripción** que publica el propio autor,
> la **documentación oficial** que él enlaza (leída), su **harness público** `rsc-harness`
> (leído) y reseñas secundarias de la charla de Hallie. **Lo que Eric dice en cada capítulo está
> pendiente de la transcripción**; los veredictos sobre legal-agents no dependen de ella, salvo
> donde se indica.
>
> Vídeo identificado: «Antes de programar con IA en 2027, cambia esto», Eric Risco, 27:40,
> publicado el 23/11/2026 — el último del canal y el único sobre 2027. Hugo lo citó como «tu
> forma de programar no está lista para 2027»; si no es el mismo, esta sección no vale.

---

## 0 · En cinco líneas

1. **La tesis del vídeo**, según su índice: el modelo ha mejorado y buena parte del arnés que
   construimos ahora estorba. Menos herramientas conectadas, `CLAUDE.md` corto y usado como
   mapa, reglas que se ejecutan (hooks, permisos) solo donde importa, skills para lo que se
   repite, subagentes para repartir. Y un aviso: dejar que el agente mejore su propio entorno no
   salió como esperaba.
2. **Para legal-agents aplican cinco cosas, y las cinco son trabajo de Claude, no tuyo:** fusionar
   ramas (las sesiones nuevas leen un `ESTADO.md` del 25/08), adelgazar `CLAUDE.md` + `ESTADO.md`
   (470 líneas en cada arranque), un hook que haga cumplir «nada se borra» en `Inputs/`, una
   skill `cerrar-pliego` y una poda de conectores. Code Mode, sandbox, Agent Teams y automejora:
   no, por ahora.
3. **Situación:** 5 de 10 pliegos, 61 filas, 207 de 700 páginas. **Queda el 70 % de las páginas**
   y los cinco pliegos más largos. 39 de 61 filas son de admisión.
4. **Lo que todavía no se había dicho:** el esquema v2 no puede representar lo que estás
   encontrando. **Unas 32 de las 39 filas de admisión no caben en ninguna de las 16 materias**
   del vocabulario cerrado de `standards/contratos.md`, que solo cubre ejecución. Si el recuento
   final confirma admisión, lo siguiente no es la rúbrica sobre el esquema actual: es un v3.
5. **Lo que más falta no es técnico:** cero conversaciones con alguien del sector.

---

## 1 · El vídeo, capítulo a capítulo — PROVISIONAL

Formato de cada bloque: **qué es** (verificado en la documentación oficial) y **qué hacer en
legal-agents**, con la razón. Hugo trabaja sobre todo en **local, en Windows**: eso decide varias
respuestas.

### 1.1 · Code Mode (00:41–03:19) — ❌ No, por ahora

- **Qué es.** Modo experimental, apagado por defecto: Claude escribe JavaScript que encadena varias
  llamadas a herramientas en un solo paso, en vez de hacerlas de una en una. Se activa con
  `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=1` (en PowerShell:
  `$env:CLAUDE_CODE_EXPERIMENTAL_CODE_MODE = "1"`). Solo terminal: no funciona en sesiones en la
  nube ni en la app de escritorio. En Windows exige Git for Windows. Los ajustes de proyecto lo
  ignoran a propósito, así que un repo clonado no puede encenderlo.
- **En legal-agents.** Ahorra llamadas cuando una tarea repite la misma operación sobre muchos
  ficheros. Tu cuello de botella es la **lectura humana de PDF**, no el número de llamadas.
  Reconsiderarlo cuando toque procesar 30–40 pliegos para el Gold.

### 1.2 · No conectes herramientas por si acaso (03:19) — ✅ Sí, diez minutos

- **Qué es.** Cada conector o servidor MCP mete sus descripciones en el contexto y amplía lo que el
  agente puede tocar.
- **En legal-agents.** Esta sesión arrancó con decenas de conectores —Gmail, Calendar, Drive,
  Indeed, Amplitude, Atlassian, Figma, Slack…— y unos dieciséis que ni siquiera conectaban.
  **Ninguno sirve a este proyecto.** En local, `/mcp` y desactivar lo que no uses aquí. El MCP de
  legislación de `progress/IDEAS.md` entra solo cuando toque anclar contra el BOE, y después de
  verificar de dónde saca los datos.

### 1.3 · Qué sobra en tu CLAUDE.md · CLAUDE.md como mapa · `/doctor` (05:33–10:48) — ✅ Sí, es lo que más aplica

- **Qué es.** La documentación fija un objetivo de **menos de 200 líneas**; lo que se deduce del
  repo no va; y `CLAUDE.md` **es contexto, no se hace cumplir**: para impedir algo hay que usar un
  hook o `permissions.deny`. `/doctor prompt-audit` (v2.1.283 o posterior) revisa `CLAUDE.md`,
  reglas, skills y comandos buscando contenido desfasado o contradictorio, propone cambios y no
  toca nada hasta que se le pide.
- **En legal-agents.** La idea de mapa ya la tienes, y bien hecha: `CLAUDE.md` remite a
  `progress/ESTADO.md` y a `standards/`. Lo que falla es el peso y la coherencia:
  - `CLAUDE.md` tiene **247 líneas** y `progress/ESTADO.md` **223**, pese a decir de sí mismo que
    «se mantiene corto a propósito». Son **470 líneas** en cada arranque.
  - **Contradicción viva:** `CLAUDE.md` enuncia la línea activa como *riesgo de ejecución*;
    `progress/ESTADO.md` dice que el encuadre está abierto y que los datos apuntan a *admisión*.
    Un modelo que lea los dos recibe dos proyectos.
  - Historia dentro de `CLAUDE.md` (la nota «Delimitado el 04/10/2026») que pertenece a
    `progress/LOG.md`, y secciones genéricas sin efecto —«Organización», «Objetivo final»—.
  - `progress/LOG.md` no se actualiza desde el **17/09**: los cinco pliegos solo constan en
    `ESTADO.md`. La capa de memoria se está desviando.
  - **Tu propia regla ya lo pedía.** `CLAUDE.md` § «Revisar este arnés cuando cambie el modelo»
    pide exactamente esta revisión, y la charla de Hallie trata de cómo cambian las buenas
    prácticas con la nueva generación de modelos. Si has cambiado de modelo desde el 04/10, la
    revisión ya toca.

### 1.4 · Auto Mode y permisos (10:48) — ✅ Sí, con una sola regla dura

- **Qué es.** En auto mode un clasificador revisa cada acción en lugar de pedirte permiso. Las
  reglas `deny` siguen mandando por encima.
- **En legal-agents.** El principio que las reseñas atribuyen a Hallie —*regla dura para lo que
  no se puede deshacer; el resto, al modelo*— encaja con precisión. En este repo **lo único
  irreversible es `Inputs/`**: está en `.gitignore`, no tiene historia, y el antiguo nº 16 se
  perdió así el 06/08/2026. Todo lo demás está en git y se recupera.

### 1.5 · Hooks: PreToolUse, PermissionRequest, PreCompact (13:17–18:03) — ✅ Uno solo

- **Qué es.** `PreToolUse` se ejecuta antes de cada herramienta y puede bloquearla (salir con
  código 2 la deniega y el motivo llega al modelo). `PreCompact`, antes de compactar el contexto.
  `PermissionRequest`, cuando hace falta una decisión de permiso. Los hooks corren **fuera del
  sandbox, con tus permisos**. En Windows usan PowerShell si no hay Git Bash.
- **En legal-agents.** **Un `PreToolUse` que impida borrar o mover nada dentro de `Inputs/` salvo
  hacia `Inputs/_depurados/`.** Convierte «Nada se borra» de texto en regla que se ejecuta. Si lo
  quieres igual en local y en la web, en Python: el contenedor no tiene PowerShell.
- **Lo que no:** `PreCompact` y `PermissionRequest` no resuelven ningún problema que tengas. Y la
  tentación a evitar es un hook por cada regla de `CLAUDE.md`: el arnés que estorba es justo de
  lo que avisa el vídeo.

### 1.6 · Sandbox y seguridad de las skills (18:03) — ❌ Sandbox · ✅ hábito de revisión

- **Qué es.** El sandbox del sistema operativo limita solo los comandos de shell. **En Windows
  nativo no existe**: hace falta WSL2. Para skills de terceros, la documentación pide revisarlas
  antes de usarlas; `skill-veil` es un escáner estático, en Rust, de skills y manifiestos MCP.
- **En legal-agents.** Sandbox no: montar WSL2 no compensa en un repo cuyo único activo sensible
  es `Inputs/`, que ya cubre el hook de 1.5. Seguridad de skills, sí como hábito: **leer entera
  toda skill de terceros antes de instalarla**. `llm-council` lo es. `skill-veil`, no: pide toda
  una toolchain de Rust para un riesgo que con dos skills se controla leyendo.

### 1.7 · Cuándo convertir un prompt en una skill (19:56) — ✅ Sí, dos cosas

- **Qué es.** Una skill es una carpeta con `SKILL.md`; se carga cuando es relevante o con
  `/nombre`. Los comandos de `.claude/commands/` ya se tratan como skills.
- **En legal-agents.**
  1. **Crear `cerrar-pliego`.** Lo has hecho cinco veces a mano —los commits «Cerrar el pliego
     N»—: filas al CSV, columnas de `corpus/pliegos-a-leer.csv`, recuento por `momento` en
     `progress/ESTADO.md`, commit. Es el criterio de libro para una skill, y el recuento lo haría
     un script en vez de a ojo.
  2. **Aplicar tu propia regla de retirada.** `RUN`, `DEBUG`, `IMPROVE` y `run_once` son de la
     línea aparcada de sentencias y **se cargan en cada sesión**: aparecen en la lista de skills
     disponibles. `CLAUDE.md` dice que las de una línea congelada se reescriben o se retiran.
     Al revés, `ver-video` vive en una rama sin fusionar, y por eso esta sesión no la veía.

### 1.8 · Subagentes: repartir trabajo y modelos (21:02) — ⏳ Más adelante

- **Qué es.** Cada subagente trabaja con su propio contexto y puede fijar su modelo.
- **En legal-agents.** Toca en el paso 7 (`pliego_agent`), como ya hace `sentencia_agent`. Una
  conexión útil con `progress/IDEAS.md`: si algún día se pre-anota el Gold con un modelo, la
  condición escrita era «modelo distinto del evaluado», y el campo de modelo del subagente es el
  mecanismo para cumplirla.

### 1.9 · Licencias y Agent Teams (23:17) — ❌ No

- **Qué es.** Experimental y apagado: varios agentes con su contexto que se hablan entre sí y
  comparten lista de tareas. Gastan bastantes más tokens que los subagentes.
- **En legal-agents.** Resuelve un problema de equipo. Tienes un solo frente activo y lo lees tú.

### 1.10 · ¿Puede un harness mejorarse solo? (24:08) — ❌ No, y refuerza algo

- **Qué es.** Según la descripción, el experimento de Eric «no salió como esperaba». **Por qué, lo
  dirá la transcripción.**
- **En legal-agents.** La Fase 5 de `progress/ROADMAP.md` («ajuste automático de prompts») choca
  con la lección que ya pagaste el 05/08: corregir reglas mirando los fallos **gastó el test**. Una
  automejora sin conjunto ciego reservado es sobreajuste automatizado. Se queda congelada hasta
  que exista ciego-2.

### 1.11 · Qué cambiar de cara a 2027 (26:29) — pendiente de la transcripción

### Paso a paso de lo aplicable, en orden

| # | Qué | Quién | Por qué en este orden |
|---|---|---|---|
| 1 | **Fusionar ramas.** PR de `claude/video-review-uow2yt` a `main`; traer `tools/video/` y la skill `ver-video`; dejar `claude/legal-automation-research-iisyip` sin fusionar (son 5 commits de la línea anterior al giro del 09/09, siguen en remoto) | Claude; tú apruebas | Es el único fallo que **rompe tu punto de entrada**: `main` va 21 commits por detrás, se quedó en el 25/08, y una sesión que arranca desde ahí lee un `ESTADO.md` sin anotador, sin pliegos y sin giro. Esta sesión arrancó así |
| 2 | **Adelgazar.** `/doctor prompt-audit` en local; `CLAUDE.md` por debajo de 200 líneas y `ESTADO.md` por debajo de 80; historia al `LOG.md`; resolver la contradicción ejecución/admisión; poner el `LOG.md` al día | Claude propone, tú decides | Cada sesión paga esas 470 líneas, y la contradicción confunde al modelo |
| 3 | **Proteger `Inputs/`** con una regla `deny` o el hook de 1.5 | Claude | Es lo único irreversible del repo |
| 4 | **Skill `cerrar-pliego`** y retirar o marcar los cuatro comandos de sentencias | Claude | Te ahorra el ritual en los cinco pliegos que quedan |
| 5 | **Podar conectores** con `/mcp` | Tú, 10 min | Menos ruido en cada sesión |

**Nada de esto compite con tu tiempo de lectura**, que es lo único que mueve el proyecto ahora.
Son una sesión de Claude y quince minutos tuyos de revisión.

---

## 2 · Dónde está legal-agents hoy

**Línea activa: el anotador de pliegos (paso 5 de la fase 2).** Lees a mano diez pliegos de la
población «un solo licitador, y fue excluido» y anotas cada riesgo en
`corpus/anotaciones-pliegos.csv`. De ahí sale por inducción la rúbrica.

| | |
|---|---|
| Pliegos cerrados | **5 de 10** — 1 (19/10), 6 (20/10), 9 (25/10), 10 (27/10), 2 (10/11) |
| Filas anotadas | **61** — unas 12 por pliego, dentro de la horquilla de 8–20 del protocolo |
| Páginas de PCAP leídas | **207 de 700.** Quedan **493, el 70 %** |
| Quedan | 7 (65 págs.), 3 (70), 8 (85), 4 (115), 5 (158) |
| Tiempo restante estimado | **8,5–10,5 horas**, aplicando la estimación de `corpus/PROTOCOLO-LECTURA.md` a las páginas que faltan |

**La señal, con n = 5:**

| `momento` | Filas | `quien_controla` | Filas | `severidad_intuitiva` | Filas |
|---|---|---|---|---|---|
| admisión | **39** | licitador | 49 | alta | **54** |
| ejecución | 21 | órgano | 10 | media | 6 |
| valoración | 1 | tercero | 2 | baja | 1 |

Y de las 39 de admisión, **17 caen entre la propuesta de adjudicación y la formalización**:
requisitos que solo se descubren al ganar. Con la cautela de recuento del pliego 9, la admisión
baja a 35 de 57. La señal aguanta igual.

**Dos cautelas de método que siguen abiertas.**

- **Claude ha escrito parte de las filas.** En el pliego 9 redactó el criterio de 5 filas; en el 10
  reescribió `como_se_falla` en 8 de 11; en el 2 añadió 5 filas y reescribió 9 de 13. Esas filas
  van a ser la rúbrica, y contra la rúbrica se medirá después a un agente: cuanto más la escriba
  el modelo, menos independiente es la medición. **Para los cinco que quedan: escríbelas tú
  enteras, y que Claude revise después dejando constancia en `notas`.**
- **`severidad_intuitiva` ya no discrimina:** 54 de 61 son `alta`. Ya está anotado que se revisa
  al inducir la rúbrica.

**Sobre el parón.** Me dijiste que han pesado la carga de la uni, que cuesta arrancar con los
largos, y la dispersión; dudas de método, no. Sin dramatismo: este informe es justo el tipo de
trabajo que tu `CLAUDE.md` señala como riesgo. Es útil, pero no mueve el pliego 7. Por eso la
sección 5 termina en una sola tarea.

---

## 3 · Después del anotador: los pasos, y a dónde llevan

### El hallazgo que cambia el orden

`standards/contratos.md` tiene un **vocabulario cerrado de 16 materias**, y su regla de cierre
dice que *una materia que no esté en la tabla no genera flags*. Las 16 son de ejecución:
penalidades, garantía definitiva, revisión de precios, modificación, resolución, pago…

Cruzado con tus 39 filas de admisión, **solo unas 7 encajan** (las de garantía definitiva, en la
materia 4). Las otras **~32** —solvencia, presentación en plazo y forma, requerimiento de
documentación al propuesto adjudicatario, justificación de la oferta anormalmente baja,
formalización— **no tienen casilla**. La cifra es una lectura mía por palabras clave, y se
confirma al agrupar.

**Consecuencia:** con el esquema v2, el agente no podría emitir la mayoría de los riesgos que
estás encontrando. **Si el recuento final confirma admisión, el paso siguiente a los diez pliegos
es un esquema v3, antes que la rúbrica.**

### La secuencia

| Paso | Qué produce | Coste | Nota |
|---|---|---|---|
| **0. Los cinco pliegos que quedan** | ~120 filas en total | 8,5–10,5 h tuyas | El orden del protocolo: 7, 3, 8, y los de 115 y 158 páginas al final |
| **1. Contar `momento`** | La decisión de encuadre: admisión o ejecución | Minutos | **Es tuya**, y el protocolo pide no decidirla antes de contar |
| **2. Esquema v3** (si sale admisión) | Materias de admisión en el vocabulario cerrado; revisión de `corpus/metrica.md` | 1–2 sesiones | Ver la observación de abajo |
| **3. Rúbrica** `corpus/rubrica-riesgos-lcsp.md` | 25–45 grupos con `id` cerrado; ancla normativa transcrita del BOE o criterio apoyado en el TACRC | El paso jurídico más duro | Aquí sí se citan artículos, y nunca de memoria |
| **4. `validate_contratos.ps1`** | Control de forma | Claude | |
| **5. `pliego_agent`** | El agente, remitiendo al estándar sin duplicarlo | Claude | Como `sentencia_agent` |
| **6. Gold** | **30–40 pliegos nuevos** anotados contra la rúbrica, en dos particiones ciegas | **El mayor coste del proyecto** | Los diez de lectura sirven de desarrollo, no de test: la rúbrica salió de ellos |
| **7. Evaluación** | La primera cifra honesta de la fase 2 | | Registrada en `corpus/evaluaciones.md` antes de mirarla |

**Lo que conviene saber ya:** acabar el anotador no acaba la anotación. El Gold es el mismo tipo
de trabajo multiplicado por tres o cuatro. Ahí es donde la pre-anotación asistida de
`progress/IDEAS.md` deja de ser una idea y pasa a ser una decisión, con sus tres condiciones
escritas.

### Una observación sobre el encuadre (interpretación mía, no dato)

Si el producto es de admisión, cambia de naturaleza. Un riesgo de ejecución pide **juicio**: ¿es
desproporcionada esta penalidad? Un riesgo de admisión es sobre todo **extracción literal**: qué
hay que aportar, en qué plazo, en qué forma y qué pasa si no. Es casi todo clase `normativo`, con
métrica exacta, y es el tipo de tarea en la que tu método ya dio **313/315 a ciegas** en
sentencias. El producto natural sería una **lista de admisión con fechas**, y lo que la hace
valiosa son esas 17 filas que solo aparecen al ganar. No decide nada: es un argumento más que
pesar cuando cuentes.

### A dónde lleva

- **Técnicamente:** a la primera herramienta **medida** sobre un corpus abierto y explotable. El
  repo pasaría de «enseña método» a «tiene un resultado».
- **Para tu carrera:** `research/03-carrera-y-emprendimiento.md` dijo que el repo «no vale para una
  entrevista». Una evaluación honesta sobre pliegos reales sí vale.
- **Como producto:** a nada sin la validación humana que no ha empezado. El comprador sigue sin
  resolverse: la pyme licitadora, o el órgano de contratación con la herramienta invertida.

---

## 4 · Otras vías viables — para situarte, no para abrir

Ordenadas por lo que reutilizan de lo que ya tienes. **Ninguna se abre antes de cerrar los diez
pliegos.** Las descartadas en `research/02-oportunidad-mercado-espanol.md` siguen descartadas: el
despacho nativo de IA, por la Ley 2/2007; la litigación en masa, por regulación e incumbentes; y
los resúmenes de sentencias como producto, porque son commodity.

| Vía | Qué reutiliza | Cuándo tendría sentido |
|---|---|---|
| **A · El TACRC como corpus de resoluciones** | El pipeline de sentencias entero —esquema, validador, Gold, método— aplicado a un corpus **abierto y sin prohibición de uso comercial**, que es lo que le faltaba a la fase 1 | **La de más sinergia.** Alimenta la parte valorativa de la rúbrica de pliegos y desaparca la fase 1 con un corpus explotable. Al llegar al paso 3 |
| **B · Publicar los desiertos de 2025** | Las cifras ya calculadas por `scripts/placsp/`: el 72 % sin ofertas y los 3.651 casos de un solo licitador excluido | Es tu **primer contacto con el mundo exterior**, y un buen pretexto para la primera conversación. Coste bajo: el análisis ya está hecho |
| **C · La herramienta invertida, para el órgano** | El mismo análisis desde el lado de quien redacta el pliego | Es el comprador alternativo que el consejo dejó sin resolver. Se decide hablando con un técnico de contratación, no en el repo |
| **D · MASC (LO 1/2025)** | Poco | Ya evaluada: el mejor proyecto de credibilidad y el peor negocio. Después de que la vía de pliegos tenga usuarios |
| **E · Vigilancia normativa estrecha** | La fase 3 de `progress/ROADMAP.md`, con el ámbito ya cerrado | Es tu recopilador de noticias, estrechado a contratación pública, el Reglamento de IA y el CGAE. Barato de automatizar más adelante; hoy sería un frente más |
| **F · Agente universidad** | Nada que construir | **Ya existe:** tu cuenta de claude.ai tiene activadas las skills `study-desk` (`study-plan`, `study-quiz`, `study-cards`, `study-exam`). Úsalas para enero en vez de construirlo |

---

## 5 · Lo que haría yo, en orden

1. **Esta semana, el pliego 7** (Junta de Castilla y León, 65 páginas, entre 60 y 90 minutos).
   Una sola tarea. Para arrancar: los primeros 15 minutos, solo el cuadro de características,
   que es lo que pide el protocolo.
2. **En paralelo, y sin quitarte tiempo:** Claude hace los pasos 1–4 de la sección 1 y tú los
   revisas en quince minutos.
3. **Una conversación antes del pliego 10.** La persona más accesible que tienes es un profesor o
   profesora de Derecho Administrativo de la UB que trabaje contratación pública, en una tutoría.
   No para venderle nada: para enseñarle el 39/21 y las 17 filas que aparecen al ganar, y
   preguntarle **por qué se excluye de verdad a una empresa**. El consejo fijó el umbral de
   reversión en «la primera conversación útil», y sigue en cero.
4. **Enero es de exámenes**, y eso no es esquivar nada. Si hay hueco, los pliegos 3 y 8; los dos
   largos (4 y 5), después.

---

## 6 · Lo que queda abierto

- **La transcripción.** Con ella se completan 1.10 y 1.11 y se contrasta lo que Eric dice en cada
  capítulo con los veredictos de la sección 1. Va a `research/transcripcion-video-risco-2027.txt`,
  igual que la del informe 1.
- **Si quieres que Claude haga ahora los pasos 1–4 de la sección 1.** El 1 implica abrir un PR a
  `main`.
- **La decisión de encuadre**, que es tuya y se toma al contar, no antes.

---

## Fuentes

- Vídeo: <https://www.youtube.com/watch?v=7_dEsn4EUQ4> — solo metadatos y capítulos
- Charla de Lydia Hallie, *Rethinking Claude Code Best Practices*:
  <https://www.youtube.com/watch?v=vlfCjWuv4es> — solo metadatos
- Reseñas secundarias de la charla, no verificadas contra el vídeo:
  <https://brycewatson.com/research/claude-code-best-practices>,
  <https://wikidocs.net/blog/@jaehong/36932/>
- Harness de Eric Risco: <https://github.com/ericrisco/rsc-harness>
- Skill Veil: <https://github.com/seifreed/skill-veil>
- Documentación de Claude Code:
  [Code Mode](https://code.claude.com/docs/en/code-mode) ·
  [Memoria y CLAUDE.md](https://code.claude.com/docs/en/memory) ·
  [Hooks](https://code.claude.com/docs/en/hooks) ·
  [Sandbox](https://code.claude.com/docs/en/sandboxing) ·
  [Skills](https://code.claude.com/docs/en/skills) ·
  [Agent Teams](https://code.claude.com/docs/en/agent-teams)
- Repo: `progress/ESTADO.md`, `progress/ROADMAP.md`, `progress/LOG.md`, `progress/IDEAS.md`,
  `corpus/PROTOCOLO-LECTURA.md`, `corpus/anotaciones-pliegos.csv`, `corpus/pliegos-a-leer.csv`,
  `corpus/documentos-pliegos.csv`, `corpus/metrica.md`, `standards/contratos.md`,
  `research/02-oportunidad-mercado-espanol.md`, `research/04-veredicto-consejo.md`
