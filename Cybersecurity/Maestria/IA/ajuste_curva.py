import numpy as np
import matplotlib.pyplot as plt
import random

# ==========================================
# 1. FUNCIONES DEL ALGORITMO GENÉTICO (BACKEND)
# ==========================================


def crear_individuo_binario():
    return [random.randint(0, 1) for _ in range(56)]

def binario_a_decimal(lista_bits):
    valor_decimal = 0
    total_bits = len(lista_bits)
    for i in range(total_bits):
        bit = lista_bits[i]
        exponente = total_bits - 1 - i
        valor_decimal += bit * (2 ** exponente)
    return valor_decimal

def decodificar_cromosoma(individuo):
    A = binario_a_decimal(individuo[0:8])
    B = binario_a_decimal(individuo[8:16])
    C = binario_a_decimal(individuo[16:24])
    D = binario_a_decimal(individuo[24:32])
    E = binario_a_decimal(individuo[32:40])
    F = binario_a_decimal(individuo[40:48])
    G = binario_a_decimal(individuo[48:56])
    return A, B, C, D, E, F, G



def decodificar_cromosoma_escalado(individuo):
    # Función interna para convertir 8 bits al rango útil (dividido entre 255)
    def a_rango(bits, maximo):
        # binario_a_decimal debe trabajar con estos 8 bits
        return (binario_a_decimal(bits) / 255) * maximo
    
    # THE CRITICAL FIX: SLICES ESTRICTOS DE 8 BITS
    A = a_rango(individuo[0:8], 20)    # Del bit 0 al 7
    B = a_rango(individuo[8:16], 50)   # Del bit 8 al 15
    C = a_rango(individuo[16:24], 10)  # Del 16 al 23
    D = a_rango(individuo[24:32], 60)  # Del 24 al 31
    E = a_rango(individuo[32:40], 20)  # Del 32 al 39
    F = a_rango(individuo[40:48], 30)  # Del 40 al 47
    G = a_rango(individuo[48:56], 50)  # Del 48 al 55 (Total 56 bits consumidos)
    
    return A, B, C, D, E, F, G

def calcular_curva(A, B, C, D, E, F, G, x):
    # Evitar división por cero
    if C == 0: C = 0.1
    if E == 0: E = 0.1
    return A * (B * np.sin(x / C) + D * np.cos(x / E)) + F * x - G

def calcular_aptitud(individuo, x_valores, y_referencia):
    A, B, C, D, E, F, G = decodificar_cromosoma_escalado(individuo)
    y_individuo = calcular_curva(A, B, C, D, E, F, G, x_valores)
    return np.sum(np.abs(y_referencia - y_individuo))

def cruzar(padre, madre):
    punto_corte = 28
    hijo1 = padre[:punto_corte] + madre[punto_corte:]
    hijo2 = madre[:punto_corte] + padre[punto_corte:]
    return hijo1, hijo2

def mutar(individuo, generacion_actual, total_generaciones):
    # La tasa baja de 0.20 a 0.02 conforme avanza el tiempo
    tasa_actual = 0.20 - (generacion_actual / total_generaciones) * 0.18
    
    for i in range(len(individuo)):
        if random.random() < tasa_actual:
            individuo[i] = 1 - individuo[i]
    return individuo


def mutar_adaptativa(individuo, gen_actual, total_gen):
    # La tasa empieza en 0.20 y termina en 0.01 (1%)
    progreso = gen_actual / total_gen
    tasa_actual = 0.20 * (1 - progreso) + 0.01
    
    for i in range(len(individuo)):
        if random.random() < tasa_actual:
            individuo[i] = 1 - individuo[i]
    return individuo



def seleccion_torneo(poblacion, aptitudes, k=10):
    # Elegimos 'k' competidores al azar
    indices_torneo = random.sample(range(len(poblacion)), k)
    # Buscamos quién de ellos tiene el error más bajo (la mejor aptitud)
    mejor_indice = min(indices_torneo, key=lambda i: aptitudes[i])
    return poblacion[mejor_indice]



# ==========================================
# 2. CONFIGURACIÓN DEL ENTORNO Y REFERENCIA
# ==========================================

TAMANO_POBLACION = 500
GENERACIONES = 400
TASA_MUTACION = 0.20

# Valores objetivo del profesor
A_ref, B_ref, C_ref, D_ref, E_ref, F_ref, G_ref = 8, 25, 4, 45, 10, 17, 35

x_valores = np.linspace(0, 10, 200)
y_referencia = calcular_curva(A_ref, B_ref, C_ref, D_ref, E_ref, F_ref, G_ref, x_valores)

# ==========================================
# 3. CONFIGURACIÓN DE LAS VENTANAS (FRONTEND)
# ==========================================

plt.ion() # Activar modo interactivo para animación
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.canvas.manager.set_window_title('U2 A3: Algoritmo Genético Clásico - Ajuste de Curva')

poblacion = [crear_individuo_binario() for _ in range(TAMANO_POBLACION)]

mejores_aptitudes_historicas = []
mejor_individuo_global = None
mejor_aptitud_global = float('inf')

print("[*] Iniciando el intérprete... Preparando entorno gráfico.")

# ==========================================
# 4. BUCLE PRINCIPAL (EVOLUCIÓN Y GRÁFICAS)
# ==========================================

for generacion in range(GENERACIONES):
    
    # Evaluar población
    aptitudes = [calcular_aptitud(ind, x_valores, y_referencia) for ind in poblacion]
    
    # Elitismo: Buscar al mejor
    indice_mejor = np.argmin(aptitudes)
    mejor_individuo_actual = poblacion[indice_mejor]
    mejor_aptitud_actual = aptitudes[indice_mejor]
    
    if mejor_aptitud_actual < mejor_aptitud_global:
        mejor_aptitud_global = mejor_aptitud_actual
        mejor_individuo_global = mejor_individuo_actual.copy()
        
    mejores_aptitudes_historicas.append(mejor_aptitud_global)
    
    # --- ACTUALIZACIÓN VISUAL (Matplotlib) ---
    # Ventana 1: Ajuste de Curva
    ax1.clear()
    ax1.plot(x_valores, y_referencia, 'r-', linewidth=3, label='Curva Objetivo (Referencia)')
    
    A, B, C, D, E, F, G = decodificar_cromosoma_escalado(mejor_individuo_global)
    y_generada = calcular_curva(A, B, C, D, E, F, G, x_valores)
    ax1.plot(x_valores, y_generada, 'b--', linewidth=2, label=f'Curva Generada (Gen {generacion})')
    
    ax1.set_title("Ventana 1: Ajuste de Curva")
    ax1.legend(loc="lower right")
    ax1.grid(True)
    
    
    ax1.text(0.05, 0.95, f"Error Absoluto: {mejor_aptitud_global:.2f}", 
             transform=ax1.transAxes, fontsize=12, verticalalignment='top', 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Ventana 2: Curva de Convergencia
    ax2.clear()
    ax2.plot(range(generacion + 1), mejores_aptitudes_historicas, 'g-', linewidth=2)
    ax2.set_title("Ventana 2: Función de Aptitud vs Generaciones")
    ax2.set_xlabel("Generación")
    ax2.set_ylabel("Error (Aptitud)")
    ax2.grid(True)
    
    plt.pause(0.001) # Pausa breve para crear el efecto de animación

    # --- CREAR NUEVA GENERACIÓN ---
    nueva_poblacion = []
    nueva_poblacion.append(mejor_individuo_global.copy()) # Elitismo
     
    while len(nueva_poblacion) < TAMANO_POBLACION:
        # Selección por torneo aleatorio (simplificada)
        padre = seleccion_torneo(poblacion, aptitudes)
        madre = seleccion_torneo(poblacion, aptitudes)
        
        hijo1, hijo2 = cruzar(padre, madre)
        hijo1 = mutar_adaptativa(hijo1, generacion, GENERACIONES)
        hijo2 = mutar_adaptativa(hijo2, generacion, GENERACIONES)
        
        nueva_poblacion.append(hijo1)
        if len(nueva_poblacion) < TAMANO_POBLACION:
            nueva_poblacion.append(hijo2)
            
    poblacion = nueva_poblacion

plt.ioff()
print(f"[*] Ejecución finalizada. Variables encontradas: A={A}, B={B}, C={C}, D={D}, E={E}, F={F}, G={G}")
plt.show() # Mantiene la ventana abierta al terminar