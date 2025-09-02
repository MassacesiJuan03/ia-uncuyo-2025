import random
import time
import pandas as pd
import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from gymnasium import wrappers

from map import generate_random_map_custom
from search_functions import bfs, dfs, dls, ucs, a_star


def generate_envs():
    envs = []
    for i in range(30):
       desc, start , goal = generate_random_map_custom(size=100, frozen_rate=0.92, seed=i)
       env = gym.make('FrozenLake-v1', render_mode='human', desc=desc, is_slippery=False)
       envs.append((env, start, goal, i))
    return envs
    

def run_environment(func, env, limit=None):
    map, start, goal, env_n = env
    map = map.unwrapped.desc.astype(str).tolist()
    
    t0 = time.time()
    
    if func.__name__ != 'dls':
        found, path, actions_cost = func(map, start, goal)
    else:
        found, path , actions_cost = func(map, start, goal, limit)
        
    t1 = time.time()
    states_n = len(path) if found else 0
    actions_count = len(path) - 1 if found else 0

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
    envs = generate_envs()
    search_funcs = [bfs, dfs, ucs, a_star]

    for func in search_funcs:
        for env in envs:
            result = run_environment(func, env)
            all_results.append(result)
    
    limit = [50,75,100]

    for l in limit:
        for env in envs:
            result = run_environment(dls, env, limit=l)
            all_results.append(result)
            
    df = pd.DataFrame(all_results)
    df.to_csv('results.csv', index=False)
    return df
    

if __name__ == "__main__":
    main()
