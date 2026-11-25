
# 04. Validación del sistema

## 1. Objetivo de la validación

Verificar la funcionalidad, consistencia y confiabilidad
de Parallel Data Cleaner mediante pruebas automatizadas,
comparaciones de archivos y ejecuciones con datasets
de diferentes fuentes y formatos.

La validación busca comprobar que las estrategias
concurrentes y paralelas mantienen las operaciones
de limpieza implementadas en la versión secuencial.

## 2. Estrategia de validación

La validación se organizó en tres niveles:

1. Pruebas automatizadas.
2. Validación de equivalencia entre estrategias.
3. Validación funcional con archivos de distintas fuentes.

Cada nivel permite evaluar diferentes características
del sistema.

Las pruebas automatizadas verifican el comportamiento
esperado de los componentes.

Las pruebas de equivalencia comprueban la consistencia
de los archivos producidos.

La validación funcional demuestra la capacidad de
procesar archivos externos al entorno experimental.

## 3. Pruebas automatizadas

Las pruebas se implementaron mediante unittest,
perteneciente a la biblioteca estándar de Python.

Los archivos correspondientes se encuentran en:

- tests/test_cleaner.py
- tests/test_processing.py
- tests/test_edge_cases.py

### 3.1 Casos evaluados

| Prueba | Objetivo | Resultado |
|---|---|---|
| Limpieza básica | Verificar las operaciones de limpieza | Aprobada |
| Equivalencia de procesamiento | Comparar los resultados de las tres estrategias | Aprobada |
| Directorio vacío | Verificar el comportamiento sin archivos de entrada | Aprobada |
| CSV sin registros | Procesar archivos que contienen únicamente encabezados | Aprobada |
| Procesamiento XLSX | Verificar la limpieza de archivos Excel | Aprobada |
| Archivo corrupto | Comprobar el aislamiento de errores individuales | Aprobada |

### 3.2 Ejecución de pruebas

Desde el directorio principal del proyecto:

```powershell
python -m unittest discover -s tests -v
```

Resultado obtenido:

```text
Ran 6 tests

OK
```

Las seis pruebas automatizadas finalizaron correctamente.

## 4. Validación del motor de limpieza

El motor de limpieza fue evaluado mediante estructuras
de datos que contienen registros duplicados, valores
faltantes y campos de texto con espacios innecesarios.

Los criterios de validación incluyen:

- Normalización de espacios.
- Identificación de valores faltantes.
- Eliminación de registros completamente duplicados.
- Consistencia de las estadísticas.
- Conservación de los datos que no requieren modificaciones.

La validación utiliza resultados esperados conocidos
para comprobar el comportamiento del motor.

## 5. Validación de equivalencia entre estrategias

La implementación secuencial se utiliza como referencia
para comprobar los resultados obtenidos mediante hilos
y procesos.

El objetivo consiste en verificar que las diferencias
en la estrategia de ejecución no alteren el contenido
de los archivos procesados.

Las tres modalidades utilizan el mismo motor de limpieza.

## 6. Comparación mediante SHA-256

Archivo responsable:

benchmarks/validate_results.py

La validación utiliza el algoritmo SHA-256 para generar
una huella digital del contenido de cada archivo CSV.

El procedimiento comprende:

1. Procesar el escenario mediante la versión secuencial.
2. Obtener los archivos de referencia.
3. Ejecutar una configuración concurrente o paralela.
4. Verificar la cantidad y los nombres de los archivos.
5. Comprobar el estado de procesamiento.
6. Calcular el hash SHA-256 de cada archivo.
7. Comparar los hashes correspondientes.
8. Registrar el resultado de la validación.

La coincidencia de hashes proporciona evidencia de
igualdad del contenido binario de los archivos CSV
comparados.

La validación no compara los tiempos de ejecución,
debido a que estos pueden variar entre estrategias.

## 7. Escenarios de validación

Se utilizaron los tres escenarios experimentales
generados de forma reproducible.

| Escenario | Archivos | Filas por archivo | Filas totales |
|---|---:|---:|---:|
| Pequeño | 5 | 1100 | 5500 |
| Mediano | 20 | 5100 | 102000 |
| Grande | 50 | 10100 | 505000 |
| Total | 75 | - | 612500 |

Los escenarios permiten evaluar la consistencia
del sistema bajo diferentes cantidades de archivos
y registros.

## 8. Configuraciones evaluadas

Cada escenario fue procesado mediante las siguientes
configuraciones:

- Secuencial como referencia.
- Hilos con un trabajador.
- Hilos con dos trabajadores.
- Hilos con cuatro trabajadores.
- Procesos con un trabajador.
- Procesos con dos trabajadores.
- Procesos con cuatro trabajadores.

Las seis configuraciones alternativas se compararon
contra la referencia secuencial de cada escenario.

## 9. Resultados de equivalencia

| Configuración | Pequeño | Mediano | Grande |
|---|---|---|---|
| Hilos (1) | Aprobada | Aprobada | Aprobada |
| Hilos (2) | Aprobada | Aprobada | Aprobada |
| Hilos (4) | Aprobada | Aprobada | Aprobada |
| Procesos (1) | Aprobada | Aprobada | Aprobada |
| Procesos (2) | Aprobada | Aprobada | Aprobada |
| Procesos (4) | Aprobada | Aprobada | Aprobada |

Resultado general:

| Indicador | Resultado |
|---|---:|
| Escenarios evaluados | 3 |
| Configuraciones alternativas por escenario | 6 |
| Configuraciones verificadas | 18 |
| Configuraciones aprobadas | 18 |
| Archivos de entrada distintos | 75 |
| Comparaciones de archivos | 450 |
| Tasa de aprobación | 100% |

Las 450 comparaciones corresponden a la evaluación
de los 75 archivos mediante seis configuraciones
alternativas.

No representan 450 archivos de entrada diferentes.

Todas las configuraciones evaluadas produjeron
archivos CSV equivalentes a los obtenidos mediante
la implementación secuencial.

## 10. Validación funcional con archivos externos

Además de las pruebas controladas, se realizó una
demostración funcional utilizando archivos de distintas
fuentes, estructuras y formatos.

Esta prueba se ejecutó mediante la aplicación
principal, sin utilizar el generador experimental.

Los archivos se colocaron en data/raw/.

### 10.1 Archivos utilizados

| Archivo | Formato | Registros originales |
|---|---|---:|
| ai_models_pricing_raw_20260803_231318.csv | CSV | 26 |
| Historical Product Demand.xlsx | XLSX | 1715 |
| productos.csv | CSV | 100000 |
| train.csv | CSV | 891 |
| ventas_sucias.csv | CSV | 630 |
| Total | - | 103262 |

Los archivos presentan diferentes estructuras
y cantidades de registros.

La aplicación no requiere que los archivos compartan
los mismos nombres de columnas.

### 10.2 Resultados de procesamiento

| Estrategia | Archivos procesados | Errores | Tiempo (s) |
|---|---:|---:|---:|
| Secuencial | 5 | 0 | 2.6654 |
| Hilos | 5 | 0 | 1.5313 |
| Procesos | 5 | 0 | 2.4720 |

Las tres estrategias finalizaron correctamente.

Se registraron 15 operaciones exitosas de
procesamiento sobre cinco archivos distintos.

### 10.3 Resultados de limpieza

Según el reporte de procesamiento revisado:

| Indicador | Resultado |
|---|---:|
| Registros originales | 103262 |
| Registros finales | 103173 |
| Duplicados eliminados | 89 |
| Valores nulos originales | 1370 |
| Valores nulos finales | 1346 |

La disminución de valores nulos no corresponde
a una imputación automática.

El sistema elimina registros duplicados, lo que
puede reducir también la cantidad de valores
faltantes presentes en los datos finales.

### 10.4 Evidencias

Los reportes de esta demostración se encuentran
versionados en:

- reports/validacion_real/reporte_secuencial.csv
- reports/validacion_real/reporte_hilos.csv
- reports/validacion_real/reporte_procesos.csv

Los archivos originales no se incluyen en el
repositorio.

## 11. Validación del manejo de errores

El sistema fue evaluado mediante un archivo XLSX
corrupto acompañado de un archivo CSV válido.

La prueba permite comprobar que un error individual
no impide necesariamente el procesamiento de los
demás archivos del lote.

El sistema registra el estado correspondiente
a cada archivo.

Los archivos procesados correctamente reciben
el estado OK.

Los archivos que presentan excepciones reciben
el estado ERROR.

Esta característica permite identificar problemas
sin descartar automáticamente todo el procesamiento.

## 12. Seguridad de la ejecución concurrente

La independencia de las tareas permite reducir
los riesgos asociados con la modificación de
estructuras compartidas.

Cada trabajador procesa un archivo diferente
y utiliza sus propias estructuras de datos.

Los resultados individuales son recuperados
por el proceso principal.

El reporte consolidado se genera después de
finalizar el procesamiento.

Las pruebas realizadas aportan evidencia de
consistencia en las configuraciones evaluadas.

Sin embargo, no constituyen una demostración
formal de ausencia de errores de concurrencia
en todas las condiciones posibles.

## 13. Reproducción de la validación

Activar el entorno virtual e instalar las
dependencias declaradas en requirements.txt.

Ejecutar las pruebas automatizadas:

```powershell
python -m unittest discover -s tests -v
```

Generar los escenarios experimentales:

```powershell
python benchmarks/generate_data.py
```

Ejecutar la validación de equivalencia:

```powershell
python benchmarks/validate_results.py
```

Resultado esperado:

```text
VALIDACION FINAL EXITOSA

Configuraciones verificadas: 18/18
```

Para realizar una validación funcional adicional,
colocar archivos CSV o XLSX compatibles en data/raw/
y ejecutar:

```powershell
python main.py
```

Seleccionar la estrategia de procesamiento deseada.

## 14. Limitaciones de la validación

- La comparación mediante SHA-256 se realizó sobre
  archivos CSV de los escenarios experimentales.

- La compatibilidad con XLSX fue evaluada mediante
  pruebas automatizadas y una demostración funcional.

- No se verificó mediante SHA-256 la equivalencia
  de los archivos de la demostración funcional.

- La demostración funcional incluye una ejecución
  registrada por cada estrategia.

- Los tiempos de esta demostración no sustituyen
  las mediciones experimentales repetidas.

- No se evaluaron todas las codificaciones,
  delimitadores y variantes posibles de CSV.

- No se realizaron pruebas de portabilidad sobre
  sistemas operativos diferentes de Windows.

- Los resultados no garantizan el funcionamiento
  con archivos que excedan la memoria disponible.

## 15. Conclusión

Parallel Data Cleaner superó las seis pruebas
automatizadas y las 18 configuraciones de
equivalencia experimental.

Las 450 comparaciones de archivos CSV aportaron
evidencia de consistencia entre las estrategias
secuencial, concurrente y paralela.

Adicionalmente, la aplicación procesó exitosamente
cinco archivos externos con diferentes estructuras
y formatos, correspondientes a 103262 registros
por modalidad.

Los resultados respaldan la funcionalidad del
sistema y permiten realizar comparaciones de
rendimiento sin identificar diferencias en los
archivos CSV de los escenarios de equivalencia
evaluados.
