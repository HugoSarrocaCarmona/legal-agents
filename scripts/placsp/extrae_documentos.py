#!/usr/bin/env python3
"""
Localiza y descarga los pliegos (PCAP y PPT) de un conjunto de expedientes.

El hallazgo que hace esto posible
---------------------------------
La ficha web de una licitación en la PLACSP es un portlet JSF: los documentos
cuelgan de *postbacks* de JavaScript y no hay un `href` que seguir. Parecía exigir
un navegador headless.

No hace falta. **El propio XML CODICE lleva la URL de descarga directa de cada
documento**, en `cac:LegalDocumentReference` (el PCAP y los pliegos
administrativos), `cac:TechnicalDocumentReference` (el PPT) y
`cac:AdditionalDocumentReference` (anexos, memorias, cuadros de características).
Son URLs de `GetDocumentByIdServlet` que responden el PDF a un `curl` normal.

Dónde aparecen, y por qué hay que recorrer todos los ficheros
-------------------------------------------------------------
Las referencias a documentos se publican en las **fases iniciales** del expediente
—el anuncio de licitación—, no en la publicación final que declara el resultado.
Quedarse con el último estado de cada expediente, que es lo correcto para contar
resultados, **pierde justamente los enlaces**. Por eso este script no deduplica por
fase: recorre todas las publicaciones y acumula todo documento que encuentre.

Uso
---
    python3 extrae_documentos.py raw/*.zip \\
        --expedientes corpus/pliegos-a-leer.csv \\
        -o corpus/documentos.csv \\
        --descargar Inputs/pliegos
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

csv.field_size_limit(10_000_000)

# Se trabaja con expresiones regulares sobre el texto del .atom en vez de con un
# parser XML. Es la excepción a lo que hace `parse_resultados.py`, y tiene motivo:
# aquí solo se buscan tres estructuras muy concretas dentro de cada <entry>, y
# recorrer el árbol completo de CODICE para eso multiplica por seis el tiempo sobre
# 1,4 GB por fichero.
RE_ENTRY = re.compile(r"<entry>.*?</entry>", re.S)
RE_EXPEDIENTE = re.compile(r"<cbc:ContractFolderID>([^<]*)</cbc:ContractFolderID>")
RE_PLATAFORMA = re.compile(r'<cbc:ID schemeName="ID_PLATAFORMA">([^<]*)</cbc:ID>')
RE_ENLACE = re.compile(r'<link href="([^"]*)"')

CLASES = {
    "LegalDocumentReference": "PCAP / administrativo",
    "TechnicalDocumentReference": "PPT / técnico",
    "AdditionalDocumentReference": "anexo",
}
RE_DOCS = {
    clase: re.compile(
        rf"<cac:{clase}>\s*<cbc:ID>([^<]*)</cbc:ID>\s*"
        rf"<cac:Attachment>\s*<cac:ExternalReference>\s*<cbc:URI>(.*?)</cbc:URI>",
        re.S,
    )
    for clase in CLASES
}

CAMPOS = ["expediente", "organo", "organo_id_plataforma", "clase",
          "nombre", "url", "fichero_local"]

CABECERAS = {
    # El servlet responde igual sin identificarse, pero enviar un agente honesto es
    # lo correcto al automatizar contra un servicio público.
    "User-Agent": "legal-agents/0.1 (proyecto académico; datos abiertos PLACSP)",
    "Accept": "*/*",
}


def claves_objetivo(ruta: Path) -> dict[tuple[str, str], dict]:
    """Lee la selección y devuelve las claves (órgano, expediente) a buscar."""
    objetivo: dict[tuple[str, str], dict] = {}
    with ruta.open(encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            organo = (fila.get("organo_id_plataforma") or fila.get("organo") or "").strip()
            objetivo[(organo, fila["expediente"].strip())] = fila
    return objetivo


def nombre_seguro(orden: str, clase: str, nombre: str) -> str:
    """Nombre de fichero legible y sin sorpresas del sistema de ficheros."""
    base = re.sub(r"[^\w.\- ]+", "_", nombre).strip().strip(".")[:70] or "documento"
    if not base.lower().endswith(".pdf"):
        base += ".pdf"
    etiqueta = {"PCAP / administrativo": "PCAP", "PPT / técnico": "PPT"}.get(clase, "anexo")
    return f"{orden:0>2}_{etiqueta}_{base}"


def descarga(url: str, destino: Path, intentos: int = 3) -> str:
    """Descarga un documento. Devuelve '' si no se pudo, nunca lanza.

    Algunas URLs de la sindicación apuntan a documentos que el servidor ya no
    sirve y responde un 500 con una excepción Java. No es un fallo del script y no
    debe interrumpir la descarga de los demás: se registra y se sigue.
    """
    for intento in range(intentos):
        try:
            peticion = urllib.request.Request(url, headers=CABECERAS)
            with urllib.request.urlopen(peticion, timeout=120) as r:
                tipo = r.headers.get("Content-Type", "")
                datos = r.read()
            if "pdf" not in tipo.lower() and not datos.startswith(b"%PDF"):
                print(f"      no es un PDF ({tipo})", file=sys.stderr)
                return ""
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_bytes(datos)
            return str(destino)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            if intento == intentos - 1:
                print(f"      no descargado: {e}", file=sys.stderr)
                return ""
            time.sleep(2 ** intento)
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("fuentes", nargs="+", type=Path)
    ap.add_argument("--expedientes", type=Path, required=True)
    ap.add_argument("-o", "--salida", type=Path, required=True)
    ap.add_argument("--descargar", type=Path, default=None,
                    help="directorio donde guardar los PDF; si se omite, solo lista")
    ap.add_argument("--solo-pliegos", action="store_true",
                    help="descarga únicamente PCAP y PPT, no los anexos")
    args = ap.parse_args()

    objetivo = claves_objetivo(args.expedientes)
    expedientes = {exp for _, exp in objetivo}
    print(f"Buscando documentos de {len(objetivo)} expedientes", file=sys.stderr)

    encontrados: dict[str, dict] = {}  # por URL, para no repetir

    for fuente in args.fuentes:
        if not fuente.exists():
            continue
        with zipfile.ZipFile(fuente) as z:
            for nombre_atom in sorted(z.namelist()):
                if not nombre_atom.lower().endswith(".atom"):
                    continue
                with z.open(nombre_atom) as f:
                    texto = io.TextIOWrapper(f, encoding="utf-8", errors="replace").read()
                # Descarte rápido: si ningún expediente buscado aparece en el
                # fichero, no merece la pena recorrer sus entradas.
                if not any(exp in texto for exp in expedientes):
                    continue
                for entrada in RE_ENTRY.finditer(texto):
                    bloque = entrada.group(0)
                    m_exp = RE_EXPEDIENTE.search(bloque)
                    if not m_exp:
                        continue
                    exp = m_exp.group(1).strip()
                    if exp not in expedientes:
                        continue
                    m_plat = RE_PLATAFORMA.search(bloque)
                    plataforma = m_plat.group(1).strip() if m_plat else ""
                    if (plataforma, exp) not in objetivo:
                        continue
                    fila_sel = objetivo[(plataforma, exp)]
                    for clase, patron in RE_DOCS.items():
                        for m in patron.finditer(bloque):
                            url = html.unescape(m.group(2)).strip()
                            if url in encontrados:
                                continue
                            encontrados[url] = {
                                "expediente": exp,
                                "organo": fila_sel.get("organo", ""),
                                "organo_id_plataforma": plataforma,
                                "clase": CLASES[clase],
                                "nombre": m.group(1).strip(),
                                "url": url,
                                "fichero_local": "",
                                "_orden": fila_sel.get("orden", "0"),
                            }
        print(f"  {fuente.name}: {len(encontrados)} documentos acumulados", file=sys.stderr)

    if args.descargar:
        for doc in sorted(encontrados.values(), key=lambda d: (d["_orden"], d["clase"])):
            if args.solo_pliegos and doc["clase"] == "anexo":
                continue
            destino = args.descargar / nombre_seguro(doc["_orden"], doc["clase"], doc["nombre"])
            print(f"  [{doc['_orden']}] {doc['clase']}: {doc['nombre'][:55]}", file=sys.stderr)
            doc["fichero_local"] = descarga(doc["url"], destino)

    args.salida.parent.mkdir(parents=True, exist_ok=True)
    with args.salida.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS)
        escritor.writeheader()
        for doc in sorted(encontrados.values(), key=lambda d: (d["_orden"], d["clase"])):
            escritor.writerow({k: doc[k] for k in CAMPOS})

    bajados = sum(1 for d in encontrados.values() if d["fichero_local"])
    exp_con_doc = len({d["expediente"] for d in encontrados.values()})
    print(f"\n{len(encontrados)} documentos de {exp_con_doc}/{len(objetivo)} expedientes"
          f"; {bajados} descargados -> {args.salida}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
