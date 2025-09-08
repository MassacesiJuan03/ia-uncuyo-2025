import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# === 1. Cargar CSV ===
df = pd.read_csv("results.csv")
df.columns = df.columns.str.strip()  # limpiar espacios por si acaso

# === 2. Definir métricas ===
metrics = ["states_n", "actions_count", "actions_cost", "time"]

# Paleta de colores para escenarios
palette = {
    1: "skyblue",
    2: "orange"
}

# === 3. Graficar por cada métrica ===
for metric in metrics:
    plt.figure(figsize=(12, 6))

    ax = sns.boxplot(
        data=df,
        x="algorithm_name",
        y=metric,
        hue="escenario",   # ← usamos directamente la columna escenario
        palette=palette,
        showmeans=True,
        meanprops={"marker":"o", "markerfacecolor":"red", "markeredgecolor":"black"}
    )

    sns.stripplot(
        data=df,
        x="algorithm_name",
        y=metric,
        hue="escenario",
        dodge=True,
        color=".25",
        size=2,
        jitter=True
    )

    # 🔑 Limpiar leyenda (solo escenarios con color)
    handles, labels = ax.get_legend_handles_labels()
    # Crea el handle para la media
    mean_handle = Line2D([], [], color='red', marker='o', linestyle='None', label='Media')
    # Agrega el handle de la media a los handles de escenarios
    ax.legend(handles[:2] + [mean_handle], labels[:2] + ['Media'], title="Escenarios", loc="upper right")

    if metric == "time":
        plt.title(f"Distribución de tiempo por algoritmo y escenario")
        plt.ylabel("Tiempo (segundos)")
    elif metric == "states_n":
        plt.title(f"Distribución de estados explorados por algoritmo y escenario")
        plt.ylabel("Número de estados explorados")
    elif metric == "actions_count":
        plt.title(f"Distribución de cantidad de acciones por algoritmo y escenario")
        plt.ylabel("Cantidad de acciones")
    elif metric == "actions_cost":
        plt.title(f"Distribución de costo de acciones por algoritmo y escenario")
        plt.ylabel("Costo de acciones")
        
    plt.scatter([], [], c="red", marker="o", label="Media")
    
    plt.xlabel("Algoritmo")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.tight_layout()

    filename = f"boxplot_{metric}.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
