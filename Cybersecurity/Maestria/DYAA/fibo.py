# Este import es necesario para manejar número grandes en Python sin problemas de límite de dígitos que puede imprimir Python
import sys
sys.set_int_max_str_digits(10000)


#Esta es la funcion donde se calcula el n-ésimo número de Fibonacci usando la matriz de transformacion 
def fibonacci(n):
    if n == 0:
        return 0
    base_matrix = [[1, 1], [1, 0]]
    result = matrix_power_iterative(base_matrix, n)
    return result[0][1]

# Esta funcion eleva una matriz a la potencia n de manera iterativa. 
def matrix_power_iterative(matrix, n):
    result = [[1, 0], [0, 1]]  # Matriz identidad
    while n > 0:
        if n % 2 == 1:
            result = multiply_matrices(result, matrix)
        matrix = multiply_matrices(matrix, matrix)
        n //= 2
    return result
# Esta funcion multiplica dos matrices 2x2 cumpliendo con la propiedad de la multiplicacion de matrices. 
def multiply_matrices(A, B):
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0],
         A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0],
         A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]

# Esta es la parte principal del programa donde se solicita al usuario el número de Fibonacci que desea calcular. 
try:
    entrada = input("¿Qué número de Fibonacci deseas calcular (n)? ").strip()
    print(f"[DEBUG] Entrada recibida: '{entrada}'")
    n = int(entrada)
    resultado = fibonacci(n)
    print(f"\nEl número F({n}) de la secuencia de Fibonacci es:\n{resultado}")
except Exception as e:
    print(f"❌ Ocurrió un error: {e}")

