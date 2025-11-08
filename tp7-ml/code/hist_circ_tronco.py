import os
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # convertir circ_tronco_cm a numérico, eliminar NaN
    df['circ_tronco_cm'] = pd.to_numeric(df['circ_tronco_cm'], errors='coerce')
    df = df.dropna(subset=['circ_tronco_cm'])
    return df


def plot_bins_comparison(values: pd.Series, bins_list: List[int], out_path: str):
    n = len(bins_list)
    cols = min(3, n)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = np.array(axes).reshape(-1)

    for i, b in enumerate(bins_list):
        ax = axes[i]
        ax.hist(values, bins=b, color=plt.cm.Blues(0.6), edgecolor='black')
        ax.set_title(f'Bins = {b}')
        ax.set_xlabel('circ_tronco_cm')
        ax.set_ylabel('Frecuencia')

    # ocultar ejes extras
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_by_inclinacion(df: pd.DataFrame, bins_list: List[int], out_path: str):
    # creamos una figura por cada número de bins, con ambos histogramas superpuestos
    figs = []
    for b in bins_list:
        fig, ax = plt.subplots(figsize=(8, 5))
        vals0 = df.loc[df['inclinacion_peligrosa'] == 0, 'circ_tronco_cm']
        vals1 = df.loc[df['inclinacion_peligrosa'] == 1, 'circ_tronco_cm']

        ax.hist(vals0, bins=b, alpha=0.6, label='No peligrosa (0)', color=plt.cm.Greens(0.6), edgecolor='black')
        ax.hist(vals1, bins=b, alpha=0.6, label='Peligrosa (1)', color=plt.cm.Reds(0.6), edgecolor='black')
        ax.set_title(f'circ_tronco_cm por inclinacion_peligrosa (bins={b})')
        ax.set_xlabel('circ_tronco_cm')
        ax.set_ylabel('Frecuencia')
        ax.legend()
        fig.tight_layout()
        figs.append((b, fig))

    # guarda todas las figuras en una sola imagen combinada verticalmente
    # para simplicidad, guardamos cada figura por separado con sufijo
    base, ext = os.path.splitext(out_path)
    for b, fig in figs:
        outp = f"{base}_bins{b}{ext}"
        fig.savefig(outp)
        plt.close(fig)


def main():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_path = os.path.join(base, 'data', 'arbolado-mendoza-dataset-train.csv')
    images_dir = os.path.join(base, 'images')
    ensure_dir(images_dir)

    if not os.path.isfile(data_path):
        print(f"Archivo no encontrado: {data_path}")
        return

    df = load_data(data_path)
    values = df['circ_tronco_cm']

    # bins solicitados: 10, 25, 50
    bins_list = [10, 25, 50]

    out1 = os.path.join(images_dir, 'circ_tronco_hist_bins.png')
    plot_bins_comparison(values, bins_list, out1)

    out2 = os.path.join(images_dir, 'circ_tronco_hist_by_inclinacion.png')
    plot_by_inclinacion(df, bins_list, out2)

    print('Histogramas generados:')
    print(' -', out1)
    # indica cada archivo por bins creado
    for b in bins_list:
        print(f' - {os.path.splitext(out2)[0]}_bins{b}{os.path.splitext(out2)[1]}')


if __name__ == '__main__':
    main()
