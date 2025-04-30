import socket

# Aqui definimos los parámetros del server
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def udp_cliente(): 
    #Creación del socket 
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True: 
        message = input("Introduce mensaje para enviar a server (escribe exit para salir): ")
        if message.lower() == "exit": 
            print("Cerrando cliente UDP")
            break



        cliente_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
        #Aqui podemos verificar que le llegó al server la info correcta 
        response, server_address = cliente_socket.recvfrom(BUFFER_SIZE)
        print(f"Respuesta del server: {response.decode()}")


    cliente_socket.close()  



if __name__ == "__main__": 
    udp_cliente()

