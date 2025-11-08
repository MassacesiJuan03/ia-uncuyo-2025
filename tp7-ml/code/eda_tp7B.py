import os
import textwrap
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def plot_inclinacion_distribution(df: pd.DataFrame, out_path: str):
    counts = df['inclinacion_peligrosa'].value_counts().sort_index()
    labels = ['No peligrosa (0)', 'Peligrosa (1)']
    fig, ax = plt.subplots(figsize=(6, 5))
    # usar colormap Purples degradando de más oscuro a más claro
    n = len(counts)
    cmap = plt.cm.Purples
    colors = [cmap(v) for v in np.linspace(0.85, 0.35, n)]
    counts.plot(kind='bar', color=colors, ax=ax)
    ax.set_title('Distribución de \"inclinacion_peligrosa\"')
    ax.set_xlabel('Clase')
    ax.set_ylabel('Cantidad de árboles')
    for p in ax.patches:
        ax.annotate(int(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom')
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_section_risk(df: pd.DataFrame, out_path: str, min_count: int | None = 30, top_n: int | None = 10):
    # agrupar por nombre de la sección para mostrar nombres en el eje x
    # (la columna 'seccion' en el CSV parece ser un id numérico)
    gp = df.groupby('nombre_seccion').agg(total=('id', 'count'), mean_risk=('inclinacion_peligrosa', 'mean'))
    # aplicar filtro por tamaño si se indicó
    if min_count is not None and min_count > 0:
        gp = gp[gp['total'] >= min_count]
    gp = gp.sort_values('mean_risk', ascending=False)
    # limitar a top_n si se indicó
    if top_n is not None and top_n > 0:
        gp = gp.head(top_n)
    # ajustar figura más ancha si hay muchas categorías
    n = len(gp)
    width = max(10, int(n * 0.6))
    fig, ax = plt.subplots(figsize=(width, 6))
    # usar colormap Reds degradando de más oscuro a más claro
    ncols = max(1, len(gp))
    cmap = plt.cm.Reds
    colors = [cmap(v) for v in np.linspace(0.85, 0.35, ncols)]
    gp['mean_risk'].plot(kind='bar', color=colors, ax=ax)
    # construir título sin mostrar 'None' cuando los parámetros son None
    if top_n is None and min_count is None:
        title = 'Secciones por proporción de inclinación peligrosa (todas)'
    elif top_n is None:
        title = f'Secciones por proporción de inclinación peligrosa (mín {min_count} árboles)'
    elif min_count is None:
        title = f'Top {top_n} secciones por proporción de inclinación peligrosa'
    else:
        title = f'Top {top_n} secciones por proporción de inclinación peligrosa (mín {min_count} árboles)'
    ax.set_title(title)
    ax.set_xlabel('Sección (nombre)')
    ax.set_ylabel('Proporción de árboles peligrosos')
    # ajustar el eje y a la ventana de los datos (más pequeña) para apreciar diferencias
    min_r = gp['mean_risk'].min()
    max_r = gp['mean_risk'].max()
    delta = max_r - min_r
    margin = max(0.01, delta * 0.2)
    ymin = max(0.0, min_r - margin)
    ymax = min(1.0, max_r + margin)
    ax.set_ylim(ymin, ymax)
    # rotar etiquetas para que se lean mejor
    ax.set_xticklabels(gp.index, rotation=45, ha='right')
    # mejorar separación de labels cuando hay muchas
    fig.tight_layout()
    for i, (idx, row) in enumerate(gp.iterrows()):
        ax.annotate(f"{row['mean_risk']:.2%}\n(n={int(row['total'])})",
                    (i, row['mean_risk']), ha='center', va='bottom', fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_species_risk(df: pd.DataFrame, out_path: str, min_count: int | None = 20, top_n: int | None = 10,
                     species_from: str | None = None, species_to: str | None = None):
    gp = df.groupby('especie').agg(total=('id', 'count'), mean_risk=('inclinacion_peligrosa', 'mean'))
    # aplicar filtro por tamaño si se indicó
    if min_count is not None and min_count > 0:
        gp = gp[gp['total'] >= min_count]
    gp = gp.sort_values('mean_risk', ascending=False)
    # si se indicó un rango por nombre de especie, tomar la porción en el orden actual
    if species_from or species_to:
        names = list(gp.index)
        try:
            start = names.index(species_from) if species_from in names else 0
        except ValueError:
            start = 0
        try:
            end = names.index(species_to) if species_to in names else len(names) - 1
        except ValueError:
            end = len(names) - 1
        if start <= end:
            gp = gp[start:end+1]
        else:
            gp = gp[end:start+1]
    else:
        if top_n is not None and top_n > 0:
            gp = gp.head(top_n)
    # ajustar figura más ancha si hay muchas especies
    n = len(gp)
    width = max(10, int(n * 0.6))
    fig, ax = plt.subplots(figsize=(width, 6))
    # usar colormap Greens degradando de más oscuro a más claro
    ncols = max(1, len(gp))
    cmap = plt.cm.Greens
    colors = [cmap(v) for v in np.linspace(0.85, 0.35, ncols)]
    gp['mean_risk'].plot(kind='bar', color=colors, ax=ax)
    # construir título sin mostrar 'None' cuando los parámetros son None
    if top_n is None and min_count is None and not (species_from or species_to):
        title = 'Especies por proporción de inclinación peligrosa (todas)'
    elif species_from or species_to:
        title = f'Especies por proporción de inclinación peligrosa ({species_from} → {species_to})'
    elif top_n is None:
        title = f'Especies por proporción de inclinación peligrosa (mín {min_count} árboles)'
    elif min_count is None:
        title = f'Top {top_n} especies por proporción de inclinación peligrosa'
    else:
        title = f'Top {top_n} especies por proporción de inclinación peligrosa (mín {min_count} árboles)'
    ax.set_title(title)
    ax.set_xlabel('Especie')
    ax.set_ylabel('Proporción de árboles peligrosos')
    # ajustar el eje y a la ventana de los datos (más pequeña) para apreciar diferencias
    min_r = gp['mean_risk'].min()
    max_r = gp['mean_risk'].max()
    delta = max_r - min_r
    margin = max(0.01, delta * 0.2)
    ymin = max(0.0, min_r - margin)
    ymax = min(1.0, max_r + margin)
    ax.set_ylim(ymin, ymax)
    # rotar etiquetas para que se lean mejor
    ax.set_xticklabels(gp.index, rotation=45, ha='right')
    fig.tight_layout()
    for i, (idx, row) in enumerate(gp.iterrows()):
        ax.annotate(f"{row['mean_risk']:.2%}\n(n={int(row['total'])})", (i, row['mean_risk']),
                    ha='center', va='bottom', fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_path = os.path.join(base, 'data', 'arbolado-mendoza-dataset-train.csv')
    images_dir = os.path.join(base, 'images')
    ensure_dir(images_dir)

    if not os.path.isfile(data_path):
        print(f"Archivo de entrenamiento no encontrado: {data_path}")
        return

    df = pd.read_csv(data_path, dtype={'inclinacion_peligrosa': 'Int64'})

    # Asegurar que la columna de interés exista y esté en 0/1
    if 'inclinacion_peligrosa' not in df.columns:
        print('La columna "inclinacion_peligrosa" no se encuentra en el CSV.')
        return

    # Gráfica 1: distribución general
    out1 = os.path.join(images_dir, 'inclinacion_distribution.png')
    plot_inclinacion_distribution(df, out1)

    # Gráfica 2: secciones con mayor proporción (filtrar por tamaño)
    out2 = os.path.join(images_dir, 'seccion_risk_all.png')
    # mostrar todas las secciones (sin filtrar ni limitar)
    plot_section_risk(df, out2, min_count=None, top_n=None)

    # Gráfica 3: especies con mayor proporción (filtrar por tamaño)
    out3 = os.path.join(images_dir, 'especie_risk_all.png')
    # mostrar todas las especies (sin filtrar ni limitar)
    plot_species_risk(df, out3, min_count=None, top_n=None)

    # gráfico específico: desde 'Algarrobo' hasta 'lamo blanco' según el orden por riesgo
    out4 = os.path.join(images_dir, 'especie_risk_algarrobo_to_lamoblanco.png')
    plot_species_risk(df, out4, min_count=None, top_n=None, species_from='Algarrobo', species_to='lamo blanco')

    print('Gráficas generadas:')
    print(' -', out1)
    print(' -', out2)
    print(' -', out3)
    print(' -', out4)


if __name__ == '__main__':
    main()
