#!/usr/bin/env python3
"""
Responde una sola pregunta con los datos abiertos de la PLACSP:
**¿por qué quedan desiertas las licitaciones públicas españolas?**

Por qué existe este fichero
---------------------------
`research/02-oportunidad-mercado-espanol.md` dio por «causa identificada» que las
licitaciones quedan desiertas porque las pymes no pueden con la complejidad del
pliego. Eso era una inferencia de fuente secundaria escrita como si fuera un dato,
y toda la línea activa del proyecto se apoya en ella. Es el bloqueo nº 0 de
`progress/ESTADO.md`. Esto lo cierra o lo tumba.

La variable que decide
----------------------
`ofertas_recibidas` parte los desiertos en dos poblaciones que no tienen nada que
ver entre sí:

  = 0   nadie se presentó. La causa está **antes** del pliego: precio inviable,
        plazo imposible, mercado inexistente o desinterés. Un analizador de riesgo
        de pliegos no resuelve esto.
  > 0   se presentaron y aun así quedó desierto: ofertas excluidas, solvencia no
        acreditada, defectos de documentación, baja anormal no justificada. Aquí
        sí hay un problema de ejecución del pliego.

La tesis del producto sobrevive en la medida en que la segunda población sea
grande. Si es residual, la tesis cae. El script no decide eso: lo cuenta.

Disciplina de clasificación
---------------------------
`resultado_motivo` es texto libre redactado por cada órgano. Clasificarlo con
reglas es inevitable y es donde se cuela el sesgo, así que:

  1. El informe imprime **primero** los motivos literales más frecuentes, antes de
     clasificar nada. Las reglas se inducen de ahí, no al revés.
  2. Toda regla aplicada se imprime con su recuento.
  3. El porcentaje **sin clasificar** se reporta siempre y en grande. Una
     clasificación que cubre el 40 % del corpus y no lo dice es propaganda.

Uso
---
    python3 analiza_desiertos.py datos/resultados.csv --anio 2025
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from codigos import (  # noqa: E402
    ADJUDICADO,
    DESIERTO,
    PROCEDIMIENTO,
    RESULTADO,
    RETIRADO_POR_EL_ORGANO,
    TIPO_CONTRATO,
    nombre,
)

csv.field_size_limit(10_000_000)


# --- Reglas de clasificación del motivo -------------------------------------
# Inducidas de los motivos literales más frecuentes (§3 del informe). Cada regla
# lleva delante el porqué; el orden importa: se aplica la primera que casa.
REGLAS = [
    (
        "sin ofertas",
        r"no se (ha|han) presentado|ninguna oferta|no se (ha|han) recibido|sin ofertas|"
        r"ausencia de (licitadores|ofertas)|no concurr|falta de licitadores|"
        r"no hubo licitadores|cero ofertas|no ha concurrido",
    ),
    (
        "ofertas excluidas o retiradas",
        r"exclu|excluid|retir|desistid|no admit|inadmis|rechaz|"
        r"todas las ofertas.*(no|excluid)|unica oferta.*(exclu|rechaz)",
    ),
    (
        "solvencia o requisitos no acreditados",
        r"solvencia|no acredit|requisit|capacidad|habilitac|clasificacion empresarial|"
        r"no reune|no cumple los requisitos",
    ),
    (
        "defecto de documentacion o plazo",
        r"documentac|no subsan|fuera de plazo|no present.*documentac|"
        r"sobre .?(a|b|c).?|firma electronica|error en la presentacion",
    ),
    (
        "oferta por encima del presupuesto",
        r"supera(n)? el presupuesto|importe superior|precio superior|"
        r"excede.*(presupuesto|licitacion)|por encima del presupuesto",
    ),
    (
        "baja anormal no justificada",
        r"anormal|desproporcionad|temerari|baja no justificada",
    ),
    (
        "incumplimiento tecnico del pliego",
        r"prescripciones tecnicas|incumpl.*(pliego|ppt|pcap)|no se ajusta al pliego|"
        r"no cumple.*tecnic|oferta tecnica",
    ),
]


def normaliza(texto: str) -> str:
    """Minúsculas, sin acentos y sin espacios repetidos, para poder comparar."""
    texto = unicodedata.normalize("NFKD", texto or "")
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(texto.lower().split())


def clasifica(motivo: str) -> str:
    m = normaliza(motivo)
    if not m:
        return "(motivo no publicado)"
    for etiqueta, patron in REGLAS:
        if re.search(patron, m):
            return etiqueta
    return "(sin clasificar)"


def a_float(valor: str) -> float | None:
    try:
        return float((valor or "").replace(",", "."))
    except ValueError:
        return None


def a_int(valor: str) -> int | None:
    try:
        return int(float((valor or "").replace(",", ".")))
    except ValueError:
        return None


def carga_y_deduplica(ruta: Path) -> list[dict]:
    """Se queda con el último estado publicado de cada (órgano, expediente, lote).

    La sindicación es un histórico de publicaciones, no un censo: el mismo
    expediente reaparece cada vez que avanza de fase. Contar las filas tal cual
    contaría varias veces la misma licitación e inflaría cualquier porcentaje.
    """
    ultimo: dict[tuple, str] = {}
    filas_por_clave: dict[tuple, list[dict]] = defaultdict(list)

    with ruta.open(encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            clave = (
                fila["organo_id_plataforma"] or fila["organo_nif"] or fila["organo"],
                fila["expediente"],
                fila["lote"],
            )
            marca = fila["actualizado"]
            if clave not in ultimo or marca > ultimo[clave]:
                ultimo[clave] = marca
                filas_por_clave[clave] = [fila]
            elif marca == ultimo[clave]:
                filas_por_clave[clave].append(fila)

    return [fila for filas in filas_por_clave.values() for fila in filas]


def tramo_importe(valor: float | None) -> str:
    if valor is None:
        return "sin importe publicado"
    for tope, etiqueta in [
        (15_000, "hasta 15.000 EUR"),
        (40_000, "15.000 - 40.000"),
        (100_000, "40.000 - 100.000"),
        (500_000, "100.000 - 500.000"),
        (2_000_000, "500.000 - 2 M"),
    ]:
        if valor < tope:
            return etiqueta
    return "mas de 2 M"


def tabla(titulo: str, contador: Counter, total: int | None = None, top: int | None = None) -> None:
    total = total or sum(contador.values())
    print(f"\n### {titulo}")
    if total == 0:
        print("  (sin datos)")
        return
    filas = contador.most_common(top)
    ancho = max((len(str(k)) for k, _ in filas), default=10)
    for clave, n in filas:
        print(f"  {str(clave):<{ancho}}  {n:>8,}  {n / total:6.1%}")
    print(f"  {'TOTAL':<{ancho}}  {total:>8,}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("csv", type=Path)
    ap.add_argument("--anio", default=None, help="filtra por año de fecha_resultado")
    ap.add_argument("--motivos-top", type=int, default=40)
    args = ap.parse_args()

    filas = carga_y_deduplica(args.csv)
    print(f"# Resultados de licitación en la PLACSP")
    print(f"\nFuente: `{args.csv.name}`. Filas tras deduplicar por (órgano, expediente, lote): {len(filas):,}")

    con_resultado = [f for f in filas if f["resultado_codigo"]]
    if args.anio:
        con_resultado = [f for f in con_resultado if f["fecha_resultado"].startswith(args.anio)]
        print(f"Filtrado a resultados con fecha en {args.anio}: {len(con_resultado):,}")

    # --- 1. Qué pasa con las licitaciones ---------------------------------
    por_resultado = Counter(nombre(RESULTADO, f["resultado_codigo"]) for f in con_resultado)
    tabla("1 · Resultado de cada (expediente, lote)", por_resultado)

    desiertos = [f for f in con_resultado if f["resultado_codigo"] in DESIERTO]
    retirados = [f for f in con_resultado if f["resultado_codigo"] in RETIRADO_POR_EL_ORGANO]
    adjudicados = [f for f in con_resultado if f["resultado_codigo"] in ADJUDICADO]

    total_resueltos = len(desiertos) + len(retirados) + len(adjudicados)
    print(f"\n  Desiertos: {len(desiertos):,}"
          f"   Desistimiento/renuncia: {len(retirados):,}"
          f"   Adjudicados: {len(adjudicados):,}")
    if total_resueltos:
        print(f"  Tasa de desierto sobre resueltos: {len(desiertos) / total_resueltos:.2%}")

    if not desiertos:
        print("\nNo hay desiertos en el conjunto filtrado. Nada que analizar.")
        return 0

    # --- 2. LA PREGUNTA: ¿se presentó alguien? ----------------------------
    print("\n### 2 · La partición que decide la tesis del proyecto")
    sin_ofertas = nadie = con_ofertas = desconocido = 0
    for f in desiertos:
        n = a_int(f["ofertas_recibidas"])
        if n is None:
            desconocido += 1
        elif n == 0:
            nadie += 1
        else:
            con_ofertas += 1
    sin_ofertas = nadie
    conocidos = nadie + con_ofertas
    print(f"  Nadie se presentó (ofertas = 0)      {sin_ofertas:>8,}"
          f"  {sin_ofertas / conocidos:6.1%} de los conocidos" if conocidos else "")
    print(f"  Hubo ofertas y aun así desierto      {con_ofertas:>8,}"
          f"  {con_ofertas / conocidos:6.1%} de los conocidos" if conocidos else "")
    print(f"  Sin dato de ofertas recibidas        {desconocido:>8,}"
          f"  {desconocido / len(desiertos):6.1%} del total de desiertos")
    print("\n  Lectura: la línea activa del proyecto (analizar el riesgo de un pliego)")
    print("  solo puede actuar sobre la segunda población. La primera tiene su causa")
    print("  antes del pliego y ninguna herramienta de lectura la resuelve.")

    # --- 2b. Cuántos concurrieron cuando hubo concurrencia ----------------
    # Un desierto con **una sola** oferta excluida no es un fracaso de mercado: es
    # una empresa que quiso el contrato y no superó el filtro. Es la única
    # población sobre la que una herramienta de lectura de pliegos puede actuar,
    # y por eso se cuenta aparte en lugar de diluirla en «hubo ofertas».
    con_oferta = [f for f in desiertos if (a_int(f["ofertas_recibidas"]) or 0) > 0]
    n_ofertas = Counter(a_int(f["ofertas_recibidas"]) for f in con_oferta)
    una_sola = n_ofertas.get(1, 0)
    print("\n### 2b · Cuántas ofertas había cuando aun así quedó desierto")
    for n in sorted(k for k in n_ofertas if k is not None)[:8]:
        print(f"  {n:>3} oferta(s)  {n_ofertas[n]:>7,}  {n_ofertas[n] / len(con_oferta):6.1%}")
    if con_oferta:
        print(f"\n  Un solo licitador, excluido: {una_sola:,}"
              f" ({una_sola / len(con_oferta):.1%} de los desiertos con ofertas,"
              f" {una_sola / len(desiertos):.1%} de todos los desiertos)")
        pymes_solas = sum(
            1 for f in con_oferta
            if f["ofertas_pymes"] and f["ofertas_pymes"] == f["ofertas_recibidas"]
        )
        print(f"  Casos en que todas las ofertas eran de pymes: {pymes_solas:,}"
              f" ({pymes_solas / len(con_oferta):.1%})")

    # --- 3. Motivos literales, ANTES de clasificar ------------------------
    # Solo sobre la población con ofertas: en la de cero ofertas el motivo es
    # tautológico («no se presentó nadie») y no informa de nada.
    con_texto = [f for f in con_oferta if f["resultado_motivo"].strip()]
    print(f"\n  Motivo publicado en {len(con_texto):,} de {len(con_oferta):,}"
          f" desiertos con ofertas"
          f" ({len(con_texto) / len(con_oferta):.1%})" if con_oferta else "")
    literales = Counter(normaliza(f["resultado_motivo"])[:110] for f in con_texto)
    tabla(f"3 · Motivos literales de los desiertos CON ofertas (top {args.motivos_top})",
          literales, total=len(con_texto), top=args.motivos_top)

    # --- 4. Clasificación, con el residuo a la vista ----------------------
    clases = Counter(clasifica(f["resultado_motivo"]) for f in desiertos)
    tabla("4 · Motivo clasificado por reglas (todos los desiertos)", clases,
          total=len(desiertos))
    sin_clasificar = clases["(sin clasificar)"] + clases["(motivo no publicado)"]
    print(f"\n  ⚠️  No clasificado: {sin_clasificar:,} de {len(desiertos):,}"
          f" ({sin_clasificar / len(desiertos):.1%}).")
    print("  Cualquier conclusión de §4 vale lo que valga ese porcentaje, y por eso")
    print("  el análisis se apoya en §2, que sale de un campo numérico obligatorio,")
    print("  y no en §4, que sale de texto libre que más de la mitad de los órganos")
    print("  no rellenan.")

    # --- 5. Dónde se concentran -------------------------------------------
    tabla("5 · Desiertos por tipo de contrato",
          Counter(nombre(TIPO_CONTRATO, f["tipo_contrato"]) for f in desiertos))
    tabla("6 · Desiertos por procedimiento",
          Counter(nombre(PROCEDIMIENTO, f["procedimiento"]) for f in desiertos))
    tabla("7 · Desiertos por tramo de importe (sin IVA)",
          Counter(tramo_importe(a_float(f["importe_sin_iva"])) for f in desiertos))

    # Tasa de desierto por tipo: más informativa que el recuento, porque corrige
    # por cuántas licitaciones hay de cada tipo.
    print("\n### 8 · Tasa de desierto por tipo de contrato")
    por_tipo_total: Counter = Counter()
    por_tipo_des: Counter = Counter()
    for f in con_resultado:
        t = nombre(TIPO_CONTRATO, f["tipo_contrato"])
        if f["resultado_codigo"] in DESIERTO or f["resultado_codigo"] in ADJUDICADO:
            por_tipo_total[t] += 1
        if f["resultado_codigo"] in DESIERTO:
            por_tipo_des[t] += 1
    ancho = max((len(t) for t in por_tipo_total), default=10)
    for t, n in por_tipo_total.most_common():
        if n < 50:
            continue  # por debajo de 50 la tasa es ruido; no se imprime
        print(f"  {t:<{ancho}}  {por_tipo_des[t]:>7,} / {n:>8,}  {por_tipo_des[t] / n:6.2%}")

    # --- 6. Dinero ---------------------------------------------------------
    # Cuidado: `importe_sin_iva` es el presupuesto **del expediente entero**, y se
    # repite idéntico en la fila de cada lote. Sumar por filas multiplica el
    # presupuesto de cada expediente por su número de lotes. La primera versión de
    # este script lo hacía y daba una cifra inflada varias veces. Se suma por
    # expediente único, y los expedientes con lotes se cuentan aparte porque su
    # importe no es atribuible al lote que quedó desierto.
    print("\n### 9 · Dinero licitado que quedó desierto")
    por_expediente: dict[tuple, float] = {}
    con_lotes: set[tuple] = set()
    for f in desiertos:
        clave = (f["organo_id_plataforma"] or f["organo"], f["expediente"])
        importe = a_float(f["importe_sin_iva"])
        if importe is None:
            continue
        por_expediente[clave] = importe
        if f["lote"]:
            con_lotes.add(clave)

    enteros = {k: v for k, v in por_expediente.items() if k not in con_lotes}
    if enteros:
        valores = sorted(enteros.values())
        print(f"  Expedientes SIN lotes, desiertos por completo: {len(enteros):,}")
        print(f"    suma     {sum(valores):>18,.0f} EUR")
        print(f"    mediana  {valores[len(valores) // 2]:>18,.0f} EUR")
    if con_lotes:
        suma_lotes = sum(por_expediente[k] for k in con_lotes)
        print(f"  Expedientes CON lotes y algún lote desierto: {len(con_lotes):,}")
        print(f"    presupuesto total de esos expedientes {suma_lotes:>15,.0f} EUR")
        print("    (cota superior: solo una parte de cada expediente quedó desierta;")
        print("     la sindicación no publica el presupuesto por lote)")
    print("\n  Ninguna de estas cifras es dinero perdido: el presupuesto base de una")
    print("  licitación desierta se relicita en su mayor parte. Presentarlo como")
    print("  pérdida —que es lo que hace la prensa sectorial— sería falso.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
