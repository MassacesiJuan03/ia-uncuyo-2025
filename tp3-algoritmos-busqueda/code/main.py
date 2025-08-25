import random
import time
import pandas as pd
import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from gymnasium import wrappers

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

def generate_envs():
    maps = []
    for i in range(30):
        maps.append(generate_random_map_custom(20,0.92))
    
    return maps
    

def run_environment(env_n, func, map):
    mapa, start, goal = map
    
    t0 = time.time()
    found, path = func(mapa, start, goal)
    t1 = time.time()
    states_n = len(path) 
    actions_count = len(path) - 1 if found else 0
    actions_cost = actions_cost_esc2(path) if found else 0
     
    results = {
        "algorithm_name": func.__name__,
        "env_n": env_n,
        "states_n": states_n,
        "actions_count": actions_count,
        "actions_cost": actions_cost,
        "time": t1 - t0,
        "solution_found": found
    }
    
    return results
    
def main():
    all_results = []
    maps = generate_envs()
    search_funcs = [bfs_search, dfs_search, uniform_cost_search, a_star_search]
    
    for func in search_funcs:
        env_n = 1
        for map in maps:
            result = run_environment(env_n, func, map)
            all_results.append(result)
            env_n += 1
        
    df = pd.DataFrame(all_results)
    df.to_csv('results.csv', index=False)
    return df
    

if __name__ == "__main__":
    #main()
    mapas = generate_envs()
    desc = mapas[0][0]
    
    nuevo_limite = 5
    env = gym.make('FrozenLake-v1', desc=desc, render_mode='ansi', is_slippery=False)
    env = wrappers.TimeLimit(env, nuevo_limite)
    
    env.reset()
    grid = env.render()
    
    print(grid)

    #found, path = bfs_search(env, mapas[0][1], mapas[0][2])


    # done = truncated = False
    # i=0
    # while not (done or truncated):
    #     action = env.action_space.sample()
    #     i+=1
    #     # Acci´on aleatoria
    #     next_state, reward, done, truncated, _ = env.step(action)
    #     grid = env.render()
    #     print(grid)
    #     print(f"Acci´on: {action}, Nuevo estado: {next_state}, Recompensa: {reward}")
    #     state = next_state
