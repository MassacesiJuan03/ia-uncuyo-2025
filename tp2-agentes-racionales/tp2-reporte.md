**Reporte de Comparativas entre Agentes**

1) Efectividad promedio por tamaño de entorno y agente  
   

![][image1]  
Este gráfico de barras compara la efectividad promedio de cada agente según el tamaño del entorno. Permite ver cómo afecta el tamaño del entorno al desempeño de los agentes y cuál de ellos mantiene mejor su efectividad en entornos más grandes o pequeños.

Se puede deducir que en entornos entre 4x4 y 8x8 ambos agentes limpian en promedio la misma cantidad de celdas sucias. Mientras más grande el entorno los agentes pierden efectividad y se comportan de manera más parecida.

2) Eficiencia promedio por tamaño de entorno y agente  
   

![][image2]  
En este gráfico de barras se compara la eficiencia promedio (performance/pasos) de los agentes para cada tamaño de entorno permitiendo identificar qué agente logra limpiar más celdas por paso y cómo varía esta relación con el tamaño del entorno.

En entornos más grandes, la eficiencia de ambos agentes disminuye, pero el Agente Reflexivo Simple sigue manteniendo una mayor eficiencia, ya que sabe que debe limpiar cuando una celda está sucia lo que le ahorra movimientos.

El Agente Random muestra una eficiencia baja y bastante estable, sin importar el tamaño del entorno, lo que indica que su desempeño no mejora. Esto se debe a que la cantidad de pasos que realiza es mayor a la performance, tiene sentido ya que no sabe cuando una celda está sucia.

3) Boxplot de efectividad por agente en entornos 4x4

![][image3]  
Este diagrama muestra la efectividad de ambos agentes en entornos pequeños (4x4) separados por dirt_rate:

**Dirt Rate = 0.1 y 0.2**: En estos escenarios con poca suciedad, ambos agentes muestran efectividades muy bajas pero similares. El Agente Reflexivo Simple tiene una mediana ligeramente superior, pero la variabilidad es alta en ambos casos. Con menos suciedad disponible, incluso el agente reflexivo tiene dificultades para encontrar y limpiar todas las celdas sucias en un entorno pequeño.

**Dirt Rate = 0.4**: Aquí se observa una diferencia significativa. El Agente Reflexivo Simple alcanza efectividades cercanas a 1.0 en la mayoría de ejecuciones (mediana alta), mientras que el Agente Random se mantiene muy bajo (cerca de 0.05). Esto demuestra que con suficiente suciedad, el agente reflexivo puede limpiar casi todo el entorno pequeño.

**Dirt Rate = 0.8**: Con alta densidad de suciedad, el Agente Reflexivo Simple mantiene su excelente desempeño con mediana cercana a 1.0, mientras que el Agente Random mejora levemente pero sigue siendo muy inefectivo. Los outliers del Random sugieren que ocasionalmente tiene suerte y limpia más de lo esperado.

4) Boxplot de eficiencia por agente en entornos 4x4

![][image4]  
Este diagrama muestra la eficiencia (celdas limpiadas por paso) en entornos 4x4:

**Dirt Rate = 0.1 y 0.2**: La eficiencia de ambos agentes es baja debido a la escasa suciedad. El Agente Reflexivo Simple muestra mayor variabilidad y algunos casos de alta eficiencia cuando logra encontrar y limpiar rápidamente las pocas celdas sucias.

**Dirt Rate = 0.4**: El Agente Reflexivo Simple muestra una eficiencia significativamente mayor, con valores concentrados entre 0.1 y 1.0, mientras que el Agente Random se mantiene cerca de 0.05. Esto indica que el agente reflexivo aprovecha mejor cada paso para limpiar.

**Dirt Rate = 0.8**: Con alta densidad de suciedad, el Agente Reflexivo Simple alcanza eficiencias entre 0.15 y 0.35, con algunos casos cercanos a 1.0, mientras que el Agente Random mejora ligeramente pero sigue siendo menos eficiente. Los outliers indican ejecuciones donde ambos agentes tuvieron un desempeño inusualmente bueno o malo.

5) Boxplot de efectividad por agente en entornos 64x64

![][image5]  
Este diagrama muestra la efectividad en entornos grandes (64x64):

**Dirt Rate = 0.1 y 0.2**: En entornos grandes con poca suciedad, ambos agentes tienen efectividades muy bajas (medianas cercanas a 0.0). La dificultad de encontrar las pocas celdas sucias en un espacio grande hace que incluso el Agente Reflexivo Simple tenga bajo desempeño.

**Dirt Rate = 0.4**: Ambos agentes mejoran ligeramente, pero siguen siendo bastante inefectivos (medianas por debajo de 0.1). El Agente Reflexivo Simple muestra una mediana marginalmente superior y mayor variabilidad, con algunos casos alcanzando 0.5-1.0 de efectividad.

**Dirt Rate = 0.8**: Con alta densidad de suciedad, el Agente Reflexivo Simple logra efectividades entre 0.05 y 0.2, con outliers cercanos a 0.35, mientras que el Agente Random se mantiene entre 0.05 y 0.13. En entornos grandes, incluso con mucha suciedad, ningún agente logra limpiar más del 35% del total en 1000 pasos.

6) Boxplot de eficiencia por agente en entornos 64x64

![][image6]  
Este diagrama muestra la eficiencia en entornos 64x64:

**Dirt Rate = 0.1 y 0.2**: La eficiencia es muy baja para ambos agentes (medianas cercanas a 0.0), con alta variabilidad. Ocasionalmente, algún agente tiene suerte y alcanza eficiencias de 0.03-0.07.

**Dirt Rate = 0.4**: Ambos agentes muestran eficiencias muy bajas (cerca de 0.0) con alta variabilidad. Los outliers indican casos excepcionales donde se logró mayor eficiencia, probablemente cuando el agente inició cerca de zonas con alta concentración de suciedad.

**Dirt Rate = 0.8**: Con alta densidad de suciedad, la eficiencia mejora ligeramente. El Agente Reflexivo Simple alcanza medianas entre 0.05 y 0.2, mientras que el Agente Random se mantiene entre 0.05 y 0.13. La alta variabilidad y presencia de outliers sugiere que la posición inicial del agente afecta significativamente su eficiencia en entornos grandes.  

[image1]: images/efectividad_por_size_y_agente.png

[image2]: images/eficiencia_por_size_y_agente.png

[image3]: images/boxplot_efectividad_4x4.png

[image4]: images/boxplot_eficiencia_4x4.png

[image5]: images/boxplot_efectividad_64x64.png

[image6]: images/boxplot_eficiencia_64x64.png
