import socket

def iniciar_cliente_tcp():
    HOST = '127.0.0.1'  # Dirección IP del servidor
    PORT = 56432        # Puerto del servidor

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))  # Conectarse al servidor
        print("Conectado al servidor. Escribe 'exit' para terminar la conexión.")

        while True:
            mensaje = input("Escribe tu mensaje: ")  # Leer mensaje desde la consola
            if mensaje.lower() == "exit":
                print("Cerrando la conexión...")
                client_socket.sendall(mensaje.encode('utf-8'))  # Enviar 'exit' al servidor
                break
            client_socket.sendall(mensaje.encode('utf-8'))  # Enviar mensaje
            data = client_socket.recv(1024)  # Recibir respuesta
            print(f"Respuesta del servidor: {data.decode('utf-8')}")

if __name__ == "__main__":
    iniciar_cliente_tcp()
