import random
import math
import numpy as np
from view_board import vector_board, print_board

def calculate_attacks(board):
        """Calcula el número de ataques entre reinas en el tablero."""
        attacks = 0
        n = len(board)
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    attacks += 1
        return attacks
    
def schedule(t):
    """Función de enfriamiento."""
    return 1/(1+t)

def probability(delta, temperature):
    """Calcula la probabilidad de aceptar una solución peor."""
    return math.exp(-delta / temperature)
    
def simulated_annealing(board, max_iterations=1000):
    current_board = board[:]
    current_h = calculate_attacks(current_board)

    initial_temp = 1000
    final_temp = 1
    cooling_rate = 0.99
    
    temperatures = np.arange(initial_temp, final_temp, -cooling_rate)
    i = 0

    for t in temperatures:
        # Enfriar la temperatura
        t = schedule(t)
    
        # Generar un vecino aleatorio
        col = random.randint(0, n - 1)
        row = random.randint(0, n - 1)
        neighbor = current_board[:]
        neighbor[col] = row

        # Calcular el costo del vecino
        neighbor_h = calculate_attacks(neighbor)

        # Si el vecino es mejor, lo aceptamos
        if neighbor_h < current_h:
            current_board = neighbor
            current_h = neighbor_h
        else:
            # Si el vecino es peor, lo aceptamos con cierta probabilidad
            delta = neighbor_h - current_h
            if delta < 0 or random.random() < probability(delta, t):
                current_board = neighbor
                current_h = neighbor_h

        if current_h == 0:
            break  # Solución óptima encontrada
        i += 1
        if i >= max_iterations:
            break  # Limitar el número de iteraciones
        

    return current_board, current_h

if __name__ == "__main__":
    n = 8
    seeds = [42, 7, 21, 15, 3, 10, 5, 30]  # Cambiar el índice para probar con diferentes semillas
    for seed in seeds:
        initial_board = vector_board(n, seed)
        print("Tablero inicial:")
        print(initial_board)

        solution, h = simulated_annealing(initial_board)

        print("Solución encontrada:")
        print(solution)

        print("Número de ataques:")
        print(h)

        print("Representación del tablero:")
        print_board(solution)