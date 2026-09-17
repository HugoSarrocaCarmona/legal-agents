#!/usr/bin/env python3
"""
Extrae el resultado de cada licitación publicada en la Plataforma de Contratación
del Sector Público a partir de los ficheros de sindicación en formato CODICE.

Qué hace y qué NO hace
----------------------
Hace: convertir XML CODICE en filas planas, una por (expediente, lote, resultado),
sin interpretar nada. Todos los campos son transcripción literal del XML.

No hace: clasificar, agregar ni deducir causas. Eso es `analiza_desiertos.py`, y va
aparte a propósito: si la extracción y el juicio viven en el mismo fichero, deja de
poder comprobarse cuál de los dos se equivocó.

Fuente
------
https://contrataciondelsectorpublico.gob.es/sindicacion/sindicacion_643/
    licitacionesPerfilesContratanteCompleto3_AAAAMM.zip

Uso
---
    python3 parse_resultados.py raw/*.zip -o datos/resultados.csv
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
import zipfile
from pathlib import Path
from typing import Iterator
from xml.etree import ElementTree as ET

# --- Campos de salida -------------------------------------------------------
# Orden fijo: el CSV se lee a mano y con pandas, y las columnas no deben bailar.
CAMPOS = [
    "atom_id",             # identificador de la publicación en la sindicación
    "actualizado",         # <updated> del entry: permite quedarse con la última versión
    "expediente",          # cbc:ContractFolderID
    "estado",              # ContractFolderStatusCode: PUB, EV, ADJ, RES, ANUL...
    "organo",              # nombre del órgano de contratación
    "organo_nif",
    "organo_id_plataforma",
    "tipo_contrato",       # ProcurementProject/cbc:TypeCode (código CODICE sin traducir)
    "cpv",                 # primer ItemClassificationCode
    "nuts",                # CountrySubentityCode del lugar de ejecución
    "importe_sin_iva",     # BudgetAmount/TaxExclusiveAmount del expediente
    "procedimiento",       # TenderingProcess/cbc:ProcedureCode
    "sistema_contratacion",  # TenderingProcess/cbc:ContractingSystemCode
    "urgencia",            # TenderingProcess/cbc:UrgencyCode
    "lote",                # ProcurementProjectLotID, vacío si no hay lotes
    "resultado_codigo",    # TenderResult/cbc:ResultCode
    "resultado_motivo",    # TenderResult/cbc:Description -- texto libre del órgano
    "fecha_resultado",     # cbc:AwardDate
    "ofertas_recibidas",   # cbc:ReceivedTenderQuantity
    "ofertas_pymes",       # cbc:SMEsReceivedTenderQuantity
    "oferta_mas_baja",     # cbc:LowerTenderAmount
    "oferta_mas_alta",     # cbc:HigherTenderAmount
    "adjudicatario",       # WinningParty/PartyName/Name
    "importe_adjudicado",  # TenderResult/LegalMonetaryTotal/TaxExclusiveAmount
    "fichero",             # de qué .atom salió, para poder rehacer el camino
]


def local(tag: str) -> str:
    """Nombre de etiqueta sin el espacio de nombres.

    CODICE mezcla cinco namespaces (cbc, cac, cbc-place-ext, cac-place-ext, ubl) y
    ha cambiado de versión varias veces. Emparejar por nombre local es lo único que
    sobrevive a eso; el precio es tener que anclar cada búsqueda a su rama.
    """
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def texto(nodo, *ruta: str) -> str:
    """Devuelve el texto del primer descendiente que sigue la ruta de nombres locales.

    Cadena vacía si no existe. Nunca None: el CSV no distingue null de vacío y
    fingir que sí lo hace sería inventarse una precisión que el formato no tiene.
    """
    actual = nodo
    for nombre in ruta:
        siguiente = None
        for hijo in actual:
            if local(hijo.tag) == nombre:
                siguiente = hijo
                break
        if siguiente is None:
            return ""
        actual = siguiente
    return (actual.text or "").strip()


def buscar(nodo, nombre: str):
    """Primer descendiente a cualquier profundidad con ese nombre local."""
    for hijo in nodo.iter():
        if local(hijo.tag) == nombre:
            return hijo
    return None


def buscar_todos(nodo, nombre: str) -> list:
    return [h for h in nodo.iter() if local(h.tag) == nombre]


def hijo(nodo, nombre: str):
    if nodo is None:
        return None
    for h in nodo:
        if local(h.tag) == nombre:
            return h
    return None


def extrae_entry(entry, fichero: str) -> Iterator[dict]:
    """Convierte un <entry> de la sindicación en una o varias filas.

    Una fila por TenderResult. Un expediente con cinco lotes adjudicados produce
    cinco filas; uno todavía en plazo produce una sola con los campos de resultado
    vacíos. Colapsar los lotes perdería justo lo que interesa: un expediente puede
    quedar desierto en un lote y adjudicarse en otro.
    """
    atom_id = texto(entry, "id")
    actualizado = texto(entry, "updated")

    cfs = hijo(entry, "ContractFolderStatus")
    if cfs is None:
        return

    expediente = texto(cfs, "ContractFolderID")
    estado = texto(cfs, "ContractFolderStatusCode")

    # --- Órgano de contratación ---
    lcp = hijo(cfs, "LocatedContractingParty")
    party = hijo(lcp, "Party") if lcp is not None else None
    organo = organo_nif = organo_plataforma = ""
    if party is not None:
        organo = texto(party, "PartyName", "Name")
        for ident in buscar_todos(party, "PartyIdentification"):
            id_nodo = hijo(ident, "ID")
            if id_nodo is None:
                continue
            esquema = id_nodo.get("schemeName", "")
            valor = (id_nodo.text or "").strip()
            if esquema == "NIF":
                organo_nif = valor
            elif esquema == "ID_PLATAFORMA":
                organo_plataforma = valor

    # --- Objeto del contrato ---
    proyecto = hijo(cfs, "ProcurementProject")
    tipo = cpv = nuts = importe = ""
    if proyecto is not None:
        tipo = texto(proyecto, "TypeCode")
        importe = texto(proyecto, "BudgetAmount", "TaxExclusiveAmount")
        clasif = buscar(proyecto, "ItemClassificationCode")
        if clasif is not None:
            cpv = (clasif.text or "").strip()
        sub = buscar(proyecto, "CountrySubentityCode")
        if sub is not None:
            nuts = (sub.text or "").strip()

    # --- Procedimiento ---
    proceso = hijo(cfs, "TenderingProcess")
    procedimiento = texto(proceso, "ProcedureCode") if proceso is not None else ""
    sistema = texto(proceso, "ContractingSystemCode") if proceso is not None else ""
    urgencia = texto(proceso, "UrgencyCode") if proceso is not None else ""

    base = {
        "atom_id": atom_id,
        "actualizado": actualizado,
        "expediente": expediente,
        "estado": estado,
        "organo": organo,
        "organo_nif": organo_nif,
        "organo_id_plataforma": organo_plataforma,
        "tipo_contrato": tipo,
        "cpv": cpv,
        "nuts": nuts,
        "importe_sin_iva": importe,
        "procedimiento": procedimiento,
        "sistema_contratacion": sistema,
        "urgencia": urgencia,
        "fichero": fichero,
    }

    resultados = [n for n in cfs.iter() if local(n.tag) == "TenderResult"]
    if not resultados:
        fila = dict.fromkeys(CAMPOS, "")
        fila.update(base)
        yield fila
        return

    for res in resultados:
        fila = dict.fromkeys(CAMPOS, "")
        fila.update(base)
        fila["resultado_codigo"] = texto(res, "ResultCode")
        fila["resultado_motivo"] = " ".join(texto(res, "Description").split())
        fila["fecha_resultado"] = texto(res, "AwardDate")
        fila["ofertas_recibidas"] = texto(res, "ReceivedTenderQuantity")
        fila["ofertas_pymes"] = texto(res, "SMEsReceivedTenderQuantity")
        fila["oferta_mas_baja"] = texto(res, "LowerTenderAmount")
        fila["oferta_mas_alta"] = texto(res, "HigherTenderAmount")

        proyecto_adj = hijo(res, "AwardedTenderedProject")
        if proyecto_adj is not None:
            fila["lote"] = texto(proyecto_adj, "ProcurementProjectLotID")

        ganador = hijo(res, "WinningParty")
        if ganador is not None:
            fila["adjudicatario"] = texto(ganador, "PartyName", "Name")

        total = hijo(res, "LegalMonetaryTotal")
        if total is not None:
            fila["importe_adjudicado"] = texto(total, "TaxExclusiveAmount")

        yield fila


def recorre_atom(flujo, fichero: str) -> Iterator[dict]:
    """Itera los <entry> de un .atom liberando memoria al terminar cada uno.

    Los ficheros mensuales descomprimen a cientos de MB. Cargarlos enteros con
    ET.parse() funciona hasta que deja de funcionar, y falla con el fichero grande,
    que es justo el que importa.
    """
    contexto = ET.iterparse(flujo, events=("end",))
    for _, elem in contexto:
        if local(elem.tag) != "entry":
            continue
        try:
            yield from extrae_entry(elem, fichero)
        finally:
            elem.clear()


def recorre_fuente(ruta: Path) -> Iterator[dict]:
    if ruta.suffix.lower() == ".zip":
        with zipfile.ZipFile(ruta) as z:
            for nombre in sorted(z.namelist()):
                if not nombre.lower().endswith(".atom"):
                    continue
                with z.open(nombre) as f:
                    yield from recorre_atom(io.BufferedReader(f), f"{ruta.name}!{nombre}")
    else:
        with ruta.open("rb") as f:
            yield from recorre_atom(f, ruta.name)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("fuentes", nargs="+", type=Path, help="ficheros .zip o .atom de la sindicación")
    ap.add_argument("-o", "--salida", type=Path, required=True)
    args = ap.parse_args()

    args.salida.parent.mkdir(parents=True, exist_ok=True)

    filas = 0
    with args.salida.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS)
        escritor.writeheader()
        for fuente in args.fuentes:
            if not fuente.exists():
                print(f"aviso: no existe {fuente}", file=sys.stderr)
                continue
            antes = filas
            for fila in recorre_fuente(fuente):
                escritor.writerow(fila)
                filas += 1
                if filas % 50_000 == 0:
                    print(f"  {filas:,} filas...", file=sys.stderr)
            print(f"{fuente.name}: {filas - antes:,} filas", file=sys.stderr)

    print(f"\n{filas:,} filas -> {args.salida}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
