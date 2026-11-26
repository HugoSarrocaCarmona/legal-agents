# 📜 Project Log

## [23/11/2026] — 🧭 Alto en el camino: informe 5 y poda del arnés

Hugo pidió parar para situarse: analizar el vídeo de Eric Risco «Antes de programar con IA en
2027, cambia esto» —que comenta la charla de Lydia Hallie, de Anthropic—, decidir qué aplicar al
repo y ver qué viene después del anotador.

### ✅ Hecho

- **`research/05-harness-2027-y-situacion.md`** — el vídeo capítulo a capítulo, con cada
  afirmación contrastada con la documentación oficial; la situación del proyecto; los pasos
  después del anotador, y otras vías posibles
- **Ramas reunidas.** La rama de trabajo junta todo lo hecho desde el 25/08 y la herramienta de
  vídeo (`tools/video/` y la skill `ver-video`), que vivía en otra rama. Se propone a `main` por PR
- **`progress/ESTADO.md`, de 223 a 76 líneas.** Lo histórico ya estaba en este LOG (09/09, 15/09
  y 17/09), salvo el avance de los pliegos, que pasa a la entrada de 19/10–10/11
- **`CLAUDE.md`, de 247 a 195 líneas.**
  - Resuelta una contradicción: decía «riesgo de ejecución» y «línea congelada», mientras
    `ESTADO.md` decía encuadre abierto y línea aparcada.
  - Fuera las mayúsculas de énfasis, la nota histórica del 04/10 (que pasa a este LOG) y las
    secciones sin efecto («Organización», «Objetivo final»).
  - Nuevo: el mapa de herramientas, `/doctor prompt-audit` y la distinción entre restricciones
    de proceso y de verdad.
- **`.claude/settings.json`** — reglas `deny` que impiden a Claude borrar, crear o sobrescribir
  nada en `Inputs/`, y lanzar `git clean -x`, que borraría los ficheros ignorados. Mover dentro de
  `Inputs/` pide confirmación.
  - **Comprobado en el contenedor:** quedan bloqueados `rm`, `git clean -x`,
    `touch`/`mkdir`/redirección y la herramienta de escritura. Leer `Inputs/` y pasar
    `Inputs/pliegos` como argumento a un script siguen funcionando.
  - **Sin comprobar:** las reglas de PowerShell, porque aquí no hay PowerShell.
- `scripts/placsp/__pycache__/` deja de versionarse
- **Retirados los cuatro comandos de sentencias** (`RUN`, `DEBUG`, `IMPROVE`, `run_once`), a
  petición de Hugo. Pertenecían a la línea aparcada y se cargaban en cada sesión, que es lo que
  `CLAUDE.md` manda retirar. Siguen en git, recuperables con `git show f64a8ac:.claude/commands/RUN.md`.
  Con `RUN` se va la regla de no sobrescribir outputs existentes: si la línea se reactiva, hay
  que decidir dónde vive

### ❌ Problemas encontrados

- **`main` llevaba parado desde el 25/08.** Una sesión que arrancara desde ahí leía un
  `ESTADO.md` sin el giro a pliegos, sin los datos de PLACSP y sin el anotador. Esta sesión
  arrancó así
- `ESTADO.md` había crecido a 223 líneas pese a declararse corto a propósito, y este LOG no se
  tocaba desde el 17/09
- **Hallazgo de fondo:** las 16 materias del vocabulario cerrado de `standards/contratos.md` son
  todas de ejecución. Unas 32 de las 39 filas de admisión no caben en ninguna: si el recuento
  confirma admisión, hace falta un esquema v3 antes que la rúbrica

### 💡 Aprendizajes

- **Para hacer cumplir una regla no hace falta un hook.** Las reglas `deny` de permisos lo hacen
  sin depender de que haya un intérprete instalado, cosa que en Windows no está garantizada. Y un
  hook que no arranca deja pasar la acción
- **Las reglas `deny` protegen contra el error, no contra la intención.** Un script que borre por
  su cuenta no lo detectan, y no está comprobado que cubran un `cd Inputs && rm x`
- **Hay restricciones de proceso y restricciones de verdad.** Las primeras se pueden soltar
  cuando el modelo mejora; las segundas son el producto, y lo que las hace cumplir es la
  evaluación

### 🔜 Siguiente paso

- **Pliego 7.** Al cerrarlo, pedir la skill `cerrar-pliego` a partir de esa misma sesión, y que
  incluya poner al día este LOG
- Pendiente de arnés: probar en local las reglas de PowerShell

---

## [19/10–10/11/2026] — 📖 Paso 5: cinco de los diez pliegos, leídos y anotados

Hugo lee a mano los pliegos de la población «un solo licitador, y fue excluido» y anota cada
riesgo con el protocolo de `corpus/PROTOCOLO-LECTURA.md`. Las filas se anotan en el anotador y se
exportan a `corpus/anotaciones-pliegos.csv`.

### ✅ Hecho

| Pliego | Expediente | Cerrado | Filas | Lo propio del documento |
|---|---|---|---|---|
| 1 | ASEPEYO, CP00004/2025, suministros | 19/10 | 8 | Los umbrales de solvencia no están en el PCAP, sino en un fichero de anexos aparte |
| 6 | Ayuntamiento de Llíria, 1401Q/2025, suministros | 20/10 | 9 | Plantilla municipal sin cuadro de características |
| 9 | Ayuntamiento de Briviesca, 922/2025, obras | 25/10 | 15 | Primero de obras. La oferta se presenta en la plataforma de la Diputación de Burgos, no en la PLACSP |
| 10 | Ayuntamiento de Gijón, 73234W/2024, servicios | 27/10 | 11 | Tres documentos —CCP, pliego modelo y PPT—; el CCP y el modelo divergen en penalidades y en la base de la garantía |
| 2 | TRAGSA, TSA0079889, servicios | 10/11 | 18 | Primer contrato de régimen privado: Tragsa es medio propio, y efectos y extinción se rigen por el derecho privado (cl. 23) |

### 🔍 La señal

- **`momento`: 39 de admisión, 21 de ejecución y 1 de valoración.**
- **17 de las 39 de admisión caen entre la propuesta de adjudicación y la formalización:** 4 del
  pliego 1, 3 del 6, 3 del 9, 2 del 10 y 5 del 2. En el pliego 2 el requerimiento pide una póliza
  que no aparece en la solvencia: el requisito solo se descubre al ganar
- La única fila de `valoracion` (pliego 10, umbral mínimo de juicio de valor) tiene como
  consecuencia la exclusión: funciona como un riesgo de admisión
- Riesgo nuevo en el pliego 2: el contrato cae si la Administración retira el encargo a Tragsa
  (`quien_controla` = `tercero`)

### ⚖️ Decisiones

- **Regla de severidad común, fijada el 20/10:** pierdes el contrato o te prohíben contratar =
  `alta`; pierdes dinero acotado = `media`; molestia = `baja`.
  - Con ella se reajustaron tres filas del pliego 1 (plan de igualdad, omisiones y errores, UTE)
    de `media` a `alta`.
  - Tras el repaso de Hugo cambiaron dos más: en el pliego 1, el 70 % de la anualidad media pasó
    de `media` a `alta`; en el pliego 6, el precio fijo pasó de `organo` a `tercero` en
    `quien_controla`.

### ⚠️ Cautelas

- **Recuento:** 5 filas de admisión del pliego 9 salen de una sola lista (cl. 14). Contadas como
  una, la admisión baja a 35 de 57
- **Método:** en el pliego 9 Claude redactó el criterio de 5 filas; en el 10 reescribió
  `como_se_falla` en 8 de las 11 filas y rehízo la de la garantía; en el 2 añadió 5 filas de
  ejecución y reescribió `como_se_falla` en 9 de las 13 de Hugo. La detección de las filas de
  admisión es de Hugo; al agrupar hay que tenerlo presente
- **`severidad_intuitiva` ya no discrimina:** 54 de 61 filas son `alta`, y las 18 del pliego 2 lo
  son todas. Se revisa al inducir la rúbrica, no antes

---

## [04/10/2026] — 🔧 Protocolo con marcadores de riesgo, y primera revisión del arnés

- **`corpus/PROTOCOLO-LECTURA.md`** — cuatro marcadores de riesgo, localizables por
  vocabulario: verbos de consecuencia, plazos cortos, reenvíos y palabras de discrecionalidad. Y
  un orden de barrido: cuadro, admisión, ejecución, anexos. El protocolo decía qué preguntar a una
  cláusula pero no dónde mirar, y eso bloqueó el primer intento de lectura
- **`CLAUDE.md` — la regla de salida JSON, delimitada.** Decía «todas las respuestas deben ser
  JSON válido, nunca devolver texto libre», sin ámbito. Se escribió cuando el repo era solo el
  extractor y se incumplía en toda conversación desde entonces. Queda limitada a la salida de un
  agente que procesa un documento. **Una regla que se incumple siempre no es una regla: es ruido
  que resta autoridad a las que sí rigen**
- **`CLAUDE.md` — el ritual «Revisar este arnés cuando cambie el modelo»**, tomado del vídeo de
  Eric Risco «Así trabajo ahora con inteligencia artificial: menos pasos, más criterio»
  (28/09/2026)

---

## [18/09/2026] — 📥 Los diez pliegos, localizados y verificados

- **`scripts/placsp/extrae_documentos.py` y `corpus/documentos-pliegos.csv`** — los 69
  documentos de los 10 expedientes, con URL de descarga directa y las páginas de cada PCAP y PPT
- **Los 20 PCAP y PPT llevan texto extraíble; ninguno está escaneado.** No hace falta OCR en esta
  fase. Cierra lo que quedaba del paso 4
- **Estimación corregida.** «35–45 minutos por pliego» se escribió antes de mirar los documentos.
  Los diez PCAP suman 700 páginas, de 25 a 158: entre 12 y 15 horas, no siete. Orden de lectura:
  primero los cuatro cortos
- Dos trampas documentadas en el protocolo: la página índice «Documento de Pliegos» no es un
  pliego, y en `GetDocumentByIdServlet` el parámetro que identifica el documento es
  `DocumentIdParam`
- `CLAUDE.md` — citar siempre los ficheros por su ruta del repo, a petición de Hugo

---

## [17/09/2026] — 📊 Primer código del proyecto: se cierra el bloqueo nº 0 con datos

Se ejecutó el paso 1 de la fase 2. Todo 2025 de la sindicación de la PLACSP —12 ficheros
mensuales, 1,7 GB comprimidos, **933.611 publicaciones**— descargado y procesado con código
propio. **Es el primer software ejecutable del repositorio**, después de una semana produciendo
documentos.

### ✅ Hecho

- **`scripts/placsp/`** — pipeline completo sin dependencias: `descarga.sh`,
  `parse_resultados.py` (XML CODICE → CSV por *streaming*), `codigos.py` (listas CODICE
  transcritas de los `.gc` oficiales), `analiza_desiertos.py` y `selecciona_pliegos.py`
- La extracción y el juicio van en **ficheros separados** a propósito: si el resultado sorprende,
  hay que poder saber cuál de los dos falló
- **`ESTADO.md`** — bloqueo nº 0 cerrado con cifras; tarea siguiente reescrita

### 🔍 Lo que dijeron los datos

Sobre 207.145 resultados (expediente, lote) con fecha en 2025:

- **18.808 declaraciones de desierto**, el **9,08 %** de los resueltos
- **72,0 % — no se presentó nadie.** La causa es anterior al pliego y ninguna herramienta de
  lectura la toca
- 28,0 % hubo ofertas y aun así quedó desierto. De esos, **el 69,3 % tenía un solo licitador, que
  fue excluido**: 3.651 casos, el 19,4 % de todos los desiertos. En el 64,5 % todas las ofertas
  eran de pymes

**La premisa del informe 2 queda parcialmente falsada**: es falsa para dos de cada tres desiertos.
La línea activa sobrevive, pero apuntando a una población mucho más estrecha y mejor definida.

**Reencuadre pendiente de decisión (de Hugo, no de Claude):** el proyecto se enunció como *riesgo
de ejecución* —«¿qué asumo si gano?»—. Los datos apuntan al *riesgo de admisión* —«¿por qué han
tirado mi oferta?»—. Se decide después de leer los diez pliegos.

### ❌ Errores corregidos, ambos propios

- **Error en el primer script: el dinero salía multiplicado.** `importe_sin_iva` es el presupuesto
  del expediente entero y se repite en la fila de cada lote; sumar por filas daba **6.233 M€ para
  un solo mes**. Corregido sumando por expediente único y separando los expedientes con lotes como
  cota superior. Es exactamente la clase de cifra que habría acabado en un informe
- **El consejo se equivocó y se da por corregido:** dijo que PLACSP publica el motivo de cada
  desierto. **Falta en el 55 %.** Lo que sí está en el 100 % es `ReceivedTenderQuantity`, y es el
  campo que decide. El análisis se apoya en el número obligatorio, no en el texto libre

### 📌 Anotado, no resuelto

- El titular de «9.819 concursos desiertos» era correcto en magnitud —son **11.088 expedientes
  desiertos por completo**— pero su presupuesto suma **2.880 M€**, no los 4.011 M€ citados
- **Patrimonial (31,2 %), concesión de servicios (26,3 %) y administrativo especial (25,2 %)**
  tienen tasas de desierto tres veces superiores a obras, servicios y suministros. Quedan fuera
  del corpus por regirse por la LPAP, pero la anomalía queda registrada

---

## [15/09/2026] — ⚖️ Auditoría de la cadena de consejo, y reordenación de la fase 2

Se instaló `llm-council` (`.claude/skills/llm-council/`) y se sometió a juicio **la propia cadena
de recomendaciones de Claude** de la última semana: el giro a pliegos, la métrica, la especialidad
recomendada y la secuencia empleo→emprendimiento. Veredicto íntegro en
[`research/04-veredicto-consejo.md`](../research/04-veredicto-consejo.md).

### ✅ Hecho

- **`corpus/metrica.md`** — umbral **F1 ≥ 0,95 suspendido**. Fijar una cifra sobre un catálogo
  que no existe no mide nada. Se fijará mirando la dispersión real de los datos. Sigue vigente el
  fallo duro: un solo flag con `base_normativa` falsa bloquea la versión
- **`standards/contratos.md`** — **la rúbrica se induce, no se deduce**. Antes: escribir el
  catálogo desde la LCSP y después anotar. Ahora: leer diez pliegos a mano, anotar todo riesgo
  que aparezca, y solo entonces anclar cada uno a su artículo. El catálogo sigue cerrado y la
  `base_normativa` se sigue transcribiendo del BOE — cambia de dónde sale la lista, no el rigor
- **`standards/contratos.md`** — añadido el **TACRC** como fuente de los flags `valorativo`
- **`ROADMAP.md`** — pasos 4 y 5 intercambiados: **PLACSP pasa del puesto 9 al 4**
- **`ESTADO.md`** — tarea siguiente reescrita, tercer bloqueo abierto, corrección sobre sentencias

### ❌ Problemas encontrados — todos en trabajo propio

- **La premisa de la línea activa nunca se verificó.** «9.819 concursos desiertos **porque** las
  pymes no pueden con la complejidad del pliego» se escribió como «causa identificada» y era una
  inferencia de fuente secundaria. Si el motivo real es precio inviable o falta de financiación,
  la tesis del producto cae. **Nuevo bloqueo nº 0**
- **El TACRC estaba mal clasificado.** El informe 2 dio por cerrada «la ley» como fuente sin
  distinguir jurisdicción de doctrina administrativa. Las resoluciones del TACRC y de los
  tribunales autonómicos son abiertas y sin prohibición de uso comercial
- **La línea de sentencias se congeló con un argumento mal aplicado.** El CENDOJ prohíbe descarga
  masiva y uso comercial; no prohíbe leer. Medir generalización exige veinte o treinta sentencias
  leídas a mano, que sí está permitido. Se confundió «no se puede comercializar» con «no se puede
  medir». Pasa de *congelada* a *aparcada*
- **Tres pliegos no son un corpus**, y bajar 200 es una tarde. Que no ocurriera mientras se
  escribían cuatro documentos es el diagnóstico entero

### 💡 Aprendizajes

- **Un dato que sostiene una tesis se verifica antes de construir sobre él, no después.** Es la
  misma regla que el proyecto aplica a `base_normativa` y no se aplicó a sí mismo
- **Una taxonomía deducida de la ley recoge lo que la ley regula; una inducida de documentos
  recoge lo que los documentos hacen.** Solo la segunda mide algo real
- **El consejo aportó valor donde no se esperaba.** Los cinco asesores convergieron en el mismo
  remedio equivocado —«haz diez llamadas»—. El hallazgo que cambia la semana —que PLACSP publica
  el motivo de cada desierto, así que es una consulta y no una entrevista— apareció **solo en la
  ronda de revisión cruzada**, y apareció cinco veces
- **Y su límite:** cinco asesores del mismo modelo comparten sesgos. La unanimidad del consejo no
  es evidencia externa. Sigue sin haber una sola persona real consultada

### 🔜 Siguiente paso

- **Descargar los datos abiertos de PLACSP y responder por qué quedaron desiertos los 9.819
  concursos.** Una tarde. Es software, no un documento. Produce el corpus y verifica la premisa a
  la vez — y puede salir mal, que es lo que ningún paso de la última semana podía

---

## [09/09/2026] — 🧭 Giro a pliegos: de analizador de contratos a analizador de riesgo de ejecución

Cambio de rumbo del proyecto. La fase 2 deja de ser un «Contract Analyzer» genérico sobre tres
regímenes y pasa a responder **una sola pregunta, desde la posición del licitador**: *¿qué me
puede costar dinero si gano este contrato público?*

### 🧭 Qué lo ha motivado

El giro no sale de una intuición sino de dos análisis encadenados, ambos en
[`research/`](../research/).

**Primero, un marco.** El análisis del mercado global de IA legal (más de mil empresas, 32 casos
de uso, 8 categorías) deja una idea aprovechable: **toda herramienta legaltech razona sobre una
de cinco fuentes de datos, y la fuente —no el modelo— es la barrera de entrada.** El modelo es
una *commodity*; el corpus, no.

**Después, ese filtro aplicado a España.** De las cinco fuentes, cuatro están cerradas para este
proyecto:

| Fuente | Situación en España |
|---|---|
| La ley misma | **Cerrada.** El CENDOJ no tiene API, prohíbe la descarga masiva y el uso comercial, y ha desplegado CAPTCHA. El corpus con valor es de cuatro editoriales que ya tienen su capa de IA encima |
| Conocimiento del despacho | Exige que un despacho abra su archivo: confianza, secreto profesional, art. 28.3 RGPD |
| Prueba del caso | Datos personales de terceros, secreto profesional, Circular 3/2026 del CGAE, Anexo III del Reglamento de IA |
| Datos operativos | Ocupado por Aranzadi, Lefebvre, Sepín y Clio-vLex. Es integración, no criterio jurídico |
| **Internet abierto** | **Abierta.** BOE, **PLACSP**, BORME, CNMV, DOUE |

**El único cuadrante viable es el quinto, y su mayor corpus jurídico-económico es la
contratación pública:** más de 201.000 expedientes y 180.600 M€ licitados en 2025, con 9.819
concursos desiertos —4.011 M€ paralizados— porque la complejidad de los pliegos ha crecido por
encima de la capacidad administrativa de las pymes. Datos abiertos, destinatario que paga y no
es abogado, sin datos de cliente y por tanto fuera del Anexo III y de las obligaciones de
encargo de tratamiento.

**Y una razón que pesa tanto como las de mercado:** `standards/contratos.md` **ya tenía escrita**
la taxonomía de riesgo administrativo —penalidades, garantías, revisión de precios, *ius
variandi*, resolución, subcontratación, plazos de pago— y la vía A del corpus **ya era PLACSP**.
El giro no abre un frente nuevo: reconoce hacia dónde apuntaba el repo sin haberlo dicho.

### 🔓 El hallazgo técnico: por qué el giro además desatasca la fase

`risk_flags` llevaba semanas sin métrica posible, y con ello bloqueada la rúbrica, el Gold y la
evaluación. **La causa no era la dificultad del campo: era que no es un campo.**

- Los flags que afirman **divergencia respecto de la LCSP** tienen respuesta única y se
  comprueban contra la ley.
- Los que afirman **desproporción dentro de lo legal** son juicio y no la tienen.

Esa frontera no existía mientras el corpus era de consumo: **el control de abusividad del
TRLGDCU es valorativo casi por entero** —el «desequilibrio importante» no tiene umbral—. La
LCSP, en cambio, **fija cifras**: 10 % y 50 % en penalidades (art. 192), 0,60 € por 1.000 € y
día (art. 193), 5 % y 10 % en garantías (art. 107), 20 % y 50 % en modificaciones (arts.
204–205), 30 + 30 días en pagos (art. 198).

**Consecuencia: la mitad de `risk_flags` pasa a admitir la misma métrica exacta que dio 315/315
en `ecli`.** El problema de medición no desaparece — se reduce a la mitad valorativa, que es
donde de verdad estaba.

### ✅ Hecho

- **`corpus/metrica.md`** — paso 1 de la fase 2, que era el bloqueo. `risk_flags` se parte en
  `normativo` (métrica exacta, umbral F1 ≥ 0,95) y `valorativo` (P/R con F₂, que pondera doble
  no omitir). **Se reportan por separado; agregarlos está prohibido.** Fija además unidad de
  medida (la cláusula, con intervalos remuestreados por documento), emparejamiento por `id` +
  ancla, `severity` como métrica secundaria, tres fallos duros y tamaños mínimos con cifra
- **`standards/contratos.md` v2** — ámbito operativo en `regimen = administrativo`; `risk_flags`
  incorpora `clase`, `base_normativa`, `clausula_ref` y `materia`; `missing_clauses` exige
  `base_normativa`; vocabulario cerrado de **16 materias** con su ancla en la LCSP verificada
  contra el texto consolidado del BOE
- **Regla nueva del régimen administrativo** — la prerrogativa de la Administración no es un
  riesgo, es el régimen. Solo son riesgo la divergencia de la ley, la omisión de lo que exige y
  la desproporción dentro de lo legal
- **Alcance revisado** — vía B (CNMV) **cerrada**, no «diferida». Vía C degradada a fuente de
  los cinco criterios valorativos: la rúbrica ya no se extrae de las 9 resoluciones de consumo
  sino de la LCSP. Ningún documento se depura: cambian de función, no de estado
- **Fase 1 congelada** y fuera del camino crítico. **Vigilancia normativa** reclasificada de
  fase futura a transversal, con ámbito cerrado a LCSP, RIA, gobernanza de IA y deontología
- **`research/`** — los dos informes que sostienen el giro, con fuentes enlazadas, y la
  transcripción del vídeo analizado

### ❌ Problemas encontrados

- **`pliego-02` puede estar fuera de alcance.** Es una concesión demanial, y las concesiones
  sobre dominio público se rigen por la **Ley 33/2003 (LPAP)**: el **art. 9.1 LCSP las excluye
  de su ámbito**. No es anotable con una rúbrica anclada en la LCSP sin añadir la LPAP como
  ancla propia — el supuesto de exclusión automática de `corpus/alcance.md`. **Verificar antes
  de anotar**; si se confirma, el corpus de arranque baja de 3 pliegos a 2
- **El ancla depende del tipo contractual, no solo de la materia.** El art. 210 regula la
  recepción con carácter general, pero en obras rige el art. 243. Se detectó al verificar contra
  el BOE una cita escrita de memoria — exactamente el fallo que el proyecto existe para no
  cometer
- **La fase 1 se congela con su bloqueo abierto.** El 315/315 sigue sin validar generalización y
  ahora no se va a corregir pronto. Es una decisión con coste, no un olvido: ampliar el corpus
  de sentencias es trabajo cuyo resultado no es explotable mientras el CENDOJ prohíba el uso
  comercial

### 💡 Aprendizajes

- **La fuente de datos es la barrera de entrada, no el modelo.** Es el criterio que ordena todas
  las decisiones de alcance de aquí en adelante
- **Un campo que no se puede medir puede ser dos campos.** Antes de inventar una métrica difusa,
  comprobar si el campo mezcla naturalezas distintas. `risk_flags` llevaba semanas bloqueado por
  esto
- **La regla del régimen era correcta, y es lo que ha permitido girar sin contaminar.** Si el
  esquema hubiera importado etiquetas de consumo, el giro a pliegos habría exigido rehacerlo
  entero en vez de estrecharlo
- **Un riesgo real de un pliego no es lo mismo que un defecto del pliego.** Analizar desde la
  posición de quien ejecuta, no de quien impugna, cambia qué es un flag y qué es
  `suggested_fix` — donde el licitador no negocia, sino que cuantifica, pregunta, impugna o
  desiste

### 🔜 Siguiente paso

- **`corpus/rubrica-riesgos-lcsp.md`** — catálogo **cerrado** de flags, no una guía: la métrica
  empareja por `id`. Bloque numérico primero (arts. 192, 193, 107, 202, 204–205, 198, 215–216),
  bloque valorativo después. Máximo ~40–50 flags en v1, cada `base_normativa` transcrita del BOE
  y no citada de memoria. **Redactar antes de anotar ningún documento**

---

## [25/08/2026] — 🧹 Reconstrucción del corpus de contratos

Sesión dedicada a que el corpus sea auditable antes de construir nada encima.

### ✅ Hecho
- **Inventario desde el disco**, no desde la tabla anterior: `corpus/inventario-contratos.csv`,
  30 filas con `sha256`. Instantánea declarada y suma reconciliada (23 activos + 7 depurados)
- **Reestructuración por vías**: `Inputs/corpus/via-{a,b,c}/` y `Inputs/_depurados/`.
  El renombrado no alteró ningún byte — los 30 hashes son idénticos a los previos
- **Dos ejes separados** en el inventario: `via` (procedencia) y `funcion` (para qué sirve)
- `corpus/alcance.md` — criterios de inclusión y exclusión por vía, escritos antes de descargar
- `corpus/evaluaciones.md` — registro de ejecuciones, para no repetir el gasto del test
- `corpus/candidatos-descartados.md` — población valorada y motivo de cada descarte
- `progress/ESTADO.md` — punto de entrada corto, enlazado desde `CLAUDE.md`
- `standards/contratos.md` v1: `risk_flags` con `regimen` y `control_aplicable`
- Copia externa del corpus a OneDrive, verificada por hash

### ❌ Problemas encontrados
- **Se perdió un documento.** El modelo argentino (nº 16) se borró el 06/08 en vez de moverse, y
  `Inputs/` está en `.gitignore`: no hay copia. Dado por perdido
- **La tabla anterior no cuadraba**: el resumen decía 9 documentos de adhesión donde la tabla
  tenía 8. Error de suma, no de depuración
- **Un fichero truncado** de 35 bytes ocupaba plaza en el corpus sin figurar en la tabla
- **Colisión de nombres**: `contrato1` significaba dos documentos distintos según la carpeta
- **Las vías A/B/C no estaban definidas en ningún sitio del repo**, solo en un documento externo

### 💡 Aprendizajes
- **Una tabla de composición sin instantánea declarada no es auditable.** Dentro de un mes no se
  puede saber qué contaba
- **Un corpus se depura moviendo, nunca borrando.** El único documento perdido lo demuestra
- **`risk_flags` no necesita datos reales de las partes.** El riesgo está en el texto y las
  cifras de la cláusula, no en quién firma. Confundirlo hizo descartar 12 documentos que eran
  justamente el corpus
- **Definir las vías por su fuente y asignarlas por su función son dos cosas distintas.**
  Mezclarlas en una columna bloqueó el inventario hasta desdoblarla en dos

### 🔜 Siguiente paso
- Paso 1 de la fase 2: decidir la métrica de campos sustantivos. Bloquea rúbrica, Gold y evaluación

---

## [06/08/2026] — 🏁 Cierre del módulo de sentencias

Fase 1 cerrada. El pipeline de extracción de sentencias está completo, medido y documentado.

### 📊 Métricas finales

| | Resultado |
|---|---|
| `eval_gold.ps1` | **315/315 (100 %)** — 35 documentos × 9 campos de cabecera, sin discrepancias |
| `validate_v2.ps1` | 35 archivos, **0 FAIL**, 9 avisos, exit 0 |
| Medición ciega (05/08) | **313/315 (99,4 %)** — dev 198/198, test-Supremo 45/45, test-otros órganos 70/72 |

Los nueve campos —`ecli`, `roj`, `resolution_number`, `appeal_number`, `id_cendoj`,
`decision_date`, `court_or_body`, `ponente`, `document_type`— al 100 %.

### 📦 Corpus

35 resoluciones del orden civil del CENDOJ: 27 del Tribunal Supremo (Sala de lo Civil) y 8 de
otros órganos —Tribunal de Instancia (Mercantil y Civil y de Instrucción), Tribunal Superior
de Justicia y Juzgado de lo Mercantil—, con **5 autos** entre ellas. Los 8 documentos fuera
del Supremo son los que ejercitaron las tres reglas del estándar v2 por primera vez.

### 🏗️ Arquitectura final

- `CLAUDE.md`: principios comunes e índice. Ni una regla de campo.
- `standards/sentencias.md`: fuente única del pipeline, el esquema de 16 campos, las reglas por
  campo y el contrato de validación.
- `standards/contratos.md`: borrador, sin ejercitar.
- `.claude/agents/sentencia_agent.md`: 40 líneas, sin duplicar ninguna regla.
- `validate_v2.ps1` (forma) + `eval_gold.ps1` (verdad) + `Gold/` de 35 ficheros.

### ⚠️ Lo que este 100 % no dice

- **No mide contenido.** `facts`, `applied_rules`, `ratio_summary` y `holding` solo tienen
  control de forma. Un output puede pasar las dos comprobaciones y contener un razonamiento
  equivocado. Los 9 campos medidos son los más mecánicos del esquema.
- **No mide generalización.** El conjunto de test **está gastado**: se evaluó el 05/08/2026,
  dio 313/315, y después se corrigieron dos reglas mirando esos dos fallos y se reprocesaron
  los documentos afectados. El 315/315 confirma que las reglas nuevas funcionan, nada más.
  Dev y test miden ya lo mismo: documentos que el estándar ha visto.
- **No cubre otros órdenes.** Todo el corpus es del orden civil.

### 🔜 Siguiente

Fase 2, Contract Analyzer. Ver `ROADMAP.md`. El primer paso no es escribir el esquema sino
**decidir cómo se evalúan campos sustantivos**: la comparación exacta que da el 100 % en
`ecli` o `decision_date` no sirve para `risk_flags` ni `missing_clauses`.

---

## [05-06/08/2026] — Test set procesado: 313/315 y el conjunto ciego se agota

### ✅ Hecho
- Estándar v2, tres cambios: `document_type` como enum cerrado leído del campo
  `Tipo de Resolución:`, `court_or_body` con niveles opcionales, regla de sección ambigua
- `validate_v2.ps1`: `document_type` que no coincide con la cabecera del input pasa de WARN a
  FAIL. Es la única comprobación que mira fuera del JSON
- Gold ampliado a 35 documentos; `document_type` entra como noveno campo evaluado
- Muestra de dev reprocesada (1, 3, 7, 9, 12, 14) y **los 13 documentos de test procesados**,
  un subagente por documento
- **313/315 (99,4 %)**: dev 198/198, test-Supremo 45/45, test-otros órganos 70/72
- `role: null` admitido en `parties`: pasa de FAIL a WARN en el validador
- Reglas nuevas de `ponente` (capitalización y acentos) y `ecli` (prefijo `ECLI:`), y
  `sentencia29` y `sentencia35` reprocesados con ellas: **315/315 (100 %)**

> **El 315/315 no es una medición de generalización.** Las dos reglas se escribieron mirando
> esos dos fallos concretos y después se reprocesaron esos dos documentos: el resultado
> confirma que las reglas hacen lo que tienen que hacer, y no dice nada sobre el rendimiento
> ante una cabecera nueva. La única cifra que mide generalización es el **313/315** de la
> primera pasada sobre test, cuando el conjunto todavía era ciego.

### ❌ Problemas encontrados
- **6 valores mal transcritos en el Gold del test**, detectados al contrastarlos con la
  cabecera: una fecha con el año cambiado, un número de sección, dos ponentes sin acentuar,
  dos sedes con paréntesis prohibidos por el propio estándar y un `null` escrito como cadena
  `"null"`. Todos eran errores del Gold, no del agente
- Los 13 agentes de la primera tanda cayeron por límite de sesión; 10 alcanzaron a escribir
- Dos errores reales del agente, ambos de transcripción de cabecera: ponente en mayúsculas sin
  acentos (`sentencia29`) y ECLI sin prefijo (`sentencia35`). Corregidos en el estándar y en
  los outputs, al precio de gastar el conjunto de test

### 💡 Aprendizajes
- Un Gold anotado a mano tiene la misma tasa de error que el sistema que pretende medir. Seis
  de las ocho discrepancias de la primera evaluación de test eran del Gold. Contrastar cada
  discrepancia contra la cabecera antes de atribuirla al agente no es opcional
- El estándar puede contradecirse a sí mismo sin que se note hasta que un documento lo fuerza:
  la sede `Palmas de Gran Canaria (Las)` chocaba con la prohibición de paréntesis en
  `court_or_body`, y el conflicto solo apareció al salir del Tribunal Supremo
- Una regla escrita mirando una cabecera no está probada hasta que se ejecuta contra ella: las
  tres del v2 pasaron 22 documentos de dev sin dispararse una sola vez
- `null` frente a rellenar: cuando el encabezamiento nombra a alguien sin rol, forzar
  `{name, role}` completo obliga a inferir justo lo que el estándar prohíbe

### 🔜 Siguiente paso
- Corpus nuevo: ya no queda conjunto ciego con el que medir generalización
- Evaluación de contenido para `facts`, `applied_rules`, `ratio_summary` y `holding`, que
  siguen sin más control que el formal

---

## [03/08/2026] — Migración a esquema v2 y control de versiones

### ✅ Hecho
- Esquema v2 (16 campos) como estándar único: `CLAUDE.md` + copia versionada `CLAUDE.v2.md`
- Campos nuevos: `case_id`, `decision_date`, `ponente`, `parties`, `cited_by_parties`, `document_quality_notes`
- Estructuras fijadas: `facts` array 5–15, `parties {name, role}`, `applied_rules {type, ref, note}`
- `validate_v2.ps1`: 12 bloques de comprobación, distingue FAIL de WARN, exit code encadenable
- Dataset completo reprocesado a v2 (6/6 validan, exit code 0)
- README técnico con pipeline, esquema y comandos
- `git init` y primer commit

### ❌ Problemas encontrados
- 5 de 6 agentes de reprocesado cayeron por límite de sesión; 4 alcanzaron a escribir su archivo
- `sentencia2.v2.json` no lo generó el agente: se construyó manualmente. Pendiente regenerarlo con el agente y comparar
- Tres specs legacy en `Agents/` contradecían el estándar vigente (esquema muerto, regla «No especificado» frente a `null`) → archivados

### 💡 Aprendizajes
- Los identificadores (ECLI, Roj, nº resolución) son extracción determinista de cabecera; dejarlos al criterio del modelo produjo 8 de 24 huecos en v1
- Separar `uncertainties` de `document_quality_notes` elimina el ruido estructural que repetían los 6 outputs
- Un validador solo sirve si distingue lo que incumple el contrato de lo que merece revisión humana

### 🔜 Siguiente paso
- Métricas de calidad (`METRICS.md` sigue vacío)
- Contract Analyzer

---

## [01/08/2026] — Inicio sistema documentación

### ✅ Hecho
- Implementado sistema de resumen de sentencias automatizado
- Creación de estructura de agentes
- Primera versión funcional del pipeline

### ⚙️ En progreso
- Mejora del CLAUDE.v2.md
- Estandarización de outputs JSON

### ❌ Problemas encontrados
- Inconsistencia en algunos outputs
- Falta de validación estructural fuerte

### 💡 Aprendizajes
- Importancia de definir schemas desde el inicio
- Claude responde mejor con instrucciones estructuradas

### 🔜 Siguiente paso
- Crear Contract Analyzer