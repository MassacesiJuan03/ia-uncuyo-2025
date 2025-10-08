from __future__ import annotations

from typing import List, Tuple

from nqueens_utils import calculate_attacks
from view_board import print_board, vector_board


def hill_climbing(
    initial_board: List[int],
    max_states: int,
    history: List[Tuple[int, int]] | None = None,
) -> Tuple[List[int], int, int]:
    """Aplica Hill Climbing con límite de estados explorados."""

    n = len(initial_board)
    current_board = initial_board[:]
    current_h = calculate_attacks(current_board)
    states_explored = 1
    best_so_far = current_h

    if history is not None:
        history.append((states_explored, best_so_far))

    while states_explored < max_states:
        neighbors = []
        for col in range(n):
            for row in range(n):
                if row != current_board[col]:
                    neighbor = current_board[:]
                    neighbor[col] = row
                    neighbors.append(neighbor)

        next_board = None
        next_h = current_h

        for neighbor in neighbors:
            if states_explored >= max_states:
                break
            attacks = calculate_attacks(neighbor)
            states_explored += 1
            if attacks < best_so_far:
                best_so_far = attacks
            if history is not None:
                history.append((states_explored, best_so_far))
            if attacks < next_h:
                next_board = neighbor
                next_h = attacks

        if not next_board or next_h >= current_h:
            break

        current_board = next_board
        current_h = next_h
        if current_h < best_so_far:
            best_so_far = current_h

        if current_h == 0:
            break

    if history and history[-1][0] != states_explored:
        history.append((states_explored, best_so_far))

    return current_board, current_h, states_explored

if __name__ == "__main__":
    n = 8
    seeds = [42, 7, 21, 15, 3, 10, 5, 30]  # Cambiar el índice para probar con diferentes semillas
    for seed in seeds:
        initial_board = vector_board(n, seed)
        print("Tablero inicial:")
        print(initial_board)

        solution, h, states = hill_climbing(initial_board, max_states=1000)
    
        print("Solución encontrada:")
        print(solution)
        
        print("Número de ataques:")
        print(h)    

        print("Estados explorados:")
        print(states)
        
        print("Representación del tablero:")
        print_board(solution)