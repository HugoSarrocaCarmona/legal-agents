---
name: ver-video
description: Ver un video a partir de un enlace o un fichero local y extraer lo que explica. Usar cuando aparezca una URL de YouTube, Vimeo, Twitter/X, LinkedIn o similar y se pida ver, resumir, analizar, transcribir o sacar conclusiones del video, o cuando haya que aprender algo de una charla, tutorial, webinar, ponencia juridica o clase grabada.
---

# Ver un video

Claude no reproduce video. Esta skill lo convierte en dos cosas que Claude si
puede leer: una **transcripcion con marcas de tiempo** y una serie de
**fotogramas clave** en JPEG. Con las dos juntas se puede seguir lo que dice y
lo que ensena en pantalla.

## 1. Comprobar dependencias

Solo la primera vez de cada sesion (el contenedor de Claude Code en la web es
efimero y se reinstala en cada sesion nueva):

```bash
command -v yt-dlp >/dev/null && command -v ffmpeg >/dev/null \
  && echo "listo" || bash tools/video/setup.sh
```

## 2. Extraer

```bash
python3 tools/video/watch_video.py "URL" --out video_out/<nombre-corto>
```

Opciones que importan:

| Situacion | Anadir |
|---|---|
| Solo interesa lo que se dice | `--no-frames` (mucho mas rapido) |
| Charla con diapositivas o demo de pantalla | `--frames 40` |
| Video largo (>1h) y solo se busca una idea | `--no-frames --chunk 60` |
| El video no trae subtitulos | nada: cae solo a whisper |
| Subtitulos automaticos malos | `--whisper --whisper-model medium` |
| Video en otro idioma | `--lang en` (o el que sea) |

Escribe en `--out`: `metadata.json`, `transcript.md`, `frames/` e `index.json`.

## 3. Leer

1. **Siempre**: `index.json` y luego `transcript.md` entero. Si pasa de ~2000
   lineas, leer por partes guiandose por los capitulos de `metadata.json`.
2. **Los fotogramas, con criterio.** No los leas todos por defecto: cada imagen
   cuesta contexto. Leelos cuando la transcripcion sola no baste — hay
   diapositivas, codigo en pantalla, graficos, una demo, o el ponente dice
   "como veis aqui". Usa las marcas de tiempo de `frames/index.json` para
   elegir los que caen en los minutos que importan.
3. Si el video no aporta nada que no estuviera ya en el titulo, dilo. No
   inventes profundidad que no hay.

## 4. Responder

Guarda un `resumen.json` junto a la salida, con esta forma:

```json
{
  "fuente": "URL",
  "titulo": "...",
  "duracion": "HH:MM:SS",
  "tipo": "charla | tutorial | entrevista | webinar | clase | otro",
  "tesis": "en una frase, lo que el video sostiene o ensena",
  "puntos_clave": [
    {"t": "MM:SS", "punto": "afirmacion concreta, no un tema"}
  ],
  "datos_citados": [
    {"t": "MM:SS", "dato": "cifra, ley, sentencia o fuente mencionada"}
  ],
  "aplicable_al_proyecto": ["que se puede usar aqui, o lista vacia"],
  "no_cubierto": ["lo que uno esperaria y el video no trata"],
  "base": "subtitulos manuales | subtitulos automaticos | whisper",
  "incertidumbres": ["audio confuso, terminos dudosos, tramos ilegibles"]
}
```

Reglas heredadas de `CLAUDE.md` que aqui tambien aplican:

- **No inventar.** Si el ponente no dice una cifra, no aparece en
  `datos_citados`. Ante la duda, `incertidumbres`.
- **Separar lo dicho de lo interpretado.** `puntos_clave` recoge lo que el
  video afirma; `aplicable_al_proyecto` es lectura propia y va aparte.
- Los subtitulos automaticos y whisper **transcriben mal los nombres propios y
  los terminos tecnicos**. Un nombre de ley, sentencia o herramienta sacado de
  ahi va marcado en `incertidumbres` salvo que se confirme en pantalla.

En el chat, explica el video en prosa: para eso se ve. El `resumen.json` es el
artefacto reutilizable, no el mensaje.

## Si YouTube lo bloquea

En Claude Code **en la web** (contenedor en la nube, IP de datacenter) YouTube
rechaza muchos videos con "Sign in to confirm you're not a bot". El script
reintenta solo con clientes alternativos; si aun asi no hay subtitulos ni audio,
falla con un mensaje explicito y deja `metadata.json`.

Cuando pase, **no lo disimules ni resumas el video por el titulo**: di que no se
ha podido acceder y ofrece las salidas reales — ejecutarlo en local, o
`--cookies-from-browser chrome`. Detalle en `tools/video/README.md`.

## Otros limites

- Video sin habla y sin texto en pantalla: los fotogramas son la unica fuente.
- Directos en curso: hay que esperar a que terminen.
- YouTube devuelve 429 si se piden muchos videos seguidos; espaciarlos.
