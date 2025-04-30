import socket
import argparse
import threading

# Función para escuchar mensajes del servidor
def escuchar_mensajes(puerto_escucha):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener_socket:
        listener_socket.bind(("127.0.0.1", puerto_escucha))
        listener_socket.listen()
        print(f"Escuchando en el puerto {puerto_escucha} para mensajes entrantes...")
        
        while True:
            conn, addr = listener_socket.accept()
            with conn:
                mensaje = conn.recv(1024).decode('utf-8')
                if mensaje:
                    print(f"Mensaje recibido: {mensaje}")
                else:
                    break

# Función de cliente TCP para enviar mensajes (solo para registro)
def registrar_nodo(mi_ip, mi_puerto):
    print("Registrando el nodo...")
    
    # Conectarse al servidor para registrarse
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(("127.0.0.1", 12345))
        
        # Enviar la información del cliente (IP y puerto)
        client_socket.sendall(f"{mi_ip}:{mi_puerto}".encode('utf-8'))
        
        # Recibir la respuesta del servidor
        respuesta = client_socket.recv(1024).decode('utf-8')
        print(respuesta)

# Configuración del cliente
if __name__ == "__main__":
    # Leer los parámetros del puerto del cliente desde la línea de comandos
    parser = argparse.ArgumentParser(description="Nodo Cliente P2P.")
    parser.add_argument("--puerto", type=int, required=True, help="Puerto en el que este nodo escuchará conexiones.")
    args = parser.parse_args()

    MI_IP = "127.0.0.1"  # Dirección IP fija para este ejemplo
    MI_PUERTO = args.puerto

    # Iniciar hilo para escuchar mensajes del servidor
    hilo_escucha = threading.Thread(target=escuchar_mensajes, args=(MI_PUERTO,))
    hilo_escucha.start()

    # Iniciar el cliente para registrarse en el servidor
    registrar_nodo(MI_IP, MI_PUERTO)
