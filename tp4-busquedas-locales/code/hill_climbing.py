from view_board import vector_board, print_board

def calculate_attacks(board):
        """Calcula el número de ataques entre reinas en el tablero."""
        attacks = 0
        n = len(board)
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    attacks += 1
        return attacks
    
def hill_climbing(board, max_iterations=1000):
    n = len(board)
    current_board = board[:]
    h = calculate_attacks(current_board)
    iterations = 0

    while iterations < max_iterations:
        neighbors = []
        for col in range(n):
            for row in range(n):
                if row != current_board[col]:
                    neighbor = current_board[:]
                    neighbor[col] = row
                    neighbors.append(neighbor)

        next_board = None
        next_h = h

        for neighbor in neighbors:
            attacks = calculate_attacks(neighbor)
            if attacks < next_h:
                next_board = neighbor
                next_h = attacks

        if not next_board or next_h >= h:
            break

        current_board = next_board
        h = next_h
        
        iterations += 1

    return current_board, h

if __name__ == "__main__":
    n = 8
    seeds = [42, 7, 21, 15, 3, 10, 5, 30]  # Cambiar el índice para probar con diferentes semillas
    for seed in seeds:
        initial_board = vector_board(n, seed)
        print("Tablero inicial:")
        print(initial_board)

        solution, h = hill_climbing(initial_board)
    
        print("Solución encontrada:")
        print(solution)
        
        print("Número de ataques:")
        print(h)    
        
        print("Representación del tablero:")
        print_board(solution)