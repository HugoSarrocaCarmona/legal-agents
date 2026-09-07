---
name: ver-video
description: Entender y analizar un video a partir de un enlace o un fichero local. Usar cuando aparezca una URL de YouTube, Vimeo, Twitter/X, LinkedIn o similar y se pida ver, resumir, analizar, transcribir o sacar conclusiones del video, o cuando haya que aprender algo de una charla, tutorial, webinar, ponencia juridica o clase grabada.
---

# Entender un video

El objetivo no es "ver" el video: es **entender que sostiene y decidir que vale**.
La extraccion es el medio, y ocupa un solo comando. El trabajo esta en el
analisis posterior.

## 1. Extraer

Comprobar dependencias solo la primera vez de cada sesion (el contenedor de
Claude Code en la web es efimero):

```bash
command -v yt-dlp >/dev/null && command -v ffmpeg >/dev/null \
  && echo "listo" || bash tools/video/setup.sh
```

```bash
python3 tools/video/watch_video.py "URL" --out video_out/<nombre-corto>
```

Por defecto saca **solo texto**: `transcript.md` (con marcas de tiempo y
seccionado por capitulos), `metadata.json` e `index.json`. Es lo rapido y es
casi siempre suficiente.

| Situacion | Anadir |
|---|---|
| Subtitulos automaticos ilegibles | `--whisper --whisper-model medium` |
| Video en otro idioma | `--lang en` |
| Hay contenido visual imprescindible (paso 3) | `--frames 24` |

## 2. Leer

Lee `index.json` y despues `transcript.md` **entero**. Si pasa de ~2000 lineas,
guiate por el indice de capitulos y lee por secciones, pero no analices sobre
un fragmento suelto: la tesis de una charla suele estar al final.

Dos lecturas, no una:

1. **Estructura.** De que va, como esta organizado, donde estan las partes con
   contenido y donde el relleno (presentaciones, agradecimientos, promocion).
2. **Afirmaciones.** Que sostiene exactamente, con que lo respalda y donde
   pasa de describir a opinar.

## 3. Fotogramas: solo si hacen falta

No los extraigas por defecto. La transcripcion te dira si los necesitas: si el
ponente dice "como veis aqui", "en esta tabla", "este grafico", o si es una
demo de pantalla o una clase con diapositivas, entonces hay contenido que el
audio no lleva. Solo en ese caso vuelve a lanzar el script con `--frames 24` y
lee **los que caen en los minutos que importan**, no todos: cada imagen cuesta
contexto.

## 4. Analizar

Esto es el trabajo. Aplica el criterio de `CLAUDE.md`: no inventar, y separar
siempre lo extraido de lo interpretado.

- **Separa afirmacion de respaldo.** Que el video diga algo no lo convierte en
  cierto. Para cada afirmacion con peso: que aporta como apoyo — un dato, una
  norma, una sentencia, una experiencia propia, o nada.
- **Clasifica el registro.** Hecho comprobable, interpretacion, prediccion o
  norma vigente son cosas distintas y se mezclan constantemente en las charlas.
- **Las citas normativas son provisionales.** Los subtitulos automaticos y
  whisper destrozan nombres propios, numeros de articulo y referencias de
  sentencias: "artículo 82" y "artículo 8.2" suenan igual. Toda cita legal
  sacada de una transcripcion va marcada como no verificada hasta contrastarla
  con la fuente primaria. **Nunca la des por buena en un output del proyecto.**
- **Situa al ponente.** Quien habla y desde donde: un webinar de un proveedor
  de software de cumplimiento tiene un interes; una clase universitaria, otro.
  No es descalificar, es contextualizar.
- **Di lo que no cubre.** Lo que un espectador razonable esperaria y no esta.
  Evita la falsa sensacion de tema cerrado.
- **Calibra.** Un explicativo de cinco minutos no da para un analisis de dos
  paginas. Si el video no aporta mas que su titulo, dilo: es una conclusion
  valida y util.

## 5. Responder

En el chat, explica el video **en prosa**: que sostiene, que tal lo sostiene y
que sacas de el. Para eso se analiza.

Guarda ademas `resumen.json` junto a la salida, como artefacto reutilizable:

```json
{
  "fuente": "URL",
  "titulo": "...",
  "duracion": "HH:MM:SS",
  "tipo": "charla | tutorial | entrevista | webinar | clase | otro",
  "base": "subtitulos manuales | subtitulos automaticos | whisper",
  "fiabilidad_transcripcion": "alta | media | baja",
  "tesis": "en una frase, lo que el video sostiene",
  "estructura": [{"t": "MM:SS", "seccion": "..."}],
  "afirmaciones": [
    {
      "t": "MM:SS",
      "afirmacion": "concreta, no un tema",
      "registro": "hecho | interpretacion | prediccion | norma",
      "apoyo": "que aporta como respaldo, o null si no aporta nada"
    }
  ],
  "citas_normativas": [
    {"t": "MM:SS", "cita": "tal y como suena en la transcripcion",
     "verificado": false, "nota": "por que hay que contrastarla"}
  ],
  "postura_del_ponente": "quien habla y desde que interes, o null",
  "aplicable_al_proyecto": ["lectura propia; va aparte de lo que dice el video"],
  "no_cubierto": ["lo que uno esperaria y no trata"],
  "incertidumbres": ["audio confuso, terminos dudosos, tramos ilegibles"]
}
```

`afirmaciones` recoge lo que el video dice. `aplicable_al_proyecto` es
interpretacion tuya y por eso va en un campo distinto: no las mezcles.

## Si YouTube lo bloquea

En Claude Code **en la web** (IP de datacenter) YouTube rechaza muchos videos
con "Sign in to confirm you're not a bot". El script reintenta con clientes
alternativos; si aun asi no hay subtitulos ni audio, falla con un mensaje
explicito y deja `metadata.json`.

Cuando pase, **no lo disimules ni analices el video por el titulo y la
descripcion**: di que no se ha podido acceder y ofrece las salidas reales —
ejecutarlo en local, o `--cookies-from-browser chrome`. Detalle en
`tools/video/README.md`.

## Otros limites

- Video sin habla y sin texto en pantalla: los fotogramas son la unica fuente.
- Directos en curso: hay que esperar a que terminen.
- YouTube devuelve 429 si se piden muchos videos seguidos; espaciarlos.
