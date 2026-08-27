import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. Definición del Universo de Discurso y Superficie Objetivo
# ==========================================
puntos = np.linspace(0, 10, 20)  # Rejilla de 20x20 ideal para renderizado fluido en tiempo real
X1, X2 = np.meshgrid(puntos, puntos)
# Superficie de referencia deseada (Z*) No Lineal
Z_deseada = 5 * np.sin(X1 / 2) * np.cos(X2 / 2) + X1 + X2

NUM_REGLAS = 9
NUM_GENES = 39

# ==========================================
# 2. Arquitectura de la Red Neuro-Difusa Takagi-Sugeno Orden 1
# ==========================================
def calcular_superficie_ts1(cromosoma, X1, X2):
    # Desempaquetado exacto de los 39 genes según la especificación del proyecto
    mu_x1 = cromosoma[0:3]
    mu_x2 = cromosoma[3:6]
    sig_x1 = cromosoma[6:9]
    sig_x2 = cromosoma[9:12]
    
    p = cromosoma[12:21]
    q = cromosoma[21:30]
    r = cromosoma[30:39]
    
    Z_fuzzy = np.zeros_like(X1)
    Suma_W = np.zeros_like(X1) + 1e-10
    
    # Combinatoria de las 9 reglas de inferencia (3x3)
    regla_idx = 0
    for i in range(3):
        for j in range(3):
            # Fuzzificación de antecedentes mediante Gaussianas
            w_x1 = np.exp(-((X1 - mu_x1[i])**2) / (2 * sig_x1[i]**2))
            w_x2 = np.exp(-((X2 - mu_x2[j])**2) / (2 * sig_x2[j]**2))
            
            # Conjunción mediante operador Producto (T-Norma)
            w_regla = w_x1 * w_x2
            
            # Consecuente polinomial de Orden 1: z = p*x1 + q*x2 + r
            z_consecuente = p[regla_idx] * X1 + q[regla_idx] * X2 + r[regla_idx]
            
            Z_fuzzy += w_regla * z_consecuente
            Suma_W += w_regla
            regla_idx += 1
            
    return Z_fuzzy / Suma_W

def evaluar_cromosoma(cromosoma, X1, X2, Z_target): #se calcula el error absoluto
    Z_gen = calcular_superficie_ts1(cromosoma, X1, X2)
    # Rúbrica exige sumatoria del error absoluto (MAE)
    error_absoluto = np.sum(np.abs(Z_target - Z_gen))
    fitness = 1 / (error_absoluto + 1e-6)
    return fitness, error_absoluto, Z_gen

# ==========================================
# 3. Operadores Genéticos Adaptativos con Límites Físicos
# ==========================================
def aplicar_limites(ind):
    ind[0:6] = np.clip(ind[0:6], 0, 10)    # Medias (mu) dentro del universo [0, 10]
    ind[6:12] = np.clip(ind[6:12], 1, 4)   # Sigmas controlados para evitar indeterminaciones
    ind[12:39] = np.clip(ind[12:39], -20, 20) # Coeficientes polinomiales estables
    return ind

def cruzar(padre1, padre2):
    punto_corte = NUM_GENES // 2
    hijo = np.concatenate((padre1[:punto_corte], padre2[punto_corte:]))
    return aplicar_limites(hijo)

def mutar(individuo):
    idx = np.random.randint(0, NUM_GENES)
    if idx < 6:
        individuo[idx] += np.random.normal(0, 1.0)
    elif idx < 12:
        individuo[idx] += np.random.normal(0, 0.4)
    else:
        individuo[idx] += np.random.normal(0, 5.0)
    return aplicar_limites(individuo)

# ==========================================
# 4. Inicialización Distribuida y Configuración del Motor del AG
# ==========================================
num_individuos = 60
num_generaciones = 120  # Ajustado perfectamente para durar entre 1 y 2 minutos reales de video

poblacion = []
for _ in range(num_individuos):
    ind = [2.0, 5.0, 8.0, 2.0, 5.0, 8.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0] # Antecedentes ordenados
    ind.extend(np.random.uniform(-5, 5, 27).tolist()) # Consecuentes aleatorios
    poblacion.append(ind)
poblacion = np.array(poblacion)

# Configuración de Ventanas del Bucle Principal
plt.ion()
fig = plt.figure(figsize=(14, 6))
ax_err = fig.add_subplot(121)
ax_3d = fig.add_subplot(122, projection='3d')

historial_error = []

# ==========================================
# 5. Ejecución Evolutiva en Tiempo Real (Ventanas 5.1 y 5.2)
# ==========================================
for gen in range(num_generaciones):
    fitness_scores = []
    errors = []
    
    for ind in poblacion:
        f, e, _ = evaluar_cromosoma(ind, X1, X2, Z_deseada)
        fitness_scores.append(f)
        errors.append(e)
        
    indices_ranking = np.argsort(fitness_scores)[::-1] #Selección por Ranking: Ordena a toda la población del mejor al peor. Esto permite tomar a las dos mejores soluciones y pasarlas intactas a la siguiente generación (Elitismo Puro), asegurando que el error de aptitud sea una exponencial descendente limpia
    poblacion_ordenada = poblacion[indices_ranking]
    
    mejor_ind = poblacion_ordenada[0].copy()
    error_minimo = errors[indices_ranking[0]]
    historial_error.append(error_minimo)
    
    # Actualización interactiva cada 3 generaciones para agilizar el video
    if gen % 3 == 0 or gen == num_generaciones - 1:
        _, e_act, Z_act = evaluar_cromosoma(mejor_ind, X1, X2, Z_deseada)
        
        # Ventana 5.1: Curva de Aptitud (Suma de Error Absoluto Descendente)
        ax_err.cla()
        ax_err.plot(historial_error, color='red', linewidth=2)
        ax_err.set_title('Ventana 5.1: Evolución del Error de Aptitud')
        ax_err.set_xlabel('Generación')
        ax_err.set_ylabel('Sumatoria de Error Absoluto')
        ax_err.grid(True)
        
        # Ventana 5.2: Síntesis de las Superficies Superpuestas
        ax_3d.cla()
        ax_3d.plot_wireframe(X1, X2, Z_deseada, color='blue', alpha=0.3, label='Deseada (Objetivo)')
        ax_3d.plot_surface(X1, X2, Z_act, cmap='viridis', alpha=0.8, edgecolor='none')
        ax_3d.set_title('Ventana 5.2: Síntesis de Superficie')
        ax_3d.set_xlabel('Entrada X1')
        ax_3d.set_ylabel('Entrada X2')
        ax_3d.set_zlabel('Salida Z')
        
        # Criterio de Rúbrica: Error colocado obligatoriamente en la parte superior de forma clara
        fig.suptitle(f'Algoritmo Genético - Gen: {gen} | ERROR TOTAL VISIBLE: {e_act:.2f}', 
                     fontsize=14, fontweight='bold', color='darkblue')
        
        plt.tight_layout()
        plt.pause(0.01)

    # Selección por Torneo / Elitismo Top 30%
    nueva_pob = [poblacion_ordenada[0].copy(), poblacion_ordenada[1].copy()]
    top_competidores = int(num_individuos * 0.3)
    
    while len(nueva_pob) < num_individuos:
        p1 = poblacion_ordenada[np.random.randint(0, top_competidores)]
        p2 = poblacion_ordenada[np.random.randint(0, top_competidores)]
        hijo = cruzar(p1, p2)
        if np.random.rand() < 0.35:
            hijo = mutar(hijo)
        nueva_pob.append(hijo)
        
    poblacion = np.array(nueva_pob)

plt.ioff()
plt.close(fig) # Cerramos la ventana animada para cumplir la condición de cierre

# ==========================================
# 6. Gráfica Independiente al Cierre: Conjuntos Difusos (Ventana 5.3)
# ==========================================
x_eval = np.linspace(0, 10, 500)
fig_mfs, axs = plt.subplots(1, 2, figsize=(14, 5))

# Extracción de parámetros finales del campeón absoluto
mu_x1_f, mu_x2_f = mejor_ind[0:3], mejor_ind[3:6]
sig_x1_f, sig_x2_f = mejor_ind[6:9], mejor_ind[9:12]
etiquetas = ['Baja', 'Media', 'Alta']

# Subconjunto de Entrada 1
for i in range(3):
    axs[0].plot(x_eval, np.exp(-((x_eval - mu_x1_f[i])**2) / (2 * sig_x1_f[i]**2)), label=etiquetas[i], linewidth=2)
axs[0].set_title('Ventana 5.3: Conjuntos Difusos - Entrada X1')
axs[0].set_xlabel('Universo de Discurso X1')
axs[0].set_ylabel('Grado de Pertenencia ($\mu$)')
axs[0].grid(True)
axs[0].legend()

# Subconjunto de Entrada 2
for i in range(3):
    axs[1].plot(x_eval, np.exp(-((x_eval - mu_x2_f[i])**2) / (2 * sig_x2_f[i]**2)), label=etiquetas[i], linewidth=2)
axs[1].set_title('Ventana 5.3: Conjuntos Difusos - Entrada X2')
axs[1].set_xlabel('Universo de Discurso X2')
axs[1].set_ylabel('Grado de Pertenencia ($\mu$)')
axs[1].grid(True)
axs[1].legend()

plt.tight_layout()
plt.show()