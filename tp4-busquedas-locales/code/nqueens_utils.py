from __future__ import annotations

from typing import List


def calculate_attacks(board: List[int]) -> int:
    """Calcula el número de pares de reinas que se atacan mutuamente."""
    attacks = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                attacks += 1
    return attacks
