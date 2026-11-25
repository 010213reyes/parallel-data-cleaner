
# 01. Planteamiento del proyecto

## Nombre del proyecto

Parallel Data Cleaner (PDC).

## Planteamiento del problema

El procesamiento de archivos de datos constituye una actividad
frecuente en áreas como la ingeniería de datos, la inteligencia
artificial y los sistemas de información.

Antes de utilizar los datos para actividades de análisis o
modelado, es necesario realizar operaciones de limpieza que
permitan identificar registros duplicados, valores faltantes
e inconsistencias en campos de texto.

Cuando se trabaja con múltiples archivos, el procesamiento
secuencial puede presentar limitaciones de rendimiento al
ejecutar cada tarea de manera consecutiva.

La programación concurrente y paralela ofrece alternativas
para distribuir estas tareas entre diferentes trabajadores.
Sin embargo, su implementación no garantiza necesariamente
una reducción del tiempo de ejecución, debido a los costos
de coordinación y administración de recursos.

## Propuesta de solución

Desarrollar una aplicación de consola capaz de procesar
múltiples archivos CSV y XLSX mediante tres estrategias:

- Procesamiento secuencial.
- Procesamiento concurrente mediante hilos.
- Procesamiento paralelo mediante procesos.

Las tres estrategias utilizan el mismo motor de limpieza,
permitiendo evaluar su rendimiento sin modificar las
operaciones aplicadas a los datos.

## Objetivo general

Diseñar, implementar y evaluar un sistema de limpieza de
archivos que permita comparar el rendimiento y la consistencia
de diferentes estrategias de programación secuencial,
concurrente y paralela.

## Objetivos específicos

- Automatizar la limpieza de archivos CSV y XLSX.
- Implementar una referencia de procesamiento secuencial.
- Distribuir tareas independientes mediante hilos y procesos.
- Verificar la consistencia de los resultados.
- Evaluar tiempos de ejecución, speedup y eficiencia relativa.
- Identificar las ventajas y limitaciones de cada estrategia.
- Garantizar la reproducibilidad de los experimentos.

## Justificación

La limpieza de datos representa una etapa fundamental dentro
de los procesos ETL, la ingeniería de datos y el desarrollo
de soluciones de inteligencia artificial.

Parallel Data Cleaner permite estudiar cómo diferentes
modelos de ejecución pueden contribuir a optimizar esta
actividad, considerando tanto sus beneficios como sus costos.

El proyecto aborda un problema práctico mediante una
implementación funcional y una metodología experimental
reproducible.

## Entradas del sistema

- Archivos CSV.
- Archivos XLSX.
- Selección del modo de procesamiento.

Los archivos pueden proceder de fuentes reales o generadas
artificialmente y no requieren una estructura de columnas
común.

## Salidas del sistema

- Archivos procesados y limpios.
- Estadísticas de limpieza.
- Cantidad de registros originales y finales.
- Cantidad de duplicados eliminados.
- Cantidad de valores nulos.
- Tiempo de procesamiento.
- Estado de ejecución por archivo.

## Criterios de éxito

- Procesar correctamente archivos CSV y XLSX compatibles.
- Conservar los archivos originales.
- Eliminar registros completamente duplicados.
- Normalizar espacios en campos de texto.
- Identificar y contabilizar valores faltantes.
- Manejar errores individuales sin detener todo el lote.
- Obtener resultados equivalentes entre estrategias.
- Registrar métricas de rendimiento reproducibles.

## Alcance

El sistema realiza operaciones generales de limpieza sobre
archivos tabulares independientes.

No implementa imputación automática, entrenamiento de
modelos de inteligencia artificial, procesamiento distribuido
ni reglas de limpieza específicas de un dominio.

## Viabilidad técnica

El proyecto utiliza Python y bibliotecas de código abierto.

Su implementación y validación se realizaron en una
computadora personal con dos núcleos físicos, cuatro
procesadores lógicos y 7.65 GB de memoria RAM reconocida
por el sistema.

No requiere servidores externos, servicios en la nube
ni infraestructura especializada.

## Evidencia de aplicación práctica

El sistema procesó exitosamente un lote de cinco archivos
de distintas fuentes y formatos, compuesto por 103,262
registros.

Se eliminaron 89 registros duplicados según el reporte
de procesamiento revisado.

Las tres modalidades finalizaron sin errores.

Adicionalmente, se realizaron 105 mediciones experimentales
controladas y 18 validaciones de equivalencia sobre
archivos CSV generados de manera reproducible.
