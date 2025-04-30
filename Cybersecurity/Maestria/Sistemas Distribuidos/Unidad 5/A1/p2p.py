import socket
import threading
import time

# Lista de nodos (IP, Puerto) en la red P2P
NODOS = [
    ("127.0.0.1", 56432),  # Jugador 1
    ("127.0.0.1", 56433),  # Jugador 2
    ("127.0.0.1", 56434), # JUgador 3
    ("127.0.0.1", 56435) #Jugador 4

]

# Función de servidor TCP para recibir mensajes
def iniciar_servidor_tcp(mi_ip, mi_puerto, callback_recibir_mensaje):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permitir reutilizar la dirección del socket para evitar el error "Address already in use"
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((mi_ip, mi_puerto))
        server_socket.listen()
        print(f"Servidor TCP escuchando en {mi_ip}:{mi_puerto}")
    except OSError as e:
        print(f"Error al iniciar servidor en {mi_puerto}: {e}")
        return

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
                callback_recibir_mensaje(mensaje)

# Función de cliente TCP con reintentos
def iniciar_cliente_tcp(mi_ip, mi_puerto, mensaje):
    print(f"Intentando enviar mensaje: {mensaje}")
    
    for ip, puerto in NODOS:
        if (ip, puerto) != (mi_ip, mi_puerto):  # No enviarse a sí mismo
            intentos = 5  # Número de reintentos
            for i in range(intentos):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((ip, puerto))
                        client_socket.sendall(mensaje.encode('utf-8'))
                        print(f"Mensaje enviado a {ip}:{puerto}")
                        break  # Si se envió correctamente, salir del bucle
                except ConnectionRefusedError:
                    print(f"Intento {i+1}/{intentos}: No se pudo conectar a {ip}:{puerto}. Reintentando...")
                    time.sleep(2)  # Esperar antes de volver a intentar
            else:
                print(f"No se pudo conectar a {ip}:{puerto} después de {intentos} intentos.")
