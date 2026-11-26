#!/usr/bin/env bash
# Instala las dependencias que necesita tools/video/watch_video.py.
#
# El contenedor de Claude Code en la web es efimero: se reinstala en cada
# sesion nueva. En local solo hace falta ejecutarlo una vez.
#
#   bash tools/video/setup.sh            # completo
#   SKIP_WHISPER=1 bash tools/video/setup.sh   # sin transcripcion local
set -euo pipefail

say() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }

say "yt-dlp (descarga de video, subtitulos y metadatos)"
if command -v yt-dlp >/dev/null 2>&1; then
  yt-dlp -U >/dev/null 2>&1 || true
  echo "ya instalado: $(yt-dlp --version)"
else
  python3 -m pip install --quiet --break-system-packages --upgrade yt-dlp \
    || python3 -m pip install --quiet --upgrade yt-dlp
  echo "instalado: $(yt-dlp --version)"
fi

say "ffmpeg / ffprobe (audio y fotogramas)"
if command -v ffmpeg >/dev/null 2>&1; then
  echo "ya instalado: $(ffmpeg -version | head -1)"
else
  if command -v apt-get >/dev/null 2>&1; then
    (apt-get update -qq && apt-get install -y -qq ffmpeg) \
      || (sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg)
  elif command -v brew >/dev/null 2>&1; then
    brew install ffmpeg
  else
    echo "AVISO: instala ffmpeg manualmente (https://ffmpeg.org/download.html)" >&2
  fi
  command -v ffmpeg >/dev/null 2>&1 && echo "instalado: $(ffmpeg -version | head -1)"
fi

say "deno (runtime JS que yt-dlp usa para YouTube)"
if command -v deno >/dev/null 2>&1; then
  echo "ya instalado: $(deno --version | head -1)"
else
  # Sin el, yt-dlp avisa de que faltan formatos en algunos videos de YouTube.
  curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh -s -- -y >/dev/null 2>&1 \
    || echo "AVISO: no se pudo instalar deno; yt-dlp seguira funcionando con avisos" >&2
  command -v deno >/dev/null 2>&1 && echo "instalado: $(deno --version | head -1)"
fi

if [ "${SKIP_WHISPER:-0}" != "1" ]; then
  say "faster-whisper (transcripcion local si el video no trae subtitulos)"
  if python3 -c "import faster_whisper" >/dev/null 2>&1; then
    echo "ya instalado"
  else
    python3 -m pip install --quiet --break-system-packages faster-whisper \
      || python3 -m pip install --quiet faster-whisper
    echo "instalado"
  fi
fi

say "Listo"
echo "Prueba:  python3 tools/video/watch_video.py 'URL' --out /tmp/video"
