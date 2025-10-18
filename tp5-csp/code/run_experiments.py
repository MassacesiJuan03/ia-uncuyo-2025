"""
Experimentos CSP para N-Reinas: Backtracking vs Forward Checking.

Ejecuta 30 repeticiones (semillas 0-29) para n=4, 8, 10 y genera CSV con resultados.
"""

import csv
import time
from pathlib import Path
from typing import List, Tuple

from backtracking import backtracking
from forward_checking import forward_checking


def run_experiment(algorithm_name: str, n: int, seed: int) -> dict:
    """Ejecuta un experimento con el algoritmo especificado."""
    start_time = time.time()
    
    if algorithm_name == 'backtracking':
        solution, nodes = backtracking(n, seed)
    elif algorithm_name == 'forward_checking':
        solution, nodes = forward_checking(n, seed)
    else:
        raise ValueError(f"Algoritmo desconocido: {algorithm_name}")
    
    exec_time = time.time() - start_time
    
    return {
        'algorithm_name': algorithm_name,
        'env_n': seed,
        'size': n,
        'best_solution': True if solution else False,
        'nodes': nodes,
        'time': exec_time
    }


def main():
    """Ejecuta experimentos y genera CSV."""
    results: List[dict] = []
    
    board_sizes = [4, 8, 10]
    seeds = range(30)
    
    algorithms = [
        ('backtracking', backtracking),
        ('forward_checking', forward_checking),
    ]
    
    total_experiments = len(board_sizes) * len(seeds) * len(algorithms)
    current = 0
    
    print(f"Ejecutando {total_experiments} experimentos...")
    print(f"Tamaños: {board_sizes}")
    print(f"Semillas: 0-29")
    print(f"Algoritmos: {[name for name, _ in algorithms]}\n")
    
    for n in board_sizes:
        for seed in seeds:
            for alg_name, alg_fn in algorithms:
                current += 1
                print(f"[{current}/{total_experiments}] {alg_name}, n={n}, seed={seed}...", end=' ')
                
                result = run_experiment(alg_name, n, seed)
                results.append(result)
                
                status = "✓" if result['best_solution'] else "✗"
                print(f"{status} (nodos: {result['nodes']}, tiempo: {result['time']:.4f}s)")

    # Guardar CSV
    output_path = Path(__file__).parent / 'tp5-Nreinas.csv'
    
    fieldnames = [
        'algorithm_name',
        'env_n',
        'size',
        'best_solution',
        'nodes',
        'time',
    ]
    
    with output_path.open('w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n✓ Resultados guardados en: {output_path}")
    print(f"  Total registros: {len(results)}")


if __name__ == '__main__':
    main()
