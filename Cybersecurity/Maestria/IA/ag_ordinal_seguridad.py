import numpy as np
import matplotlib.pyplot as plt
import random
import time

# ==========================================
# 1. CONFIGURACIÓN DEL ENTORNO (CIBERSEGURIDAD)
# ==========================================
NUM_NODOS = 20
np.random.seed(42) # Semilla para reproducibilidad
nodos = np.random.rand(NUM_NODOS, 2) * 100 

# Parámetros del Algoritmo Genético
TAMANO_POBLACION = 150
GENERACIONES = 100
TASA_MUTACION = 0.1

# ==========================================
# 2. FUNCIONES BASE DEL TSP Y REPRESENTACIÓN ORDINAL
# ==========================================
def calcular_distancia(nodo1, nodo2):
    return np.linalg.norm(nodo1 - nodo2)

# Matriz de distancias (o "Latencia" entre servidores)
matriz_distancias = np.zeros((NUM_NODOS, NUM_NODOS))
for i in range(NUM_NODOS):
    for j in range(NUM_NODOS):
        matriz_distancias[i][j] = calcular_distancia(nodos[i], nodos[j])

def evaluar_ruta(ruta):
    distancia_total = sum([matriz_distancias[ruta[i], ruta[(i+1)%NUM_NODOS]] for i in range(NUM_NODOS)])
    return distancia_total

def crear_individuo_ordinal():
    # En un cromosoma ordinal de N, la posición i toma valores de 0 a (N - i - 1)
    return [random.randint(0, NUM_NODOS - i - 1) for i in range(NUM_NODOS)]

def decodificar_ordinal_a_ruta(cromosoma_ordinal):
    # Convierte la lista ordinal a una ruta real de servidores
    lista_referencia = list(range(NUM_NODOS))
    ruta = []
    for indice in cromosoma_ordinal:
        servidor = lista_referencia.pop(indice)
        ruta.append(servidor)
    return ruta

# ==========================================
# 3. OPERADORES GENÉTICOS
# ==========================================
def cruzar_ordinal(padre1, padre2):
    # Gracias a la representación ordinal, podemos usar un cruce simple de 1 punto
    punto = random.randint(1, NUM_NODOS - 2)
    hijo1 = padre1[:punto] + padre2[punto:]
    hijo2 = padre2[:punto] + padre1[punto:]
    return hijo1, hijo2

def mutar_ordinal(individuo):
    for i in range(NUM_NODOS):
        if random.random() < TASA_MUTACION:
            individuo[i] = random.randint(0, NUM_NODOS - i - 1)
    return individuo

# ==========================================
# 4. CONFIGURACIÓN DE LAS DOS VENTANAS (RÚBRICA)
# ==========================================
plt.ion() # Modo interactivo para actualizar en vivo

# VENTANA 1: La ruta del agente viajero (Topología de Escaneo)
fig_ruta, ax_ruta = plt.subplots(num="Ventana 1 - Topología de Red y Ruta")
fig_ruta.set_size_inches(6, 5)

# VENTANA 2: Convergencia de Aptitud
fig_curva, ax_curva = plt.subplots(num="Ventana 2 - Convergencia de Aptitud")
fig_curva.set_size_inches(6, 5)

historico_mejores_distancias = []

# ==========================================
# 5. BUCLE PRINCIPAL DEL ALGORITMO EVOLUTIVO
# ==========================================
# Inicializar población
poblacion = [crear_individuo_ordinal() for _ in range(TAMANO_POBLACION)]
mejor_distancia_global = float('inf')
mejor_ruta_global = []

print("[*] Iniciando Escaneo de Vulnerabilidades (Optimizador Evolutivo)...")

for generacion in range(GENERACIONES):
    # Decodificar y evaluar
    rutas_reales = [decodificar_ordinal_a_ruta(ind) for ind in poblacion]
    aptitudes = [evaluar_ruta(ruta) for ruta in rutas_reales]
    
    # Encontrar el mejor de la generación
    indice_mejor = np.argmin(aptitudes)
    mejor_distancia_actual = aptitudes[indice_mejor]
    mejor_ruta_actual = rutas_reales[indice_mejor]
    
    if mejor_distancia_actual < mejor_distancia_global:
        mejor_distancia_global = mejor_distancia_actual
        mejor_ruta_global = mejor_ruta_actual
        
    historico_mejores_distancias.append(mejor_distancia_global)

    # --- ACTUALIZAR VENTANA 1 (Ruta) ---
    ax_ruta.clear()
    ax_ruta.set_title(f"Gen {generacion+1} | Distancia Óptima (Latencia): {mejor_distancia_global:.2f} ms", fontsize=11, fontweight='bold')
    ax_ruta.scatter(nodos[:, 0], nodos[:, 1], c='red', s=50, label='Servidores')
    
    # Trazar las líneas de la ruta
    ruta_x = [nodos[i, 0] for i in mejor_ruta_global] + [nodos[mejor_ruta_global[0], 0]]
    ruta_y = [nodos[i, 1] for i in mejor_ruta_global] + [nodos[mejor_ruta_global[0], 1]]
    ax_ruta.plot(ruta_x, ruta_y, c='blue', alpha=0.7)
    
    # --- ACTUALIZAR VENTANA 2 (Curva de Aptitud) ---
    ax_curva.clear()
    ax_curva.set_title(f"Aptitud Mínima Alcanzada: {mejor_distancia_global:.2f}", fontsize=11, fontweight='bold')
    ax_curva.set_xlabel("Generaciones")
    ax_curva.set_ylabel("Distancia (Latencia)")
    ax_curva.plot(historico_mejores_distancias, c='green', linewidth=2)
    ax_curva.grid(True)

    # Redibujar las ventanas
    fig_ruta.canvas.draw()
    fig_ruta.canvas.flush_events()
    fig_curva.canvas.draw()
    fig_curva.canvas.flush_events()
    
    # Pausa para dar tiempo a que el video dure ~1.5 minutos (100 gen * 0.7s)
    time.sleep(0.7) 

    # --- SELECCIÓN Y REPRODUCCIÓN (Torneo simple) ---
    nueva_poblacion = []
    # Elitismo: guardamos al mejor
    nueva_poblacion.append(poblacion[indice_mejor])
    
    while len(nueva_poblacion) < TAMANO_POBLACION:
        padre1 = poblacion[random.randint(0, TAMANO_POBLACION-1)]
        padre2 = poblacion[random.randint(0, TAMANO_POBLACION-1)]
        
        hijo1, hijo2 = cruzar_ordinal(padre1, padre2)
        nueva_poblacion.append(mutar_ordinal(hijo1))
        if len(nueva_poblacion) < TAMANO_POBLACION:
            nueva_poblacion.append(mutar_ordinal(hijo2))
            
    poblacion = nueva_poblacion

print(f"[+] Optimización finalizada. Ruta óptima asegurada: {mejor_distancia_global:.2f}")
plt.ioff()
plt.show() # Mantiene las ventanas abiertas al terminar