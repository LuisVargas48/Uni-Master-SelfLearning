# Importamos 'defaultdict' para facilitar el conteo
from collections import defaultdict
from scapy.all import rdpcap, IP, ICMP, TCP, Raw

def analizar_paquetes(archivo_pcap):
    """
    Lee un archivo .pcap y analiza cada paquete buscando:
    1. Pings (ICMP)
    2. Tráfico no cifrado (HTTP/FTP)
    3. Posibles credenciales en texto plano
    4. Escaneos de puertos (TCP SYN Scan)
    """
    print(f"Intentando leer el archivo: {archivo_pcap}...")
    
    try:
        paquetes = rdpcap(archivo_pcap)
        print(f"¡Éxito! Se leyeron {len(paquetes)} paquetes.")
        print("Iniciando análisis de patrones...\n")
        
    except FileNotFoundError:
        print(f"\nError: ¡No se encontró el archivo '{archivo_pcap}'!")
        return
    except Exception as e:
        print(f"Ocurrió un error inesperado al leer el archivo: {e}")
        return

    # --- INICIO DE LA LÓGICA DE ANÁLISIS ---
    
    hallazgos = []
    
    # --- Lógica de rastreo de SYN Scan ---
    # { (ip_origen, ip_destino): {puerto1, puerto2, ...} }
    syn_track = defaultdict(set)
    # ------------------------------------

    for numero_paquete, paquete in enumerate(paquetes):
        
        # --- Regla 1: Detección de ICMP (Ping) ---
        if paquete.haslayer(ICMP) and paquete.haslayer(IP):
            # ... (código de ICMP igual que antes) ...
            if paquete[ICMP].type == 8: tipo_icmp = "Echo Request (Ping)"
            elif paquete[ICMP].type == 0: tipo_icmp = "Echo Reply (Respuesta de Ping)"
            else: tipo_icmp = f"Otro tipo ICMP (Tipo: {paquete[ICMP].type})"
            info = f"[*] [Paquete #{numero_paquete}] Ping Detectado: {tipo_icmp} | Origen: {paquete[IP].src} -> Destino: {paquete[IP].dst}"
            hallazgos.append(info)
            
        # --- Regla 2: Detección de TCP (HTTP, FTP, SYN Scan, Credenciales) ---
        elif paquete.haslayer(TCP) and paquete.haslayer(IP):
            
            ip_origen = paquete[IP].src
            ip_destino = paquete[IP].dst
            puerto_origen = paquete[TCP].sport
            puerto_destino = paquete[TCP].dport
            
            # 2.1 - Lógica de rastreo de SYN Scan
            # El flag 'S' (0x02) significa que SÓLO el bit SYN está activado
            if paquete[TCP].flags == 'S':
                syn_track[(ip_origen, ip_destino)].add(puerto_destino)

            # 2.2 - Buscar tráfico en puertos no cifrados conocidos
            if puerto_destino == 80 or puerto_origen == 80:
                info = f"[*] [Paquete #{numero_paquete}] Tráfico HTTP (Puerto 80) detectado | Origen: {ip_origen}:{puerto_origen} -> Destino: {ip_destino}:{puerto_destino}"
                hallazgos.append(info)
                
            elif puerto_destino == 21 or puerto_origen == 21:
                info = f"[!] [Paquete #{numero_paquete}] Tráfico FTP (Puerto 21) detectado | Origen: {ip_origen}:{puerto_origen} -> Destino: {ip_destino}:{puerto_destino}"
                hallazgos.append(info)

            # 2.3 - Buscar posibles credenciales en texto plano
            if paquete.haslayer(Raw):
                try:
                    payload = paquete[Raw].load.decode('utf-8', errors='ignore').lower()
                    if 'user' in payload or 'pass' in payload or 'login' in payload:
                        info = f"[¡ALERTA!] [Paquete #{numero_paquete}] Posibles credenciales en TEXTO PLANO | Origen: {ip_origen}:{puerto_origen} -> Destino: {ip_destino}:{puerto_destino}"
                        hallazgos.append(info)
                except Exception:
                    pass 

    # --- FIN DEL BUCLE ---

    # --- Lógica de Reporte de SYN Scan ---
    # Analizamos el diccionario 'syn_track' DESPUÉS de revisar todos los paquetes
    UMBRAL_PUERTOS_SCAN = 20 # Si una IP escanea >20 puertos, es sospechoso
    
    for (origen, destino), puertos in syn_track.items():
        if len(puertos) > UMBRAL_PUERTOS_SCAN:
            info = f"[¡¡ALERTA DE ESCANEO!!] Posible SYN Scan detectado | "
            info += f"Origen: {origen} -> Destino: {destino} | "
            info += f"Puertos únicos escaneados: {len(puertos)}"
            hallazgos.append(info)

    # --- FIN DE LA LÓGICA DE ANÁLISIS ---

    # --- Imprimir el informe final ---
    print("\n--- INFORME DE ANÁLISIS ---")
    if hallazgos:
        # Imprimimos las alertas más graves primero
        for linea in sorted(hallazgos, key=lambda x: "!" not in x):
             print(linea)
    else:
        print("No se encontraron patrones de interés (ICMP, HTTP, FTP, SYN Scan).")
    
    # Guardamos el informe en un archivo
    with open("informe_analisis.txt", "w", encoding='utf-8') as f:
        f.write("--- INFORME DE ANÁLISIS DE TRÁFICO ---\n\n")
        if hallazgos:
            for linea in sorted(hallazgos, key=lambda x: "!" not in x):
                f.write(linea + "\n")
        else:
            f.write("No se encontraron patrones de interés.")
    print("----------------------------")
    print("\n[+] Informe completo guardado en 'informe_analisis.txt'")


# --- Punto de entrada del script ---
if __name__ == "__main__":
    archivo_de_captura = "captura_datos.pcap"
    analizar_paquetes(archivo_de_captura)