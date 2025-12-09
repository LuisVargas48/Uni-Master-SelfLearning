import secrets
import time

def probar_algoritmo():
    print("--- INICIANDO PRUEBA DE ALGORITMO DE UNA VÍA ---\n")

    # 1. DEFINICIÓN DE PARÁMETROS (PÚBLICOS)
    # Usamos un primo grande (hardcodeado para el ejemplo, en real se genera)
    # Este número tiene 50+ dígitos.
    P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE65381FFFFFFFFFFFFFFFF
    
    G = 2 # El generador base

    print(f"[1] Parámetros del Sistema:")
    print(f"    Módulo Primo (P): {str(P)[:50]}... (es enorme, solo se muestran los primeros 50 digitos)")
    print(f"    Generador (G): {G}\n")

    # 2. TU SECRETO (PRIVADO)
    # Generamos un número aleatorio seguro de 256 bits
    mi_secreto_x = secrets.randbits(256)
    
    print(f"[2] Generando tu secreto (x)...")
    print(f"    Tu secreto es: {mi_secreto_x}")
    print("    (Mantenlo oculto, esto es lo que queremos proteger)\n")

    # 3. CÁLCULO DE UNA VÍA (LO QUE HACE EL ALGORITMO)
    # Fórmula: y = (G ^ x) % P
    print(f"[3] Ejecutando la función de una vía (y = G^x mod P)...")
    
    inicio = time.time()
    valor_publico_y = pow(G, mi_secreto_x, P) # Esta es la función mágica
    fin = time.time()

    # 4. RESULTADOS
    print(f"\n--- RESULTADO FINAL ---")
    print(f"    Valor Público (y): {valor_publico_y}")
    print(f"    Tiempo de cálculo: {fin - inicio:.6f} segundos.")
    
    print("\n--- CONCLUSIÓN ---")
    print("Observemos  lo rápido que se generó 'y'.")
    print("Ahora, intentar deducir 'x' viendo solo el número de arriba ('y') y 'P'.")
    print("Es matemáticamente imposible hacerlo en un tiempo razonable.")

if __name__ == "__main__":
    probar_algoritmo()