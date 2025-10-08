from __future__ import annotations

import random
from typing import List, Tuple

from nqueens_utils import calculate_attacks
from view_board import print_board


def init_board(n: int, rng: random.Random) -> List[int]:
    return [rng.randint(0, n - 1) for _ in range(n)]


def seleccion(
    poblacion: List[List[int]],
    aptitudes: List[float],
    rng: random.Random,
) -> List[int]:
    # Convertir fitness negativos a pesos positivos para random.choices
    min_fitness = min(aptitudes)
    if min_fitness < 0:
        # Desplazar todos los valores para que sean positivos
        pesos = [f - min_fitness + 1 for f in aptitudes]
    else:
        pesos = aptitudes[:]
    
    total = sum(pesos)
    if total == 0:
        return poblacion[rng.randrange(len(poblacion))][:]
    return rng.choices(poblacion, weights=pesos, k=1)[0][:]


def cruzar(parent1: List[int], parent2: List[int], rng: random.Random) -> List[int]:
    n = len(parent1)
    if n <= 1:
        return parent1[:]
    punto = rng.randint(1, n - 1)
    return parent1[:punto] + parent2[punto:]


def mutar(child: List[int], rng: random.Random, tasa_mutacion: float) -> List[int]:
    n = len(child)
    for i in range(n):
        if rng.random() < tasa_mutacion:
            child[i] = rng.randint(0, n - 1)
    return child


def algoritmo_genetico(
    initial_board: List[int],
    max_states: int,
    seed: int | None = None,
    tamaño_poblacion: int = 500,
    tasa_mutacion: float = 0.1,
    history: List[Tuple[int, int]] | None = None,
) -> Tuple[List[int], int, int]:
    rng = random.Random(seed)

    n = len(initial_board)
    population = [initial_board[:]] + [
        init_board(n, rng) for _ in range(max(tamaño_poblacion - 1, 0))
    ]

    best_board = initial_board[:]
    best_h = calculate_attacks(best_board)
    states_explored = 1

    fitnesses: List[float] = [-best_h]

    if history is not None:
        history.append((states_explored, best_h))

    for board in population[1:]:
        if states_explored >= max_states:
            return best_board, best_h, states_explored
        h = calculate_attacks(board)
        states_explored += 1
        if h < best_h:
            best_board = board[:]
            best_h = h
        if history is not None:
            history.append((states_explored, best_h))
        fitnesses.append(-h)

    if best_h == 0 or states_explored >= max_states:
        return best_board, best_h, states_explored

    while states_explored < max_states and best_h > 0:
        new_population: List[List[int]] = [best_board[:]]
        new_fitnesses: List[float] = [-best_h]

        while len(new_population) < tamaño_poblacion and states_explored < max_states:
            parent1 = seleccion(population, fitnesses, rng)
            parent2 = seleccion(population, fitnesses, rng)
            child = cruzar(parent1, parent2, rng)
            child = mutar(child, rng, tasa_mutacion)
            h_child = calculate_attacks(child)
            states_explored += 1
            if h_child < best_h:
                best_board = child[:]
                best_h = h_child
            if history is not None:
                history.append((states_explored, best_h))
            new_population.append(child)
            new_fitnesses.append(-h_child)

            if best_h == 0 or states_explored >= max_states:
                break

        population = new_population
        fitnesses = new_fitnesses

    if history is not None and (not history or history[-1][0] != states_explored):
        history.append((states_explored, best_h))

    return best_board, best_h, states_explored


if __name__ == "__main__":
    for n in [4, 8, 10]:
        board = [i % n for i in range(n)]
        solution, attacks, states = algoritmo_genetico(board, max_states=5000, seed=42)
        print(f"Tablero {n}x{n} -> ataques: {attacks}, estados: {states}")
        print_board(solution)