import random
import time
import pandas as pd
import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from gymnasium import wrappers
import matplotlib.pyplot as plt

from map import generate_random_map_custom
from search_functions import bfs, dfs, dls, ucs, a_star1, a_star2

seeds = [384927102, 123456789, 987654321, 192837465, 564738291, 1029384756, 6758493021, 9182736450, 5647382910, 1231231230,
         3213213210, 4564564560, 6546546540, 7897897890, 9879879870, 1472583690, 9638527410, 2583691470, 3692581470, 7418529630,
         1593572580, 7531594560, 8524561230, 9513572580, 3571594560, 4561237890, 1237894560, 7894561230, 4567891230, 3216549870]

def generate_envs():
    envs = []
    for i in range(30): 
       desc, start , goal = generate_random_map_custom(size=100, frozen_rate=0.92, seed=seeds[i])
       env = gym.make('FrozenLake-v1', render_mode='human', desc=desc, is_slippery=False)
       envs.append((env, start, goal, seeds[i]))
    return envs
    

def run_environment(func, env, escenario, limit=None):
    map, start, goal, env_n = env
    map = map.unwrapped.desc.astype(str).tolist()
    
    t0 = time.time()
    
    if func.__name__ != 'dls':
        explored, path, actions_cost = func(map, start, goal)
    else:
        explored, path, actions_cost = func(map, start, goal, limit)

    t1 = time.time()
    actions_count = path if path else 0

    results = {
        "algorithm_name": func.__name__.upper() + (f"_{limit}" if limit else ""),
        "escenario": escenario,
        "env_n": env_n,
        "states_n": explored,
        "actions_count": actions_count,
        "actions_cost": actions_cost if escenario == "2" else actions_count,
        "time": t1 - t0,
        "solution_found": True if actions_count > 0 else False
    }
    
    return results
    
def main():
    all_results = []
    envs = generate_envs()
    search_funcs_escenario1 = [bfs, dfs, ucs, a_star1]
    search_funcs_escenario2 = [bfs, dfs, ucs, a_star2]

    # Escenario 1
    for func in search_funcs_escenario1:
        for env in envs:
            result = run_environment(func, env, escenario="1")
            all_results.append(result)
    
    # Escenario 2
    for func in search_funcs_escenario2:
        for env in envs:
            result = run_environment(func, env, escenario="2")
            all_results.append(result)
            
    limit = [50,75,100]
    for l in limit:
        for env in envs:
            result1 = run_environment(dls, env, escenario="1", limit=l)
            result2 = run_environment(dls, env, escenario="2", limit=l)
            all_results.append(result1)
            all_results.append(result2)


    df = pd.DataFrame(all_results)
    df.to_csv('results.csv', index=False)
    return df
    

if __name__ == "__main__":
    main()

