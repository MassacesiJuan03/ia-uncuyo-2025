from __future__ import annotations

import csv
import time
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Tuple

from genetic import algoritmo_genetico
from hill_climbing import hill_climbing
from random_solver import random_search
from simulated_annealing import simulated_annealing
from view_board import vector_board

MAX_STATES = 5000
BOARD_SIZES: Iterable[int] = (4, 8, 10)
SEEDS: Iterable[int] = range(30)
OUTPUT_PATH = Path(__file__).with_name("tp4-Nreinas.csv")

AlgorithmFn = Callable[[int, int, int], Tuple[List[int], int, int]]


def run_random(size: int, seed: int) -> Tuple[List[int], int, int]:
    return random_search(size, MAX_STATES, seed)


def run_hill_climbing(size: int, seed: int) -> Tuple[List[int], int, int]:
    initial_board = vector_board(size, seed)
    return hill_climbing(initial_board, MAX_STATES)


def run_simulated_annealing(size: int, seed: int) -> Tuple[List[int], int, int]:
    initial_board = vector_board(size, seed)
    return simulated_annealing(initial_board, MAX_STATES, seed=seed)


def run_genetic(size: int, seed: int) -> Tuple[List[int], int, int]:
    initial_board = vector_board(size, seed)
    return algoritmo_genetico(initial_board, MAX_STATES, seed=seed)


ALGORITHMS: Dict[str, Callable[[int, int], Tuple[List[int], int, int]]] = {
    "random": run_random,
    "HC": run_hill_climbing,
    "SA": run_simulated_annealing,
    "GA": run_genetic,
}


def main() -> None:
    records: List[Dict[str, object]] = []

    for size in BOARD_SIZES:
        for env_id, seed in enumerate(SEEDS):
            for name, solver in ALGORITHMS.items():
                start = time.perf_counter()
                board, h_value, states = solver(size, seed)
                elapsed = time.perf_counter() - start

                records.append(
                    {
                        "algorithm_name": name,
                        "env_n": env_id,
                        "size": size,
                        "best_solution": board,
                        "H": h_value,
                        "states": states,
                        "time": elapsed,
                    }
                )

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "algorithm_name",
                "env_n",
                "size",
                "best_solution",
                "H",
                "states",
                "time",
            ],
        )
        writer.writeheader()
        for row in records:
            row = {**row, "best_solution": str(row["best_solution"])}
            writer.writerow(row)

    print(f"Resultados guardados en {OUTPUT_PATH.resolve()}")
    print(f"MAX_STATES utilizado: {MAX_STATES}")


if __name__ == "__main__":
    main()
