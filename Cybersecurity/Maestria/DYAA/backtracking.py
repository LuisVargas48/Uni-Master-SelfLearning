# Función para imprimir el tablero de Sudoku
def imprimir_sudoku(tablero):
    for fila in range(9):
        if fila % 3 == 0 and fila != 0:
            print("-" * 21)
        for col in range(9):
            if col % 3 == 0 and col != 0:
                print("|", end=" ")
            print(tablero[fila][col] if tablero[fila][col] != 0 else ".", end=" ")
        print()

# Verificar si un número puede colocarse en una posición
def es_valido(tablero, fila, col, num):
    for i in range(9):
        if tablero[fila][i] == num or tablero[i][col] == num:
            return False
    start_fila = 3 * (fila // 3)
    start_col = 3 * (col // 3)
    for i in range(start_fila, start_fila + 3):
        for j in range(start_col, start_col + 3):
            if tablero[i][j] == num:
                return False
    return True

# Algoritmo de backtracking para resolver el Sudoku
def resolver_sudoku(tablero):
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                for num in range(1, 10):
                    if es_valido(tablero, fila, col, num):
                        tablero[fila][col] = num
                        if resolver_sudoku(tablero):
                            return True
                        tablero[fila][col] = 0
                return False
    return True

# Sudoku 1 (Imagen 1)
sudoku_1 = [
    [5, 0, 0, 9, 1, 3, 7, 2, 0],
    [3, 0, 0, 0, 8, 0, 5, 0, 9],
    [0, 9, 0, 2, 0, 5, 0, 8, 0],
    [6, 8, 0, 4, 7, 0, 2, 3, 0],
    [0, 0, 9, 5, 0, 0, 4, 6, 0],
    [7, 0, 4, 0, 0, 0, 0, 0, 5],
    [0, 2, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 8, 9, 1, 6, 0, 0],
    [8, 5, 0, 7, 2, 0, 0, 0, 3]
]

# Sudoku 2 (Imagen 2 corregido)
sudoku_2 = [
    [6, 9, 0, 0, 0, 0, 7, 0, 0],
    [0, 0, 0, 0, 9, 6, 0, 0, 0],
    [0, 8, 0, 7, 5, 3, 0, 9, 0],
    [0, 2, 0, 3, 7, 4, 5, 6, 1],
    [3, 6, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 9, 6, 0, 3, 7, 8],
    [0, 0, 6, 0, 3, 1, 0, 8, 4],
    [0, 4, 5, 8, 0, 7, 6, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 7]
]

# Resolver y mostrar Sudoku 1
print("Sudoku 1 - Original:")
imprimir_sudoku(sudoku_1)
if resolver_sudoku(sudoku_1):
    print("\nSudoku 1 - Resuelto:")
    imprimir_sudoku(sudoku_1)
else:
    print("No se pudo resolver Sudoku 1.")

# Resolver y mostrar Sudoku 2
print("\n" + "="*40 + "\n")
print("Sudoku 2 - Original:")
imprimir_sudoku(sudoku_2)
if resolver_sudoku(sudoku_2):
    print("\nSudoku 2 - Resuelto:")
    imprimir_sudoku(sudoku_2)
else:
    print("No se pudo resolver Sudoku 2.")

