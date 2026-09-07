#!/usr/bin/env python3
"""Convierte un video en texto analizable, sin reproducirlo.

Dado un enlace (YouTube, Vimeo, Twitter/X, y ~1800 sitios mas via yt-dlp) o un
fichero local, produce en un directorio de salida:

    metadata.json    titulo, canal, duracion, fecha, descripcion, capitulos
    transcript.md    transcripcion con marcas de tiempo, seccionada por capitulos
    index.json       inventario de lo generado y como se obtuvo
    frames/          fotogramas clave en JPEG; solo con --frames N

La transcripcion sale de los subtitulos del propio video cuando existen (rapido
y exacto) y, si no los hay, de una transcripcion local con faster-whisper.

Los fotogramas son opcionales a proposito: sirven cuando el audio no lleva la
informacion (diapositivas, demos, graficos) y cuestan tiempo y contexto.

Uso:
    python3 tools/video/watch_video.py URL [--out DIR] [--lang es] [--frames 24]

Ver --help para el resto de opciones.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
from collections import deque
from pathlib import Path

# --------------------------------------------------------------------------
# utilidades
# --------------------------------------------------------------------------

TAG_RE = re.compile(r"<[^>]+>")
CUE_RE = re.compile(
    r"^(\d{1,2}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{1,2}:\d{2}:\d{2}[.,]\d{3})"
)
SKIP_PREFIXES = ("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE", "REGION")


def log(msg: str) -> None:
    print(f"[watch] {msg}", file=sys.stderr, flush=True)


def run(cmd: list[str], timeout: int = 1800, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if check and proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-8:]
        raise RuntimeError(f"fallo `{cmd[0]}` (codigo {proc.returncode}):\n" + "\n".join(tail))
    return proc


def require(binary: str) -> str:
    path = shutil.which(binary)
    if not path:
        raise SystemExit(
            f"Falta `{binary}`. Ejecuta tools/video/setup.sh para instalar las dependencias."
        )
    return path


def hhmmss(seconds: float, force_hours: bool = False) -> str:
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h or force_hours:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def to_seconds(stamp: str) -> float:
    stamp = stamp.replace(",", ".")
    parts = stamp.split(":")
    h, m, s = (["0"] * (3 - len(parts))) + parts
    return int(h) * 3600 + int(m) * 60 + float(s)


# --------------------------------------------------------------------------
# metadatos
# --------------------------------------------------------------------------

# YouTube devuelve 429 con facilidad; estas opciones reparten las peticiones.
YTDLP_BASE = [
    "--no-playlist",
    "--retries", "5",
    "--extractor-retries", "5",
    "--sleep-requests", "1",
    "--no-warnings",
]

# Opciones de autenticacion (cookies), rellenadas desde los argumentos.
YTDLP_AUTH: list[str] = []

# YouTube rechaza a los clientes por defecto desde IPs de datacenter con
# "Sign in to confirm you're not a bot". Algunos clientes alternativos pasan.
# None = el que elija yt-dlp; el resto se prueban en orden.
YT_CLIENTS: list[str | None] = [None, "web_safari", "mweb", "tv", "web_embedded"]

BOT_CHECK = "not a bot"


def client_args(client: str | None) -> list[str]:
    if client is None:
        return []
    # Sin formatos descargables aun se obtienen metadatos y, a veces, subtitulos.
    return ["--extractor-args", f"youtube:player_client={client}",
            "--ignore-no-formats-error"]


def fetch_metadata(url: str) -> tuple[dict, str | None]:
    """Devuelve (info, cliente_que_funciono). Prueba clientes alternativos si el
    de por defecto choca con la verificacion anti-bot de YouTube."""
    log("descargando metadatos")
    last_err = ""
    for client in YT_CLIENTS:
        proc = run(
            ["yt-dlp", *YTDLP_BASE, *YTDLP_AUTH, *client_args(client),
             "--skip-download", "--dump-single-json", url],
            timeout=300, check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            try:
                info = json.loads(proc.stdout)
            except json.JSONDecodeError:
                last_err = proc.stdout[-300:]
                continue
            if client:
                log(f"el cliente por defecto fue rechazado; usando '{client}'")
            return info, client
        last_err = (proc.stderr or proc.stdout or "").strip()
        if BOT_CHECK not in last_err and "Requested format" not in last_err:
            break  # el fallo no es la verificacion anti-bot: no insistir
    if BOT_CHECK in last_err:
        raise RuntimeError(
            "YouTube pide verificacion anti-bot para este video desde esta IP.\n"
            "Soluciones, por orden:\n"
            "  1. Ejecutarlo desde tu propio ordenador.\n"
            "  2. Pasar cookies del navegador:  --cookies-from-browser chrome\n"
            "  3. Exportar cookies a un fichero y pasar:  --cookies cookies.txt\n"
            f"Detalle: {last_err.splitlines()[-1][:200] if last_err else 'sin detalle'}"
        )
    raise RuntimeError("no se pudieron obtener los metadatos:\n" + last_err[-400:])


def summarize_metadata(info: dict) -> dict:
    chapters = [
        {
            "start": round(c.get("start_time") or 0, 2),
            "start_hms": hhmmss(c.get("start_time") or 0),
            "title": c.get("title"),
        }
        for c in (info.get("chapters") or [])
    ]
    upload = info.get("upload_date")
    if upload and len(upload) == 8:
        upload = f"{upload[:4]}-{upload[4:6]}-{upload[6:]}"
    return {
        "id": info.get("id"),
        "title": info.get("title"),
        "channel": info.get("channel") or info.get("uploader"),
        "channel_url": info.get("channel_url") or info.get("uploader_url"),
        "webpage_url": info.get("webpage_url"),
        "duration_seconds": info.get("duration"),
        "duration_hms": hhmmss(info["duration"]) if info.get("duration") else None,
        "upload_date": upload,
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "language": info.get("language"),
        "categories": info.get("categories"),
        "tags": (info.get("tags") or [])[:30],
        "chapters": chapters,
        "description": info.get("description"),
    }


# --------------------------------------------------------------------------
# subtitulos
# --------------------------------------------------------------------------

def pick_sub_track(info: dict, langs: list[str]) -> tuple[str, bool] | None:
    """Elige una sola pista: manual en el idioma pedido > manual cualquiera >
    automatica en el idioma pedido > automatica cualquiera.

    Se descarga una unica pista a proposito: pedir varias dispara el 429.
    """
    manual = info.get("subtitles") or {}
    auto = info.get("automatic_captions") or {}
    # Las claves "live_chat" no son subtitulos.
    manual = {k: v for k, v in manual.items() if k != "live_chat"}
    auto = {k: v for k, v in auto.items() if k != "live_chat"}

    def match(pool: dict) -> str | None:
        for want in langs:
            if want in pool:
                return want
            # es-419, es-ES, en-orig ...
            for key in pool:
                if key.split("-")[0].lower() == want.lower():
                    return key
        return None

    for pool, is_auto in ((manual, False), (auto, True)):
        hit = match(pool)
        if hit:
            return hit, is_auto
    if manual:
        return sorted(manual)[0], False
    if auto:
        return sorted(auto)[0], True
    return None


def download_subs(url: str, lang: str, is_auto: bool, workdir: Path,
                  client: str | None = None) -> Path | None:
    log(f"descargando subtitulos ({lang}, {'automaticos' if is_auto else 'manuales'})")
    cmd = [
        "yt-dlp", *YTDLP_BASE, *YTDLP_AUTH, *client_args(client),
        "--skip-download",
        "--write-auto-subs" if is_auto else "--write-subs",
        "--sub-langs", lang,
        "--sub-format", "vtt/srt/best",
        "-o", str(workdir / "subs.%(ext)s"),
        url,
    ]
    run(cmd, timeout=600, check=False)
    found = sorted(workdir.glob("subs*.vtt")) + sorted(workdir.glob("subs*.srt"))
    return found[0] if found else None


def parse_cues(path: Path) -> list[tuple[float, list[str]]]:
    cues: list[tuple[float, list[str]]] = []
    start: float | None = None
    buf: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        m = CUE_RE.match(line)
        if m:
            if start is not None and buf:
                cues.append((start, buf))
            start, buf = to_seconds(m.group(1)), []
            continue
        if not line or line.startswith(SKIP_PREFIXES) or line.isdigit():
            continue
        if start is not None:
            buf.append(line)
    if start is not None and buf:
        cues.append((start, buf))
    return cues


def clean_line(text: str) -> str:
    text = TAG_RE.sub("", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def dedupe(cues: list[tuple[float, list[str]]]) -> list[tuple[float, str]]:
    """Los subtitulos automaticos de YouTube son 'rolling': cada cue repite la
    linea anterior y le anade palabras. Esto reconstruye el texto lineal."""
    out: list[tuple[float, str]] = []
    recent: deque[str] = deque(maxlen=8)
    for start, lines in cues:
        for raw in lines:
            line = clean_line(raw)
            if not line:
                continue
            norm = line.lower()
            if norm in recent:
                continue
            if out:
                prev = out[-1][1].lower()
                if norm in prev:          # el cue nuevo es un trozo del anterior
                    continue
                if prev in norm:          # el cue anterior crecio: se sustituye
                    out[-1] = (out[-1][0], line)
                    recent.append(norm)
                    continue
            recent.append(norm)
            out.append((start, line))
    return out


# --------------------------------------------------------------------------
# transcripcion local (sin subtitulos disponibles)
# --------------------------------------------------------------------------

def download_audio(url: str, workdir: Path) -> Path:
    log("descargando pista de audio")
    run(
        ["yt-dlp", *YTDLP_BASE, *YTDLP_AUTH, "-f", "bestaudio/best",
         "-o", str(workdir / "audio.%(ext)s"), url],
        timeout=1800,
    )
    files = [p for p in workdir.glob("audio.*") if p.is_file()]
    if not files:
        raise RuntimeError("no se pudo descargar el audio")
    return files[0]


def to_wav16k(src: Path, workdir: Path) -> Path:
    dst = workdir / "audio16k.wav"
    run(["ffmpeg", "-y", "-i", str(src), "-ac", "1", "-ar", "16000", "-vn", str(dst)],
        timeout=1800)
    return dst


def whisper_transcribe(audio: Path, model_size: str, lang: str | None,
                       vad: bool = False) -> list[tuple[float, str]]:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise SystemExit(
            "Falta faster-whisper. Ejecuta tools/video/setup.sh (o pip install faster-whisper)."
        )
    log(f"transcribiendo con faster-whisper ({model_size}); puede tardar")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def attempt(use_vad: bool) -> list[tuple[float, str]]:
        segments, _ = model.transcribe(
            str(audio), language=lang, vad_filter=use_vad, beam_size=1,
        )
        return [(seg.start, seg.text.strip()) for seg in segments if seg.text.strip()]

    out = attempt(vad)
    # El filtro VAD depende de un modelo aparte que en algunos entornos no carga
    # y descarta el audio entero en silencio, sin lanzar error.
    if not out and vad:
        log("el filtro VAD no devolvio nada: reintentando sin VAD")
        out = attempt(False)
    return out


# --------------------------------------------------------------------------
# fotogramas
# --------------------------------------------------------------------------

def download_video(url: str, workdir: Path, max_height: int) -> Path:
    log(f"descargando video (max {max_height}p, sin audio si es posible)")
    fmt = (
        f"bv*[height<={max_height}][ext=mp4]/bv*[height<={max_height}]/"
        f"b[height<={max_height}]/worstvideo/worst"
    )
    run(["yt-dlp", *YTDLP_BASE, *YTDLP_AUTH, "-f", fmt,
         "-o", str(workdir / "video.%(ext)s"), url],
        timeout=2400)
    files = [p for p in workdir.glob("video.*") if p.is_file()]
    if not files:
        raise RuntimeError("no se pudo descargar el video")
    return files[0]


PTS_RE = re.compile(r"pts_time:([0-9]+(?:\.[0-9]+)?)")


def scene_timestamps(video: Path, threshold: float) -> list[float]:
    """Detecta cambios de plano con select+showinfo sobre una copia reducida a
    320px: el resultado es el mismo que a resolucion completa y el escaneo va
    unas 30x mas rapido que el tiempo real del video.

    (`ffprobe -f lavfi movie=...` parece equivalente pero no computa `scene`
    correctamente: devuelve un unico fotograma.)
    """
    log("detectando cambios de plano")
    proc = run(
        ["ffmpeg", "-nostdin", "-i", str(video),
         "-vf", f"scale=320:-2,select='gt(scene,{threshold})',showinfo",
         "-an", "-f", "null", "-"],
        timeout=2400, check=False,
    )
    return [float(m) for m in PTS_RE.findall(proc.stderr)]


def thin(values: list[float], limit: int) -> list[float]:
    if len(values) <= limit:
        return values
    step = (len(values) - 1) / (limit - 1) if limit > 1 else 1
    return [values[round(i * step)] for i in range(limit)]


def grab_frames(video: Path, stamps: list[float], outdir: Path, height: int) -> list[dict]:
    outdir.mkdir(parents=True, exist_ok=True)
    frames = []
    for i, t in enumerate(stamps, start=1):
        name = f"frame_{i:03d}_{hhmmss(t, force_hours=True).replace(':', '')}.jpg"
        dst = outdir / name
        proc = run(
            ["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1",
             "-vf", f"scale=-2:{height}", "-q:v", "4", str(dst)],
            timeout=300, check=False,
        )
        if dst.exists() and dst.stat().st_size > 0:
            frames.append({"file": name, "t": round(t, 2), "t_hms": hhmmss(t)})
    log(f"{len(frames)} fotogramas extraidos")
    return frames


# --------------------------------------------------------------------------
# salida
# --------------------------------------------------------------------------

def render_transcript(lines: list[tuple[float, str]], meta: dict, source: str,
                      chunk: int) -> str:
    """Transcripcion en bloques con marca de tiempo, seccionada por los
    capitulos del video cuando los publica. La estructura es lo que permite
    analizar un video largo por partes en vez de leerlo entero de una vez."""
    long_video = (meta.get("duration_seconds") or 0) >= 3600
    blocks: list[tuple[float, str]] = []
    block_start: float | None = None
    buf: list[str] = []
    for start, text in lines:
        if block_start is None:
            block_start = start
        if start - block_start >= chunk and buf:
            blocks.append((block_start, " ".join(buf)))
            block_start, buf = start, []
        buf.append(text)
    if buf and block_start is not None:
        blocks.append((block_start, " ".join(buf)))

    words = sum(len(t.split()) for _, t in lines)
    head = [
        f"# {meta.get('title') or 'Video'}",
        "",
        f"- Fuente: {meta.get('webpage_url') or 'fichero local'}",
        f"- Canal: {meta.get('channel') or '-'}",
        f"- Duracion: {meta.get('duration_hms') or '-'}",
        f"- Transcripcion obtenida de: {source}",
        f"- {words} palabras en bloques de ~{chunk}s",
        "",
    ]
    if meta.get("chapters"):
        head += ["## Indice", ""]
        head += [f"- [{c['start_hms']}] {c['title']}" for c in meta["chapters"]]
        head += [""]
    head += ["## Transcripcion", ""]

    pending = list(meta.get("chapters") or [])
    body: list[str] = []
    for t, text in blocks:
        while pending and (pending[0]["start"] or 0) <= t:
            ch = pending.pop(0)
            body.append(f"### [{ch['start_hms']}] {ch['title']}\n")
        body.append(f"**[{hhmmss(t, force_hours=long_video)}]** {text}\n")
    return "\n".join(head + body)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Extrae transcripcion, metadatos y fotogramas clave de un video.",
    )
    ap.add_argument("source", help="URL del video o ruta a un fichero local")
    ap.add_argument("--out", default=None,
                    help="directorio de salida (por defecto ./video_out/<id>)")
    ap.add_argument("--lang", default="es,en",
                    help="idiomas preferidos de subtitulos, por orden (por defecto es,en)")
    ap.add_argument("--frames", type=int, default=0,
                    help="extraer hasta N fotogramas clave (por defecto 0: solo texto)")
    ap.add_argument("--no-frames", action="store_true",
                    help="(ya es el comportamiento por defecto)")
    ap.add_argument("--frame-height", type=int, default=540,
                    help="alto en px de los fotogramas (por defecto 540)")
    ap.add_argument("--max-height", type=int, default=480,
                    help="calidad maxima del video descargado para fotogramas")
    ap.add_argument("--scene-threshold", type=float, default=0.25,
                    help="sensibilidad de deteccion de cambio de plano (0-1)")
    ap.add_argument("--chunk", type=int, default=None,
                    help="segundos por bloque (por defecto 30, o 60 si dura mas de 30 min)")
    ap.add_argument("--whisper", action="store_true",
                    help="forzar transcripcion local aunque haya subtitulos")
    ap.add_argument("--whisper-model", default="small",
                    help="modelo faster-whisper: tiny/base/small/medium/large-v3")
    ap.add_argument("--vad", action="store_true",
                    help="filtrar silencios antes de transcribir (requiere el modelo VAD)")
    ap.add_argument("--keep-media", action="store_true",
                    help="conservar el audio y el video descargados")
    ap.add_argument("--cookies", metavar="FICHERO",
                    help="cookies en formato Netscape (para videos que exigen sesion)")
    ap.add_argument("--cookies-from-browser", metavar="NAVEGADOR",
                    help="tomar las cookies del navegador: chrome, firefox, edge, safari...")
    args = ap.parse_args()

    if args.cookies:
        YTDLP_AUTH.extend(["--cookies", args.cookies])
    if args.cookies_from_browser:
        YTDLP_AUTH.extend(["--cookies-from-browser", args.cookies_from_browser])

    require("yt-dlp")
    want_frames = not args.no_frames and args.frames > 0
    if want_frames:
        require("ffmpeg")
        require("ffprobe")

    local = Path(args.source)
    is_local = local.exists() and local.is_file()
    client: str | None = None

    # ---- metadatos
    if is_local:
        info = {"id": local.stem, "title": local.stem}
        try:
            probe = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                         "-of", "csv=p=0", str(local)], timeout=120, check=False)
            info["duration"] = float(probe.stdout.strip())
        except (ValueError, RuntimeError):
            pass
    else:
        info, client = fetch_metadata(args.source)
    meta = summarize_metadata(info)

    outdir = Path(args.out) if args.out else Path("video_out") / (meta.get("id") or "video")
    outdir.mkdir(parents=True, exist_ok=True)
    workdir = outdir / ".work"
    workdir.mkdir(exist_ok=True)
    (outdir / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log(f"salida en {outdir}")

    # ---- transcripcion
    lines: list[tuple[float, str]] = []
    source_label = "ninguna"
    langs = [x.strip() for x in args.lang.split(",") if x.strip()]

    if not args.whisper and not is_local:
        track = pick_sub_track(info, langs)
        if track:
            lang, is_auto = track
            sub_path = download_subs(args.source, lang, is_auto, workdir, client)
            if sub_path:
                lines = dedupe(parse_cues(sub_path))
                kind = "automaticos" if is_auto else "manuales"
                source_label = f"subtitulos {kind} del video ({lang})"
        else:
            log("el video no publica subtitulos")

    if not lines:
        if not is_local and client is not None:
            # Los clientes alternativos dan metadatos pero no formatos
            # descargables, asi que no hay audio que transcribir.
            raise RuntimeError(
                "Este video no expone subtitulos y YouTube no permite descargar "
                "su audio desde esta IP.\nPasa cookies del navegador "
                "(--cookies-from-browser chrome) o ejecutalo desde tu ordenador.\n"
                f"Los metadatos si se han guardado en {outdir}/metadata.json"
            )
        media = local if is_local else download_audio(args.source, workdir)
        wav = to_wav16k(media, workdir)
        lang_hint = langs[0] if len(langs) == 1 else None
        lines = whisper_transcribe(wav, args.whisper_model, lang_hint, vad=args.vad)
        source_label = f"transcripcion local con faster-whisper ({args.whisper_model})"

    chunk = args.chunk
    if chunk is None:
        chunk = 60 if (meta.get("duration_seconds") or 0) > 1800 else 30
    transcript = render_transcript(lines, meta, source_label, chunk)
    (outdir / "transcript.md").write_text(transcript, encoding="utf-8")
    words = sum(len(t.split()) for _, t in lines)
    log(f"transcripcion: {len(lines)} segmentos, ~{words} palabras")

    # ---- fotogramas
    frames: list[dict] = []
    if want_frames and not is_local and client is not None:
        log("sin formatos descargables desde esta IP: se omiten los fotogramas")
        want_frames = False
    if want_frames:
        try:
            video = local if is_local else download_video(args.source, workdir, args.max_height)
            stamps = scene_timestamps(video, args.scene_threshold)
            duration = meta.get("duration_seconds") or 0
            if len(stamps) < max(4, args.frames // 4) and duration:
                log("pocos cambios de plano: se muestrea de forma uniforme")
                step = duration / (args.frames + 1)
                stamps = [step * (i + 1) for i in range(args.frames)]
            stamps = thin(sorted(stamps), args.frames)
            frames = grab_frames(video, stamps, outdir / "frames", args.frame_height)
            (outdir / "frames" / "index.json").write_text(
                json.dumps(frames, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception as exc:  # los fotogramas son opcionales: no tumban la extraccion
            log(f"no se pudieron extraer fotogramas: {exc}")

    # ---- inventario
    index = {
        "source": args.source,
        "output_dir": str(outdir),
        "metadata": "metadata.json",
        "transcript": "transcript.md",
        "transcript_source": source_label,
        "transcript_segments": len(lines),
        "transcript_words": words,
        "frames_dir": "frames" if frames else None,
        "frames": frames,
        "title": meta.get("title"),
        "duration_hms": meta.get("duration_hms"),
    }
    (outdir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if not args.keep_media:
        shutil.rmtree(workdir, ignore_errors=True)

    print(json.dumps(index, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        log(f"ERROR: {exc}")
        sys.exit(1)
