import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. Configuración del Universo de Discurso
# ==========================================
puntos_entrada = np.linspace(0, 100, 100)
X1, X2 = np.meshgrid(puntos_entrada, puntos_entrada)

# ==========================================
# 2. Funciones de Pertenencia (Gaussianas)
# ==========================================
# Parámetros para Entrada 1 (Vulnerabilidad): [centro, ancho]
params_x1 = {'Baja': [20, 15], 'Media': [50, 15], 'Alta': [80, 15]}
# Parámetros para Entrada 2 (Amenaza): [centro, ancho]
params_x2 = {'Baja': [20, 15], 'Media': [50, 15], 'Alta': [80, 15]}

def gausiana(x, centro, ancho):
    return np.exp(-((x - centro)**2) / (2 * ancho**2))

# ==========================================
# 3. Definición de Reglas TS-1 (Polinomios)
# ==========================================
# Cada regla tiene coeficientes [p, q, r] para: z = p*x1 + q*x2 + r
# 3 funciones x 3 funciones = 9 reglas combinatorias
reglas_coeficientes = {
    ('Baja', 'Baja'):    [0.1, 0.1, 5],    # Riesgo mínimo
    ('Baja', 'Media'):   [0.15, 0.25, 15],
    ('Baja', 'Alta'):    [0.2, 0.45, 30],
    ('Media', 'Baja'):   [0.25, 0.15, 15],
    ('Media', 'Media'):  [0.4, 0.4, 25],   # Punto medio equilibrado
    ('Media', 'Alta'):   [0.35, 0.55, 45],
    ('Alta', 'Baja'):    [0.45, 0.2, 30],
    ('Alta', 'Media'):   [0.55, 0.35, 55],
    ('Alta', 'Alta'):    [0.75, 0.75, 50]  # Riesgo crítico máximo
}

# ==========================================
# 4. Motor de Inferencia Takagi-Sugeno
# ==========================================
def inferencia_ts1(x1_grid, x2_grid):
    num_puntos = x1_grid.shape[0]
    Z_output = np.zeros_like(x1_grid)
    
    # Evaluamos cada punto de la malla tridimensional
    for i in range(num_puntos):
        for j in range(num_puntos):
            v_x1 = x1_grid[i, j]
            v_x2 = x2_grid[i, j]
            
            suma_pesos = 0.0
            suma_ponderada = 0.0
            
            # Procesamiento de las 9 combinaciones de reglas
            for (label_1, p_1), (label_2, p_2) in [((l1, params_x1[l1]), (l2, params_x2[l2])) for l1 in params_x1 for l2 in params_x2]:
                # Fuzzificación de los antecedentes
                mu_1 = gausiana(v_x1, p_1[0], p_1[1])
                mu_2 = gausiana(v_x2, p_2[0], p_2[1])
                
                # Conjunción Difusa (Operador AND mediante Producto T-Norma)
                w_regla = mu_1 * mu_2
                
                # Evaluación del consecuente polinomial de Orden 1
                p, q, r = reglas_coeficientes[(label_1, label_2)]
                z_consecuente = p * v_x1 + q * v_x2 + r
                
                suma_pesos += w_regla
                suma_ponderada += w_regla * z_consecuente
                
            # Defuzzificación por promedio ponderado de áreas
            Z_output[i, j] = suma_ponderada / (suma_pesos + 1e-10)
            
    return Z_output

# Calculamos la superficie tridimensional de salida
Z = inferencia_ts1(X1, X2)

# ==========================================
# 5. Visualización Exigida por la Rúbrica
# ==========================================
fig = plt.figure(figsize=(18, 5))

# --- Gráfica 1: Conjuntos Difusos de Entrada 1 ---
ax1 = fig.add_subplot(131)
for etiqueta, params in params_x1.items():
    ax1.plot(puntos_entrada, gausiana(puntos_entrada, params[0], params[1]), label=etiqueta)
ax1.set_title('Entrada 1: Nivel de Vulnerabilidad del Sistema')
ax1.set_xlabel('Universo de Discurso X1 (%)')
ax1.set_ylabel('Grado de Pertenencia ($\mu$)')
ax1.grid(True)
ax1.legend()

# --- Gráfica 2: Conjuntos Difusos de Entrada 2 ---
ax2 = fig.add_subplot(132)
for etiqueta, params in params_x2.items():
    ax2.plot(puntos_entrada, gausiana(puntos_entrada, params[0], params[1]), label=etiqueta)
ax2.set_title('Entrada 2: Nivel de Amenaza del Entorno')
ax2.set_xlabel('Universo de Discurso X2 (%)')
ax2.set_ylabel('Grado de Pertenencia ($\mu$)')
ax2.grid(True)
ax2.legend()

# --- Gráfica 3: Superficie de Control Tridimensional (Salida) ---
ax3 = fig.add_subplot(133, projection='3d')
superficie = ax3.plot_surface(X1, X2, Z, cmap='viridis', edgecolor='none', alpha=0.9)
ax3.set_title('Salida del Sistema: Evaluación de Riesgo Total')
ax3.set_xlabel('Vulnerabilidad (X1)')
ax3.set_ylabel('Amenaza (X2)')
ax3.set_zlabel('Riesgo Calculado (Z)')
fig.colorbar(superficie, ax=ax3, shrink=0.5, aspect=5)

plt.tight_layout()
plt.show()