**AIMA Questions**

2.10 Consider a modified version of the vacuum environment in Exercise 2.8, in which the agent is penalized one point for each movement.

a. Can a simple reflex agent be perfectly rational for this environment? Explain.

El agente no va a ser perfectamente racional debido a que sigue realizando acciones luego de haber limpiado todas las celdas sucias. El agente se detendrá una vez que su vida útil termine, es decir, realice los 1000 pasos.  
Una consecuencia de esto es que el agente tendrá una puntuación negativa y no maximizará su rendimiento. 

b. What about a reflex agent with state? Design such an agent.

El agente reflexivo con estados es racional, ya que si una casilla está sucia la limpia y luego puede moverse hacía otras casillas no visitadas. Una vez que limpie todas las casillas sucias se detiene para no obtener puntos de penalización.

c. How do your answers to a and b change if the agent’s percepts give it the clean/dirty status of every square in the environment?

El agente del punto a) seguiría sin ser racional debido a que por más tenga una percepción de las casillas sucias y limpias solo se detendrá hasta acabar con todos sus movimientos. No maximiza su rendimiento.

El agente del punto b) si sería racional, el conocer las casillas sucias le permitiría seguir la mejor ruta/camino para limpiar estas y minimizar las penalizaciones.  

2.11 Consider a modified version of the vacuum environment in Exercise 2.8, in which the geography of the environment—its extent, boundaries, and obstacles—is unknown, as is the initial dirt configuration. (The agent can go Up and Down as well as Left and Right.) 

a. Can a simple reflex agent be perfectly rational for this environment? Explain. 

No, no podría ser racional ya que una de las condiciones para serlo es conocer el entorno. Sin conocerlo no sé puede garantizar que el agente lo pueda cubrir en su totalidad.

b. Can a simple reflex agent with a randomized agent function outperform a simple reflex agent? Design such an agent and measure its performance on several environments. 

Al ser la función aleatoria el agente podría estar sobre una casilla sucia y no limpiarla, con el reflexivo simple eso no pasaría por como está definido. No tendría mejor rendimiento pero en entornos medianos podrían estar parejos.

c. Can you design an environment in which your randomized agent will perform poorly? Show your results. 

Su rendimiento es pobre en entornos grandes como 64x64 o 128x128 con una tasa de suciedad pequeña.

d. Can a reflex agent with state outperform a simple reflex agent? Design such an agent and measure its performance on several environments. Can you design a rational agent of this type?

Con entorno desconocido la racionalidad no es alcanzable, pero el agente puede ser racional explorando, limpiando cuando se detecta suciedad y detenerse cuando no hay más suciedad.

El agente reflexivo con estados hace lo anterior y además no visita celdas que ya ha visitado. Eso hace que su rendimiento sea mejor que el del agente reflexivo simple por el hecho de que no obtendrá puntos de penalización visitando celdas que fueron limpiadas.