from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt

from genetic import algoritmo_genetico
from hill_climbing import hill_climbing
from random_solver import random_search
from simulated_annealing import simulated_annealing
from view_board import vector_board

RESULTS_PATH = Path(__file__).with_name("results.csv")
IMAGES_DIR = Path(__file__).with_name("images")
MAX_STATES = 5000
DEFAULT_SEED = 0

ALGORITHM_ORDER: List[str] = ["random", "HC", "SA", "GA"]
ALGORITHM_LABELS: Dict[str, str] = {
    "random": "Random",
    "HC": "Hill Climbing",
    "SA": "Simulated Annealing",
    "GA": "Genetic Algorithm",
}
ALGORITHM_COLORS: Dict[str, str] = {
    "random": "#ffb347",
    "HC": "#6baed6",
    "SA": "#74c476",
    "GA": "#d95f02",
}

METRIC_SPECS = (
    {
        "key": "H",
        "filename": "boxplot_H.png",
        "title": "Distribución de H final por algoritmo",
        "ylabel": "Conflictos (H)",
    },
    {
        "key": "states",
        "filename": "boxplot_states.png",
        "title": "Distribución de estados explorados por algoritmo",
        "ylabel": "Estados explorados",
    },
    {
        "key": "time",
        "filename": "boxplot_time.png",
        "title": "Distribución de tiempo por algoritmo",
        "ylabel": "Tiempo (s)",
    },
)


def load_results() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    with RESULTS_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                {
                    "algorithm": row["algorithm_name"],
                    "env": int(row["env_n"]),
                    "size": int(row["size"]),
                    "solution": row["best_solution"],
                    "H": int(row["H"]),
                    "states": int(row["states"]),
                    "time": float(row["time"]),
                }
            )
    return rows


def ensure_directories() -> None:
    IMAGES_DIR.mkdir(exist_ok=True)


def generate_boxplots(records: List[Dict[str, object]]) -> None:
    sizes: List[int] = sorted({row["size"] for row in records})

    for metric in METRIC_SPECS:
        fig, axes = plt.subplots(
            1,
            len(sizes),
            figsize=(6 * len(sizes), 5),
            squeeze=False,
        )
        axes_row = axes[0]

        for idx, size in enumerate(sizes):
            ax = axes_row[idx]
            values_per_algorithm: List[List[float]] = []
            labels: List[str] = []
            colors: List[str] = []

            for algorithm in ALGORITHM_ORDER:
                values = [row[metric["key"]] for row in records if row["size"] == size and row["algorithm"] == algorithm]
                if not values:
                    continue
                values_per_algorithm.append(values)
                labels.append(ALGORITHM_LABELS[algorithm])
                colors.append(ALGORITHM_COLORS[algorithm])

            if not values_per_algorithm:
                ax.set_visible(False)
                continue

            box = ax.boxplot(values_per_algorithm, patch_artist=True)

            for patch, color in zip(box["boxes"], colors):
                patch.set(facecolor=color, alpha=0.6)
            for median in box["medians"]:
                median.set(color="#333333", linewidth=1.5)

            ax.set_title(f"Tablero {size}x{size}")
            ax.set_xticks(range(1, len(labels) + 1))
            ax.set_xticklabels(labels, rotation=20)
            ax.set_ylabel(metric["ylabel"] if idx == 0 else "")
            ax.grid(axis="y", alpha=0.25)

        fig.suptitle(metric["title"])
        fig.tight_layout(rect=(0, 0, 1, 0.95))
        output_path = IMAGES_DIR / metric["filename"]
        fig.savefig(output_path, dpi=300)
        plt.close(fig)


def run_history_for_size(size: int, seed: int) -> Dict[str, List[Tuple[int, int]]]:
    histories: Dict[str, List[Tuple[int, int]]] = {}

    history_random: List[Tuple[int, int]] = []
    random_search(size, MAX_STATES, seed=seed, history=history_random)
    histories["random"] = history_random

    board = vector_board(size, seed)
    history_hc: List[Tuple[int, int]] = []
    hill_climbing(board, MAX_STATES, history=history_hc)
    histories["HC"] = history_hc

    board = vector_board(size, seed)
    history_sa: List[Tuple[int, int]] = []
    simulated_annealing(board, MAX_STATES, seed=seed, history=history_sa)
    histories["SA"] = history_sa

    board = vector_board(size, seed)
    history_ga: List[Tuple[int, int]] = []
    algoritmo_genetico(board, MAX_STATES, seed=seed, history=history_ga)
    histories["GA"] = history_ga

    return histories


def plot_histories(size: int, histories: Dict[str, List[Tuple[int, int]]]) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))

    for algorithm in ALGORITHM_ORDER:
        history = histories.get(algorithm)
        if not history:
            continue
        states = [point[0] for point in history]
        values = [point[1] for point in history]
        ax.plot(
            states,
            values,
            label=ALGORITHM_LABELS[algorithm],
            color=ALGORITHM_COLORS[algorithm],
            linewidth=2,
        )

    ax.set_title(f"Evolución de H - Tablero {size}x{size}")
    ax.set_xlabel("Estados evaluados")
    ax.set_ylabel("Mejor H acumulado")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()

    output_path = IMAGES_DIR / f"h_evolution_size_{size}.png"
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def main() -> None:
    ensure_directories()
    records = load_results()
    if not records:
        raise SystemExit("No se encontraron datos en results.csv")

    generate_boxplots(records)

    sizes = sorted({row["size"] for row in records})
    for size in sizes:
        histories = run_history_for_size(size, DEFAULT_SEED)
        plot_histories(size, histories)

    print("Boxplots generados en", IMAGES_DIR.resolve())


if __name__ == "__main__":
    main()
