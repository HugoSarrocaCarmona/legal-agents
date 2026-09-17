#!/usr/bin/env python3
"""
Selecciona los pliegos que hay que leer a mano para inducir la rúbrica de riesgos.

Por qué esta población y no otra
--------------------------------
`analiza_desiertos.py` parte los desiertos de 2025 en dos. En el 72 % no se
presentó nadie: la causa es anterior al pliego y ninguna herramienta que lea
documentos la toca. En el 28 % restante hubo ofertas, y de esos **el 69 % tenía un
solo licitador, que fue excluido**.

Esa es la población: **una empresa quiso el contrato, presentó oferta y se quedó
fuera.** Es el único sitio donde un problema de lectura de pliego produce un
resultado observable en los datos abiertos, y por tanto el único corpus del que se
puede inducir una rúbrica que mida algo real.

Leer diez pliegos al azar habría dado el catálogo de lo que la LCSP regula. Leer
diez de estos da el catálogo de **lo que hace caer a quien licita**, que es lo que
el consejo exigió al invertir el orden de la rúbrica.

Qué se excluye y por qué
------------------------
- **Tipos distintos de obras, servicios y suministros.** Patrimonial (31 % de
  desierto), concesión de servicios (26 %) y administrativo especial (25 %) tienen
  tasas muy superiores, pero se rigen en todo o en parte por la LPAP y no por la
  LCSP. Meterlos contaminaría la rúbrica con base normativa de otra ley — el mismo
  error de régimen que `standards/contratos.md` trata como fallo duro.
- **Procedimientos sin pliego publicado.** El negociado sin publicidad y los
  derivados de acuerdo marco no publican un PCAP comparable.
- **Importes por debajo del umbral del contrato menor.** Sin pliego que leer.

Estratificación
---------------
Un órgano por pliego como máximo, y reparto por tipo de contrato y tramo de
importe. Es la mitigación del bloqueo nº 2 de `ESTADO.md`: los pliegos se redactan
sobre plantillas de cada órgano, y un corpus concentrado mediría plantillas en vez
de contratación pública.

Uso
---
    python3 selecciona_pliegos.py datos/resultados_2025.csv -n 10 -o corpus/pliegos-a-leer.csv
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from codigos import DESIERTO, PROCEDIMIENTO, TIPO_CONTRATO, nombre  # noqa: E402

csv.field_size_limit(10_000_000)

# Obras, servicios y suministros: los tres tipos que la LCSP regula de lleno y los
# únicos para los que el vocabulario de materias de `standards/contratos.md` está
# anclado a artículos verificados.
TIPOS_LCSP = {"1", "2", "3"}

# Abierto y abierto simplificado. Son el 87 % de los desiertos y los únicos que
# publican siempre un PCAP completo y comparable.
PROCEDIMIENTOS_CON_PLIEGO = {"1", "9"}

# Por debajo del umbral del contrato menor de servicios y suministros no hay pliego
# que leer (art. 118 LCSP).
IMPORTE_MINIMO = 15_000

SALIDA = [
    "orden", "expediente", "organo", "tipo_contrato", "procedimiento",
    "importe_sin_iva", "tramo", "cpv", "nuts", "lote",
    "ofertas_recibidas", "ofertas_pymes", "fecha_resultado",
    "motivo_publicado", "enlace",
    # Columnas vacías, para rellenar A MANO durante la lectura. El fichero es la
    # hoja de trabajo, no solo la lista.
    "pcap_descargado", "riesgos_anotados", "notas",
]


def a_float(v: str) -> float | None:
    try:
        return float((v or "").replace(",", "."))
    except ValueError:
        return None


def tramo(v: float | None) -> str:
    if v is None:
        return "?"
    if v < 40_000:
        return "15k-40k"
    if v < 100_000:
        return "40k-100k"
    if v < 500_000:
        return "100k-500k"
    return "500k+"


def carga(ruta: Path, anio: str | None) -> list[dict]:
    """Último estado publicado de cada (órgano, expediente, lote)."""
    ultimo: dict[tuple, str] = {}
    filas: dict[tuple, list[dict]] = defaultdict(list)
    with ruta.open(encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            if anio and not fila["fecha_resultado"].startswith(anio):
                continue
            clave = (fila["organo_id_plataforma"] or fila["organo"],
                     fila["expediente"], fila["lote"])
            marca = fila["actualizado"]
            if clave not in ultimo or marca > ultimo[clave]:
                ultimo[clave] = marca
                filas[clave] = [fila]
            elif marca == ultimo[clave]:
                filas[clave].append(fila)
    return [f for v in filas.values() for f in v]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("csv", type=Path)
    ap.add_argument("-n", "--cuantos", type=int, default=10)
    ap.add_argument("-o", "--salida", type=Path, required=True)
    ap.add_argument("--anio", default="2025")
    ap.add_argument("--semilla", type=int, default=20250917,
                    help="fija el muestreo para que la selección sea reproducible")
    args = ap.parse_args()

    filas = carga(args.csv, args.anio)

    candidatos = [
        f for f in filas
        if f["resultado_codigo"] in DESIERTO
        and (f["ofertas_recibidas"] or "").strip() == "1"
        and f["tipo_contrato"] in TIPOS_LCSP
        and f["procedimiento"] in PROCEDIMIENTOS_CON_PLIEGO
        and (a_float(f["importe_sin_iva"]) or 0) >= IMPORTE_MINIMO
        and f["enlace"]
    ]
    print(f"Población objetivo (1 licitador, excluido, LCSP, con pliego): "
          f"{len(candidatos):,}", file=sys.stderr)

    if not candidatos:
        print("Sin candidatos. ¿Falta la columna `enlace` en el CSV?", file=sys.stderr)
        return 1

    # Estratos: tipo de contrato x tramo de importe. Se recorren por turnos para
    # que diez pliegos no acaben siendo diez servicios de 100.000 EUR.
    estratos: dict[tuple, list[dict]] = defaultdict(list)
    for f in candidatos:
        estratos[(f["tipo_contrato"], tramo(a_float(f["importe_sin_iva"])))].append(f)

    azar = random.Random(args.semilla)
    for lista in estratos.values():
        azar.shuffle(lista)

    claves = sorted(estratos, key=lambda k: -len(estratos[k]))
    elegidos: list[dict] = []
    organos_usados: set[str] = set()
    i = 0
    while len(elegidos) < args.cuantos and claves:
        clave = claves[i % len(claves)]
        lista = estratos[clave]
        while lista:
            cand = lista.pop()
            organo = cand["organo_id_plataforma"] or cand["organo"]
            if organo in organos_usados:
                continue  # un órgano, un pliego: el sesgo de plantilla es real
            organos_usados.add(organo)
            elegidos.append(cand)
            break
        else:
            claves.remove(clave)
            continue
        i += 1

    args.salida.parent.mkdir(parents=True, exist_ok=True)
    with args.salida.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=SALIDA)
        escritor.writeheader()
        for n, c in enumerate(elegidos, 1):
            escritor.writerow({
                "orden": n,
                "expediente": c["expediente"],
                "organo": c["organo"],
                "tipo_contrato": nombre(TIPO_CONTRATO, c["tipo_contrato"]),
                "procedimiento": nombre(PROCEDIMIENTO, c["procedimiento"]),
                "importe_sin_iva": c["importe_sin_iva"],
                "tramo": tramo(a_float(c["importe_sin_iva"])),
                "cpv": c["cpv"],
                "nuts": c["nuts"],
                "lote": c["lote"],
                "ofertas_recibidas": c["ofertas_recibidas"],
                "ofertas_pymes": c["ofertas_pymes"],
                "fecha_resultado": c["fecha_resultado"],
                "motivo_publicado": c["resultado_motivo"],
                "enlace": c["enlace"],
                "pcap_descargado": "",
                "riesgos_anotados": "",
                "notas": "",
            })

    print(f"{len(elegidos)} pliegos -> {args.salida}", file=sys.stderr)
    print(f"Órganos distintos: {len(organos_usados)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
