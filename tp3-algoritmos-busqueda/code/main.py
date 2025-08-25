import random
import time
import pandas as pd
from map import generate_random_map_custom
from search_functions import bfs_search, dfs_search, uniform_cost_search, a_star_search
import concurrent.futures

def actions_cost_esc2(path):
    cost = 0
    for i in range(len(path)-1):
        x1, _ = path[i]
        x2, _ = path[i+1]
        if x2 != x1:
            cost += 10
        else:
            cost += 1
    return cost

def run_env(env_n):
    mapa, start, goal = generate_random_map_custom(20, 0.92)

    #imprimir mapa
    # print(f"Environment {env_n}:")
    # for row in mapa:
    #     print(" ".join(row))
    # print(f"Start: {start}, Goal: {goal}\n")
    # print("-" * 40)
    
    # BFS
    t0 = time.time()
    found, path = bfs_search(mapa, start)
    t1 = time.time()
    states_n = len(path) 
    actions_count = len(path) - 1 if found else 0
    actions_cost = actions_cost_esc2(path) if found else 0
     
    result_bfs = {
        "algorithm_name": "BFS",
        "env_n": env_n,
        "states_n": states_n,
        "actions_count": actions_count,
        "actions_cost": actions_cost,
        "time": t1 - t0,
        "solution_found": found
    }

    # DFS
    t0 = time.time()
    found, path = dfs_search(mapa, start)
    t1 = time.time()
    states_n = len(path) 
    actions_count = len(path) - 1 if found else 0
    actions_cost = actions_cost_esc2(path) if found else 0
            
    result_dfs = {
        "algorithm_name": "DFS",
        "env_n": env_n,
        "states_n": states_n,
        "actions_count": actions_count,
        "actions_cost": actions_cost,
        "time": t1 - t0,
        "solution_found": found
    }

    # UCS
    t0 = time.time()
    found, path = uniform_cost_search(mapa, start)
    t1 = time.time()
    states_n = len(path) 
    actions_count = len(path) - 1 if found else 0
    actions_cost = actions_cost_esc2(path) if found else 0
    
    result_ucs = {
        "algorithm_name": "UCS",
        "env_n": env_n,
        "states_n": states_n,
        "actions_count": actions_count,
        "actions_cost": actions_cost,
        "time": t1 - t0,
        "solution_found": found
    }

    # A*
    t0 = time.time()
    found, path = a_star_search(mapa, start, goal)
    t1 = time.time()
    states_n = len(path) 
    actions_count = len(path) - 1 if found else 0
    actions_cost = actions_cost_esc2(path) if found else 0
    
    result_aStar = {
        "algorithm_name": "A*",
        "env_n": env_n,
        "states_n": states_n,
        "actions_count": actions_count,
        "actions_cost": actions_cost,
        "time": t1 - t0,
        "solution_found": found
    }
    
    return [result_bfs, result_dfs, result_ucs, result_aStar]

def main():
    all_results = []
    for i in range(30):
        all_results.extend(run_env(i))
 
    df = pd.DataFrame(all_results)
    df.to_csv('results.csv', index=False)
    return df
        

if __name__ == "__main__":
    main()