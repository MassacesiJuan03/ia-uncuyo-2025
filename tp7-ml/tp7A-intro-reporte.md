Trabajo Práctico 7A: Introducción a ML

## Ejercicio 1
En cada uno de los siguientes ejercicios, indique si en general se espera que un método de aprendizaje de máquinas flexible se comporte mejor o peor que uno inflexible. Justifique su respuesta.

### a) El tamaño de la muestra n es extremadamente grande, y el número de predictores p es pequeño.
**Respuesta: flexible.** 
Con muchas observaciones y pocos predictores, hay suficientes datos para que un modelo flexible aprenda patrones complejos sin sobreajustar.

### b) El número de predictores p es extremadamente grande, y el número de observaciones n es pequeño.
**Respuesta: ineflexible.** 
Con pocos datos y muchos predictores, un modelo flexible tiende a sobreajustar, capturando ruido en lugar de patrones reales.

### c) La relación entre los predictores y la variable dependiente es altamente no lineal.
**Respuesta: flexible.** 
Los modelos flexibles pueden capturar relaciones no lineales complejas, mientras que los inflexibles están limitados a relaciones más simples.

### d) La varianza de los términos de error, σ² = Var(ϵ), es extremadamente alta.
**Respuesta: ineflexible.** 
Con alta varianza en el error, un modelo flexible tiende a ajustarse al ruido, aumentando el error por varianza.

## Ejercicio 2
Explique si cada escenario representa un problema de clasificación o de regresión, e indique si el interés principal es inferir o predecir. Especifique n (cantidad de observaciones) y p (cantidad de predictores) en cada caso.

### a) Conjunto de datos sobre las 500 empresas más importantes de Estados Unidos
- **Tipo:** Regresión
- **Objetivo:** Inferencia
- **n:** 500 observaciones
- **p:** 3 predictores 

### b) Lanzamiento de un nuevo producto
- **Tipo:** Clasificación
- **Objetivo:** Predicción
- **n:** 20 observaciones
- **p:** 13 predictores 

### c) Predicción del cambio en el tipo de cambio USD/Euro
- **Tipo:** Regresión
- **Objetivo:** Predicción
- **n:** 52 observaciones 
- **p:** 3 predictores 

## Ejercicio 3
¿Cuáles son las ventajas y desventajas de un enfoque muy flexible? (versus uno menos flexible)
para la regresión o clasificación? ¿Bajo qué circunstancias podría preferirse un enfoque más
flexible a uno menos flexible? ¿Cuándo podría preferirse un enfoque menos flexible?

### Ventajas de un enfoque flexible:
- Puede capturar relaciones complejas y no lineales en los datos
- Mejor ajuste cuando la relación real es compleja
- Reduce el sesgo del modelo

### Desventajas de un enfoque flexible:
- Mayor riesgo de sobreajuste
- Requiere más datos de entrenamiento
- Menor interpretabilidad
- Mayor varianza en las predicciones

### ¿Cuándo preferir un enfoque flexible?
- Cuando n es grande y p es pequeño
- Cuando la relación entre variables es no lineal
- Cuando el objetivo principal es la predicción y no la interpretabilidad

### ¿Cuándo preferir un enfoque inflexible?
- Cuando n es pequeño o p es grande
- Cuando la interpretabilidad es importante
- Cuando hay alta varianza en los errores
- Cuando se busca inferencia sobre las relaciones entre variables

## Ejercicio 4
Describa las diferencias entre un enfoque paramétrico y uno no paramétrico. ¿Cuáles son las
ventajas y desventajas de un enfoque paramétrico para regresión o clasificación, a diferencia de
un enfoque no paramétrico?

### Enfoque Paramétrico:
- Asume una forma funcional específica para f (ej: lineal)
- Reduce el problema a estimar un conjunto finito de parámetros
- Ejemplo: regresión lineal, regresión logística

### Ventajas del enfoque paramétrico:
- Más fácil de interpretar
- Requiere menos datos para entrenar
- Computacionalmente más eficiente
- Menor varianza

### Desventajas del enfoque paramétrico:
- Si la forma funcional asumida es incorrecta, el modelo será pobre
- Alto sesgo si la realidad es más compleja
- Limitado a capturar relaciones simples

### Enfoque No Paramétrico:
- No asume una forma funcional predefinida para f
- Busca una estimación de f que se ajuste bien a los datos sin restricciones
- Ejemplo: KNN, árboles de decisión

### Ventajas del enfoque no paramétrico:
- Mayor flexibilidad
- Puede capturar relaciones complejas
- No requiere supuestos sobre la forma funcional

### Desventajas del enfoque no paramétrico:
- Requiere muchos más datos
- Riesgo de sobreajuste
- Menor interpretabilidad
- Computacionalmente más costoso

## Ejercicio 5
La siguiente tabla muestra un conjunto de entrenamiento que consta de seis observaciones, tres predictores, y una variable dependiente cualitativa.

Dataset de entrenamiento con 6 observaciones. Predicción usando K vecinos más cercanos para X₁ = X₂ = X₃ = 0.

### a) Distancia Euclidiana entre cada observación y el punto de prueba (0, 0, 0)

| Obs. | X₁ | X₂ | X₃ |   Y   | Distancia |
|------|----|----|----|-------|-----------|
| 1    | 0  | 3  | 0  | Rojo  |   3.00    |
| 2    | 2  | 0  | 0  | Rojo  |   2.00    |
| 3    | 0  | 1  | 3  | Rojo  |   3.16    |
| 4    | 0  | 1  | 2  | Verde |   2.24    |
| 5    | -1 | 0  | 1  | Verde |   1.41    |
| 6    | 1  | 1  | 1  | Rojo  |   1.73    |

### b) Predicción con K = 1
**Predicción: Verde**

El vecino más cercano es la observación 5 con Y = Verde.

### c) Predicción con K = 3
**Predicción: Rojo**

Los 3 vecinos más cercanos son:
- Obs. 5: distancia 1.41 → Verde
- Obs. 6: distancia 1.73 → Rojo
- Obs. 2: distancia 2.00 → Rojo

Conteo de votos: Rojo = 2, Verde = 1. Por mayoría, la predicción es Rojo.

### d) Si el límite de decisión de Bayes es altamente no lineal, ¿se espera que el mejor valor para K sea grande o pequeño?
**Se espera un K pequeño.**

Un K pequeño permite límites de decisión más flexibles y no lineales. Un K grande suaviza el límite de decisión, haciéndolo más lineal y menos flexible.
