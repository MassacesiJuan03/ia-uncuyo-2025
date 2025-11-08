import argparse
import csv
import os
import random
import sys


def split_csv(input_path: str, train_path: str, val_path: str, val_fraction: float = 0.2, seed: int | None = None) -> tuple[int, int]:
    """Lee el CSV en input_path (preserva la primera fila como header),
    mezcla las filas de forma uniforme, separa val_fraction para validacion
    y escribe train y validation en train_path y val_path.

    Retorna (n_train, n_val).
    """
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random.Random()

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Archivo de entrada no encontrado: {input_path}")

    with open(input_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            # archivo vac\u00edo
            header = None
            rows = []
        else:
            rows = list(reader)

    n = len(rows)
    if n == 0:
        # escribir archivos vac\u00edos con header si existiera
        for path in (train_path, val_path):
            with open(path, 'w', newline='', encoding='utf-8') as out_f:
                writer = csv.writer(out_f)
                if header:
                    writer.writerow(header)
        return 0, 0

    rng.shuffle(rows)

    n_val = max(1, int(round(n * val_fraction))) if n > 0 else 0
    n_train = n - n_val
    # asegurar al menos un train cuando sea posible
    if n_train == 0 and n > 1:
        n_train = n - 1
        n_val = 1

    train_rows = rows[:n_train]
    val_rows = rows[n_train:]

    # escribir archivos
    for path, chunk in ((train_path, train_rows), (val_path, val_rows)):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', newline='', encoding='utf-8') as out_f:
            writer = csv.writer(out_f)
            if header:
                writer.writerow(header)
            writer.writerows(chunk)

    return n_train, n_val


def main():
    parser = argparse.ArgumentParser(description='Separar CSV de arbolado en train/validation (80/20).')
    parser.add_argument('--input', '-i', default='tp7-ml/data/arbolado-mza-dataset.csv',
                        help='Ruta del CSV de entrada (por defecto: tp7-ml/data/arbolado-mza-dataset.csv)')
    parser.add_argument('--train-out', default=None,
                        help='Ruta de salida para el CSV de entrenamiento (por defecto: same folder -> arbolado-mendoza-dataset-train.csv)')
    parser.add_argument('--val-out', default=None,
                        help='Ruta de salida para el CSV de validaci\u00f3n (por defecto: same folder -> arbolado-mendoza-dataset-validation.csv)')
    parser.add_argument('--seed', type=int, default=None, help='Seed opcional para reproducibilidad')
    parser.add_argument('--val-fraction', type=float, default=0.2, help='Fracci\u00f3n para validaci\u00f3n (por defecto 0.2)')

    args = parser.parse_args()

    input_path = args.input

    # comprobar existencia y carpeta
    if not os.path.isfile(input_path):
        print(f"Archivo de entrada no encontrado en '{input_path}'. Verifique la ruta.")
        sys.exit(2)

    folder = os.path.dirname(os.path.abspath(input_path))

    train_out = args.train_out or os.path.join(folder, 'arbolado-mendoza-dataset-train.csv')
    val_out = args.val_out or os.path.join(folder, 'arbolado-mendoza-dataset-validation.csv')

    try:
        n_train, n_val = split_csv(input_path, train_out, val_out, val_fraction=args.val_fraction, seed=args.seed)
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        sys.exit(1)

    print(f"Archivo de entrada: {input_path}")
    print(f"Salida train: {train_out}  ({n_train} filas)")
    print(f"Salida validation: {val_out}  ({n_val} filas)")


if __name__ == '__main__':
    main()
