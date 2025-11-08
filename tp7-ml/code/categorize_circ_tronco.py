"""
Crea la variable categórica `circ_tronco_cm_cat` a partir de `circ_tronco_cm` usando cortes
basados en los cuartiles (Q1,Q2,Q3) y guarda el nuevo CSV en:

  tp7-ml/data/arbolado-mendoza-dataset-circ_tronco_cm-train.csv

Etiquetas usadas: 'bajo', 'medio', 'alto', 'muy alto' (de menor a mayor).

"""
import os
import pandas as pd


def categorize_value(v, q1, q2, q3):
    if pd.isna(v):
        return pd.NA
    if v <= q1:
        return 'bajo'
    elif v <= q2:
        return 'medio'
    elif v <= q3:
        return 'alto'
    else:
        return 'muy alto'


def main():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    in_path = os.path.join(base, 'data', 'arbolado-mendoza-dataset-train.csv')
    out_path = os.path.join(base, 'data', 'arbolado-mendoza-dataset-circ_tronco_cm-train.csv')

    if not os.path.isfile(in_path):
        print(f"Archivo de entrada no encontrado: {in_path}")
        return

    df = pd.read_csv(in_path)
    # convertir a numérico
    df['circ_tronco_cm'] = pd.to_numeric(df['circ_tronco_cm'], errors='coerce')

    # calcular cuartiles (usar percentiles 25/50/75)
    q1 = df['circ_tronco_cm'].quantile(0.25)
    q2 = df['circ_tronco_cm'].quantile(0.50)
    q3 = df['circ_tronco_cm'].quantile(0.75)

    print('Puntos de corte (cuartiles):')
    print(f'Q1 (25%): {q1}')
    print(f'Q2 (50%): {q2}')
    print(f'Q3 (75%): {q3}')

    # crear columna categórica
    df['circ_tronco_cm_cat'] = df['circ_tronco_cm'].apply(lambda v: categorize_value(v, q1, q2, q3))
    # asegurar tipo categoría y orden
    df['circ_tronco_cm_cat'] = pd.Categorical(df['circ_tronco_cm_cat'], categories=['bajo','medio','alto','muy alto'], ordered=True)

    # guardar CSV
    df.to_csv(out_path, index=False)

    # mostrar conteos
    counts = df['circ_tronco_cm_cat'].value_counts(sort=False)
    print('\nConteos por categoría:')
    print(counts.to_string())
    print(f'Archivo guardado en: {out_path}')


if __name__ == '__main__':
    main()
