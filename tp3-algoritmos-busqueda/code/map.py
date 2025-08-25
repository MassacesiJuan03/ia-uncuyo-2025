import math
import random
import gymnasium as gym

def generate_random_map_custom(size: int, frozen_rate: float) -> tuple:
    map = [["F"] * size for _ in range(size)]
    
    hole_cells =  math.ceil(size * size * (1 - frozen_rate))
    #print(f"Hole cells: {hole_cells}")
    
    for _ in range(hole_cells):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        map[x][y] = "H"
    
    while True:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if map[x][y] == "F":
            map[x][y] = "S"
            start = (x, y)
            break    
        
    while True:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if map[x][y] == "F":
            map[x][y] = "G"
            goal = (x, y)
            break
    
    return (map, start, goal)
    
    