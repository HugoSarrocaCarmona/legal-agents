# 🧭 INFORME 5 — El vídeo de Eric Risco y dónde está legal-agents

**Fecha:** 23/11/2026 · **Pedido por Hugo:** extraer el vídeo, decir qué aplicar y qué no, y hacer
un alto para situar el proyecto: dónde estamos, qué viene después del anotador, a dónde lleva, y
qué otras vías existen.

> **Fuente.** «Antes de programar con IA en 2027, cambia esto», Eric Risco, 27:40, publicado el
> 23/11/2026. Desde el contenedor YouTube no dejó sacar nada; la base es la **transcripción
> automática que pegó Hugo**. **Fiabilidad media:** deforma los nombres propios —«Cloud Code»
> por Claude Code, «Lydia Holly» por Lydia Hallie, «Skill Baale» por Skill Veil, «barrace
> context» por `/context`— y no tiene puntuación fiable. Cada afirmación se ha contrastado con la
> **documentación oficial** que el propio vídeo enlaza.
>
> **La transcripción no se versiona.** Es el texto íntegro de un tercero, y las marcas de tiempo
> bastan para volver al vídeo.

---

## 0 · En cinco líneas

1. **La tesis del vídeo:** los modelos mejoran en cada versión, y el arnés que les ponemos encima
   tiene cada vez menos sentido. Hay que soltarles las restricciones de *proceso* y mantener solo
   barreras de **código** —hooks— para lo que no se puede deshacer. Lo demás son trucos para
   gastar menos contexto: menos herramientas, `CLAUDE.md` corto y sin gritos, skills para lo
   repetido y subagentes para repartir.
2. **Para legal-agents aplican cinco cosas, y las cinco son trabajo de Claude, no tuyo:**
   - fusionar ramas: las sesiones nuevas leen un `ESTADO.md` del 25/08;
   - adelgazar `CLAUDE.md` + `ESTADO.md`: 470 líneas en cada arranque, y se contradicen;
   - un hook que haga cumplir «nada se borra» en `Inputs/`;
   - una skill `cerrar-pliego`, creada al terminar el pliego 7 con el truco del propio vídeo;
   - una poda de conectores.

   Code Mode, sandbox, Agent Teams y automejora: no, por ahora.
3. **Situación:** 5 de 10 pliegos, 61 filas, 207 de 700 páginas. **Queda el 70 % de las páginas**
   y los cinco pliegos más largos. 39 de 61 filas son de admisión.
4. **Lo que todavía no se había dicho:** el esquema v2 no puede representar lo que estás
   encontrando. **Unas 32 de las 39 filas de admisión no caben en ninguna de las 16 materias**
   del vocabulario cerrado de `standards/contratos.md`, que solo cubre ejecución. Si el recuento
   final confirma admisión, lo siguiente no es la rúbrica sobre el esquema actual: es un v3.
5. **Lo que más falta no es técnico:** cero conversaciones con alguien del sector.

---

## 1 · El vídeo

### Quién habla y desde dónde

Eric Risco comenta la charla de Lydia Hallie (Anthropic, *Rethinking Claude Code Best
Practices*) y la mezcla con su experiencia. **Tiene un producto propio en el tema:** su
meta-harness `rsc-harness`, que menciona una decena de veces. No lo descalifica, pero lo sitúa:
varias recomendaciones están pensadas para quien programa aplicaciones a diario con varios
chats abiertos, no para un proyecto de extracción jurídica de una sola persona.

### Lo que afirma, y con qué lo respalda

| Min | Afirmación | Registro | Respaldo |
|---|---|---|---|
| 00:08 | Anthropic pasó de 2.500 a más de 30.000 cambios de código **al día** desde abril | Hecho de segunda mano | La charla de Hallie. Él mismo lo llama «fantasmada» al empezar, y su descripción corrige la fecha: mayo–septiembre |
| 01:48 | Code Mode gasta un 30–50 % menos de tokens con MCP | Hecho de segunda mano | Atribuido a Anthropic, sin fuente citada |
| 02:29 | Code Mode no siempre gana: va más lento y a veces da peor resultado | Hecho de segunda mano | Atribuido a Anthropic |
| 03:56 | Con 30–40 herramientas conectadas el modelo elige peor | Interpretación | «Después de hacer muchas pruebas»; sin datos |
| 07:20 | Escribir en mayúsculas o con IMPORTANT/NEVER empeora a los modelos actuales | Interpretación | Atribuido a los ingenieros de Anthropic y a su experiencia; sin datos |
| 08:13 | Si se puede sacar del código, no va en `CLAUDE.md` | Norma práctica | **Coincide con la documentación oficial** |
| 10:24 | `/doctor prompt-audit` señala instrucciones para modelos antiguos, rutas que ya no existen y ficheros que se contradicen | Descripción de herramienta | **Coincide con la documentación** («outdated or conflicting content») |
| 11:58 | Auto mode es el modo por defecto en cualquier versión | Hecho | **No coincide del todo:** según la documentación, `/doctor` *ofrece* ponerlo por defecto |
| 12:13 | Probado con 1.053 acciones peligrosas: las personas detectaron el 14 %, auto mode bloqueó más del 89 %, y la gente aprueba más del 97 % de los avisos | Hecho de segunda mano | Atribuido a Anthropic; no verificado |
| 14:33 | Un hook que sale con 0 deja seguir; con 2, para y explica | Hecho | **Coincide con la documentación** para `PreToolUse` |
| 19:27 | El sandbox protege también los `curl` que lanzan los hooks | Hecho | **Erróneo.** La documentación dice que los hooks corren *fuera* del sandbox, y la descripción del propio vídeo lo corrige |
| 20:00 | Un estudio de Microsoft: el 30 % de las tareas de programación repite algo ya hecho | Hecho | Cita sin referencia |
| 21:59 | Un orquestador que reparte a subagentes da una «ganancia de calidad brutal» | Experiencia propia | Ninguno más allá de ella |
| 26:02 | Un arnés que se mejora a sí mismo todavía no termina tareas complejas | Experiencia propia | Una prueba suya, más lo leído en Reddit y Twitter |
| 26:48 | Los arneses tendrán cada vez menos sentido con cada versión del modelo | Predicción | — |

**Lo que no cubre, y para legal-agents es lo principal: la verificación.** La charla de Hallie
tiene un capítulo entero sobre estrategias de verificación (10:53–14:00) y otro sobre CI y pull
requests (14:00–15:10). Eric no toca ninguno. En un proyecto donde el producto es acertar y
poder demostrarlo, ese es el tramo que más interesa. **Son tres minutos: velos desde casa**,
donde YouTube no bloquea. No los he visto, así que no puedo decir qué contienen.

### Capítulo a capítulo, y qué hacer en legal-agents

Hugo trabaja sobre todo en **local, en Windows**: eso decide varias respuestas.

#### 1.1 · Code Mode (00:41–03:19) — ❌ No, por ahora

- **Qué dice.** En vez de pedir datos a las herramientas uno a uno y acumularlos en el contexto,
  Claude escribe un pequeño script que hace las peticiones de una vez y analiza el resultado.
  Ahorra tokens, pero va más lento y a veces sale peor. Se activa con
  `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=1` antes de lanzar `claude`, y solo funciona en la terminal.
  En PowerShell: `$env:CLAUDE_CODE_EXPERIMENTAL_CODE_MODE = "1"`.
- **Matiz.** Eric lo presenta como «paralelizar» y dice que se pierde información cuando una
  llamada depende de otra. Según la documentación, el script *sí* puede encadenar llamadas. Lo que
  se pierde es que el modelo **razone** sobre el resultado intermedio antes de decidir la
  siguiente. En Windows exige además Git for Windows.
- **En legal-agents.** Tu cuello de botella es la **lectura humana de PDF**, no el número de
  llamadas. Reconsiderarlo cuando toque procesar los 30–40 pliegos del Gold.

#### 1.2 · No conectes herramientas por si acaso (03:19–05:33) — ✅ Sí, diez minutos

- **Qué dice.** Cada herramienta conectada carga su nombre y su descripción en *cada* petición.
  Con muchas, el modelo elige peor y puede perder diez minutos en una que no necesitaba. Dos
  consejos: mirar con **`/context`** qué ocupa el contexto, y tener activos solo los MCP que cada
  proyecto necesita.
- **En legal-agents.** Esta sesión arrancó con decenas de conectores —Gmail, Calendar, Drive,
  Indeed, Amplitude, Atlassian, Figma, Slack…— y una veintena que ni siquiera conectaban.
  **Ninguno sirve a este proyecto.** En local, primero `/context` para ver qué te cargan a ti, y
  después `/mcp` para desactivarlos en este proyecto. El MCP de legislación de
  `progress/IDEAS.md` entra solo cuando toque anclar contra el BOE, y después de verificar de
  dónde saca los datos.

#### 1.3 · Qué sobra en `CLAUDE.md` · `CLAUDE.md` como mapa · `/doctor` (05:33–10:48) — ✅ Sí, es lo que más aplica

- **Qué dice.** Tres cosas:
  - **Dejar de gritar.** Nada de mayúsculas, ni de IMPORTANT o NEVER. Con los modelos actuales,
    dice, el modelo «se obsesiona», hace más llamadas y rinde peor. Y las restricciones que
    tiran unas de otras acaban rompiendo algo: el meme de la persiana.
  - **Una nota en la nevera, no un manual.** Lo que el modelo puede sacar del código no va. Él
    solo pone dónde están las herramientas y el índice de la documentación.
  - **`/doctor prompt-audit`** al cambiar de modelo. Marca instrucciones pensadas para modelos
    viejos, rutas que ya no existen y ficheros que se contradicen.
- **En legal-agents.**
  - **Gritar, no gritas.** `CLAUDE.md` tiene tres palabras de énfasis en mayúsculas («SIEMPRE»,
    «OBLIGATORIO», «NO»), y el agente, ninguna. Lo que abunda es la negrita: 79 tramos en las 223
    líneas de `progress/ESTADO.md`. No es lo que critica el vídeo, pero es la misma inflación: si
    todo está resaltado, nada lo está. Prioridad baja.
  - **El mapa ya lo tienes**, y bien hecho: `CLAUDE.md` remite a `progress/ESTADO.md` y a
    `standards/`. Lo que falla es el peso: `CLAUDE.md` tiene **247 líneas** y `ESTADO.md` **223**,
    pese a decir de sí mismo que «se mantiene corto a propósito». Son **470 líneas** en cada
    arranque, cuando la documentación fija menos de 200 para `CLAUDE.md`.
  - **La persiana ya la tienes.** `CLAUDE.md` enuncia la línea activa como *riesgo de ejecución*;
    `progress/ESTADO.md` dice que el encuadre está abierto y que los datos apuntan a *admisión*.
    `/doctor prompt-audit` lo marcaría en su tercera comprobación.
  - **Fuera del mapa sobra:** la nota histórica «Delimitado el 04/10/2026», que pertenece a
    `progress/LOG.md`, y las secciones genéricas sin efecto —«Organización», «Objetivo final»—.
    Y `progress/LOG.md` no se actualiza desde el **17/09**: los cinco pliegos solo constan en
    `ESTADO.md`.
  - **Tu propia regla ya lo pedía.** `CLAUDE.md` § «Revisar este arnés cuando cambie el modelo»
    es exactamente lo que Eric hace con `/doctor prompt-audit` en cada versión nueva. Y el 04/10
    ya aplicaste su lógica sin conocerla, al delimitar la regla de salida JSON que se incumplía
    siempre.
- **Lo que no se toca.** «No inventar» y «`null` antes que inferencia» no son estilo: **son el
  producto**. Se quitan las mayúsculas, no la regla.

#### 1.4 · Auto Mode y permisos (10:48–13:17) — ✅ Sí, con una sola regla dura

- **Qué dice.** Antes había dos modos: aprobarlo todo sin mirar, o que te lo preguntara todo.
  Eran el mismo, porque nadie lee el aviso número cincuenta. Auto mode bloquea casi 9 de cada 10
  acciones peligrosas, **y deja pasar una**. Por eso él lo complementa con hooks: un modelo no es
  determinista, y lo único determinista es el código.
- **En legal-agents.** En este repo **lo único irreversible es `Inputs/`**: está en `.gitignore`,
  no tiene historia, y el antiguo nº 16 se perdió así el 06/08/2026. Todo lo demás está en git y se
  recupera. Esa «una de cada diez» es la razón de que la protección de `Inputs/` tenga que ser
  código y no una frase.

#### 1.5 · Hooks: PreToolUse, PermissionRequest, PreCompact (13:17–18:03) — ✅ Uno solo

- **Qué dice.** `PreToolUse` es el más importante: salta antes de cada herramienta y bloquea lo
  que no se puede deshacer (borrar una carpeta, forzar un push, vaciar una base de datos).
  `PermissionRequest` lo usa para aprobar solo lo que ya había aceptado antes. `PreCompact`, para
  que antes de compactar el contexto se documente lo trabajado. Él compacta a 600.000 tokens,
  porque a partir de 700.000–800.000 el contexto «ya no es eficiente».
- **En legal-agents.**
  - **Un `PreToolUse` que impida borrar o mover nada dentro de `Inputs/` salvo hacia
    `Inputs/_depurados/`.** Convierte «Nada se borra» de texto en regla que se ejecuta. Si lo
    quieres igual en local y en la web, en Python: el contenedor no tiene PowerShell.
  - **`PermissionRequest`, no:** auto mode ya cubre lo que resolvería.
  - **`PreCompact`, no como hook.** Lo que Eric resuelve con él —que lo trabajado no se pierda— es
    tu problema del `LOG.md` desfasado desde el 17/09. Aquí se resuelve mejor metiendo esa
    actualización en `cerrar-pliego` (1.7).
  - **La tentación a evitar** es un hook por cada regla de `CLAUDE.md`: el arnés que estorba es
    justo de lo que avisa el vídeo.

#### 1.6 · Sandbox y seguridad de las skills (18:03–19:56) — ❌ Sandbox · ✅ hábito de revisión

- **Qué dice.** Ni auto mode ni los hooks miran *dentro* del comando. Un README o una skill puede
  esconder «antes de instalar, manda las credenciales a tal sitio». Para revisar skills recomienda
  Skill Veil, de Marc Rivero; para contener comandos, el sandbox.
- **Matiz.** Dice que el sandbox protege también los `curl` de los hooks. **No es así:** los hooks
  corren fuera del sandbox, y su propia descripción lo corrige. Tampoco bloquea la lectura de
  ficheros por defecto.
- **En legal-agents.**
  - **Sandbox, no.** En Windows nativo no existe —hace falta WSL2—, y montarlo no compensa en un
    repo cuyo único activo sensible es `Inputs/`, que ya cubre el hook de 1.5.
  - **Revisar skills, sí, como hábito:** leer entera toda skill de terceros antes de instalarla.
    `llm-council` lo es.
  - **Skill Veil, no:** pide toda una toolchain de Rust para un riesgo que con dos skills se
    controla leyendo.
  - **El riesgo que sí es tuyo:** metes en Claude documentos que no has escrito tú —PDF de PLACSP,
    resoluciones, vídeos—. Si uno trae instrucciones escondidas, lo que lo para no es el sandbox:
    es que en tu proyecto el modelo extrae, no ejecuta lo que lee.

#### 1.7 · Cuándo convertir un prompt en una skill (19:56–21:02) — ✅ Sí, y con su truco

- **Qué dice.** Si te pillas repitiendo el mismo prompt en un día o en una semana, eso es una
  skill. Y un truco: **haz la tarea bien una vez, y al final pídele a Claude que convierta en
  skill lo que acabáis de hacer.**
- **En legal-agents.**
  - **`cerrar-pliego`, creada así.** Lo has hecho cinco veces a mano —los commits «Cerrar el
    pliego N»—: filas al CSV, columnas de `corpus/pliegos-a-leer.csv`, recuento por `momento` en
    `progress/ESTADO.md`, commit. **Al cerrar el pliego 7, pide la skill a partir de esa misma
    sesión**, no en abstracto. Que incluya poner al día `progress/LOG.md`, y que el recuento lo
    haga un script en vez de a ojo. No abre ningún frente: es el final de una tarea que ya
    tienes.
  - **Aplicar tu propia regla de retirada.** `RUN`, `DEBUG`, `IMPROVE` y `run_once` son de la
    línea aparcada de sentencias y **se cargan en cada sesión**: aparecen en la lista de skills
    disponibles. `CLAUDE.md` dice que las de una línea congelada se reescriben o se retiran. Al
    revés, `ver-video` vive en una rama sin fusionar, y por eso esta sesión no la veía.

#### 1.8 · Subagentes: repartir trabajo y modelos (21:02–23:17) — ⏳ Más adelante, con su límite

- **Qué dice.** Un solo chat con el modelo más capaz como orquestador, que reparte tareas ya
  definidas a subagentes en segundo plano y revisa lo que devuelven. Con una regla: **como mucho
  tres iteraciones, y si a la tercera no está, al humano.** Pedir «hasta que esté perfecto» es un
  bucle que quema tokens sin fin. Y con un aviso de coste: sin un plan alto, lanzar subagentes
  puede agotar en diez minutos el límite de cinco horas.
- **En legal-agents.** Toca en el paso 7 (`pliego_agent`). Dos cosas aprovechables ya:
  - **El tope de tres iteraciones** es la regla que le falta al ciclo `DEBUG` → `IMPROVE` si
    algún día se reactiva.
  - **El campo de modelo del subagente** es el mecanismo para cumplir la condición de
    `progress/IDEAS.md` sobre pre-anotar el Gold: «modelo distinto del evaluado».

#### 1.9 · Licencias y Agent Teams (23:17–24:08) — ❌ No

- **Qué dice.** Hay un modo experimental (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) que hace lo
  mismo de forma nativa: un orquestador que lanza equipos de agentes.
- **En legal-agents.** Resuelve un problema de equipo. Tienes un solo frente activo y lo lees tú.

#### 1.10 · ¿Puede un harness mejorarse solo? (24:08–26:29) — ❌ No, y con un dato curioso

- **Qué dice.** Su experimento: `CLAUDE.md` vacío, tres herramientas —terminal, leer y escribir
  ficheros— y una tarea. El agente debía construirse sus propias herramientas, skills, hooks,
  tests y notas para el futuro. La tarea era **una herramienta que entienda un vídeo** por sus
  fotogramas y su audio. Montó bastante —hooks, un modelo de transcripción—, se dio cuenta de
  que estaba en bucle, creó un hook para pararse a sí mismo, y **no terminó**. Conclusión suya:
  para webs pequeñas sí; para tareas complejas, todavía no.
- **El dato curioso.** Es exactamente la herramienta que tu repo ya tiene: `tools/video/`, en la
  rama `claude/install-claude-video-plugin-p8lgrn`. Se construyó con Claude, pero **dirigido por
  ti y con un criterio escrito**, y está terminada, con varios arreglos documentados que no eran
  triviales. Es una anécdota contra otra (n = 1 cada una), no una prueba. Pero apunta al mismo
  sitio que tu experiencia.
- **En legal-agents.** La Fase 5 de `progress/ROADMAP.md` («ajuste automático de prompts») choca
  con la lección que ya pagaste el 05/08: corregir reglas mirando los fallos **gastó el test**.
  Una automejora sin conjunto ciego reservado es sobreajuste automatizado. Se queda congelada
  hasta que exista ciego-2.

#### 1.11 · Qué cambiar de cara a 2027 (26:29–27:40) — ⚠️ Aplicar con una distinción

- **Qué dice.** Skills que antes iban bien ahora hacen la tarea peor. Encorsetar al modelo tiene
  cada vez menos sentido: «hay que quitarle las barreras, tiene que volar». Pero siguen haciendo
  falta barreras **de código** para ciertas acciones.
- **En legal-agents hay dos clases de restricción, y el consejo solo vale para una.**
  - **Restricciones de proceso**, sobre *cómo* trabaja el modelo: el «pipeline obligatorio» en
    orden estricto de `standards/sentencias.md`, los pasos prescritos de `RUN`. Aquí el consejo
    aplica, y tu `CLAUDE.md` ya lo dice: «pasos intermedios que el modelo ya hace solo».
    Candidatas a soltar.
  - **Restricciones de verdad**, sobre *qué cuenta como correcto*: no inventar, `null` antes que
    inferencia, `base_normativa` transcrita del BOE. Estas no son arnés: **son el producto**. Y
    no se pueden convertir en hook, porque un script no sabe si una cita es falsa. Lo que las
    hace cumplir es la **evaluación** —el Gold y la métrica—, que es justo lo que el vídeo no
    cubre.

  Un programador puede soltar al modelo y mirar si la web funciona. Un extractor jurídico no
  puede «volar» sobre la verdad de una cita.

### Paso a paso de lo aplicable, en orden

| # | Qué | Quién | Por qué en este orden |
|---|---|---|---|
| 1 | **Fusionar ramas.** PR de `claude/video-review-uow2yt` a `main`; traer `tools/video/` y la skill `ver-video`; dejar `claude/legal-automation-research-iisyip` sin fusionar (son 5 commits de la línea anterior al giro del 09/09, y siguen en remoto) | Claude; tú apruebas | Es el único fallo que **rompe tu punto de entrada**: `main` va 21 commits por detrás, se quedó en el 25/08, y una sesión que arranca desde ahí lee un `ESTADO.md` sin anotador, sin pliegos y sin giro. Esta sesión arrancó así |
| 2 | **Adelgazar.** `/doctor prompt-audit` en local; `CLAUDE.md` por debajo de 200 líneas y `ESTADO.md` por debajo de 80; historia al `LOG.md`; resolver la contradicción ejecución/admisión; retirar o marcar los cuatro comandos de sentencias | Claude propone, tú decides | Cada sesión paga esas 470 líneas, y la contradicción confunde al modelo |
| 3 | **Proteger `Inputs/`** con una regla `deny` o el hook de 1.5 | Claude | Es lo único irreversible del repo |
| 4 | **Skill `cerrar-pliego`**, que incluya el `LOG.md` | Tú la pides al cerrar el pliego 7; Claude la escribe | El truco del vídeo: se construye desde una ejecución real |
| 5 | **Podar conectores:** `/context` y después `/mcp` | Tú, 10 min | Menos ruido en cada sesión |
| — | Ver el tramo de verificación de la charla de Hallie (10:53–14:00) | Tú, 3 min | Es lo que el vídeo de Eric no cubre y lo que más importa aquí |

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
   que es lo que pide el protocolo. **Al cerrarlo, pide la skill `cerrar-pliego`** a partir de
   esa sesión.
2. **En paralelo, y sin quitarte tiempo:** Claude hace los pasos 1–3 de la sección 1 y tú los
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

- **Si quieres que Claude haga ahora los pasos 1–3 de la sección 1.** El 1 implica abrir un PR a
  `main`.
- **La decisión de encuadre**, que es tuya y se toma al contar, no antes.

---

## Fuentes

- Vídeo: <https://www.youtube.com/watch?v=7_dEsn4EUQ4> — transcripción automática pegada por
  Hugo, más los metadatos y capítulos
- Charla de Lydia Hallie, *Rethinking Claude Code Best Practices*:
  <https://www.youtube.com/watch?v=vlfCjWuv4es> — solo metadatos y capítulos
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
  `standards/sentencias.md`, `research/02-oportunidad-mercado-espanol.md`,
  `research/04-veredicto-consejo.md`
