# 🇪🇸 INFORME 2 — Dónde hay oportunidad real de mercado en la abogacía española

**Para:** Hugo Sarroca · 2.º de Derecho, UB · septiembre 2026
**Base:** marco de las 5 fuentes de datos del [informe 1](01-nichos-legaltech-video.md) +
investigación sobre el mercado, la regulación y la competencia españolas.

> **Advertencia de método.** Este informe está escrito para ser útil, no para ser agradable.
> Descarta explícitamente tres de las cuatro cosas que probablemente te apetecía construir, y
> lo hace con razones. Si algo aquí es incómodo, es porque el mercado lo es.

---

## 0. VEREDICTO EN UNA PÁGINA

**El vídeo describe un mercado que en su mayor parte no puedes atacar desde España, y menos
siendo estudiante de 2.º.** No por falta de talento: por tres barreras duras que ninguna
cantidad de ingeniería resuelve.

1. **La fuente de datos más valiosa está vallada.** En España «la ley» como corpus explotable
   no es un bien público. El CENDOJ no tiene API, prohíbe la descarga masiva y el uso
   comercial, y ha puesto CAPTCHA. Las bases con valor están en manos de cuatro editoriales.
   **La categoría estrella del vídeo —investigación jurídica— te está cerrada.**
2. **El despacho nativo de IA es ilegal aquí.** Garfield existe por la SRA; Eudia por Arizona.
   La Ley 2/2007 exige que el control de la sociedad profesional esté en manos de socios
   profesionales. **La única categoría genuinamente nueva del vídeo no tiene versión española.**
3. **El comprador natural es el peor pagador de Europa occidental.** El 73 % de la abogacía
   española ejerce sola o en despacho pequeño, con baja alfabetización tecnológica y presupuesto
   de software de 20–100 €/mes. Vender a abogados españoles es un negocio duro.

**Y sin embargo hay una puerta abierta, y es exactamente donde ya está apuntando tu repo sin
que lo hayas planteado en términos de mercado:**

> **La contratación pública. Fuente de datos abierta y masiva (PLACSP), dolor documentado y
> cuantificado, comprador que no es abogado sino empresa —y por tanto paga, no tiene secreto
> profesional y no te mete en el Anexo III del Reglamento de IA.**

Tu `standards/contratos.md` ya contiene, escrita, la taxonomía de riesgo administrativo que
nadie más está explotando. Es tu único activo con encaje comercial inmediato. El resto del
repo es infraestructura de aprendizaje excelente y producto malo.

---

## 1. LOS SEIS HECHOS ESTRUCTURALES DEL MERCADO ESPAÑOL

Nada de lo que decidas debería contradecir estos seis datos.

### 1.1 · La abogacía española está atomizada y no compra tecnología

- **> 130.000 abogados ejercientes** (CGAE).
- **73 % ejerce en despacho pequeño (38 %) o en solitario (35 %).**
- Solo **19 despachos superan los 250 empleados** — 12.092 personas en total. Ese es todo tu
  mercado «enterprise» nacional, y ya está cubierto por Harvey, Legora, Aranzadi y Lefebvre.
- **Solo el 31 % considera la adopción tecnológica muy importante; el 24 % le da poca
  relevancia.** No es un mercado que espera tu producto: es un mercado que hay que convencer.
- Rango de precio real de software jurídico: **20–100 €/mes/usuario**. LexIAGest desde 29 €,
  Clio por encima de 80 €.

**Implicación brutal:** el LTV de un abogado solo español es de unos pocos cientos de euros al
año, con coste de adquisición alto y ciclo de venta lento por desconfianza. Un producto dirigido
al abogado individual español necesita miles de clientes para ser algo. **Los productos
verticales para abogados solos son el camino más romántico y menos rentable.**

### 1.2 · El corpus jurídico español no es reutilizable

| Fuente | ¿Abierta? | Realidad operativa |
|---|---|---|
| **BOE** | ✅ Sí | API y datos abiertos. Legislación estatal utilizable. |
| **DOUE / EUR-Lex** | ✅ Sí | Abierto, multilingüe, reutilizable. |
| **PLACSP** (contratación) | ✅ Sí | Datos abiertos, volumen masivo. **La joya infrautilizada.** |
| **BORME, CNMV, registros** | ✅ Sí | Abiertos con fricción. |
| **CENDOJ** (jurisprudencia) | ❌ **No** | Sin API pública. Aviso legal prohíbe descarga masiva y uso comercial. CAPTCHA que bloquea de facto a agentes de IA. Requiere licencia formal de reutilización. |
| **Aranzadi / vLex / Lefebvre / Tirant** | ❌ No | Corpus propietario. **Es el foso, y no es tuyo.** |

Las cuatro editoriales ya han montado su capa de IA sobre su propio corpus: **Vincent AI**
(vLex), **GenIA-L** (Lefebvre), **Sof-IA** (Tirant), Aranzadi LA LEY. Además **vLex fue
absorbida por Clio**, lo que fusiona el corpus jurídico con la gestión del despacho.

**Traducción:** cualquier producto español cuya fuente sea «la ley» compite contra empresas que
tienen los datos, la marca, la red comercial y el colegio profesional de su lado. Tú no tienes
ninguna de las cuatro cosas. **No compitas ahí.**

### 1.3 · El despacho nativo de IA no cabe en el ordenamiento español

La **Ley 2/2007, de sociedades profesionales** ordena la sociedad de modo que **el control
—patrimonial y orgánico— corresponda a los socios profesionales**, con mayorías cualificadas. El
propio CGAE consideró un error abrir siquiera parcialmente el capital a socios no profesionales,
precisamente por el conflicto con el **secreto profesional** y la **independencia colegial**.

| | Inglaterra y Gales | Arizona | **España** |
|---|---|---|---|
| Propiedad no letrada | ✅ ABS autorizadas por la SRA | ✅ ABS desde 2021 | ❌ Control reservado a socios profesionales |
| Caso real | Garfield AI | Eudia, Manifest | **Ninguno posible** |

Y a esto se suma lo obvio: **prestar servicios jurídicos exige colegiación**, que exige el grado
y el máster de acceso. Estás a años de eso.

**Conclusión sin adornos:** el modelo del vídeo que más ilusión hace —montar tú el despacho de
IA que reclama facturas impagadas por 2 € la carta— **no es una opción legal para ti en España,
ni ahora ni al acabar la carrera sin cambio normativo.** Guárdalo como hipótesis a 10 años y no
diseñes nada asumiendo que llegará.

### 1.4 · Los tribunales españoles ya están sancionando la IA no verificada

Esto no es una tendencia futura: es jurisprudencia disciplinaria en curso, y **escala rápido**.

| Fecha | Órgano | Hechos | Sanción |
|---|---|---|---|
| 09/09/2024 | **Tribunal Constitucional** | Letrado de Barcelona falsea **19 sentencias del propio TC** en un amparo | Apercibimiento + traslado al Colegio |
| 2024 | TSJ Navarra | Cita el **Código Penal colombiano** en lugar del español | Ninguna (reconoció el error) |
| 10/02/2026 | **TSJ Canarias** | **48 sentencias falsas** del TS + un informe del CGPJ inexistente | **420 €** + traslado al Colegio |
| 04/2026 | TSJ Navarra | Letrada cita sentencias inventadas de TC, TS, TSJ Navarra y TSJ Madrid | Ninguna (pidió perdón) |
| 07/2026 | **TSJ Canarias** | Múltiples citas entrecomilladas inexistentes; **no reconoció el error** | **840 €** |

**El criterio de cuantificación es pedagógico y explícito:** 420 € ≈ **la mitad** del coste
anual de una herramienta jurídica profesional; 840 € ≈ **el coste anual completo**. El mensaje
del tribunal es literalmente *«la multa es lo que te habría costado la herramienta que lo
habría evitado»*. Y por mala fe procesal las multas pueden llegar a **6.000 €**.

De apercibimiento a 840 € en 22 meses. La curva sube.

### 1.5 · El CGAE ha convertido la verificación en deber deontológico

La **Circular 3/2026 del CGAE**, dictada al amparo del **art. 23 de la LO 5/2024 del Derecho de
Defensa**, regula el **deber de verificación y control del abogado sobre la IA generativa**. El
mapa normativo que activa:

| Incumplimiento | Norma | Naturaleza |
|---|---|---|
| Verificación deficiente del *output* | art. 125.u EGAE | Deontológica |
| Uso tecnológico no diligente | art. 21 CDAE | Deontológica |
| Falta de contrato de encargo de tratamiento | art. 28.3 y 83.4 RGPD | Administrativa |
| Omisión de evaluación de impacto | art. 35 RGPD | Administrativa |
| Exposición del secreto profesional | art. 542.3 LOPJ · art. 16 LO 5/2024 · **art. 199.2 CP** | Penal y disciplinaria |

Y un dato de mercado enterrado en el texto: **la Circular constata la ausencia generalizada de
contratos de encargo de tratamiento** entre despachos y proveedores de IA. Es decir: **el
regulador ha declarado por escrito que casi toda la profesión está incumpliendo.**

**Implicación doble y contradictoria:**
- ✅ Es una **demanda creada por decreto**. Alguien tiene que resolverle esto a 130.000 letrados.
- ❌ Es también **una barrera para ti**: en el momento en que tu herramienta toque datos de
  clientes de un despacho, entras en la cadena como encargado del tratamiento, con art. 28.3
  RGPD, medidas técnicas, subencargados y transferencias internacionales. Con Claude por debajo,
  eso es un contrato serio, no un `README`.

### 1.6 · El Reglamento de IA te afecta según a quién vendas

- **Anexo III, punto 8 del RIA**: es de alto riesgo el sistema destinado a auxiliar a una
  autoridad judicial en la investigación e interpretación de los hechos y del derecho. El uso
  por un abogado en el contexto de la administración de justicia **puede aproximarse a ese
  supuesto**.
- El **Reglamento Ómnibus (UE) 2026/1744 aplaza las obligaciones de alto riesgo del Anexo III
  al 2 de diciembre de 2027.** Tienes ventana, no indulto.
- En España, el **Proyecto de Ley Orgánica de gobernanza de la IA** (Consejo de Ministros
  26/05/2026, en el Congreso desde 12/06/2026) designa a **AESIA** (A Coruña) como autoridad de
  vigilancia y concreta sanciones en los rangos del art. 99 RIA: **hasta 35 M€ o el 7 % del
  volumen de negocio mundial**.

**Regla práctica que deberías grabarte:** *un producto que ayuda a una empresa a decidir si se
presenta a una licitación no es alto riesgo. Un producto que ayuda a construir el escrito que
lee un juez, se acerca peligrosamente.* Esto por sí solo debería reorientar tu hoja de ruta.

---

## 2. EL FILTRO: las 5 fuentes de datos aplicadas a España

Aquí es donde el marco del vídeo se convierte en una decisión.

| Fuente | Situación en España | ¿Viable para ti hoy? |
|---|---|---|
| **1. La ley** | CENDOJ cerrado; corpus en manos de 4 editoriales con IA ya desplegada | 🔴 **No** |
| **2. Conocimiento del despacho** | Requiere que un despacho te abra su archivo → confianza + secreto profesional + art. 28.3 RGPD | 🟠 **No aún** |
| **3. Prueba del caso** | Datos personales reales de terceros, secreto profesional, Circular 3/2026, RIA | 🔴 **No** |
| **4. Datos operativos** | Ocupado por Aranzadi, Lefebvre, Sepín, Clio-vLex. Es integración, no criterio jurídico | 🔴 **No** |
| **5. Internet abierto** | **BOE, PLACSP, BORME, CNMV, DOUE, boletines autonómicos: abiertos, masivos, reutilizables** | 🟢 **Sí** |

**Este es todo el análisis, condensado.** El único cuadrante verde es la fuente 5. Y el mayor
corpus jurídico-económico abierto de España, con diferencia, es la contratación pública.

---

## 3. LAS RAMAS, UNA A UNA

Evaluación con cuatro ejes: **implicación** (qué exige de ti), **dificultad técnica**,
**adherencia al mercado español** y **rentabilidad del público objetivo**.

### 🟢 RAMA A — Análisis de riesgo jurídico de pliegos (LCSP)

**Qué es.** No «ayúdame a ganar la licitación» sino **«qué me va a costar este contrato si lo
gano»**: penalidades por demora, régimen de garantías, revisión de precios, *ius variandi*,
causas de resolución, subcontratación y cesión, confidencialidad, plazos de pago. Es decir:
exactamente la lista de riesgos administrativos que **ya tienes escrita** en
`standards/contratos.md`.

**Los números del mercado (PLACSP, 2025):**
- **180.600 M€ licitados** (+32,3 % interanual) en **más de 201.000 expedientes**.
- **350.000–450.000 anuncios anuales** entre licitaciones, adjudicaciones y formalizaciones.
- **9.819 concursos desiertos = 4.011 M€ de dinero público paralizado.**
- Causa identificada: **la complejidad técnica de los pliegos ha crecido muy por encima de la
  capacidad administrativa de pymes y autónomos**, exigiendo conocimiento de LCSP, normativa
  ambiental y criterios sociales.

**Por qué encaja contigo específicamente:**
- Es la **fuente 5**: datos abiertos, sin CENDOJ, sin CAPTCHA, sin licencia de reutilización.
- El comprador es **una empresa, no un abogado**: paga por ROI medible (ganar contratos, evitar
  penalidades), no por «productividad».
- **Sin secreto profesional, sin datos de clientes de despacho, sin Anexo III.**
- Tu vía A del corpus **ya es PLACSP**. No empiezas de cero.

**La competencia, sin edulcorar.** Hay al menos cinco actores: **LICAI** (Eivor), **LicitaBot**,
**El Vínculo**, **ialicitaciones.com**, **Everglow**. Todos hacen extracción del PCAP y el PPT:
objeto, presupuesto, criterios de adjudicación y su peso, umbrales de solvencia, plazos.

**Pero todos están del lado de la oferta: optimizan *ganar*.** Ninguno modela el riesgo jurídico
de *ejecutar*. Esa es tu grieta, y es una grieta jurídica —no técnica—, que es justo el terreno
donde tú tienes ventaja sobre un ingeniero.

| Eje | Valoración |
|---|---|
| Implicación | Media. Dominar LCSP (Ley 9/2017) de verdad. Es estudio, y es materia de tu carrera. |
| Dificultad técnica | **Media-baja.** Es tu pipeline de contratos con corpus abierto. |
| Adherencia al mercado ES | **Alta.** Dolor cuantificado en euros públicos. |
| Rentabilidad del público | **Alta.** Pyme licitadora paga; el contrato vale seis cifras. |
| Riesgo principal | Que los actores de oferta añadan una pestaña «riesgos». Tu defensa es profundidad de la taxonomía LCSP, no la funcionalidad. |

**Veredicto: 🟢 Es tu apuesta principal. Es la única rama donde tus activos actuales, la
regulación y la estructura del mercado apuntan en la misma dirección.**

---

### 🟡 RAMA B — MASC: el requisito de procedibilidad de la LO 1/2025

**Qué es.** Desde el **3 de abril de 2025**, el art. 5 de la LO 1/2025 convierte el intento de
un **MASC** (negociación, mediación, conciliación privada, oferta vinculante confidencial,
dictamen de experto independiente, derecho colaborativo) en **requisito de procedibilidad** para
acceder a la jurisdicción civil y mercantil en materia disponible.

**Por qué es un hueco real:**
- Es **nuevo** (18 meses). No hay incumbente.
- **La demanda se inadmite** si no se acredita la identidad del oferente, la recepción efectiva
  por la otra parte y la fecha de recepción.
- Hay tensión estructural jugosa: **hay que probar el intento sin revelar el contenido** (la
  negociación es confidencial). Se recomienda un estándar documental más alto que el de una
  simple reclamación amistosa, *porque si el expediente MASC va corto de prueba, la demanda
  queda expuesta*.
- La doctrina menor aún se está formando: basta invitación de buena fe sin propuesta concreta;
  discrepancia entre juzgados sobre si aplica a separación, divorcio y medidas paternofiliales.

**Lo que es en realidad:** un problema de **trazabilidad probatoria**, no de razonamiento
jurídico. Generar el requerimiento correcto, acreditar recepción fehaciente, fechar, custodiar,
y producir el documento acreditativo que acompaña a la demanda sin romper confidencialidad.

**Por qué no es tu apuesta principal, siendo honesto:**
- El comprador es el abogado solo español: **el peor pagador del análisis** (§1.1).
- El foso técnico es **bajo**. Una buena plantilla más un burofax electrónico más una hoja de
  seguimiento cubre el 80 %. Es defendible por producto y marca, no por tecnología.
- Roza el **acto procesal**, con lo que la sombra del Anexo III y de la Circular 3/2026 vuelve.

| Eje | Valoración |
|---|---|
| Implicación | Baja-media. Procesal civil, que estudiarás igualmente. |
| Dificultad técnica | **Baja.** |
| Adherencia al mercado ES | **Alta** — es obligatorio por ley. |
| Rentabilidad del público | **Baja.** Abogado solo, 20–40 €/mes como techo. |

**Veredicto: 🟡 El mejor proyecto de credibilidad y aprendizaje, el peor negocio.** Constrúyelo
segundo, pequeño, y úsalo para aprender a hablar con abogados reales —que es la habilidad que
más te falta y la que menos se aprende programando.

---

### 🔴 RAMA C — Verificación de citas jurisprudenciales

**El dolor está validado como en ningún otro sitio** (§1.4 y §1.5): sanciones reales, criterio
económico explícito del tribunal, deber deontológico expreso del CGAE.

**Y aun así: no lo construyas como negocio.** Dos razones que pesan más que el dolor.

1. **Ya está ocupado, y por gente rápida.** En pocos meses han aparecido al menos cuatro:
   **Nearius** (MCP que conecta Claude/ChatGPT a jurisprudencia real con ECLI y detecta citas
   inexistentes), **Jurisprudenciator**, **JurisFind** (busca en CENDOJ y vLex a la vez con
   enlace de verificación) y **Estudia Derecho**. Llegas tarde a una carrera de commodities.
2. **Todos dependen del CENDOJ, cuyos términos prohíben exactamente lo que hacen.** Descarga
   masiva prohibida, explotación comercial prohibida, CAPTCHA desplegado. Están sobre una capa
   de hielo legal. **No construyas un negocio cuyo insumo crítico puede desaparecer por un
   cambio de aviso legal**, y menos siendo tú quien va a ser abogado.

Y hay un tercer argumento, más incómodo: el propio CGPJ ha señalado que **verificar contra el
CENDOJ es trivial y cuesta minutos**. Un producto cuyo valor es «hacer lo que el regulador dice
que es trivial» tiene un techo de precio muy bajo.

| Eje | Valoración |
|---|---|
| Implicación | Baja. |
| Dificultad técnica | Baja-media. |
| Adherencia al mercado ES | Alta pero **saturada**. |
| Rentabilidad | **Baja.** Precio anclado por el tribunal en ~840 €/año *de la herramienta completa*. |

**Veredicto: 🔴 No como producto. 🟢 Sí como componente interno.** Un *gate* de verificación de
citas dentro de tu propio pipeline es obligatorio, gratis de construir y es la diferencia entre
un proyecto serio y una demo. Constrúyelo, no lo vendas.

---

### 🔴 RAMA D — Extracción y resumen de sentencias (tu pipeline actual)

Hay que decirlo claro porque es donde está tu trabajo hecho: **`sentencias` v2 no es un producto
en España.**

- El corpus está vallado (§1.2). Sin CENDOJ reutilizable, no hay escala.
- Resumir una sentencia es hoy una **funcionalidad** dentro de Vincent AI, GenIA-L y Sof-IA, no
  un producto. Compites contra quien ya tiene la sentencia y al cliente.
- Tu propio `ESTADO.md` reconoce las dos limitaciones que impiden venderlo: **el test está
  gastado** (315/315 tras corregir reglas mirando los fallos → no mide generalización) y **los
  campos sustantivos no tienen evaluación de contenido**. Un output puede pasar la validación y
  contener un razonamiento equivocado. **No puedes vender calidad que no has medido.**

**Pero no lo tires, porque su valor es otro y es alto.** Te ha dado el esquema v2, el validador,
35 ficheros *gold*, el ciclo DEBUG/IMPROVE y —lo más importante— **la disciplina**: no inventar,
`null` antes que inferencia, cabecera como fuente primaria, consciencia de régimen. Eso es
infraestructura y criterio, y se transfiere entero a la rama A.

**Veredicto: 🔴 Como producto. 🟢 Como banco de pruebas y como prueba de tu método.** Sigue
siendo tu mejor carta de presentación técnica; simplemente no es lo que se vende.

---

### 🔴 RAMA E — Despacho nativo de IA (Garfield / Eudia a la española)

Cerrado por §1.3. Ley 2/2007 + colegiación obligatoria. **No hay ruta.** Ni siquiera como
«empiezo y ya veremos»: montar una estructura que preste servicios jurídicos sin habilitación te
expone a intrusismo (art. 403 CP) y a un expediente que te seguiría toda la carrera profesional
que aún no has empezado.

**Veredicto: 🔴 Descartado por imperativo legal, no por dificultad.**

---

### 🔴 RAMA F — *Litigation sourcing* / litigación en masa (modelo Darrow)

Sobre el papel es tentador: **más de 4 millones de hipotecas firmadas entre 2005 y 2019** con
alguna cláusula reclamable (gastos, suelo, IRPH, vencimiento anticipado), y los **juzgados
especializados en cláusulas abusivas prorrogados hasta el 31/12/2026**. Fuente 5, volumen brutal.

**Tres razones por las que no:**
1. **Ya está industrializado** por *claim farms* y despachos a resultado. No hay hueco de
   detección: hay hueco de captación, y eso es marketing, no IA.
2. **El patrón automatizable se está cerrando.** El Tribunal Supremo ha rechazado declarar
   abusivas todas las cláusulas IRPH de forma generalizada: **hay que mirar caso por caso**. Un
   criterio caso a caso es precisamente lo que no se automatiza.
3. **Monetizarlo exige ser despacho o aliarte con uno**, y volvemos a §1.3.

**Veredicto: 🔴 Atractivo y bloqueado por regulación e incumbencia a la vez.**

---

### 🟡 RAMA G — Cumplimiento del uso de IA en despachos (Circular 3/2026 + RIA)

**El viento regulatorio más fuerte del informe.** Demanda creada por decreto (§1.5), plazo del
RIA acercándose (§1.6), AESIA en marcha, y el propio CGAE constatando incumplimiento
generalizado.

**Por qué aún no es tuyo:**
- Es **consultoría, no software**. El entregable es una política de uso de IA, un contrato de
  encargo del art. 28.3 RGPD, una EIPD del art. 35 RGPD y un registro de sistemas.
- Y la consultoría **se vende con autoridad**. Un decano de colegio no compra un marco de
  cumplimiento deontológico a un estudiante de segundo. Es un hecho del mercado, no un juicio
  sobre ti.

**Lo que sí puedes hacer hoy con esto:** convertirlo en **contenido**. Ser la persona que
explica bien la Circular 3/2026, el calendario del RIA y el proyecto de LO de gobernanza es
barato, es afín a tu agente de noticias, y construye la autoridad que necesitarás para vender
cualquier cosa a un despacho dentro de tres años.

**Veredicto: 🟡 Aparcar como producto. Explotar ya como reputación.**

---

## 4. MATRIZ COMPARATIVA

| Rama | Fuente | Dificultad | Adherencia ES | Público | Rentabilidad | Legal | **Prioridad** |
|---|---|---|---|---|---|---|---|
| **A · Riesgo de pliegos LCSP** | 5 abierta | Media-baja | 🟢 Alta | Pyme licitadora | 🟢 Alta | 🟢 Limpio | **1** |
| **B · MASC** | 5 + 2 | Baja | 🟢 Alta (obligatorio) | Abogado solo | 🔴 Baja | 🟡 Roza lo procesal | **2** |
| **G · Cumplimiento IA** | 1 | Media | 🟢 Alta | Despachos, colegios | 🟡 Media | 🟢 Limpio | **3 (contenido)** |
| **C · Verificación de citas** | 1 vallada | Baja | 🟡 Saturada | Abogado solo | 🔴 Baja | 🔴 CENDOJ | **Interno** |
| **D · Sentencias** | 1 vallada | Media | 🔴 Commodity | — | 🔴 Nula | 🟡 CENDOJ | **Banco de pruebas** |
| **F · Litigación masa** | 5 | Alta | 🔴 Ocupada | — | 🔴 Bloqueada | 🔴 Ley 2/2007 | **Descartado** |
| **E · Despacho IA** | — | — | — | — | — | 🔴 **Ilegal** | **Descartado** |

---

## 5. LAS CINCO COSAS INCÓMODAS QUE HAY QUE DECIR

**1. Tu ventaja no es técnica, y llevas meses invirtiendo como si lo fuera.**
Habrá miles de personas mejores que tú programando *pipelines*. Casi ninguna sabe por qué una
cláusula declarada abusiva por un juez de consumo **no es una etiqueta transferible a un pliego
administrativo**. Ese párrafo de tu `contratos.md` vale más que todo el código del repo. Es
criterio jurídico, no es replicable con un *prompt*, y es lo único que un ingeniero no puede
copiarte. **Construye donde ese criterio sea el producto.**

**2. Tu repo mide forma, no fondo, y tú ya lo sabes.**
`ESTADO.md` lo dice con una honestidad poco común: el test está gastado y los campos sustantivos
no tienen evaluación de contenido. Mantén esa honestidad, porque es tu rasgo más valioso — pero
entiende la consecuencia comercial: **hasta que no midas contenido, no tienes nada que vender,
solo algo que enseñar.** El siguiente hito serio no es una rama nueva: es un corpus reservado y
no mirado, y una evaluación de fondo.

**3. Ser de 2.º no es un problema para construir; es un problema para vender.**
No lo resuelvas fingiendo experiencia. Resuélvelo **eligiendo un comprador que no compre
autoridad jurídica**: una pyme que licita compra ganar contratos y no perder dinero en
penalidades. Un despacho compra criterio, y ese aún no te lo compran. La rama A está elegida
también por eso.

**4. Cuatro objetivos a la vez es cero objetivos.**
Agentes jurídicos + agente universitario + recopilador de noticias es una carga que sostiene un
equipo, no una persona en 2.º de carrera. El agente universitario es puro consumo interno —
constrúyelo simple y no lo llames proyecto. El de noticias **sí** es estratégico, pero solo si
lo estrechas: no «IA + legaltech + noticias globales + regulación», sino **regulación de IA y
legaltech en España y la UE**. Estrecho es lo que lo hace valioso y lo que lo hace sostenible.

**5. El riesgo real no es equivocarte de nicho: es no llegar nunca a un usuario.**
Tienes 35 ficheros *gold*, dos estándares, un validador y cero personas que hayan usado esto
para algo. **El siguiente error probable no es técnico, es no salir del repo.** Diez
conversaciones con responsables de licitaciones de pymes valen más que tres meses de refactor.

---

## 6. RUTA RECOMENDADA

**Fase 1 — Consolidar antes de ampliar (ahora)**
- Cerrar el bloqueo 1 de `ESTADO.md`: corpus de sentencias reservado y **no mirado**, medición
  honesta. Es lo que convierte el repo en evidencia de método.
- Añadir el *gate* de verificación de citas como componente interno (rama C).
- **No abrir ninguna rama nueva hasta esto.**

**Fase 2 — Girar el pipeline de contratos hacia pliegos (siguiente)**
- Ejercitar `contratos.md` v1 contra la vía A (PLACSP), que ya es tu corpus.
- Construir la **taxonomía de riesgo LCSP en ejecución**: penalidades por demora, garantías,
  revisión de precios, *ius variandi*, resolución, subcontratación, cesión, confidencialidad,
  plazos de pago. Con `regimen: administrativo` y sin importar etiquetas de consumo.
- Objetivo del entregable: **una ficha de riesgo de ejecución de un pliego**, trazable a
  cláusula, que un responsable de licitaciones lea en dos minutos y entienda qué le puede costar
  dinero si gana.

**Fase 3 — Validar con humanos (en paralelo, no después)**
- Enseñárselo a 10 pymes licitadoras y a 2 abogados de administrativo.
- La pregunta no es «¿te gusta?» sino **«¿qué riesgo se te ha escapado alguna vez y te ha
  costado dinero?»**. Esa respuesta define el esquema mejor que cualquier diseño previo.

**Fase 4 — MASC como segundo producto (después de A)**
- Solo cuando A tenga usuarios reales.

**Transversal — el agente de noticias, estrechado**
- Ámbito: RIA y su calendario, Proyecto de LO de gobernanza de IA / AESIA, circulares del CGAE,
  resoluciones sancionadoras por uso de IA, LCSP y doctrina de tribunales de contratación.
- No es una distracción: es **cómo mantienes la ventaja de criterio del punto 1** y cómo
  construyes audiencia antes de tener producto.

---

## 7. FUENTES

**Vídeo analizado**
- [Understand the Legal AI market in 40 mins. — Mags Chilaev](https://youtu.be/WtWs-BtKECE)

**Mercado y profesión**
- [Cifras y Datos Abogacía — CGAE](https://www.abogacia.es/publicaciones/abogacia-en-datos/) ·
  [Radiografía en datos de la profesión (Confilegal)](https://confilegal.com/20251014-el-cgae-hace-una-radiografia-en-datos-de-la-profesion-de-la-abogacia-y-sale-positiva-segun-su-presidente-salvador-gonzalez/)
- [Radiografía del despacho profesional — Wolters Kluwer](https://www.wolterskluwer.com/es-es/expert-insights/radiografia-del-despacho-profesional-2026)
- [La falta de educación tecnológica frena el LegalTech — Fundación Mutualidad](https://fundacionmutualidad.org/la-falta-de-educacion-tecnologica-de-los-abogados-frena-el-desarrollo-legaltech-en-espana/)
- [GLTHindex, índice de adopción tecnológica del sector legal](https://www.murciastartup.com/articulo/nuevas-tecnologias/legaltech-toma-bolsa-barcelona-global-legaltech-hub-presenta-primer-indice-madurez-tecnologica-sector-juridico/20260305044510007627.html)
- [Precios de software jurídico 2026 — KosmaLabs](https://kosmalabs.com/blog/software-despacho-abogados-pequeno-precios/) ·
  [Comparativa software jurídico — LexIAGest](https://lexiagest.com/comparativa-software-juridico/)

**Corpus y acceso a jurisprudencia**
- [Del limitado acceso a las resoluciones judiciales — Hay Derecho](https://www.hayderecho.com/2022/07/07/del-limitado-acceso-a-las-resoluciones-judiciales/)
- [Resoluciones judiciales, CENDOJ y scraping](https://www.linkedin.com/pulse/resoluciones-judiciales-cendoj-y-scraping-miguel-gonz%C3%A1lez-herrera) ·
  [CENDOJ como fuente oficial — OpenMercantil](https://openmercantil.es/fuentes/cendoj)
- [Base de datos del CENDOJ — ICA Las Palmas](https://www.icalpa.es/colegiados/actualidad/base-de-datos-del-cendoj-jurisprudencia-online-de-acceso-gratuito)

**Sanciones por IA no verificada**
- [El TSJC multa con 840 € por 25 sentencias falsas — Infobae](https://www.infobae.com/espana/2026/07/29/el-tsjc-multa-con-840-euros-a-un-abogado-por-citar-en-un-recurso-judicial-al-menos-25-sentencias-falsas-inventadas-por-una-inteligencia-artificial/)
- [Multa por 48 sentencias falsas — Xataka](https://www.xataka.com/magnet/tribunal-superior-justicia-canarias-multa-a-abogado-citar-48-sentencias-falsas-se-habia-sugerido-ia)
- [Abogada que citó sentencias inventadas se libra por pedir perdón — El Español](https://www.elespanol.com/espana/tribunales/20260404/abogada-cito-recurso-sentencias-inventadas-ia-libra-sancion-pedir-perdon-tribunal/1003744194050_0.html)
- [Multas cada vez más altas por «mala fe» — El Español](https://www.elespanol.com/espana/tribunales/20260817/aviso-jueces-mal-uso-ia-multas-vez-altas-abogados-mala-fe-traicion-cliente/1003744346246_0.html)
- [Informe: cómo los tribunales españoles sancionan el uso no supervisado de IA](https://epokan.com/informe/)

**Deontología y regulación de IA**
- [La Circular 3/2026 del CGAE sobre uso de IA en la Abogacía — Confilegal](https://confilegal.com/20260516-circular-3-2026-cgae-ia-abogacia-proteccion-datos-secreto-profesional/)
- [Nuevo calendario de obligaciones de alto riesgo del RIA — Augusta Abogados](https://augustaabogados.com/reglamento-de-inteligencia-artificial-nuevo-calendario-para-las-obligaciones-aplicables-a-los-sistemas-de-alto-riesgo/)
- [Ley Orgánica de IA: AESIA, sanciones y sandboxes — Economist & Jurist](https://www.economistjurist.es/zbloque-1/ley-organica-de-ia-espana-aterriza-el-ai-act-con-aesia-sanciones-y-sandboxes/) ·
  [Proyecto de Ley 121/000096 — Congreso](https://www.congreso.es/public_oficiales/L15/CONG/BOCG/A/BOCG-15-A-97-1.PDF)
- [Gobernanza de la IA en España — LAW21](https://law21.xyz/gobernanza-de-la-ia-en-espana-autoridades-competentes-regimen-sancionador-y-los-limites-de-legislar-sobre-un-reglamento-directamente-aplicable/)

**Estructura societaria**
- [Ley 2/2007, de sociedades profesionales — BOE](https://www.boe.es/buscar/act.php?id=BOE-A-2007-5584) ·
  [Estatuto General de la Abogacía Española](https://www.abogacia.es/wp-content/uploads/2012/06/Estatuto-General-de-la-Abogacia-Espanola31.pdf)
- [Arizona's Alternative Business Structures — Arizona State Law Journal](https://arizonastatelawjournal.org/2026/01/27/arizonas-alternative-business-structures-innovation-meets-neighboring-resistance/)

**MASC / LO 1/2025**
- [LO 1/2025 de eficiencia del Servicio Público de Justicia — Abogacía Española](https://www.abogacia.es/actualidad/ley-eficiencia-del-servicio-publico-de-justicia/) ·
  [Guía sobre la regulación de los MASC — CGAE (PDF)](https://www.abogacia.es/wp-content/uploads/2025/04/GUIA_MASC_CONSEJO_GENERAL_ABOGACIA.pdf)
- [Nueva regulación sobre los MASC — ICAM](https://web.icam.es/nueva-regulacion-sobre-los-medios-adecuados-de-solucion-de-controversias-masc-en-la-ley-organica-1-2025/)
- [Cómo demostrar el intento de MASC — Sepín](https://blog.sepin.es/blog/2026/03/16/intento-masc-negociaciones-abogados/) ·
  [La negociación entre abogados basta para cumplir el MASC — Confilegal](https://confilegal.com/20260807-la-negociacion-entre-los-abogados-de-las-partes-es-suficiente-para-cumplir-con-el-masc/)

**Contratación pública**
- [España alcanza los 180.600 millones en licitaciones, deja desiertos 4.011 millones — APTIE](https://aptie.org/noticias-sobre-tendencias/espana-alcanza-los-180-600-millones-en-licitaciones-publicas-pero-deja-desiertos-4-011-millones/)
- [Año 2025: licitaciones en cifras — AlertaLicita](https://alertalicita.com/es/ano-2025-licitaciones-en-cifras/) ·
  [Guía PLACSP 2026 — LicitaDiario](https://licitadiario.es/blog/guia-plataforma-contratacion-sector-publico)
- Competencia: [LICAI (Eivor)](https://eivor.es/solucion/automatizaciones-con-ia/gestion-de-licitaciones-en-espana/) ·
  [LicitaBot](https://licitabot.net/blog/analisis-inteligente-pliegos-licitaciones) ·
  [El Vínculo](https://el-vinculo.com/) · [ialicitaciones](https://ialicitaciones.com/en/)

**Litigación en masa**
- [El Supremo cierra la puerta a declarar abusivas todas las cláusulas IRPH — Noticias Jurídicas](https://noticias.juridicas.com/actualidad/noticias/20683-el-supremo-cierra-la-puerta-a-declarar-abusivas-todas-las-clausulas-irph-de-manera-generalizada:-hay-que-mirar-caso-por-caso/)
- [Prórroga de los juzgados especializados en cláusulas abusivas hasta 31/12/2026](https://lopezmanso.com/prorroga-de-los-juzgados-especializados-en-clausulas-abusivas-hasta-el-31-de-diciembre-de-2026/)

**Competencia en verificación de citas**
- [Nearius](https://www.nearius.com/) · [Jurisprudenciator](https://jurisprudenciator.lexiaipro.org/) ·
  [JurisFind](https://jurisfind.vindica.es/) · [Estudia Derecho](https://estudiaderecho.es/buscador-jurisprudencia/)
