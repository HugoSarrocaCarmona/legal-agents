#!/usr/bin/env bash
# Descarga los ficheros mensuales de sindicación de la PLACSP.
#
#   ./descarga.sh 2025 datos/raw          # el año entero
#   ./descarga.sh 2025 datos/raw 01 02    # solo enero y febrero
#
# Cada mes son ~145 MB comprimidos y ~1,4 GB de XML descomprimido, y tarda unos
# dos minutos. El año completo ocupa ~1,7 GB en disco: no va al repositorio.
#
# Se descarga en serie y sin paralelizar a propósito. Es un servidor público, la
# licencia de reutilización no ampara martillearlo, y el cuello de botella del
# proyecto no es la velocidad de descarga.
set -euo pipefail

ANIO="${1:?uso: descarga.sh AAAA DESTINO [MM...]}"
DESTINO="${2:?uso: descarga.sh AAAA DESTINO [MM...]}"
shift 2
MESES=("$@")
if [ ${#MESES[@]} -eq 0 ]; then
    MESES=(01 02 03 04 05 06 07 08 09 10 11 12)
fi

BASE="https://contrataciondelsectorpublico.gob.es/sindicacion/sindicacion_643"
mkdir -p "$DESTINO"

for MES in "${MESES[@]}"; do
    FICHERO="$DESTINO/placsp_${ANIO}${MES}.zip"
    if [ -s "$FICHERO" ]; then
        echo "  $ANIO-$MES ya está descargado, se omite"
        continue
    fi
    echo -n "  $ANIO-$MES ... "
    if curl -fsS --max-time 1800 --retry 3 --retry-delay 5 \
            -o "$FICHERO" \
            "$BASE/licitacionesPerfilesContratanteCompleto3_${ANIO}${MES}.zip"; then
        echo "$(stat -c%s "$FICHERO" | numfmt --to=iec) ok"
    else
        # Un mes que aún no ha cerrado no existe como fichero mensual. No es un
        # error del script y no debe dejar un .zip vacío detrás.
        rm -f "$FICHERO"
        echo "no disponible"
    fi
done
