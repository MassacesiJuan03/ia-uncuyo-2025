import random
from typing import Dict, List, Optional, Set, Tuple


def select_mrv_var(domains: Dict[int, Set[int]], assignment: Dict[int, int], seed: int = None):
    """Selecciona la variable no asignada con menor tamaño de dominio (MRV)"""
    unassigned = [v for v in domains.keys() if v not in assignment]
    
    if seed is not None:
        # Agrupar por tamaño de dominio
        min_size = min(len(domains[v]) for v in unassigned)
        mrv_vars = [v for v in unassigned if len(domains[v]) == min_size]
        # Si hay empate, elegir aleatoriamente
        if len(mrv_vars) > 1:
            random.seed(seed + len(assignment))  # Semilla diferente en cada nivel
            return random.choice(mrv_vars)
        return mrv_vars[0]
    else:
        # Orden determinístico: ordenar por tamaño de dominio, tie-break por índice
        unassigned.sort(key=lambda v: (len(domains[v]), v))
        return unassigned[0]


def forward_checking_recursive(
    assignment: Dict[int, int],
    domains: Dict[int, Set[int]],
    n: int,
    states_explored: List[int],
    domain_order: List[int],
    seed: int = None,
):
    
    states_explored[0] += 1

    # caso base
    if len(assignment) == n:
        return dict(assignment)

    var = select_mrv_var(domains, assignment, seed)

    # usar el orden de dominio definido (puede ser aleatorio)
    values_to_try = [v for v in domain_order if v in domains[var]]
    
    for value in values_to_try:
        # crear copia local de dominios para aplicar forward checking
        new_domains: Dict[int, Set[int]] = {v: set(domains[v]) for v in domains}

        # asignar
        assignment[var] = value
        new_domains[var] = {value}

        failed = False

        # forward checking: eliminar valores inconsistentes en variables no asignadas
        for other in range(n):
            # saltar columnas ya asignadas o la misma columna
            if other in assignment or other == var:
                continue

            to_remove = set()
            for r in new_domains[other]:
                # misma fila
                if r == value:
                    to_remove.add(r)
                    continue
                # misma diagonal
                if abs(r - value) == abs(other - var):
                    to_remove.add(r)

            if to_remove:
                new_domains[other] -= to_remove

            if not new_domains[other]:
                failed = True
                break

        if not failed:
            result = forward_checking_recursive(assignment, new_domains, n, states_explored, domain_order, seed)
            if result is not None:
                return result

        # backtrack: desasignar y continuar
        del assignment[var]

    return None


def forward_checking(n: int, seed: int = None):
    domains: Dict[int, Set[int]] = {i: set(range(n)) for i in range(n)}
    assignment: Dict[int, int] = {}
    states_explored = [0]
    
    # Definir orden del dominio
    domain_order = list(range(n))
    if seed is not None:
        random.seed(seed)
        random.shuffle(domain_order)

    result = forward_checking_recursive(assignment, domains, n, states_explored, domain_order, seed)

    if result is None:
        return None, states_explored[0]

    solution = [result[i] for i in range(n)]
    return solution, states_explored[0]


def print_board(solution: Optional[List[int]]):
    if solution is None:
        print("No hay solución")
        return

    n = len(solution)
    for row in range(n):
        line = ""
        for col in range(n):
            if solution[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)
    print()


if __name__ == "__main__":
    for n in [4, 8, 10]:
        print(f"\n{'='*40}")
        print(f"N-Reinas con n={n} (Forward Checking)")
        print('='*40)

        solution, states = forward_checking(n)

        if solution:
            print(f"Solución encontrada: {solution}")
            print(f"Estados explorados: {states}")
            print("\nTablero:")
            print_board(solution)
        else:
            print(f"No se encontró solución")
            print(f"Estados explorados: {states}")
