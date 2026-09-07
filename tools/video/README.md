# Ver videos

Claude no reproduce video. Esta carpeta convierte un video en lo que si puede
leer: **transcripcion con marcas de tiempo** y **fotogramas clave** en JPEG.

## Instalacion

```bash
bash tools/video/setup.sh
```

Instala `yt-dlp`, `ffmpeg`, `deno` y `faster-whisper`.

> En Claude Code en la web el contenedor es **efimero**: hay que ejecutarlo una
> vez por sesion. En local, una sola vez.

## Uso

```bash
python3 tools/video/watch_video.py "https://www.youtube.com/watch?v=..." --out video_out/charla
```

Tambien acepta un fichero local (`.mp4`, `.mkv`, `.webm`, `.mp3`...) y cualquier
sitio soportado por yt-dlp (Vimeo, Twitter/X, LinkedIn, Twitch...).

### Salida

```
video_out/charla/
├── metadata.json     titulo, canal, duracion, fecha, descripcion, capitulos
├── transcript.md     transcripcion en bloques de ~30s, sin duplicados
├── frames/           fotogramas en los cambios de plano, nombrados por timestamp
│   └── index.json
└── index.json        inventario y procedencia de la transcripcion
```

### Opciones

| Opcion | Por defecto | Para que |
|---|---|---|
| `--lang es,en` | `es,en` | idiomas de subtitulos preferidos, por orden |
| `--frames N` | `24` | maximo de fotogramas |
| `--no-frames` | — | solo transcripcion; bastante mas rapido |
| `--frame-height` | `540` | alto de los JPEG |
| `--max-height` | `480` | calidad del video descargado para los fotogramas |
| `--scene-threshold` | `0.25` | sensibilidad del cambio de plano (bajar = mas cortes) |
| `--chunk` | `30` | segundos por bloque de transcripcion |
| `--whisper` | — | forzar transcripcion local aunque haya subtitulos |
| `--whisper-model` | `small` | `tiny`/`base`/`small`/`medium`/`large-v3` |
| `--vad` | — | filtrar silencios (ver limitaciones) |
| `--keep-media` | — | conservar audio y video descargados |
| `--cookies-from-browser` | — | `chrome`, `firefox`, `edge`... para videos bloqueados |
| `--cookies` | — | fichero de cookies en formato Netscape |

## Como obtiene la transcripcion

Por orden de preferencia, y **una sola pista** (pedir varias dispara el 429 de
YouTube):

1. Subtitulos **manuales** en el idioma pedido — exactos, instantaneos.
2. Subtitulos manuales en cualquier idioma.
3. Subtitulos **automaticos** en el idioma pedido.
4. Subtitulos automaticos en cualquier idioma.
5. **faster-whisper** en local, si no hay ninguno.

Los subtitulos automaticos de YouTube son *rolling*: cada linea repite la
anterior y le anade palabras. El script reconstruye el texto lineal; sin eso la
transcripcion sale con todo triplicado.

## Notas de implementacion

Tres cosas que costaron encontrar y conviene no deshacer:

- **La deteccion de cambio de plano usa `ffmpeg ... showinfo`, no
  `ffprobe -f lavfi movie=...`.** El segundo parece equivalente y no lo es: no
  calcula bien `scene` y devuelve un unico fotograma. Comprobado sobre el mismo
  video: 84 cortes frente a 1.
- **El analisis se hace sobre una copia reducida a 320px.** Mismo resultado,
  ~30x mas rapido que el tiempo real del video.
- **El filtro VAD de faster-whisper viene desactivado.** Depende de un modelo
  aparte que en este entorno no carga y descarta el audio entero *sin lanzar
  error* (0 segmentos en un audio de 213s). `--vad` lo activa y, si vuelve
  vacio, el script reintenta sin el.

## Coste aproximado

| Tarea | Video de 1h |
|---|---|
| Transcripcion desde subtitulos | segundos |
| Transcripcion con whisper `small` en CPU | 5-15 min |
| Deteccion de planos + 24 fotogramas | 2-4 min |

Para leer rapido: `--no-frames`.

## El bloqueo de YouTube (importante)

YouTube responde **"Sign in to confirm you're not a bot"** a muchas peticiones
que vienen de IPs de datacenter. Eso afecta de lleno a **Claude Code en la web**,
que corre en un contenedor en la nube. Medido en este repositorio: videos muy
populares pasan, pero videos normales (una charla, un webinar) son rechazados.

**Desde tu propio ordenador esto no ocurre**: la IP es residencial y funciona sin
mas.

El script no se rinde a la primera. Si el cliente por defecto es rechazado,
reintenta con `web_safari`, `mweb`, `tv` y `web_embedded`. Esos clientes
recuperan **metadatos**, pero normalmente no dan ni subtitulos ni formatos
descargables, asi que la salida queda en `metadata.json` y el script lo dice
claramente en vez de fingir que ha funcionado.

Para desbloquearlo del todo, por orden de comodidad:

1. Ejecutarlo en local.
2. `--cookies-from-browser chrome` (o `firefox`, `edge`...) en local.
3. Exportar las cookies a un fichero Netscape y pasar `--cookies cookies.txt`;
   asi tambien sirve dentro del contenedor.

Las cookies son credenciales de tu cuenta de Google: **no se suben al
repositorio** (y `video_out/` esta en `.gitignore`).

## Otras limitaciones

- Directos en curso: hay que esperar a que terminen.
- YouTube devuelve 429 con peticiones seguidas; espaciar los videos.
- La calidad de whisper depende del modelo: `tiny` es rapido y poco fiable con
  nombres propios; `medium` es notablemente mejor y bastante mas lento.
- Sitios que no sean YouTube (Vimeo, Twitter/X...) no tienen este problema,
  pero tampoco la cadena de clientes alternativos.
