import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler  # <- Nueva librería para normalizar

# 1. DATASET SINTÉTICO
X = np.array([
    [2.5, 45, 0],   # Benigno
    [1.2, 12, 0],   # Benigno
    [0.1, 1, 1],    # Port Scan (Alerta)
    [300, 9500, 1], # Exfiltración (Alerta)
    [3.1, 50, 0],   # Benigno
    [0.05, 1, 1],   # Port Scan (Alerta)
    [450, 12000, 1] # Exfiltración (Alerta)
])
y = np.array([0, 0, 1, 1, 0, 1, 1])

# === PASO CRÍTICO: Normalizar los datos ===
scaler = StandardScaler()
X_escalado = scaler.fit_transform(X) # Ajusta y transforma los datos de entrenamiento
# ==========================================

# 2. CONFIGURACIÓN DE LA RED NEURONAL
red_neuronal = MLPClassifier(hidden_layer_sizes=(5,), solver='lbfgs', max_iter=1000, random_state=42)

# 3. ENTRENAMIENTO (Con datos escalados)
print("[*] Entrenando la red neuronal con datos normalizados...")
red_neuronal.fit(X_escalado, y)
print("[+] Entrenamiento completado.\n")

# 4. PRUEBA EN VIVO (Nuevas conexiones)
nuevas_conexiones = np.array([
    [2.1, 35, 0],    # Debería ser Seguro (0)
    [0.08, 2, 1],    # Debería ser Alerta (1)
    [600, 15000, 1]  # Debería ser Alerta (1) -> El que fallaba
])

# CRÍTICO: Las nuevas conexiones deben escalarse con las mismas reglas
nuevas_conexiones_escaladas = scaler.transform(nuevas_conexiones)

predicciones = red_neuronal.predict(nuevas_conexiones_escaladas)
probabilidades = red_neuronal.predict_proba(nuevas_conexiones_escaladas)

# 5. RESULTADOS
print("=== RESULTADOS DEL ANÁLISIS DE TRÁFICO CORREGIDO ===")
for i, conex in enumerate(nuevas_conexiones):
    estado = "⚠️ ALERTA (Ataque Detectado)" if predicciones[i] == 1 else "✅ SEGURO (Tráfico Normal)"
    confianza = probabilidades[i][predicciones[i]] * 100
    print(f"Conexión {i+1} {conex} -> {estado} [Confianza: {confianza:.2f}%]")