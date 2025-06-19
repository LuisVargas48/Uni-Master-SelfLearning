import socket
import concurrent.futures

def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((host, port))
            if result == 0:
                return port
    except Exception:
        pass
    return None

def scan_ports_parallel(host, start_port, end_port, workers=10):
    open_ports = []
    ports = range(start_port, end_port + 1)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_port = {executor.submit(scan_port, host, port): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            result = future.result()
            if result is not None:
                open_ports.append(result)
    return sorted(open_ports)

if __name__ == "__main__":
    target_host = input("Host/IP a escanear: ").strip()
    start = int(input("Puerto inicial: "))
    end = int(input("Puerto final: "))
    workers = int(input("Número de hilos (ej. 20): "))
    print(f"Escaneando puertos {start}-{end} en {target_host} usando {workers} hilos...")
    open_ports = scan_ports_parallel(target_host, start, end, workers)
    if open_ports:
        print("Puertos abiertos encontrados:", open_ports)
    else:
        print("No se encontraron puertos abiertos en el rango especificado.")