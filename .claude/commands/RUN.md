Objetivo:
1. Procesar todos los archivos de Inputs/dev/ a JSON siguiendo CLAUDE.md
2. Guardar cada resultado en /Outputs/sentenciaN.v2.json,conservando el mismo número que el input

Reglas:
1. No sobrescribir archivos ya existentes en /Outputs
2. Procesar en paralelo los archivos faltantes
3. Validar que el JSON cumple el esquema
4. Añadir "uncertainties" si hay dudas o inconsistencias
5. No inventar datos
6. Detectar errores OCR o incoherencias internas

Después:
7. Revisar todos los JSON generados
8. Detectar posibles mejoras de calidad
9. Proponer correcciones sin aplicarlas automáticamente