# TP4 - Búsquedas Locales
## Reporte Evaluación de Desempeño de Algoritmos para N-Queens

---

## 1. Introducción

Este reporte presenta la evaluación comparativa de cuatro algoritmos de búsqueda local para resolver el problema de las N-Reinas:

1. **Búsqueda Aleatoria (Random)**: Genera tableros aleatorios hasta encontrar una solución o agotar el límite de estados.
2. **Hill Climbing (HC)**: Algoritmo de ascensión de colina que explora vecinos y se mueve al mejor disponible.
3. **Simulated Annealing (SA)**: Recocido simulado con temperatura inicial de 1000 y factor de enfriamiento de 0.995.
4. **Algoritmo Genético (GA)**: Población de 500 individuos, tasa de mutación 0.1, selección por aptitud y elitismo.

## 1.1 Especificaciones de Implementación

### 1.1.1 Simulated Annealing

**Función de Schedule (Cronograma de Enfriamiento):**
- Se utiliza un schedule exponencial con la fórmula: `T(t+1) = T(t) × α`
- Temperatura inicial: `T₀ = 1000.0`
- Factor de enfriamiento: `α = 0.995`
- Temperatura final mínima: `T_min = 1e-3`

**Criterios de Terminación:**
- Temperatura alcanza el umbral mínimo (`temperature ≤ 1e-3`)
- Se encuentra una solución óptima (`H = 0`)
- Se agota el límite de estados evaluados (`states_explored ≥ 5000`)

**Mecanismo de Aceptación:**
- Movimientos que mejoran la solución se aceptan siempre (`ΔE < 0`)
- Movimientos que empeoran se aceptan con probabilidad `P = e^(-ΔE/T)`
- Se utiliza la distribución uniforme para generar vecinos (cambio de posición de una reina aleatoria)

### 1.1.2 Algoritmo Genético

**a) Definición de Individuos:**
- Cada individuo representa una configuración del tablero N×N
- Codificación: Vector de enteros de longitud N, donde `individuo[i]` indica la fila de la reina en la columna `i`
- Ejemplo para N=4: `[1, 3, 0, 2]` significa reinas en posiciones (0,1), (1,3), (2,0), (3,2)

**b) Estrategia de Selección:**
- **Selección por ruleta (fitness-proportionate selection)**
- Proceso: Se calcula la suma total de fitness, cada individuo tiene probabilidad = fitness_individual / suma_total
- Fitness de cada individuo: `f(i) = -H(i)` donde `H(i)` es el número de conflictos
- Probabilidad de selección proporcional al fitness relativo transformado

**Características de la Selección por Ruleta:**
- Los individuos con mayor fitness tienen mayor probabilidad de ser seleccionados
- Puede seleccionar individuos débiles ocasionalmente, manteniendo diversidad genética
- Sensible a diferencias grandes de fitness (individuos muy superiores pueden dominar)
- Permite convergencia gradual hacia mejores soluciones
- Maneja fitness negativos mediante transformación lineal que preserva proporciones relativas

**c) Estrategia de Reemplazo:**
- **Reemplazo generacional con elitismo**
- El mejor individuo de cada generación se preserva automáticamente
- La nueva población reemplaza completamente a la anterior (excepto el élite)
- Tamaño de población constante: 500 individuos

**d) Operadores:**
- **Cruce (Crossover):** Cruce de un punto
  - Punto de cruce aleatorio entre posiciones 1 y N-1
  - Hijo hereda segmento inicial del padre1 y segmento final del padre2
- **Mutación:** Mutación uniforme
  - Tasa de mutación: 0.1 (10%)
  - Cada gen tiene probabilidad 0.1 de mutar a un valor aleatorio entre 0 y N-1

**e) Criterios de Terminación:**
- Se encuentra una solución óptima (`H = 0`)
- Se agota el límite de estados evaluados (`states_explored ≥ 5000`)
- Cada evaluación de fitness cuenta como un estado explorado

## 2. Metodología Experimental

### 2.1 Configuración
- **Tamaños de tablero**: 4×4, 8×8, 10×10
- **Semillas**: 30 experimentos por algoritmo y tamaño (semillas 0-29)
- **Límite de estados**: 5000 evaluaciones por ejecución
- **Función objetivo**: Minimizar H (número de pares de reinas que se atacan)
- **Criterio de éxito**: H = 0 (solución óptima)

## 3. Resultados Estadísticos

### 3.1 Distribución de Conflictos (H)

![Distribución de H por Algoritmo](code/images/boxplot_H.png)

La figura muestra la distribución de la función objetivo H (número de conflictos) para cada algoritmo y tamaño de tablero:

- **Tablero 4×4**: Random, SA y GA logran consistentemente H=0 (solución óptima), mientras HC presenta mayor variabilidad con algunos casos sin resolver.
- **Tablero 8×8**: SA mantiene excelente desempeño con la mayoría de casos en H=0, GA muestra mayor dispersión pero con mediana baja, HC y Random presentan valores de H más altos.
- **Tablero 10×10**: Solo SA y GA encuentran soluciones óptimas, con SA mostrando mejor consistencia (menor variabilidad).

### 3.2 Estados Explorados

![Distribución de Estados Explorados](code/images/boxplot_states.png)

El análisis de eficiencia computacional revela:

- **Hill Climbing** es el más eficiente en número de estados explorados, especialmente en tableros pequeños, pero su efectividad disminuye drásticamente con el tamaño.
- **Random Search** utiliza pocos estados en 4×4 donde es efectivo, pero requiere el límite máximo (5000 estados) sin éxito en tableros mayores.
- **Simulated Annealing** presenta un uso moderado y consistente de estados, con buena relación efectividad/eficiencia.
- **Algoritmo Genético** requiere significativamente más estados debido a la evaluación poblacional, especialmente en tableros grandes.

### 3.3 Tiempo de Ejecución

![Distribución de Tiempo de Ejecución](code/images/boxplot_time.png)

Los tiempos de ejecución muestran patrones coherentes con la complejidad algorítmica:

- **Hill Climbing** presenta los menores tiempos cuando converge exitosamente.
- **Random y SA** mantienen tiempos bajos y consistentes across diferentes tamaños.
- **Algoritmo Genético** requiere considerablemente más tiempo, especialmente en tableros grandes, debido a las operaciones poblacionales (selección, cruce, mutación).

## 4. Análisis de Resultados

### 4.1 Efectividad por Tamaño de Problema

**Tablero 4×4**: Problema trivial donde Random, SA y GA logran 100% de éxito. Hill Climbing muestra limitaciones tempranas debido a mínimos locales.

**Tablero 8×8**: La complejidad aumenta significativamente. Simulated Annealing domina, seguido por GA y HC. Random no encuentra soluciones.

**Tablero 10×10**: Solo SA y GA encuentran soluciones. Random y HC fallan completamente, evidenciando sus limitaciones en espacios de búsqueda grandes.

### 4.2 Eficiencia Computacional

**Velocidad**: Hill Climbing es el más rápido cuando converge, seguido por Random y SA. GA es el más lento debido a la evaluación poblacional.

**Estados Explorados**: HC utiliza muy pocos estados pero con baja efectividad. SA y GA requieren más evaluaciones pero con mejor tasa de éxito.

### 4.3 Escalabilidad

El análisis revela un patrón claro de degradación del desempeño conforme aumenta el tamaño del problema:

- **Random**: Efectivo solo en problemas pequeños (4×4)
- **Hill Climbing**: Vulnerable a mínimos locales, falla en tableros grandes  
- **Simulated Annealing**: Mejor escalabilidad, mantiene efectividad hasta 10×10
- **Algoritmo Genético**: Escalabilidad moderada, efectivo pero costoso computacionalmente

## 5. Evolución de la Función Objetivo

### 5.1 Tablero 4×4

![Evolución H - 4x4](code/images/h_evolution_size_4.png)

En el tablero 4×4, todos los algoritmos muestran convergencia rápida hacia la solución óptima. Random encuentra la solución casi inmediatamente, HC converge en pocos pasos, mientras SA y GA requieren más evaluaciones pero alcanzan H=0 de forma consistente.

### 5.2 Tablero 8×8

![Evolución H - 8x8](code/images/h_evolution_size_8.png)

El aumento de complejidad en 8×8 revela las diferencias algorítmicas:
- **SA** muestra convergencia sostenida hacia H=0, evitando eficazmente los mínimos locales
- **GA** presenta mejoras graduales con algunas fluctuaciones poblacionales
- **HC** converge rápidamente pero se estanca en mínimos locales (H>0)
- **Random** no logra progresar significativamente más allá de las primeras evaluaciones

### 5.3 Tablero 10×10

![Evolución H - 10x10](code/images/h_evolution_size_10.png)

En el problema más complejo, solo SA y GA muestran capacidad de encontrar soluciones:
- **SA** mantiene un patrón de convergencia gradual pero efectivo
- **GA** requiere más exploraciones pero eventualmente mejora H
- **HC y Random** se estancan en valores altos de H, demostrando sus limitaciones en espacios de búsqueda complejos

## 6. Conclusiones

### 6.1 Desempeño Relativo
1. **Simulated Annealing** emerge como el algoritmo más robusto, con la mejor combinación de efectividad y escalabilidad
2. **Algoritmo Genético** ofrece buen desempeño pero a mayor costo computacional
3. **Hill Climbing** es eficiente en tiempo pero limitado por mínimos locales
4. **Búsqueda Aleatoria** solo viable para problemas muy simples

### 6.2 Algoritmo Más Adecuado: Simulated Annealing

**Simulated Annealing es el algoritmo más adecuado para resolver el problema de las N-Reinas** basado en:

**Justificación:**
- **Mejor escalabilidad**: Mantiene efectividad en tableros grandes (8×8, 10×10)
- **Equilibrio eficiencia/efectividad**: Costo computacional moderado con alta tasa de éxito
- **Robustez**: Mecanismo probabilístico evita mínimos locales sin colapsar en problemas complejos
- **Simplicidad**: Menos parámetros críticos que GA, más efectivo que HC en tableros grandes


