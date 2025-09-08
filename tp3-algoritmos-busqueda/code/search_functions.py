from collections import deque
from queue import PriorityQueue
import random
import heapq

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

    while queue:
        current = queue.popleft()
        steps += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return steps, len(path[::-1]), cost[goal]

        for move, neighbor in get_neighbors_cost(env, current):
            if neighbor not in visited:
                visited[neighbor] = current
                cost[neighbor] = cost[current] + move_cost[move]
                queue.append(neighbor)

    return steps, None, 0

def dfs(env, start, goal):
    move_cost = {'LEFT':1, 'RIGHT':1, 'UP':10, 'DOWN':10}
    stack = [start]
    visited = {start:None}
    steps = 0
    cost = {start: 0}

    while stack:
        current = stack.pop()

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return steps, len(path[::-1]), cost[goal]

        for move, neighbor in get_neighbors_cost(env, current):
            if neighbor not in visited:
                visited[neighbor] = current
                cost[neighbor] = cost[current] + move_cost[move]
                stack.append((neighbor))
        steps += 1

    return steps, None, 0

def dls(env, start, goal, limit):
    move_cost = {'LEFT':1, 'RIGHT':1, 'UP':10, 'DOWN':10}
    stack = [start]
    visited = {start:None}
    steps = 0
    cost = {start: 0}

    while steps < limit and stack:
        current = stack.pop()
        
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return steps, len(path[::-1]), cost[goal]

        for move, neighbor in get_neighbors_cost(env, current):
            if neighbor not in visited:
                visited[neighbor] = current
                cost[neighbor] = cost[current] + move_cost[move]
                stack.append(neighbor)

        steps += 1

    return steps, None, 0

def ucs(env, start, goal):
    cost_env = {'LEFT': 1, 'RIGHT': 1, 'UP': 10, 'DOWN': 10}
    pq = [(0, start)]  
    visited = {start: None}
    g_cost = {start: 0}
    steps = 0

    while pq:
        cost, current = heapq.heappop(pq)
        steps += 1  

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return steps, len(path[::-1]), g_cost[goal]

        for move, neighbor in get_neighbors_cost(env, current):
            new_cost = g_cost[current] + cost_env[move]
            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                visited[neighbor] = current
                g_cost[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))

    return steps, None, 0


def a_star1(env, start, goal):
    cost_env = {'LEFT':1, 'RIGHT':1, 'UP':1, 'DOWN':1}
    # Distancia Manhattan
    heuristic = lambda pos: (abs(pos[0]-goal[0]) + abs(pos[1]-goal[1]))

    pq = [(heuristic(start), 0, start)]
    visited = {start: None}
    g_cost = {start: 0}
    steps = 0

    while pq:
        _, g_cost_current, current = heapq.heappop(pq)
        steps += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return steps, len(path[::-1]), g_cost[goal]

        for move, neighbor in get_neighbors_cost(env, current):
            new_g_cost = g_cost_current + cost_env[move]
            if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_g_cost
                f_cost = new_g_cost + heuristic(neighbor)
                visited[neighbor] = current
                heapq.heappush(pq, (f_cost, new_g_cost, neighbor))

    return steps, None, 0

def a_star2(env, start, goal):
    cost_env = {'LEFT':1, 'RIGHT':1, 'UP':10, 'DOWN':10}
    # Distancia de Manhattan
    heuristic = lambda pos: (abs(pos[0]-goal[0])*10) + abs(pos[1]-goal[1])

    pq = [(heuristic(start), 0, start)]
    visited = {start: None}
    g_cost = {start: 0}
    steps = 0

    while pq:
        _, g_cost_current, current = heapq.heappop(pq)
        steps += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return steps, len(path[::-1]), g_cost[goal]

        for move, neighbor in get_neighbors_cost(env, current):
            new_g_cost = g_cost_current + cost_env[move]
            if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_g_cost
                f_cost = new_g_cost + heuristic(neighbor)
                visited[neighbor] = current
                heapq.heappush(pq, (f_cost, new_g_cost, neighbor))

    return steps, None, 0

def Random(env, start, goal, max_steps=1000):
    move_cost = {'LEFT':1, 'RIGHT':1, 'UP':10, 'DOWN':10}
    steps = 0
    cost = 0
    current = start
    path = [current]

    while steps < max_steps:
        if current == goal:
            return steps, len(path), cost

        neighbors = get_neighbors_cost(env, current)

        move, neighbor = random.choice(neighbors)
        cost += move_cost[move]
        current = neighbor
        path.append(current)

        steps += 1

    return steps, None, 0
