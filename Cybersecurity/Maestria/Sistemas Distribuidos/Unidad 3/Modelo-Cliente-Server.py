import threading
import socket
import argparse

# Lista de nodos (IP, Puerto) en la red P2P
NODOS = [
    ("127.0.0.1", 56432),  # Nodo 1
    ("127.0.0.1", 56433),  # Nodo 2
    ("127.0.0.1", 56434)   # Nodo 3
]

# Función de servidor TCP para recibir mensajes
def iniciar_servidor_tcp(mi_ip, mi_puerto):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((mi_ip, mi_puerto))
        server_socket.listen()
        print(f"Servidor TCP escuchando en {mi_ip}:{mi_puerto}")

        while True:
            conn, addr = server_socket.accept()
            print(f"Conexión establecida con {addr}")
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print(f"Cliente {addr} desconectado.")
                        break
                    print(f"Mensaje recibido de {addr}: {data.decode('utf-8')}")

# Función de cliente TCP para enviar mensajes
def iniciar_cliente_tcp(mi_ip, mi_puerto):
    print("Escribe 'exit' para salir.")
    while True:
        mensaje = input("Tu mensaje: ")
        if mensaje.lower() == "exit":
            print("Saliendo del chat...")
            break

        # Enviar mensaje a todos los nodos en la red
        for ip, puerto in NODOS:
            if (ip, puerto) != (mi_ip, mi_puerto):  # No enviarse a sí mismo
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((ip, puerto))
                        client_socket.sendall(mensaje.encode('utf-8'))
                        print(f"Mensaje enviado a {ip}:{puerto}")
                except ConnectionRefusedError:
                    print(f"No se pudo conectar a {ip}:{puerto}")

if __name__ == "__main__":
    # Argumentos de línea de comandos para configurar IP y puerto
    parser = argparse.ArgumentParser(description="Nodo P2P tipo chat.")
    parser.add_argument("--puerto", type=int, required=True, help="Puerto en el que este nodo escuchará conexiones.")
    args = parser.parse_args()

    MI_IP = "127.0.0.1"  # Dirección IP fija para este ejemplo
    MI_PUERTO = args.puerto

    # Crear e iniciar los hilos
    hilo_servidor = threading.Thread(target=iniciar_servidor_tcp, args=(MI_IP, MI_PUERTO), daemon=True)
    hilo_cliente = threading.Thread(target=iniciar_cliente_tcp, args=(MI_IP, MI_PUERTO))

    hilo_servidor.start()
    hilo_cliente.start()

    # Esperar a que el cliente termine
    hilo_cliente.join()
    print("El programa ha finalizado.")

