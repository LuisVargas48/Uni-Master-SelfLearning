import time
import random

# --- CONFIGURACIÓN DEL ESCENARIO (Igual que tu tarea) ---
P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE65381FFFFFFFFFFFFFFFF
G = 2 

def simular_hackeo():
    print("--- 1. GENERANDO ESCENARIO VULNERABLE ---")
    # TRUCO: Usamos un rango pequeño (1 a 500,000) para que la demo termine rápido.
    # En la vida real, este número sería de 77 dígitos y el ataque sería imposible.
    secreto_real_x = random.randint(1, 500000) 
    
    # Calculamos el valor público 'y' (lo único que ve el hacker)
    valor_publico_y = pow(G, secreto_real_x, P)
    
    print(f"Secreto (x): {secreto_real_x} (El hacker NO sabe esto)")
    print(f"Valor Público (y): {str(valor_publico_y)[:30]}... (El hacker ve esto)")
    print("-" * 50)

    print("\n--- 2. INICIANDO ATAQUE DE FUERZA BRUTA ---")
    print("El script probará: 2^1, 2^2, 2^3... hasta encontrar coincidencia con 'y'")
    
    inicio_ataque = time.time()
    intento = 1
    encontrado = False

    while not encontrado:
        # --- EL NÚCLEO DEL ATAQUE ---
        # Calculamos el hash para el intento actual
        calculo_hacker = pow(G, intento, P)
        
        # Comparamos con el valor público robado
        if calculo_hacker == valor_publico_y:
            encontrado = True
            tiempo_total = time.time() - inicio_ataque
            
            print(f"\n[!!!] ¡CLAVE ENCONTRADA! [!!!]")
            print(f"El secreto era: {intento}")
            print(f"Intentos realizados: {intento}")
            print(f"Tiempo tomado: {tiempo_total:.4f} segundos")
        else:
            # Log visual cada 50,000 intentos para que veas que está trabajando
            if intento % 50000 == 0:
                print(f"Probando... van {intento} intentos sin éxito.")
            
            intento += 1

if __name__ == "__main__":
    simular_hackeo()