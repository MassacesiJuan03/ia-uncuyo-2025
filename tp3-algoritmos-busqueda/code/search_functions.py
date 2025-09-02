from collections import deque
from queue import PriorityQueue
import random

def get_neighbors_cost(env, position):
    x, y = position
    moves = {'LEFT':(0,-1), 'RIGHT':(0,1), 'UP':(-1,0), 'DOWN':(1,0)}
    neighbors = []
    
    for move, (dx, dy) in moves.items():
        if 0 <= x + dx < len(env) and 0 <= y + dy < len(env[0]):
            if env[x + dx][y + dy] != "H":
                neighbors.append((move, (x + dx, y + dy)))           
    return neighbors

def bfs(env, start, goal):
    move_cost = {'LEFT':1, 'RIGHT':1, 'UP':10, 'DOWN':10}
    queue = deque([start])  
    visited = {start: None}
    cost = {start: 0}
    steps = 0

    while steps < 1000:
        current = queue.popleft()
        steps += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return True, path[::-1], cost[goal]

        for move, neighbor in get_neighbors_cost(env, current):
            if neighbor not in visited:
                visited[neighbor] = current
                cost[neighbor] = cost[current] + move_cost[move]
                queue.append(neighbor)

    return False, [], 0

def dfs(env, start, goal):
    move_cost = {'LEFT':1, 'RIGHT':1, 'UP':10, 'DOWN':10}
    stack = [start]
    visited = {start:None}
    steps = 0
    cost = {start: 0}

    while steps < 1000:
        current = stack.pop()
        steps += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return True, path[::-1], cost[goal]

        for move, neighbor in get_neighbors_cost(env, current):
            if neighbor not in visited:
                visited[neighbor] = current
                cost[neighbor] = cost[current] + move_cost[move]
                stack.append((neighbor))

    return False, [], 0

def dls(env, start, goal, limit):
    move_cost = {'LEFT':1, 'RIGHT':1, 'UP':10, 'DOWN':10}
    stack = [start]
    visited = {start:None}
    steps = 0
    cost = {start: 0}

    while steps < limit:
        current = stack.pop()
        steps += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return True, path[::-1], cost[goal]

        for move, neighbor in get_neighbors_cost(env, current):
            if neighbor not in visited:
                visited[neighbor] = current
                cost[neighbor] = cost[current] + move_cost[move]
                stack.append(neighbor)

    return False, [], 0

def ucs(env, start, goal):
    cost_env = {'LEFT':1, 'RIGHT':1, 'UP':10, 'DOWN':10}
    pq = PriorityQueue()
    pq.put((0, start))
    visited = {start: None}
    g_cost = {start:0}
    steps = 0

    while not pq.empty() and steps < 1000:
        cost, current = pq.get()
        steps += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return True, path[::-1], g_cost[goal]

        for move, neighbor in get_neighbors_cost(env, current):
            new_cost = g_cost[current] + cost_env[move]
            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                visited[neighbor] = current
                g_cost[neighbor] = new_cost
                pq.put((new_cost, neighbor))

    return False, [], 0

def a_star(env, start, goal):
    cost_env = {'LEFT':1, 'RIGHT':1, 'UP':10, 'DOWN':10}
    # Distancia de Manhattan
    heuristic = lambda pos: (abs(pos[0]-goal[0])*10) + abs(pos[1]-goal[1])

    pq = PriorityQueue()
    pq.put((heuristic(start), 0, start))
    visited = {start: None}
    g_cost = {start: 0}
    steps = 0

    while not pq.empty() and steps < 1000:
        _, g_cost_current, current = pq.get()
        steps += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return True, path[::-1], g_cost[goal]

        for move, neighbor in get_neighbors_cost(env, current):
            new_g_cost = g_cost_current + cost_env[move]
            if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_g_cost
                f_cost = new_g_cost + heuristic(neighbor)
                visited[neighbor] = current
                pq.put((f_cost, new_g_cost, neighbor))

    return False, [], 0

def random_search(env, start, goal):
    move_cost = {'LEFT':1, 'RIGHT':1, 'UP':10, 'DOWN':10}
    visited = {start: None}
    cost = {start: 0}
    steps = 0
    current = start

    while steps < 1000:
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return True, path[::-1], cost[goal]

        neighbors = get_neighbors_cost(env, current)
        if not neighbors:
            break

        move, neighbor = random.choice(neighbors)
        visited[neighbor] = current
        cost[neighbor] = cost[current] + move_cost[move]
        current = neighbor
        
        steps += 1
    return False, [], 0