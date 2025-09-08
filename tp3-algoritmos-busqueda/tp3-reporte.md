# Reporte de algoritmos de búsqueda

El análisis se basa en la evaluación de **BFS, DFS, DLS, UCS y A\*** bajo dos escenarios distintos. 

Configuración de los entornos:

- **Tamaño: 100x100**  
- **Porcentaje de hielo: 0.92**  
- **Porcentaje de obstáculo: 0.08**  

Los boxplots permiten observar la distribución, variabilidad, mediana y la media de cada métrica por algoritmo y escenario.

Heuristica usada para A*: **Distancia de Manhattan**

![][image1] 

## Costo de acciones
- **DFS** presenta un costo de acciones alto debido a la penalización vértical en el escenario 2, lo que evidencia su ineficiencia para encontrar soluciones óptimas cuando no existe un límite de profundidad.  
- **BFS y UCS** logran soluciones de costo bajo y estable. Se comportan de la misma manera, mostrando menor variabilidad.  
- **A\*** mantiene costos bajos en ambos escenarios, destacándose como uno de los métodos más eficientes.  
- **DLS (50, 75, 100)** produce costos nulos en la mayoría de los casos, estos escenarios no alcanzó soluciones viables.

![][image2] 

## Cantidad de acciones
- **DFS** es el que más acciones toma debido a que no siempre encuentra la ruta más optima. Debido a eso muestra mayor dispersión.  
- **BFS, UCS y A\*** utilizan menos acciones en comparación al DFS ya que siempre encuentran la ruta más corta, confirmando su eficiencia.  
- **DLS** valores nulos debido a que no encuentra soluciones.  

![][image3] 

## Estados explorados
- **BFS, DFS y UCS** exploran una gran cantidad de estados, mostrando distribuciones similares entre los escenarios reflejando su carácter exhaustivo.  
- **A\*** explora muchos menos estados en ambos escenarios, debido al usar heurísticas para guiar la búsqueda.  
- **DLS** explora muy pocos estados debido a la limitación en la profundidad.

![][image4] 

## Tiempo de ejecución
- **BFS, DFS y UCS** consumen más tiempo que A\*, manteniendo distribuciones relativamente estables entre escenarios.  
- **A\*** el algoritmo más rápido, mostrando tiempos de ejecución muy bajos y poca variabilidad.  
- **DLS** muchas veces no encuentra solución y finaliza prematuramente.

---

**A\*** demuestra ser el algoritmo más competente en ambos escenarios gracias a su bajo costo de acciones, pocos estados explorados, menor cantidad de acciones y tiempos reducidos.


[image1]: tp3-algoritmos-busqueda/images/boxplot_actions_cost.png

[image2]: tp3-algoritmos-busqueda/images/boxplot_actions_count.png

[image3]: tp3-algoritmos-busqueda/images/boxplot_states_n.png

[image4]: tp3-algoritmos-busqueda/images/boxplot_time.png
