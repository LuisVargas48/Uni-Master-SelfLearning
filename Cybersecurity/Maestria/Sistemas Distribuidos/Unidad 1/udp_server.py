import socket

#Configuracion del servidor 
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024 


def udp_server(): 
 #Crear el socket UDP
 server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 server_socket.bind((SERVER_IP, SERVER_PORT))
 print(f"Servidor escuchando  en: {SERVER_IP}:{SERVER_PORT}")

 while True: 
  #Este while recibe datos de cliente y responde 
  message, client_address = server_socket.recvfrom(BUFFER_SIZE)
  print(f"Mensaje recibido de: {client_address}: {message.decode()}")


  response = f"Mensaje recibido: {message.decode()}"
  server_socket.sendto(response.encode(), client_address)
  print(f"Respuesta enviada a: {client_address}")


if __name__ == "__main__": 
   udp_server() 