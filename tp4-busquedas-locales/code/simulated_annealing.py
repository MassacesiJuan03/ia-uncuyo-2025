import random
import math
from view_board import vector_board, print_board


def simulated_annealing(board):
    """Aplica el algoritmo de recocido simulado para resolver el problema de las n-reinas.
    
    Args:
        board (list): Una lista que representa las posiciones de las reinas en cada columna.
        temperature (float): La temperatura inicial para el recorrido simulado.
        cooling_rate (float): La tasa de enfriamiento.
    
    Returns:
        list: Una lista que representa la solución encontrada o la mejor solución local.
    """
    def calculate_attacks(board):
        """Calcula el número de ataques entre reinas en el tablero."""
        attacks = 0
        n = len(board)
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    attacks += 1
        return attacks

    current_board = board[:]
    current_h = calculate_attacks(current_board)
    best_board = current_board[:]
    best_h = current_h

    t = 1.0
    cooling_rate = 0.99

    while t > 0.01:
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

            # Actualizar la mejor solución encontrada
            if current_h < best_h:
                best_board = current_board[:]
                best_h = current_h
        else:
            # Aceptar el vecino con una probabilidad
            if math.exp((current_h - neighbor_h) / t) > random.random():
                current_board = neighbor
                current_h = neighbor_h

        # Enfriar la temperatura
        t *= cooling_rate

    return best_board, best_h

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