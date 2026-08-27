import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. Configuración y Curva Objetivo
# ==========================================
A, B, C, D, E, F, G = 8, 25, 4, 45, 10, 17, 35
x = np.linspace(0, 100, 1000)
y_ref = A * (B * np.sin(x / C) + D * np.cos(x / E)) + F * x - G

NUM_REGLAS = 10  # 10 reglas nos dan la máxima flexibilidad
NUM_GENES = NUM_REGLAS * 3

# ==========================================
# 2. Funciones Core (Red Neuro-Difusa)
# ==========================================
def calcular_curva_neurodifusa(cromosoma, x):
    suma_mu = np.zeros_like(x) + 1e-10
    y_fuzzy = np.zeros_like(x)
    
    for i in range(NUM_REGLAS):
        mu = cromosoma[i*3]
        sig = cromosoma[i*3 + 1]
        k = cromosoma[i*3 + 2]
        
        m = np.exp(-((x - mu)**2) / (2 * sig**2))
        suma_mu += m
        y_fuzzy += m * k
        
    return y_fuzzy / suma_mu

def evaluar_cromosoma(cromosoma, x, y_ref):
    y_fuzzy = calcular_curva_neurodifusa(cromosoma, x)
    error = np.sum((y_ref - y_fuzzy)**2)
    fitness = 1 / (error + 0.0001)
    return fitness, error, y_fuzzy

# ==========================================
# 3. Operadores Genéticos Optimizados
# ==========================================
def aplicar_limites(ind):
    for i in range(NUM_REGLAS):
        ind[i*3] = np.clip(ind[i*3], 0, 100)        # Límite para mu (Posición)
        ind[i*3 + 1] = np.clip(ind[i*3 + 1], 2, 20) # Límite para sigma (Ancho)
    return ind

def cruzar(padre1, padre2):
    # Cruce de un punto en la mitad del cromosoma
    punto_corte = len(padre1) // 2
    hijo = np.concatenate((padre1[:punto_corte], padre2[punto_corte:]))
    return aplicar_limites(hijo)

def mutar(individuo):
    indice = np.random.randint(0, NUM_GENES)
    tipo_gen = indice % 3
    
    # Mutación inteligente según el tipo de gen
    if tipo_gen == 0:   # Es mu (Centro)
        individuo[indice] += np.random.normal(0, 3.0)
    elif tipo_gen == 1: # Es sigma (Ancho)
        individuo[indice] += np.random.normal(0, 1.5)
    else:               # Es k (Altura, requiere cambios drásticos)
        individuo[indice] += np.random.normal(0, 150.0)
        
    return aplicar_limites(individuo)

# ==========================================
# 4. Motor del Algoritmo Genético
# ==========================================
num_individuos = 100
num_generaciones = 300

# Inicialización distribuida
poblacion = []
for _ in range(num_individuos):
    ind = []
    for i in range(NUM_REGLAS):
        mu_in = (100 / (NUM_REGLAS - 1)) * i 
        sig_in = 8 
        k_in = np.random.uniform(0, 1500)
        ind.extend([mu_in, sig_in, k_in])
    poblacion.append(ind)
poblacion = np.array(poblacion)

plt.ion() 
fig, axs = plt.subplots(1, 3, figsize=(18, 6))
historial_fitness = []

for gen in range(num_generaciones):
    fitness_scores = []
    for ind in poblacion:
        f, e, _ = evaluar_cromosoma(ind, x, y_ref)
        fitness_scores.append(f)
    
    # ORDENAR POBLACIÓN (El secreto del éxito para no atascarse)
    indices_ordenados = np.argsort(fitness_scores)[::-1] # De mayor a menor
    poblacion_ordenada = poblacion[indices_ordenados]
    
    mejor_individuo = poblacion_ordenada[0].copy()
    historial_fitness.append(np.max(fitness_scores))
    
    # --- Actualización Visual (Cada 5 Generaciones) ---
    if gen % 5 == 0:
        f_act, e_act, curva_act = evaluar_cromosoma(mejor_individuo, x, y_ref)
        
        axs[0].cla()
        axs[0].plot(x, y_ref, label='Referencia', color='blue')
        axs[0].plot(x, curva_act, label='Generada', color='red', linestyle='--')
        axs[0].set_title(f'Ajuste de Curva - Gen: {gen}')
        
        # --- AQUÍ ESTÁ EL CAMBIO DEL RMSE ---
        rmse = np.sqrt(e_act / len(x))
        axs[0].text(0, 1400, f'Error Promedio (RMSE): {rmse:.2f}', bbox=dict(facecolor='white', alpha=0.5))
        # ------------------------------------
        
        axs[0].legend(loc='lower right')
        
        axs[1].cla()
        axs[1].plot(historial_fitness, color='green')
        axs[1].set_title('Convergencia del AG')
        axs[1].set_xlabel('Generación')
        axs[1].set_ylabel('Fitness (Aptitud)')
        
        axs[2].cla()
        for i in range(NUM_REGLAS):
            mu_val, sig_val = mejor_individuo[i*3], mejor_individuo[i*3 + 1]
            axs[2].plot(x, np.exp(-((x - mu_val)**2) / (2 * sig_val**2)))
        axs[2].set_title(f'Funciones de Pertenencia ({NUM_REGLAS} Reglas)')
        
        plt.tight_layout()
        plt.pause(0.01) 

    # --- Evolución con Selección Inteligente ---
    # Elitismo: pasamos a los 2 mejores intactos
    nueva_poblacion = [poblacion_ordenada[0].copy(), poblacion_ordenada[1].copy()] 
    
    # Para el resto, cruzamos solo a los "aptos" (Top 30%)
    top_30_percent = int(num_individuos * 0.3)
    
    while len(nueva_poblacion) < num_individuos:
        p1 = poblacion_ordenada[np.random.randint(0, top_30_percent)]
        p2 = poblacion_ordenada[np.random.randint(0, top_30_percent)]
        
        hijo = cruzar(p1, p2)
        
        # 40% de probabilidad de mutación para mantener variedad
        if np.random.rand() < 0.40: 
            hijo = mutar(hijo)
            
        nueva_poblacion.append(hijo)
        
    poblacion = np.array(nueva_poblacion)

plt.ioff()
plt.show()