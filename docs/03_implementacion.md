
# 03. Implementación del sistema

## 1. Introducción

La implementación de Parallel Data Cleaner se realizó
mediante Python, utilizando una estructura modular que
permite separar las operaciones de limpieza de las
estrategias de procesamiento.

El desarrollo se organizó mediante fases independientes,
utilizando Git como herramienta de control de versiones.

La versión funcional del sistema se encuentra identificada
mediante la etiqueta v1.0.0.

## 2. Tecnologías de implementación

| Tecnología | Aplicación |
|---|---|
| Python | Lenguaje de programación |
| pandas | Lectura, transformación y escritura de datos |
| openpyxl | Procesamiento de archivos XLSX |
| pathlib | Administración de rutas y archivos |
| concurrent.futures | Administración de trabajadores |
| time | Medición de tiempos de ejecución |
| hashlib | Comparación de archivos mediante SHA-256 |
| unittest | Pruebas automatizadas |
| matplotlib | Visualización de resultados |
| Git | Control de versiones |
| GitHub | Almacenamiento del repositorio |

## 3. Organización del código fuente

El código principal se encuentra distribuido en los
siguientes módulos:

- main.py
- src/cleaner.py
- src/sequential.py
- src/threaded.py
- src/parallel.py

Los componentes experimentales y las pruebas automatizadas
se mantienen separados de la aplicación principal.

## 4. Motor de limpieza

Archivo: src/cleaner.py

El motor de limpieza constituye el componente central
del sistema.

La función clean_dataframe recibe un DataFrame y devuelve
los datos procesados junto con las estadísticas de limpieza.

Las operaciones implementadas incluyen:

1. Copia de la estructura de datos original.
2. Contabilización de registros originales.
3. Contabilización de valores nulos originales.
4. Normalización de espacios en campos de texto.
5. Normalización de representaciones de valores faltantes.
6. Eliminación de registros completamente duplicados.
7. Restablecimiento del índice.
8. Cálculo de estadísticas finales.

### 4.1 Normalización de texto

Los campos de texto se procesan para eliminar espacios
innecesarios al inicio y al final, así como para reducir
secuencias de espacios internos.

La operación conceptual utilizada es:

```python
" ".join(value.split())
```

Por ejemplo:

| Valor original | Valor normalizado |
|---|---|
| "  Guadalajara  " | "Guadalajara" |
| "Luis   Alberto" | "Luis Alberto" |
| "  Producto A  " | "Producto A" |

Esta operación facilita la identificación de registros
duplicados que presentan diferencias únicamente en
sus espacios.

### 4.2 Tratamiento de valores faltantes

El sistema reconoce diferentes representaciones
textuales de valores faltantes, entre ellas:

- Cadenas vacías.
- N/A.
- n/a.
- NULL.
- null.
- None.

Estas representaciones se normalizan mediante los
mecanismos de valores faltantes de pandas.

El sistema contabiliza los valores nulos, pero no
realiza imputación automática.

Esta decisión evita introducir valores artificiales
sin conocer el significado de las variables.

### 4.3 Eliminación de duplicados

La eliminación de registros duplicados se realiza
considerando todas las columnas del DataFrame.

No se utilizan identificadores específicos ni reglas
dependientes del dominio de los datos.

La operación permite eliminar registros completamente
duplicados después de aplicar la normalización.

No se implementan técnicas de detección de duplicados
aproximados o semánticos.

### 4.4 Estadísticas de limpieza

El motor genera las siguientes estadísticas:

| Campo | Descripción |
|---|---|
| original_rows | Cantidad de registros originales |
| cleaned_rows | Cantidad de registros finales |
| duplicates_removed | Registros duplicados eliminados |
| original_nulls | Valores nulos antes de la limpieza |
| final_nulls | Valores nulos después de la limpieza |

Estas estadísticas permiten evaluar las transformaciones
realizadas sobre cada archivo.

## 5. Procesamiento individual de archivos

Archivo: src/sequential.py

La función process_file centraliza el procesamiento
individual de archivos.

Esta función es reutilizada por las tres estrategias
de ejecución.

El procedimiento general comprende:

1. Identificar la extensión del archivo.
2. Leer los datos mediante pandas.
3. Ejecutar el motor de limpieza.
4. Guardar el archivo procesado.
5. Registrar el tiempo de ejecución.
6. Devolver las estadísticas correspondientes.

### 5.1 Procesamiento de CSV

Los archivos CSV se leen mediante pandas y se exportan
nuevamente en formato CSV después de la limpieza.

La implementación utiliza la configuración predeterminada
de lectura de pandas.

Los archivos con delimitadores o codificaciones especiales
pueden requerir configuraciones adicionales.

### 5.2 Procesamiento de XLSX

Los archivos XLSX se procesan utilizando pandas y openpyxl.

La implementación trabaja con la primera hoja del archivo.

Los datos procesados se exportan nuevamente en formato XLSX.

No se garantiza la conservación de estilos, formatos
visuales, fórmulas ni otras características del libro
original.

### 5.3 Conservación de los archivos originales

Los archivos de entrada se almacenan en data/raw/.

Los resultados se escriben en data/cleaned/.

Esta separación evita modificar directamente los archivos
originales durante el procesamiento.

## 6. Implementación secuencial

Archivo: src/sequential.py

La función run_sequential identifica los archivos
compatibles y los procesa individualmente.

Cada tarea debe finalizar antes de iniciar la siguiente.

Pseudocódigo:

```text
Identificar archivos compatibles

Para cada archivo:
    Intentar:
        Procesar archivo
        Registrar resultado
    Si ocurre un error:
        Registrar error

Devolver resultados
```

Esta implementación constituye la referencia utilizada
para evaluar las estrategias concurrentes y paralelas.

## 7. Implementación concurrente mediante hilos

Archivo: src/threaded.py

La función run_threaded utiliza ThreadPoolExecutor
para administrar múltiples trabajadores dentro del
mismo proceso.

Cada archivo se envía como una tarea independiente.

Los resultados se recuperan mediante objetos Future
y la función as_completed.

Pseudocódigo:

```text
Identificar archivos compatibles

Crear ThreadPoolExecutor

Para cada archivo:
    Enviar tarea al ejecutor

Para cada tarea completada:
    Intentar:
        Recuperar resultado
    Si ocurre un error:
        Registrar error

Ordenar resultados por nombre de archivo

Devolver resultados
```

La implementación utiliza cuatro trabajadores de manera
predeterminada.

Durante la evaluación experimental se utilizaron
configuraciones de uno, dos y cuatro trabajadores.

## 8. Implementación paralela mediante procesos

Archivo: src/parallel.py

La función run_parallel utiliza ProcessPoolExecutor
para distribuir las tareas entre procesos independientes.

Cada proceso ejecuta el mismo motor de procesamiento
individual de archivos.

Pseudocódigo:

```text
Identificar archivos compatibles

Crear ProcessPoolExecutor

Para cada archivo:
    Enviar tarea al ejecutor

Para cada tarea completada:
    Intentar:
        Recuperar resultado
    Si ocurre un error:
        Registrar error

Ordenar resultados por nombre de archivo

Devolver resultados
```

A diferencia de los hilos, los procesos utilizan espacios
de memoria independientes.

Esta característica permite aprovechar múltiples núcleos,
aunque introduce costos adicionales de inicialización,
comunicación y administración de memoria.

## 9. Reutilización del código

Las tres estrategias utilizan la misma función de
procesamiento individual y el mismo motor de limpieza.

Esta decisión evita implementar tres algoritmos de
limpieza diferentes.

Las diferencias entre modalidades se concentran en la
forma de distribuir, ejecutar y recuperar las tareas.

Esto permite realizar comparaciones de rendimiento
más consistentes.

## 10. Interfaz de consola

Archivo: main.py

La aplicación proporciona una interfaz de consola
que permite seleccionar el modo de procesamiento.

```text
=============================================
       PARALLEL DATA CLEANER
=============================================

Selecciona el modo de procesamiento:

1. Secuencial
2. Hilos
3. Procesos
```

La función principal administra:

- Creación de directorios necesarios.
- Selección del modo de procesamiento.
- Validación de la opción seleccionada.
- Invocación de la estrategia correspondiente.
- Medición del tiempo total.
- Generación del reporte.
- Presentación del resumen de ejecución.

Si no se encuentran archivos compatibles, la aplicación
informa al usuario y finaliza la ejecución.

## 11. Generación de reportes

El proceso principal recupera las estadísticas de
todos los archivos procesados.

Los resultados se convierten en un DataFrame y se
exportan mediante un archivo CSV.

Los reportes disponibles son:

- reports/reporte_secuencial.csv
- reports/reporte_hilos.csv
- reports/reporte_procesos.csv

Cada registro procesado correctamente incluye:

| Campo | Descripción |
|---|---|
| file | Nombre del archivo |
| original_rows | Registros originales |
| cleaned_rows | Registros finales |
| duplicates_removed | Duplicados eliminados |
| original_nulls | Valores nulos originales |
| final_nulls | Valores nulos finales |
| time_seconds | Tiempo individual de procesamiento |
| status | Estado de ejecución |

Cuando ocurre un error, se registra el estado ERROR
y la información correspondiente a la excepción.

La generación centralizada del reporte evita que
múltiples trabajadores escriban simultáneamente
sobre el mismo archivo de estadísticas.

## 12. Manejo de errores

El sistema incorpora mecanismos de manejo de excepciones
durante el procesamiento individual de archivos.

Si un archivo presenta problemas de lectura, formato
o escritura, se registra el error correspondiente.

Los demás archivos pueden continuar su procesamiento.

Esta característica fue evaluada mediante pruebas
automatizadas que incluyen un archivo XLSX corrupto
junto con un archivo CSV válido.

El manejo individual de excepciones no implica que
el sistema pueda recuperarse de todas las posibles
fallas del sistema operativo o del hardware.

## 13. Medición de tiempos

La aplicación utiliza time.perf_counter para medir
el tiempo de ejecución.

El tiempo total incluye la invocación de la estrategia
de procesamiento y la recuperación de sus resultados.

En las modalidades concurrente y paralela, también
se consideran los costos asociados con la gestión
de los trabajadores.

La escritura del reporte consolidado se realiza
después de finalizar la medición del tiempo total
en main.py.

Los tiempos individuales de los archivos no deben
sumarse para calcular el tiempo total concurrente,
debido a que las tareas pueden superponerse.

## 14. Implementación de los benchmarks

Archivo: benchmarks/generate_data.py

Este componente genera escenarios experimentales
mediante semillas reproducibles.

Archivo: benchmarks/run_benchmarks.py

Este componente ejecuta las diferentes configuraciones
de procesamiento y registra sus tiempos.

Archivo: benchmarks/validate_results.py

Este componente compara los archivos CSV producidos
por las estrategias concurrentes y paralelas con
los resultados de la implementación secuencial.

Archivo: benchmarks/plot_results.py

Este componente genera las gráficas de tiempos,
speedup y eficiencia relativa.

Los benchmarks son herramientas independientes de
la aplicación principal.

No es necesario generar datos experimentales para
procesar archivos CSV y XLSX proporcionados por
el usuario.

## 15. Aplicación sobre archivos de distintas fuentes

La aplicación fue ejecutada utilizando un lote compuesto
por cuatro archivos CSV y un archivo XLSX.

Los archivos presentaban diferentes estructuras,
cantidades de registros y características.

| Archivo | Registros originales | Registros finales |
|---|---:|---:|
| Historical Product Demand.xlsx | 1715 | 1656 |
| ai_models_pricing_raw_20260803_231318.csv | 26 | 26 |
| productos.csv | 100000 | 100000 |
| train.csv | 891 | 891 |
| ventas_sucias.csv | 630 | 600 |
| Total | 103262 | 103173 |

Las tres modalidades procesaron los cinco archivos
sin errores.

Los reportes correspondientes se encuentran versionados
en reports/validacion_real/.

Esta demostración confirma la capacidad del sistema
para procesar archivos con estructuras diferentes
sin modificar el código fuente.

## 16. Portabilidad y dependencias

Las dependencias externas se encuentran declaradas
en requirements.txt.

El sistema utiliza un entorno virtual de Python
para mantener aisladas sus dependencias.

La implementación fue desarrollada y validada
en Windows utilizando Python 3.12.

La protección del punto de entrada mediante
if __name__ == "__main__" permite utilizar
ProcessPoolExecutor bajo el modelo de creación
de procesos de Windows.

No se realizaron pruebas de portabilidad sobre
otros sistemas operativos.

## 17. Control de versiones

El desarrollo se organizó mediante las siguientes
ramas:

| Rama | Implementación |
|---|---|
| feature/limpieza-secuencial | Motor de limpieza |
| feature/concurrencia-paralelismo | Hilos y procesos |
| feature/benchmarks | Evaluación experimental |
| feature/validacion-final | Validación y gráficas |
| docs/entrega-final | Documentación |

La etiqueta v1.0.0 identifica la versión funcional
de la aplicación antes de la fase de documentación.

## 18. Limitaciones de implementación

- Cada archivo se carga completamente en memoria.
- Los archivos XLSX se procesan considerando la primera hoja.
- No se realiza imputación automática de valores faltantes.
- No se implementan reglas de limpieza específicas de un dominio.
- No se garantiza la compatibilidad con todos los formatos de CSV.
- No se realiza procesamiento distribuido.
- Las ejecuciones posteriores pueden sobrescribir resultados anteriores.
- El rendimiento depende de los recursos disponibles.

## 19. Conclusión

La implementación de Parallel Data Cleaner permite
procesar archivos tabulares mediante tres estrategias
de ejecución diferentes.

La reutilización del motor de limpieza facilita la
comparación experimental y el mantenimiento del código.

La separación de responsabilidades, el manejo individual
de errores y la generación centralizada de reportes
constituyen las principales decisiones técnicas
del desarrollo.
