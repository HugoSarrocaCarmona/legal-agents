# Datos abiertos de la PLACSP

Primer código ejecutable del proyecto. Existe para cerrar el **bloqueo nº 0** de
[`progress/ESTADO.md`](../../progress/ESTADO.md): la premisa sobre la que se apoya toda la línea
activa nunca se había verificado.

## El pipeline

```bash
# 1 · descargar (fuera del repositorio: ~145 MB/mes, ~1,7 GB el año)
./scripts/placsp/descarga.sh 2025 /ruta/fuera/del/repo/raw

# 2 · XML CODICE -> CSV plano, una fila por (expediente, lote, resultado)
python3 scripts/placsp/parse_resultados.py /ruta/raw/*.zip -o /ruta/datos/resultados_2025.csv

# 3 · responder la pregunta
python3 scripts/placsp/analiza_desiertos.py /ruta/datos/resultados_2025.csv --anio 2025
```

Sin dependencias: biblioteca estándar de Python 3.11. `parse_resultados.py` hace *streaming*
con `iterparse`, así que la memoria no depende del tamaño del fichero — los mensuales
descomprimen a ~1,4 GB cada uno.

## Los ficheros

| Fichero | Qué hace |
|---|---|
| `descarga.sh` | Baja los mensuales de sindicación. En serie, sin paralelizar |
| `parse_resultados.py` | XML → CSV. **Transcribe, no interpreta** |
| `codigos.py` | Listas CODICE transcritas de los `.gc` oficiales (17/09/2026) |
| `analiza_desiertos.py` | El análisis. Clasifica y agrega — aquí sí hay juicio |

La separación entre el paso 2 y el paso 3 es deliberada. Si la extracción y el juicio viven en
el mismo fichero, cuando el resultado sorprenda no se puede saber cuál de los dos falló.

## Las tres reglas que sigue el análisis

1. **La respuesta sale de un campo numérico obligatorio, no de texto libre.**
   `ReceivedTenderQuantity` está en el 100 % de los desiertos; `Description` no llega a la
   mitad. Un análisis apoyado en el texto mediría qué órganos rellenan formularios.
2. **El porcentaje sin clasificar se imprime siempre.** Una clasificación que cubre el 19 % del
   corpus y no lo dice es propaganda.
3. **Los códigos se transcriben de la fuente, nunca de memoria.** Misma regla que
   `base_normativa` en [`standards/contratos.md`](../../standards/contratos.md): un código mal
   traducido produce una estadística falsa, y sobre esa estadística se decide el rumbo.

## Trampas del formato, por si alguien retoma esto

- **La sindicación es un histórico de publicaciones, no un censo.** El mismo expediente
  reaparece cada vez que cambia de fase. Hay que quedarse con el último estado de cada
  `(órgano, expediente, lote)` o se cuenta varias veces la misma licitación.
- **`importe_sin_iva` es el presupuesto del expediente entero** y se repite en la fila de cada
  lote. Sumar por filas multiplica el presupuesto por el número de lotes. La primera versión de
  `analiza_desiertos.py` cometía ese error y daba 6.200 M€ para un solo mes.
- **Desierto son tres códigos** (`3`, `6`, `7`), no uno. Los órganos usan indistintamente el
  genérico y los de fase.
- **Desistimiento (`4`) y renuncia (`5`) no son desierto.** Son decisiones del órgano
  (art. 152 LCSP), no falta de ofertas. Mezclarlos es un error de categoría.
- Los `.gc` de CODICE solo responden por **https**; por http devuelven 404.
- El servidor **ignora las peticiones `Range`** y responde `HEAD` con conexión vacía. Para
  comprobar si un fichero existe hay que empezar a descargarlo.
