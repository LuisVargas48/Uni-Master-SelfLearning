# PROBLEMA 1: MOCHILA (0/1 KNAPSACK)
def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    # Recuperar objetos seleccionados
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i)
            w -= weights[i - 1]

    selected.reverse()
    return dp[n][capacity], selected


# PROBLEMA 2: CORTE DE CUERDA (CUTTING ROD)
def cut_rod(prices, length):
    dp = [0] * (length + 1)
    cuts = [0] * (length + 1)

    for i in range(1, length + 1):
        max_val = float('-inf')
        for j in range(1, i + 1):
            if j <= len(prices):
                if prices[j - 1] + dp[i - j] > max_val:
                    max_val = prices[j - 1] + dp[i - j]
                    cuts[i] = j
        dp[i] = max_val

    # Reconstruir cortes
    decomposition = []
    while length > 0:
        decomposition.append(cuts[length])
        length -= cuts[length]

    return dp[-1], decomposition


# PROBLEMA 3: PARENTIZACIÓN ÓPTIMA (MATRIX CHAIN ORDER)
import sys

def matrix_chain_order(p):
    n = len(p) - 1
    m = [[0] * n for _ in range(n)]
    s = [[0] * n for _ in range(n)]

    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            m[i][j] = sys.maxsize
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    def build_solution(s, i, j):
        if i == j:
            return f"A{i + 1}"
        else:
            return f"({build_solution(s, i, s[i][j])} x {build_solution(s, s[i][j] + 1, j)})"

    return m[0][n - 1], build_solution(s, 0, n - 1)


# DATOS DEL DOCUMENTO
# Mochila
values = [79, 32, 47, 18, 26, 85, 33, 40, 45, 59]
weights = [85, 26, 48, 21, 22, 95, 43, 45, 55, 52]
capacity = 140

# Corte de cuerda
prices = [1, 4, 10, 12, 15, 20, 21, 32, 31, 41, 51]
length = 11

# Parentización
p = [5, 10, 3, 12, 5, 50, 6]

# RESULTADOS
valor_mochila, objetos_mochila = knapsack(values, weights, capacity)
precio_cuerda, cortes_cuerda = cut_rod(prices, length)
multiplicaciones, parentizacion = matrix_chain_order(p)

# MOSTRAR RESULTADOS
print("==== PROBLEMA DE LA MOCHILA ====")
print("Valor óptimo:", valor_mochila)
print("Objetos seleccionados:", objetos_mochila)

print("\n==== PROBLEMA DE CORTE DE CUERDA ====")
print("Precio máximo:", precio_cuerda)
print("Cortes óptimos:", cortes_cuerda)

print("\n==== PROBLEMA DE PARENTIZACIÓN ÓPTIMA ====")
print("Mínimo de multiplicaciones escalares:", multiplicaciones)
print("Parentización óptima:", parentizacion)
