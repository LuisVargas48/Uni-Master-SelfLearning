import socket
import threading

# Lista que almacenará los nodos registrados como tuplas (IP, Puerto)
nodos_registrados = []

# Función para manejar la conexión de cada cliente
def manejar_cliente(conn, addr):
    print(f"Conexión establecida con {addr}")
    
    # Recibir la información del cliente (IP y Puerto)
    datos_cliente = conn.recv(1024).decode('utf-8')
    if datos_cliente:
        ip, puerto = datos_cliente.split(':')
        puerto = int(puerto)
        nodo = (ip, puerto)
        
        if nodo not in nodos_registrados:
            nodos_registrados.append(nodo)  # Registrar el nodo
            print(f"Nodo registrado: {nodo}")
            conn.sendall(f"Nodo registrado: {nodo}".encode('utf-8'))
        else:
            conn.sendall(f"Este nodo ya está registrado.".encode('utf-8'))
    
    conn.close()

# Función para enviar mensajes a todos los nodos registrados
def enviar_mensaje_a_nodos():
    while True:
        # Leer mensaje desde la consola
        mensaje = input("Escribe un mensaje para enviar a todos los nodos: ")
        
        # Enviar mensaje a todos los nodos registrados
        if mensaje.lower() == "exit":
            print("Saliendo del servidor...")
            break
        
        for nodo in nodos_registrados:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(nodo)
                    client_socket.sendall(mensaje.encode('utf-8'))
                    print(f"Mensaje enviado a {nodo}")
            except ConnectionRefusedError:
                print(f"No se pudo conectar a {nodo}")

# Función que maneja las conexiones entrantes
def iniciar_servidor_tcp(host, puerto):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, puerto))
        server_socket.listen()
        print(f"Servidor escuchando en {host}:{puerto}")
        
        while True:
            conn, addr = server_socket.accept()
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo_cliente.start()

# Iniciar el servidor en el puerto 12345
if __name__ == "__main__":
    # Iniciar hilo para manejar la recepción de mensajes desde consola
    hilo_mensaje = threading.Thread(target=enviar_mensaje_a_nodos, daemon=True)
    hilo_mensaje.start()
    
    # Iniciar el servidor para escuchar conexiones entrantes
    iniciar_servidor_tcp("127.0.0.1", 12345)
