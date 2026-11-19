# Parallel Data Cleaner 

Sistema de limpieza de archivos CSV y XLSX mediante técnicas de programación secuencial, concurrente y paralela en Python.

## Objetivo

Desarrollar y evaluar una aplicación capaz de procesar múltiples datasets, comparando el rendimiento de una implementación secuencial y dos alternativas basadas en hilos y procesos.

## Tecnologías

- Python 3.12
- pandas
- openpyxl
- concurrent.futures (fases posteriores)

## Funcionalidades de limpieza

- Eliminación de registros completamente duplicados.
- Normalización de espacios en columnas de texto.
- Identificación y contabilización de valores nulos.
- Exportación de archivos procesados.
- Generación de reportes de ejecución.

## Estado del proyecto

**Fase 1 — Limpieza secuencial**

Implementación inicial del motor de limpieza y procesamiento de archivos.

## Instalación

Crear y activar un entorno virtual de Python.

Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Ejecución

Colocar los archivos CSV o XLSX en `data/raw/`.

Ejecutar:

```powershell
python main.py
```

Los archivos procesados se almacenarán en `data/cleaned/` y el reporte en `reports/`.

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

## Fases del proyecto

1. Preparación y limpieza secuencial.
2. Programación concurrente y paralela.
3. Pruebas de equivalencia y benchmarks.
4. Documentación y entrega final.

## Limitaciones iniciales

La versión actual utiliza la configuración predeterminada de lectura de pandas. En archivos XLSX procesa la primera hoja y no conserva el formato visual original.

Los valores nulos se reportan, pero no se modifican automáticamente.

## Repositorio

https://github.com/010213reyes/parallel-data-cleaner