from collections import deque
from queue import PriorityQueue

def get_neighbors(map, position):
    x, y = position
    neighbors = []
    
    # Arriba
    if x-1 >= 0 and map[x-1][y] != "H":
        neighbors.append((x-1, y))
            
    # Abajo
    if x+1 < len(map) and map[x+1][y] != "H":
        neighbors.append((x+1, y))
    
    # Izquierda    
    if y-1 >= 0 and map[x][y-1] != "H":
        neighbors.append((x, y-1))
    
    # Derecha   
    if y+1 < len(map) and map[x][y+1] != "H":
        neighbors.append((x, y+1))
        
    return neighbors

def bfs_search(map, start, max_lifetime=1000):
    queue = deque([(start, [])])  
    visited = set()
    
    Lifetime = 0
    while queue:
        current, path = queue.popleft()
        
        Lifetime += 1
        if Lifetime >= max_lifetime:
            return False, path
        
        if map[current[0]][current[1]] == "G":
            return True, path + [current]
        
        for neighbor in get_neighbors(map, current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [current]))
    
    return False, path

def dfs_search(map, start, max_lifetime=1000):
    stack = [(start, [])]
    visited = set()
    
    Lifetime = 0
    while stack:
        current, path = stack.pop()
        
        Lifetime += 1
        if Lifetime >= max_lifetime:
            return False, path
        
        if map[current[0]][current[1]] == "G":
            return True, path + [current]
        
        for neighbor in get_neighbors(map, current):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [current]))
                
    return False, path

def dfs_search_limited(map, start, limit):
    stack = [(start, [], 0)]  
    visited = set()
    
    while stack:
        current, path, depth = stack.pop()
        
        if map[current[0]][current[1]] == "G":
            return True, path + [current]
        
        if depth < limit:
            for neighbor in get_neighbors(map, current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [current], depth + 1))
    
    return False, path

def uniform_cost_search(map, start, max_lifetime=1000):
    pq = PriorityQueue()
    pq.put((0, start, []))  
    visited = set()
    
    Lifetime = 0
    while not pq.empty():
        cost, current, path = pq.get()
        
        Lifetime += 1
        if Lifetime >= max_lifetime:
            return False, path
        
        if map[current[0]][current[1]] == "G":
            return True, path + [current]
        
        for neighbor in get_neighbors(map, current):
            if neighbor not in visited:
                visited.add(neighbor)
                pq.put((cost + 1, neighbor, path + [current]))
    
    return False, path

def a_star_search(map, start, goal, max_lifetime=1000):
    # Distancia de Manhattan
    heuristic = lambda pos: abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])
    
    pq = PriorityQueue()
    pq.put((heuristic(start), 0, start, []))
    visited = set()
    
    Lifetime = 0
    while not pq.empty():
        _, g_cost, current, path = pq.get()
        
        visited.add(current)
        
        Lifetime += 1
        if Lifetime >= max_lifetime:
            return False, path
        
        if map[current[0]][current[1]] == "G":
            return True, path + [current]
        
        for neighbor in get_neighbors(map, current):
            if neighbor not in visited:
                new_g_cost = g_cost + 1
                new_f_cost = new_g_cost + heuristic(neighbor)
                pq.put((new_f_cost, new_g_cost, neighbor, path + [current]))
    
    return False, path