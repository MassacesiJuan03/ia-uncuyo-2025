import random
from typing import Dict, List, Optional


def is_consistent(assignment: Dict[int, int], var: int, value: int):
    for assigned_var, assigned_value in assignment.items():
        # Restricción 1: No dos reinas en la misma fila
        if assigned_value == value:
            return False
        
        # Restricción 2: No dos reinas en la misma diagonal
        if abs(assigned_value - value) == abs(assigned_var - var):
            return False
    
    return True


def backtracking_recursive(
    assignment: Dict[int, int],
    n: int,
    states_explored: List[int],
    variables: List[int],
    domain: List[int]
):

    states_explored[0] += 1
    
    # Caso base: si todas las variables están asignadas, retornar solución
    if len(assignment) == n:
        return assignment
    
    # Seleccionar siguiente variable sin asignar (del orden aleatorizado)
    var = None
    for v in variables:
        if v not in assignment:
            var = v
            break
    
    # Intentar cada valor (fila) en el dominio (orden aleatorizado)
    for value in domain:
        if is_consistent(assignment, var, value):
            # Hacer asignación
            assignment[var] = value
            
            
            result = backtracking_recursive(assignment, n, states_explored, variables, domain)
            if result is not None:
                return result
            
            # Backtrack: deshacer asignación
            del assignment[var]
    
    # No hay solución en esta rama
    return None


def backtracking(n: int, seed: int = None):
    states_explored = [0]  # Lista mutable para pasar por referencia
    assignment = {}
    
    # Crear orden de variables y dominio
    variables = list(range(n))
    domain = list(range(n))
    
    # Si hay semilla, barajar el orden
    if seed is not None:
        random.seed(seed)
        random.shuffle(variables)
        random.shuffle(domain)

    result = backtracking_recursive(assignment, n, states_explored, variables, domain)

    if result is None:
        return None, states_explored[0]
    
    # Convertir diccionario a lista
    solution = [result[i] for i in range(n)]
    return solution, states_explored[0]


def print_board(solution: List[int]):
    """Imprime el tablero de forma visual."""
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
    # Probar con diferentes tamaños
    for n in [4, 8, 10]:
        print(f"\n{'='*40}")
        print(f"N-Reinas con n={n} (Backtracking)")
        print('='*40)

        solution, states = backtracking(n)

        if solution:
            print(f"Solución encontrada: {solution}")
            print(f"Estados explorados: {states}")
            print("\nTablero:")
            print_board(solution)
        else:
            print(f"No se encontró solución")
            print(f"Estados explorados: {states}")
