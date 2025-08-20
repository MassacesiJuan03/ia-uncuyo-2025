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

3) Boxplot de efectividad por agente  
   

![][image3]  
En este diagrama de cajas de efectividad por agente se puede observar lo siguiente:

La mediana, la dispersión y la presencia de valores extremos.

Se observa que el Agente Reflexivo Simple tiene una mediana de efectividad claramente mayor que el Agente Random. Esto significa que, en la mayoría de los casos, limpia un mayor porcentaje de la suciedad total.

La dispersión de la efectividad es bastante alta en ambos agentes, pero especialmente en el Random, donde la mayoría de los valores están por debajo de 0.2 y algunos pocos alcanzan valores altos. El Agente Random presenta una mayor concentración de sus datos entre el 0.0 y la mediana, es decir, su efectividad promedio es bastante baja a comparación del Agente Reflexivo Simple.

El Agente Reflexivo Simple logra valores de efectividad cercanos a 1 (100%) en más ocasiones, lo que indica que es más probable que limpie todo el entorno. Ambos agentes pueden tener ejecuciones muy malas (efectividad cercana a 0).

4) Boxplot de eficiencia por agente

![][image4]  
En este diagrama de cajas de eficiencia por agente se puede observar lo siguiente:

El Agente Reflexivo Simple tiene una eficiencia promedio (mediana) mayor que el Agente Random. Esto indica que, en general, limpia más celdas por paso.

La variabilidad de la eficiencia es mayor en el Agente Reflexivo Simple, pero ambos agentes tienen la mayoría de sus valores de eficiencia en la parte baja del gráfico, es decir, son bastante ineficientes en término de esta.

Ambos agentes presentan outliers (círculos por encima de la caja), es decir, hay ejecuciones donde la eficiencia fue mucho mayor a lo habitual. Sin embargo, la mayoría de las ejecuciones se concentran en valores bajos.

El Agente Random es menos eficiente y más consistente, pero su eficiencia máxima es mucho menor que la del Agente Reflexivo Simple.  

[image1]: images/efectividad_por_size_y_agente.png

[image2]: images/eficiencia_por_size_y_agente.png

[image3]: images/boxplot_efectividad_por_agente.png

[image4]: images/boxplot_eficiencia_por_agente.png
