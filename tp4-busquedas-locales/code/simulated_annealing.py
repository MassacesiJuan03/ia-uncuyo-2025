from __future__ import annotations

import math
import random
from typing import List, Tuple

from nqueens_utils import calculate_attacks
from view_board import print_board, vector_board


def simulated_annealing(
    initial_board: List[int],
    max_states: int,
    seed: int | None = None,
    history: List[Tuple[int, int]] | None = None,
) -> Tuple[List[int], int, int]:
    rng = random.Random(seed)
    n = len(initial_board)
    current_board = initial_board[:]
    current_h = calculate_attacks(current_board)
    best_board = current_board[:]
    best_h = current_h
    states_explored = 1

    if history is not None:
        history.append((states_explored, best_h))

    temperature = 1000.0
    final_temp = 1e-3
    cooling_rate = 0.995

    while temperature > final_temp and states_explored < max_states:
        col = rng.randrange(n)
        row = rng.randrange(n)
        neighbor = current_board[:]
        neighbor[col] = row

        neighbor_h = calculate_attacks(neighbor)
        states_explored += 1
        delta = neighbor_h - current_h

        if delta < 0:
            current_board = neighbor
            current_h = neighbor_h
        else:
            acceptance_probability = math.exp(-delta / max(temperature, 1e-9))
            if rng.random() < acceptance_probability:
                current_board = neighbor
                current_h = neighbor_h

        if current_h < best_h:
            best_board = current_board[:]
            best_h = current_h

        if history is not None:
            history.append((states_explored, best_h))

        if best_h == 0:
            break

        temperature *= cooling_rate

    return best_board, best_h, states_explored

if __name__ == "__main__":
    n = 8
    seeds = [42, 7, 21, 15, 3, 10, 5, 30]  # Cambiar el índice para probar con diferentes semillas
    for seed in seeds:
        initial_board = vector_board(n, seed)
        print("Tablero inicial:")
        print(initial_board)

        solution, h, states = simulated_annealing(initial_board, max_states=1000, seed=seed)

        print("Solución encontrada:")
        print(solution)

        print("Número de ataques:")
        print(h)

        print("Estados explorados:")
        print(states)

        print("Representación del tablero:")
        print_board(solution)