from __future__ import annotations

import random
from typing import List, Tuple

from nqueens_utils import calculate_attacks


def random_search(
    n: int,
    max_states: int,
    seed: int | None = None,
    history: List[Tuple[int, int]] | None = None,
) -> Tuple[List[int], int, int]:
    """Búsqueda aleatoria para N-Queens.

    Genera tableros aleatorios hasta encontrar una solución sin ataques o
    alcanzar el límite de estados.
    """

    rng = random.Random(seed)
    best_board: List[int] | None = None
    best_h = float("inf")
    states_explored = 0

    while states_explored < max_states:
        board = [rng.randint(0, n - 1) for _ in range(n)]
        h = calculate_attacks(board)
        states_explored += 1
        if h < best_h:
            best_board = board[:]
            best_h = h
            if history is not None:
                history.append((states_explored, best_h))
            if best_h == 0:
                break
        elif history is not None and best_h < float("inf"):
            history.append((states_explored, best_h))

    if best_board is None:
        best_board = [rng.randint(0, n - 1) for _ in range(n)]
        best_h = calculate_attacks(best_board)
        if history is not None:
            fallback_states = max(states_explored, 1)
            history.append((fallback_states, best_h))

        return best_board, best_h, max(states_explored, 1)

    return best_board, best_h, states_explored
