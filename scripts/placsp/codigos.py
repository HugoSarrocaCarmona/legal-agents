#!/usr/bin/env python3
"""
Listas de códigos CODICE usadas por la sindicación de la PLACSP.

Todos los valores de este fichero están **transcritos de los ficheros genericode
oficiales**, descargados el 17/09/2026. Ninguno se ha escrito de memoria. La misma
regla que rige para `base_normativa` en `standards/contratos.md` rige aquí: un
código mal traducido produce una estadística falsa, y una estadística falsa sobre
la que se decide el rumbo del proyecto es peor que no tener estadística.

Fuente (sustituir <ver> y <nombre> por los de cada lista):
    https://contrataciondelestado.es/codice/cl/<ver>/<nombre>-<ver>.gc
"""

# TenderResultCode-2.09.gc — el resultado de la licitación.
# Es la lista que decide el análisis: separa lo adjudicado de lo que no llegó a serlo.
RESULTADO = {
    "1": "Adjudicado provisionalmente",
    "2": "Adjudicado definitivamente",
    "3": "Desierto",
    "4": "Desistimiento",
    "5": "Renuncia",
    "6": "Desierto provisionalmente",
    "7": "Desierto definitivamente",
    "8": "Adjudicado",
    "9": "Formalizado",
    "10": "Licitador mejor valorado",
    "11": "Encargo formalizado",
}

# Los tres códigos de desierto conviven: los órganos usan indistintamente el
# genérico (3) y los de fase (6, 7). Contar solo el 3 subestimaría el fenómeno.
DESIERTO = {"3", "6", "7"}

# Desistimiento y renuncia NO son desierto. Son decisiones de la Administración
# (art. 152 LCSP), no falta de ofertas, y mezclarlas con el desierto es el error
# de categoría que este análisis existe para no cometer.
RETIRADO_POR_EL_ORGANO = {"4", "5"}

ADJUDICADO = {"1", "2", "8", "9", "10", "11"}

# ContractCode-2.08.gc — tipo de contrato.
TIPO_CONTRATO = {
    "1": "Suministros",
    "2": "Servicios",
    "3": "Obras",
    "21": "Gestión de servicios públicos",
    "22": "Concesión de servicios",
    "31": "Concesión de obras públicas",
    "32": "Concesión de obras",
    "40": "Colaboración entre el sector público y el sector privado",
    "7": "Administrativo especial",
    "8": "Privado",
    "50": "Patrimonial",
}

# SyndicationTenderingProcessCode-2.07.gc — procedimiento de adjudicación.
PROCEDIMIENTO = {
    "1": "Abierto",
    "2": "Restringido",
    "3": "Negociado sin publicidad",
    "4": "Negociado con publicidad",
    "5": "Diálogo competitivo",
    "6": "Contrato menor",
    "7": "Derivado de acuerdo marco",
    "8": "Concurso de proyectos",
    "9": "Abierto simplificado",
    "10": "Asociación para la innovación",
    "11": "Derivado de asociación para la innovación",
    "12": "Basado en un sistema dinámico de adquisición",
    "13": "Licitación con negociación",
    "100": "Normas internas",
    "999": "Otros",
}

# SyndicationContractFolderStatusCode-2.04.gc — estado del expediente.
ESTADO = {
    "PRE": "Anuncio previo",
    "PUB": "En plazo",
    "EV": "Pendiente de adjudicación",
    "ADJ": "Adjudicada",
    "RES": "Resuelta",
    "ANUL": "Anulada",
}


def nombre(tabla: dict, codigo: str) -> str:
    """Traduce un código; si no está en la lista lo devuelve marcado, no lo inventa."""
    codigo = (codigo or "").strip()
    if not codigo:
        return "(sin código)"
    return tabla.get(codigo, f"(código {codigo} no documentado)")
