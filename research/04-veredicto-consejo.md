# ⚖️ VEREDICTO DEL CONSEJO — auditoría de la cadena de consejo

**Fecha:** 15/09/2026 · **Herramienta:** `llm-council` (Remy Gaskell, commit `55ee36e`), instalada
en `.claude/skills/llm-council/`. Metodología de Andrej Karpathy: 5 asesores independientes →
revisión cruzada anónima → síntesis.

**Sometido a juicio:** la cadena de cuatro decisiones estratégicas recomendadas por Claude a Hugo
entre el 07/09 y el 15/09/2026 — el giro a pliegos, el diseño de la métrica, la especialidad
recomendada y la secuencia empleo→emprendimiento.

> **Este fichero es corto a propósito.** El consejo dictaminó que el problema de este proyecto es
> producir documentos en lugar de código. Un veredicto de veinte páginas sobre eso sería la
> prueba del delito. Lo que importa no es este fichero: son los cambios que ha provocado en
> `ESTADO.md`, `ROADMAP.md`, `standards/contratos.md` y `corpus/metrica.md`.

---

## Convergencia inusual de la revisión cruzada

Los cinco revisores, sin saber qué asesor escribió qué:

- **5 de 5** eligieron al **Ejecutor** como la respuesta más fuerte.
- **5 de 5** señalaron al **Expansionista** como la de mayor punto ciego — *«responde
  "amplía a 27 países" a alguien que no ha procesado tres documentos»*.
- **5 de 5** identificaron **el mismo punto ciego compartido por todos los asesores**.

Esa unanimidad es señal, no ruido.

---

## 1 · Donde el consejo está de acuerdo

**a) El diagnóstico no es sobre el giro. Es sobre quién lo escribió.**
Cuatro de los cinco asesores llegaron por su cuenta al mismo hecho: en una semana se produjeron
**4 documentos de estrategia y 0 líneas de software**, en la misma semana en que se escribió en
`CLAUDE.md` que el modo de fallo característico de este proyecto es *documentar en lugar de
ejecutar*. El Outsider lo llamó «the tell». El Ejecutor: *«eso es el diagnóstico entero»*.

**b) El hecho que sostiene toda la tesis nunca se verificó.**
«9.819 concursos desiertos = 4.011 M€ **porque** las pymes no pueden con la complejidad de los
pliegos.» Tres asesores lo atacaron por separado. Un concurso queda desierto también porque el
precio es inviable, el margen es malo, el plazo es imposible, se retira la financiación o el
pliego está escrito para un proveedor concreto. **Si la causa es cualquiera de esas, el producto
no tiene razón de existir.** El informe 2 lo presentó como «causa identificada» apoyándose en una
fuente secundaria. Era una inferencia vestida de dato.

**c) La decisión de especialidad no estaba madura y está haciendo daño.**
Cuatro asesores pidieron aplazarla o cancelarla. El Ejecutor fue el más preciso:
*«"especialízate en contratación pública de IA" es una etiqueta, no una tarea, y ahora mismo
funciona como excusa para no escribir la rúbrica»*. El First Principles añadió el argumento que
más incomoda: **es consejo infalsificable hasta 2029, y el consejo que no puede demostrarse
equivocado dentro del horizonte no le cuesta nada a quien lo da.**

**d) Tres pliegos no son un corpus, y es una herida autoinfligida.**
PLACSP publica datos abiertos masivos. Descargar 200 PCAP es una tarde de *scripting*, no un
proyecto de investigación. Que no haya ocurrido mientras se escribían cuatro documentos es, otra
vez, el diagnóstico.

---

## 2 · Donde el consejo choca

**Escala.** El Expansionista sostiene que el giro es correcto y **corto de miras**: la LCSP
transpone las Directivas 2014/24 y 2014/25, TED publica avisos de toda la UE en formato abierto
y legible por máquina, y con el ancla normativa apuntando al artículo de la directiva con
excepción nacional, Portugal o Italia serían configuración y no reescritura — €2 bn en vez de
€180 mm. Los otros cuatro responden que el problema no es el techo sino que no se ha entregado
nada. **Los cinco revisores dieron la razón a los cuatro en la dosis**, y a la vez marcaron la
aportación del Expansionista como el mejor hecho aislado de todo el consejo (§3.b).

**El comprador.** El Contrarian: *«una pyme que no sabe licitar es el peor cliente posible de
software — licita cuatro veces al año, paga poco y se va»*. El Expansionista: el segundo
comprador es **el propio órgano de contratación**, que redacta los pliegos, pierde los recursos y
dejó 4.011 M€ sin adjudicar. Misma herramienta, invertida. **Sin resolver, y decide el modelo de
negocio.**

**El umbral de reversión.** El informe 3 fijó «3 empresas usándolo y 1 pagando en 18 meses». El
First Principles: *«el umbral debería ser una conversación, no un cliente de pago»*. Los cinco
coinciden en que 18 meses es demasiado tarde para enterarse.

---

## 3 · Puntos ciegos que solo aparecieron en la revisión cruzada

**a) El hallazgo principal — los cinco revisores, por separado.**
Los cinco asesores enviaron a Hugo a hacer diez llamadas para verificar la causa de los
desiertos. **Los cinco revisores señalaron que no hacen falta llamadas: PLACSP publica el motivo
de cada declaración de desierto, desistimiento y renuncia.** Es una consulta sobre los datos
abiertos que ya había que descargar. Una tarde. Decisivo. Y más barato que cualquier remedio
propuesto por el consejo.

> Es el mejor argumento a favor de la herramienta: ningún asesor individual lo vio, y emergió
> cinco veces en la ronda de revisión.

**b) El TACRC es un corpus de jurisprudencia abierto, y el informe 2 lo dio por cerrado.**
Las resoluciones del Tribunal Administrativo Central de Recursos Contractuales y de los
tribunales autonómicos **se publican sin las restricciones del CENDOJ y sin prohibición de uso
comercial**. Y tratan exactamente de qué cláusulas de pliego se anulan. Eso **disuelve buena
parte del problema `valorativo`**: en vez de que un modelo opine que una cláusula es
desproporcionada, se cita que cláusulas de esa forma fueron anuladas. El informe 2 escribió «la
ley está cerrada» sin distinguir jurisdicción de doctrina administrativa. **Error mío.**

**c) El problema difícil es el *parsing*, no la taxonomía.**
Los PCAP son heterogéneos y muchos son PDF escaneados. `corpus/alcance.md` ya anticipaba esto
—exige capa de texto y comprobar extractabilidad antes de muestrear— pero **ningún informe costeó
ese trabajo**, y es donde se va el tiempo real.

**d) La línea de sentencias se congeló con un argumento mal aplicado.**
El aviso legal del CENDOJ prohíbe la **descarga masiva y el uso comercial**. No prohíbe leer.
Medir generalización exige veinte o treinta sentencias leídas a mano, que es exactamente lo que
sí está permitido. **Confundí «no se puede comercializar» con «no se puede medir».** El bloqueo
histórico del proyecto sigue siendo reparable con trabajo manual, y decir lo contrario fue una
racionalización cómoda.

**e) El despacho no es un retraso: es un canal.** Un despacho con práctica de público es una vía
de distribución hacia licitadores, no una espera antes de ellos. La Decisión 4 se defendió con el
argumento equivocado.

---

## 4 · La recomendación

**El giro a pliegos no se revierte.** Ningún asesor lo falsó. Pero **descansa sobre una premisa
no verificada que es barata de verificar**, y eso se resuelve esta semana, con datos y no con
llamadas.

**La decisión de especialidad se suspende seis meses.** No estaba madura, no es exigible hasta
2028 y está funcionando como coartada. Lo que no se suspende es estudiar LCSP en serio: eso rinde
en cualquier escenario, y es además temario de la carrera.

**La rúbrica se invierte.** El diseño decía: escribir el catálogo desde la LCSP y después anotar.
El orden correcto es **leer diez pliegos a mano, anotar todo riesgo que aparezca, y solo entonces
anclar cada uno a su artículo**. La disciplina se conserva —el catálogo sigue siendo cerrado y la
`base_normativa` sigue transcribiéndose del BOE— pero la taxonomía se **induce de documentos
reales** en vez de deducirse de una ley en abstracto. Un catálogo deducido recoge lo que la ley
regula; uno inducido recoge lo que los pliegos hacen. Solo el segundo sirve.

**El umbral de F1 ≥ 0,95 queda suspendido** hasta que exista el catálogo que mide. Fijar un
objetivo numérico sobre algo que no existe es, en palabras del consejo, teatro.

**El umbral de reversión baja de 18 meses a la primera conversación útil.**

---

## 5 · La única cosa que hacer primero

> ### Descargar los datos abiertos de PLACSP y responder una sola pregunta con ellos: **por qué quedaron desiertos esos 9.819 concursos.**

Una tarde. Es software, no un documento. Produce **a la vez** el corpus que desbloquea la tarea
parada desde el 09/09 y la verificación de la premisa sobre la que se apoya todo lo demás.

Y tiene la propiedad que ningún otro paso de esta semana ha tenido: **puede salir mal.** Si el
motivo mayoritario es precio inviable o falta de financiación, la tesis del producto cae y se
sabrá en un día en vez de en dos años.

---

## Nota sobre la herramienta

El consejo funcionó, y su valor no estuvo donde se esperaba. Los cinco asesores individuales
dieron buen análisis pero **convergieron en el mismo remedio equivocado** —«haz diez llamadas»—.
El hallazgo que de verdad cambia la semana apareció **solo en la ronda de revisión cruzada**, y
apareció cinco veces. Es exactamente el mecanismo que Karpathy describe, y es la razón de no
saltarse ese paso.

**Su límite, dicho también:** cinco asesores generados por el mismo modelo comparten sesgos. La
unanimidad del consejo no es evidencia externa. Sigue sin haber ni una sola persona real
consultada — y eso, que es la crítica central del propio veredicto, este veredicto tampoco lo
arregla.
