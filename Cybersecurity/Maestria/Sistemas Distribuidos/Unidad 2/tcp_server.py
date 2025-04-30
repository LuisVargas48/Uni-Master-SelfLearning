import socket

def iniciar_servidor_tcp():
    HOST = '127.0.0.1'  # Dirección IP local
    PORT = 56432        # Puerto para escuchar

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))  # Asociar IP y puerto
        server_socket.listen()            # Escuchar conexiones entrantes
        print(f"Servidor TCP escuchando en {HOST}:{PORT}")

        conn, addr = server_socket.accept()  # Aceptar una conexión
        print(f"Conexión establecida con {addr}")
        with conn:
            while True:
                data = conn.recv(1024)  # Recibir datos
                if not data:
                    print("Cliente desconectado.")
                    break
                print(f"Mensaje recibido: {data.decode('utf-8')}")
                # Enviar un eco de vuelta al cliente
                conn.sendall(data)

if __name__ == "__main__":
    iniciar_servidor_tcp()
