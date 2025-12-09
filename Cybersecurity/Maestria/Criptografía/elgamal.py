import time

def paso_a_paso_elgamal():
    print("--- INICIO DEMOSTRACIÓN ELGAMAL ---")
    time.sleep(1)
    
    # 1. Configuración Pública
    p = 23
    g = 5
    print(f"\n[PÚBLICO] Parámetros del grupo: Primo (p)={p}, Generador (g)={g}")
    time.sleep(2)

    # 2. Alice Genera Llaves
    x = 6 # Privada
    y = pow(g, x, p) # Pública (g^x mod p)
    print(f"\n[ALICE] Genera sus llaves:")
    print(f"   -> Clave Privada (x): {x}")
    print(f"   -> Clave Pública (y): {y} (calculado como {g}^{x} mod {p})")
    time.sleep(2)

    # 3. Bob Cifra un mensaje
    m = 19
    k = 3 # Aleatorio
    print(f"\n[BOB] Quiere enviar el mensaje: {m}")
    print(f"   -> Elige número aleatorio (k): {k}")
    
    c1 = pow(g, k, p)
    s = pow(y, k, p) # Secreto compartido temporal
    c2 = (m * s) % p
    
    print(f"   -> Calcula c1 (g^k mod p): {c1}")
    print(f"   -> Calcula c2 (m * y^k mod p): {c2}")
    print(f"   -> ENVÍA TEXTO CIFRADO: ({c1}, {c2})")
    time.sleep(2)

    # 4. Alice Descifra
    print(f"\n[ALICE] Recibe ({c1}, {c2}) y descifra:")
    
    # Matemáticamente s = c1^x mod p
    s_recuperado = pow(c1, x, p)
    
    # Inverso modular de s para 'quitar' la máscara
    s_inverso = pow(s_recuperado, -1, p)
    
    mensaje_final = (c2 * s_inverso) % p
    print(f"   -> Usa su clave privada {x} para calcular el inverso.")
    print(f"   -> Mensaje Recuperado: {mensaje_final}")
    
    if mensaje_final == m:
        print("\n[RESULTADO] ¡Éxito! El mensaje coincide.")

# Ejecutar
paso_a_paso_elgamal()