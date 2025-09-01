from search_functions import bfs, dfs, ucs, a_star
from main import generate_envs

def view_env(env, path):
    env.reset()
    # Mostrar el camino en la UI
    if path:
        for step, pos in enumerate(path):
            # Actualizar la posición manualmente usando env.unwrapped.s
            env.unwrapped.s = pos[0] * env.unwrapped.ncol + pos[1]
            env.render()
    else:
        print("No hay camino encontrado")

if __name__ == "__main__":
    envs = generate_envs()

    for env, start, goal, _ in envs:
        desc = env.unwrapped.desc.astype(str).tolist()
        
        print("BFS")
        _, path_bfs, _ = bfs(desc, start, goal)
        view_env(env, path_bfs)

        print("DFS")
        _, path_dfs, _ = dfs(desc, start, goal)
        view_env(env, path_dfs)

        print("Uniform Cost Search")
        _, path_ucs, _ = ucs(desc, start, goal)
        view_env(env, path_ucs)

        print("A* Search")
        _, path_a_star, _ = a_star(desc, start, goal)
        view_env(env, path_a_star)
        
    env.close()