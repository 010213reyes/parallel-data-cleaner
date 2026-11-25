
# 06. Conclusiones y cierre del proyecto

## 1. Conclusión general

Parallel Data Cleaner permitió diseñar, implementar
y evaluar un sistema de limpieza de archivos mediante
tres estrategias de procesamiento:

- Programación secuencial.
- Programación concurrente mediante hilos.
- Programación paralela mediante procesos.

El proyecto demuestra que la incorporación de
concurrencia y paralelismo puede mejorar el rendimiento
de un sistema de procesamiento de datos, dependiendo
de las características de la carga de trabajo y de
los recursos computacionales disponibles.

La implementación de un motor de limpieza común
permitió mantener constantes las transformaciones
aplicadas a los datos durante la evaluación de las
diferentes estrategias.

## 2. Cumplimiento del objetivo general

Se desarrolló una aplicación funcional de consola
capaz de procesar múltiples archivos CSV y XLSX
mediante tres estrategias de ejecución.

El sistema permite seleccionar la modalidad de
procesamiento, ejecutar las operaciones de limpieza
y generar reportes individuales de los archivos
procesados.

La evaluación experimental permitió comparar los
tiempos de ejecución, el speedup, la eficiencia
relativa y el rendimiento de procesamiento.

Por lo tanto, se considera cumplido el objetivo
general dentro del alcance establecido.

## 3. Cumplimiento de los objetivos específicos

| Objetivo | Evidencia | Estado |
|---|---|---|
| Automatizar la limpieza de archivos | Aplicación funcional CSV y XLSX | Cumplido |
| Implementar procesamiento secuencial | src/sequential.py | Cumplido |
| Implementar concurrencia | src/threaded.py | Cumplido |
| Implementar paralelismo | src/parallel.py | Cumplido |
| Verificar la equivalencia | 18 configuraciones verificadas | Cumplido |
| Evaluar el rendimiento | 105 mediciones experimentales | Cumplido |
| Analizar ventajas y limitaciones | Documentación de resultados | Cumplido |
| Facilitar la reproducibilidad | Scripts, semillas y reportes | Cumplido |

## 4. Principales resultados

### 4.1 Resultados funcionales

La aplicación permite realizar operaciones generales
de limpieza sobre archivos tabulares con diferentes
estructuras.

Las operaciones implementadas incluyen:

- Normalización de espacios en campos de texto.
- Normalización de representaciones de valores faltantes.
- Eliminación de registros completamente duplicados.
- Contabilización de estadísticas.
- Exportación de archivos procesados.
- Manejo individual de errores.
- Generación de reportes consolidados.

La aplicación no depende de una estructura de columnas
específica ni del generador de datos experimentales.

### 4.2 Resultados de validación

| Indicador | Resultado |
|---|---:|
| Pruebas automatizadas aprobadas | 6/6 |
| Configuraciones de equivalencia aprobadas | 18/18 |
| Comparaciones mediante SHA-256 | 450 |
| Archivos experimentales distintos | 75 |
| Registros experimentales de entrada | 612500 |
| Mediciones de rendimiento | 105 |

La validación permitió comprobar que las estrategias
concurrentes y paralelas produjeron archivos CSV
equivalentes a los obtenidos mediante la referencia
secuencial en los escenarios evaluados.

La equivalencia se verificó mediante la comparación
del contenido de los archivos utilizando SHA-256.

### 4.3 Resultados de rendimiento

| Escenario | Mejor configuración | Tiempo mediano (s) | Speedup |
|---|---|---:|---:|
| Pequeño | Hilos (2) | 0.0789 | 1.5626 |
| Mediano | Hilos (4) | 0.6430 | 1.2237 |
| Grande | Procesos (4) | 2.6653 | 1.2265 |

Los resultados muestran que no existe una estrategia
universalmente superior dentro de las configuraciones
evaluadas.

La selección del modelo de ejecución depende de
la cantidad de archivos, el tamaño de los datos
y los costos asociados con la administración de
los trabajadores.

## 5. Conclusiones sobre programación concurrente

La implementación mediante ThreadPoolExecutor obtuvo
los menores tiempos medianos en los escenarios
pequeño y mediano.

Los hilos constituyen una alternativa para cargas
que combinan operaciones de entrada y salida con
transformaciones de datos.

Sin embargo, incrementar el número de hilos no
garantiza una mejora proporcional del rendimiento.

En el escenario pequeño, dos hilos obtuvieron
un tiempo mediano inferior al registrado mediante
cuatro hilos.

Este resultado demuestra la importancia de evaluar
experimentalmente la cantidad de trabajadores.

## 6. Conclusiones sobre programación paralela

La implementación mediante ProcessPoolExecutor
obtuvo su mejor resultado relativo en el escenario
grande utilizando cuatro procesos.

En esta configuración se registró un speedup
de aproximadamente 1.2265 respecto a la referencia
secuencial.

Las configuraciones basadas en procesos fueron
considerablemente más lentas en el escenario pequeño.

Este comportamiento es consistente con los costos
adicionales de creación, comunicación y administración
de procesos.

Los resultados sugieren que una mayor carga de
trabajo puede favorecer el aprovechamiento del
paralelismo.

No obstante, los costos individuales de administración
de procesos no fueron medidos de manera aislada.

## 7. Conclusiones sobre escalabilidad

El incremento de trabajadores no produjo una
aceleración lineal.

Las mejores configuraciones experimentales
presentaron las siguientes eficiencias relativas:

| Escenario | Configuración | Eficiencia relativa |
|---|---|---:|
| Pequeño | Hilos (2) | 78.13 % |
| Mediano | Hilos (4) | 30.59 % |
| Grande | Procesos (4) | 30.66 % |

La eficiencia relativa representa la aceleración
obtenida por trabajador respecto a la referencia
secuencial.

No constituye una medición directa de la utilización
del procesador.

El equipo utilizado dispone de dos núcleos físicos
y cuatro procesadores lógicos.

Estas características, junto con la memoria
disponible y el almacenamiento, pueden limitar
la escalabilidad del sistema.

## 8. Conclusiones sobre coordinación y seguridad

La descomposición del problema mediante archivos
independientes permitió distribuir las tareas
sin introducir dependencias directas entre ellas.

Cada trabajador utiliza sus propias estructuras
de datos y genera un archivo de salida independiente.

La recuperación de resultados se realiza mediante
objetos Future.

El proceso principal administra la consolidación
de estadísticas y la escritura del reporte final.

Esta arquitectura reduce la necesidad de utilizar
mecanismos explícitos de exclusión mutua.

La ausencia de locks explícitos constituye una
decisión arquitectónica fundamentada en la
independencia de las tareas.

Las pruebas realizadas aportan evidencia de
consistencia, aunque no garantizan la ausencia
de errores bajo todas las condiciones posibles.

## 9. Aplicación práctica

Además de la evaluación experimental controlada,
el sistema fue utilizado para procesar cinco
archivos de distintas fuentes y formatos.

El lote incluyó cuatro archivos CSV y un archivo
XLSX.

| Indicador | Resultado |
|---|---:|
| Archivos de entrada | 5 |
| Registros originales | 103262 |
| Registros finales | 103173 |
| Duplicados eliminados | 89 |
| Operaciones exitosas entre las tres modalidades | 15 |
| Errores registrados | 0 |

Los resultados de limpieza corresponden a las
estadísticas del reporte revisado.

Las tres modalidades procesaron correctamente
el lote completo.

| Modalidad | Tiempo registrado (s) |
|---|---:|
| Secuencial | 2.6654 |
| Hilos | 1.5313 |
| Procesos | 2.4720 |

La modalidad concurrente obtuvo una reducción
aproximada del 42.55 % respecto al tiempo
secuencial en esta demostración.

Estos resultados corresponden a una ejecución
por modalidad y no deben generalizarse como
resultados experimentales definitivos.

La demostración permite confirmar la capacidad
del sistema para procesar archivos externos
sin modificar su código fuente.

## 10. Aportación del proyecto

Parallel Data Cleaner constituye una aplicación
práctica de los fundamentos de programación
concurrente y paralela dentro del procesamiento
de datos.

El proyecto integra conocimientos relacionados con:

- Descomposición de problemas.
- Distribución de tareas.
- Administración de trabajadores.
- Coordinación de resultados.
- Manejo de excepciones.
- Validación de equivalencia.
- Medición de rendimiento.
- Análisis experimental.
- Control de versiones.
- Reproducibilidad.

Su principal aportación consiste en proporcionar
una implementación funcional que permite estudiar
las diferencias entre modelos de ejecución
aplicados a un problema de limpieza de datos.

El proyecto no pretende desarrollar un algoritmo
de limpieza novedoso, sino evaluar distintas
estrategias para ejecutar las mismas operaciones.

## 11. Limitaciones del proyecto

Las principales limitaciones identificadas son:

- Procesamiento de archivos completos en memoria.
- Compatibilidad limitada a CSV y XLSX.
- Procesamiento de la primera hoja de archivos XLSX.
- Ausencia de imputación automática.
- Ausencia de reglas específicas de un dominio.
- Evaluación experimental realizada en un solo equipo.
- Cinco mediciones por configuración.
- Ausencia de mediciones individuales de CPU y memoria.
- Ausencia de pruebas sobre otros sistemas operativos.
- Benchmarks controlados exclusivamente sobre CSV.
- Posibles efectos del orden de ejecución y las cachés.
- Ausencia de pruebas de significancia estadística.

Estas limitaciones delimitan el alcance de las
conclusiones obtenidas.

## 12. Trabajo futuro

Como posibles líneas de ampliación se identifican:

- Procesamiento de archivos mediante bloques.
- Evaluación sobre equipos con diferentes capacidades.
- Incorporación de métricas de consumo de memoria.
- Medición de utilización de CPU.
- Evaluación experimental específica para XLSX.
- Comparación con mayores cantidades de trabajadores.
- Configuración personalizada de reglas de limpieza.
- Selección automática de estrategias según la carga.

Estas propuestas no forman parte de la versión
v1.0.0 y no fueron implementadas durante el proyecto.

## 13. Aprendizajes obtenidos

El desarrollo permitió comprender que la concurrencia
y el paralelismo no representan soluciones
automáticamente superiores al procesamiento
secuencial.

Una implementación concurrente o paralela puede
presentar un rendimiento inferior cuando los
costos adicionales superan los beneficios de
la distribución de tareas.

También se identificó la importancia de verificar
la equivalencia de los resultados antes de
interpretar las mejoras de rendimiento.

La utilización de mediciones repetidas, estadísticas
descriptivas y escenarios reproducibles permitió
fundamentar las conclusiones mediante evidencia
experimental.

El control de versiones facilitó la organización
del desarrollo y la conservación de las diferentes
etapas de implementación.

## 14. Estado final del sistema

Nombre: Parallel Data Cleaner.

Versión funcional: v1.0.0.

Estado técnico: desarrollo concluido dentro del
alcance establecido.

Modalidades implementadas:

- Secuencial.
- Concurrente mediante hilos.
- Paralela mediante procesos.

Componentes concluidos:

- Motor de limpieza.
- Procesamiento individual de archivos.
- Interfaz de consola.
- Administración de trabajadores.
- Generación de reportes.
- Pruebas automatizadas.
- Validación de equivalencia.
- Benchmarks reproducibles.
- Visualización de resultados.
- Documentación técnica.

## 15. Conclusión personal

El desarrollo de Parallel Data Cleaner me permitió
aplicar los conocimientos adquiridos en programación
concurrente y paralela a un problema relacionado
con la ingeniería de datos.

Durante el proyecto comprendí que optimizar un
sistema no consiste únicamente en incrementar
la cantidad de trabajadores, sino en identificar
las características del problema y evaluar
experimentalmente las alternativas disponibles.

Los resultados obtenidos demostraron que una
estrategia puede ser eficiente bajo determinadas
condiciones y presentar un rendimiento inferior
cuando cambia la carga de trabajo.

Considero que la principal enseñanza del proyecto
es la importancia de combinar una implementación
correcta con una metodología de validación y
evaluación reproducible.

La programación concurrente y paralela constituye
una herramienta relevante para el procesamiento
de datos, siempre que su aplicación se encuentre
justificada mediante evidencia técnica.

## 16. Declaración sobre el uso de inteligencia artificial

Durante el desarrollo del proyecto se utilizaron
herramientas de inteligencia artificial como apoyo
para la planificación, elaboración y revisión del
código, interpretación de resultados y redacción
de la documentación técnica.

Las pruebas de funcionamiento, las ejecuciones
experimentales y la obtención de los resultados
se realizaron en el entorno local del proyecto.

Las conclusiones se fundamentan en las mediciones
registradas y en las evidencias conservadas en
el repositorio.

## 17. Cierre técnico

Parallel Data Cleaner concluye su ciclo de desarrollo
con una aplicación funcional, pruebas automatizadas,
resultados experimentales y documentación técnica.

La versión v1.0.0 representa el cierre del alcance
funcional establecido para el proyecto.

Las evidencias obtenidas permiten reproducir los
experimentos y analizar las ventajas y limitaciones
de las estrategias implementadas.
