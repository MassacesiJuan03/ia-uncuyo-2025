import random

def vector_board(n, seed=0):
    """Genera un tablero n x n con n reinas en posiciones aleatorias.
    
    Args:
        n (int): El tamaño del tablero y el número de reinas.
        seed (int): Semilla para la generación aleatoria.
    
    Returns:
        list: Una lista que representa las posiciones de las reinas en cada columna.
    """
    random.seed(seed)
    return [random.randint(0, n - 1) for _ in range(n)]

def print_board(board):
    """Imprime el tablero de n-reinas en la consola.
    
    Args:
        board (list): Una lista que representa las posiciones de las reinas en cada columna.
    """
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)
    print("\n")
    