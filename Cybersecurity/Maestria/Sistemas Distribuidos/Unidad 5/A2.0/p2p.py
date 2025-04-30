# p2p.py
import socket
import threading

NODOS = [
    ("127.0.0.1", 56432),
    ("127.0.0.1", 56433),
    ("127.0.0.1", 56434),
    ("127.0.0.1", 56435)
]

palabra_global = None  # Variable compartida para la palabra sincronizada

# ======== Servidor TCP ========
def iniciar_servidor_tcp(mi_ip, mi_puerto, callback_recibir_mensaje):
    global palabra_global
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((mi_ip, mi_puerto))
        server_socket.listen()
        print(f"Servidor TCP escuchando en {mi_ip}:{mi_puerto}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                data = conn.recv(1024).decode('utf-8')
                if data.startswith("PALABRA:"):
                    palabra_global = data.split(":")[1]
                    print(f"🔑 Palabra sincronizada recibida: {palabra_global}")
                else:
                    callback_recibir_mensaje(data)

# ======== Cliente TCP ========
def iniciar_cliente_tcp(mi_ip, mi_puerto, mensaje):
    for ip, puerto in NODOS:
        if (ip, puerto) != (mi_ip, mi_puerto):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((ip, puerto))
                    client_socket.sendall(mensaje.encode('utf-8'))
            except ConnectionRefusedError:
                print(f"❌ No se pudo conectar a {ip}:{puerto}")
