import math
import random

def generate_random_map_custom(size: int, frozen_rate: float, seed=None) -> tuple:
    if seed is not None:
        random.seed(seed)
    
    # Generar el mapa como lista de listas
    desc = [['F' if random.random() < frozen_rate else 'H' for _ in range(size)]
            for _ in range(size)]
    
    free_positions = [(i, j) for i in range(size) for j in range(size) if desc[i][j] == 'F']
    if len(free_positions) < 2:
        raise ValueError("No hay suficientes casillas transitables para colocar inicio y objetivo")
    
    start_pos = random.choice(free_positions)
    free_positions.remove(start_pos)
    goal_pos = random.choice(free_positions)
    
    desc[start_pos[0]][start_pos[1]] = 'S'
    desc[goal_pos[0]][goal_pos[1]] = 'G'
    
    # Convertir el mapa a una lista de strings (una por fila)
    desc_str_list = ["".join(row) for row in desc]
    
    return desc_str_list, start_pos, goal_pos

