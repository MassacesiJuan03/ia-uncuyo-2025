

1. Jugar al CS (o cualquier otro 3d Shooter):

   Performance: ganar rondas, kills, asistencias, % de tiros acertados

   Entorno: mapa del shooter (visión acotada)

   Actuadores/Acciones: acciones de movimiento(arriba, abajo, derecha, izquierda, agacharse, saltar), disparar, apuntar, cambiar de arma, etc.

   Sensores: minimapa, radar, barra de vida

   

* Totalmente observable o parcialmente observable: Entorno desde la perspectiva del personaje dentro del videojuego es parcialmente observable ya que por ejemplo lo que sucede detrás del personaje no se puede ver debido al ángulo de visión.


* Agente simple o multi-agente: Entorno multi-agente, en un shooter puede haber más de un agente (players).


* Deterministas o Estocásticos: Entorno estocástico si estamos considerando las decisiones a realizar, por ejemplo ir a plantar en A y que yendo a plantar me maten. No se puede asegurar que si se piensa algo vaya a suceder. Si lo vemos desde la perspectiva de las acciones que el personaje puede realizar sería determinista ya que están programadas para no ser aleatorias.


* Episódicos o Secuenciales: Entorno secuencial ya que las acciones anteriores afectan a las actuales, por ejemplo si mueres ya no pueden seguir jugando ese ronda en el caso del CS.


* Estáticos o Dinámicos: Entorno dinámico ya que mientras pasa el tiempo o se realiza una acción el entorno cambia, por ejemplo cuando comienza la ronda están todos vivos y a medida que pasa el tiempo van muriendo.


* Discretos o Continuos: Entorno continuo ya que no hay una cantidad de acciones finitas sobre este. No se pueden contabilizar las combinaciones que afectan el espacio de movimiento en un shooter.


* Conocidos o Desconocidos: Desde el punto de vista de un jugador el entorno es conocido si ya ha jugado con anterioridad y conoce las mecánicas del juego, por ejemplo sabe como funcionan las grandas, conoce las posiciones y sectores del mapa,etc. En el caso de un jugador inexperto o bot el entorno sería desconocido y tendría que aprender jugando para que sea conocido.


2. Explorar los océanos:

   Performance: descubrir especies, descubrir lugares/áreas

   Entorno: océano 

   Actuadores/Acciones: equipos de buceo, submarinos, bucear, navegar

   Sensores: cámara de grabación, brújula, linterna, oído, vista, tacto, sensores de profundidad

   

* Totalmente observable o parcialmente observable: Entorno parcialmente observable, no se tiene un panorama completo del océano.


* Agente simple o multi-agente: Puede ser ambos, generalmente es multi-agente ya que pueden haber varias personas o submarinos explorando el área.


* Deterministas o Estocásticos: Entorno estocástico ya que no se tiene control sobre las corrientes marinas y la fauna del océano.


* Episódicos o Secuenciales: Entorno secuencial las acciones anteriores afectan al panorama actual.


* Estáticos o Dinámicos: Entorno dinámico ya que a medida que se actúa por ejemplo la fauna cambia, en general en entorno cambia.


* Discretos o Continuos: Entorno continuo, no existen acciones finitas a realizar, todo sucede de manera continua.


* Conocidos o Desconocidos: Entorno desconocido no sé conoce todo lo que hay alrededor.


  

3. Comprar y vender tokens cripto (algunos)

   Performance: obtener ganancias

   Entorno: mercado/plataforma de tokens cripto

   Actuadores/Acciones: dispositivos electrónicos, transferir tokens, enviar compra, aceptar venta

   Sensores: confirmación de transacción, precios en el mercado, tendencias del mercado

   

* Totalmente observable o parcialmente observable: Entorno parcialmente observable ya que no se conoce con exactitud los movimientos futuros del mercado.


* Agente simple o multi-agente: Entorno multi-agente debido a que otros traders interactúan afectando el precio y disponibilidad de tokens.


* Deterministas o Estocásticos: Entorno estocástico, el precio de los tokens cambia de manera impredecible por acciones de otros traders u otros agentes.


* Episódicos o Secuenciales: Entorno secuencial debido a que cada acción (compra, venta) afecta el estado de la billetera virtual.


* Estáticos o Dinámicos: Entorno dinámico, el mercado cambia en tiempo real.


* Discretos o Continuos: Las acciones de compra y venta son discretas pero el mercado y el precio de los tokens cambia lo que hace que sea continuo.


* Conocidos o Desconocidos: Entorno desconocido, como el mercado cambia no se puede conocer su comportamiento.


  

4. Practicar tenis contra una pared

   Performance: precisión, aciertos, fallos

   Entorno: cancha de tenis con pared

   Acciones/Actuadores: golpear la pelota, moverse hacia atrás, adelante, costados

   Sensores: tacto, visión, fuerza aplicada, raqueta

   

* Totalmente observable o parcialmente observable: Entorno totalmente observable, la persona puede ver la pelota y la pared mientras practica.


* Agente simple o multi-agente: Entorno con agente simple, solo un jugador interactúa con la pelota.


* Deterministas o Estocásticos: Las acciones son deterministas pero debido al error humano la precisión del golpe puede variar y generar que el rebote sea impredecible derivando a un entorno más estocástico.


* Episódicos o Secuenciales: Entorno secuencial debido a que los golpes afectan la posición de la pelota.


* Estáticos o Dinámicos: Entorno dinámico ya que la pelota cambia de lugar, esto afecta el posicionamiento de la persona.


* Discretos o Continuos: Entorno continuo, la posición de la pelota, fuerza aplicada, posicionamiento cambian con el tiempo.


* Conocidos o Desconocidos: Entorno conocido, la persona conoce los movimientos y reglas del entorno.

5. Realizar un salto de altura:

   Performance: altura superada, no dejar caer la barra, técnica correcta

   Entorno: barra, pista, colchoneta

   Acciones/Actuadores: correr, impulsarse, cuerpo de la persona

   Sensores: vista, percepción, equilibrio

   

* Totalmente observable o parcialmente observable: Entorno totalmente observable, la persona visualiza la pista, barra, colchoneta y percibe su propio cuerpo.


* Agente simple o multi-agente: Entorno con agente simple, la persona que realiza el salto.


* Deterministas o Estocásticos: Entorno estocástico debido a que en el salto pueden influir factores que hace que no siempre se consiga el mismo resultado.


* Episódicos o Secuenciales: Entorno episódico, los saltos son independientes uno de otros. 


* Estáticos o Dinámicos: Entorno dinámico ya que el entorno puede cambiar debido al movimiento de la persona.


* Discretos o Continuos: Entorno continuo ya que la velocidad de la persona, la fuerza de impulso y la altura pueden cambiar.


* Conocidos o Desconocidos: Entorno conocido, las reglas para realizar el salto son conocidas.


  

6. Pujar por un artículo en una subasta:

   Performance: obtener artículo al menor precio

   Entorno: participantes, aplicación de subasta en línea, subasta presencial

   Acciones/Actuadores: ingresar monto para la puja, botones (subasta online), levantar cartel (subasta física)

   Sensores: detalles del artículo, dinero máximo ofertado, dinero disponible, tiempo restante, cantidad de postores

   

* Totalmente observable o parcialmente observable: Entorno totalmente observable, el apostador ve las pujas y el precio del artículo.


* Agente simple o multi-agente: Entorno multi-agente, varias personas pujando por el artículo.


* Deterministas o Estocásticos: Entorno estocástico debido a que el precio varía de acuerdo a las acciones de los demás.


* Episódicos o Secuenciales: Entorno secuencial, ya que las acciones afectan al resultado final, por ejemplo, el pujar por el artículo o esperar.


* Estáticos o Dinámicos: Entorno dinámico, las acciones de los demás o de uno influyen sobre el precio del producto (entorno).


* Discretos o Continuos: Entorno discreto, las acciones son pujar o no hacerlo por lo que son finitas. 


* Conocidos o Desconocidos: Entorno conocido, las reglas de la subasta son conocidas, pero no se conoce el comportamiento de los otros agentes ni el valor que le dan al artículo.


  
