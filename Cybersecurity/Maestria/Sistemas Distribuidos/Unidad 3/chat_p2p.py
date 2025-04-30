import socket
import threading

# Lista de nodos (IP, Puerto) en la red P2P
NODOS = [
    ("127.0.0.1", 56432),  # Nodo 1
    ("127.0.0.1", 56433),  # Nodo 2
    ("127.0.0.1", 56434)   # Nodo 3
]

# Función de servidor TCP para recibir mensajes
def iniciar_servidor_tcp(mi_ip, mi_puerto, callback_recibir_mensaje):
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
                    mensaje = data.decode('utf-8')
                    callback_recibir_mensaje(f"Mensaje recibido de {addr}: {mensaje}")

# Función de cliente TCP para enviar mensajes
def iniciar_cliente_tcp(mi_ip, mi_puerto, mensaje):
    print(f"Enviando mensaje a los nodos: {mensaje}")
    
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

