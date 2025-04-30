import jsonrpclib

# Dirección del servidor remoto (ajusta la IP si es necesario)
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
server = jsonrpclib.ServerProxy(f"http://{SERVER_IP}:{SERVER_PORT}")

def enviar_movimiento(i, j, jugador):
    try:
        respuesta = server.realizar_movimiento(i, j, jugador)
        print("Respuesta del servidor:", respuesta)
        return respuesta
    except Exception as e:
        print("Error en la comunicación con el servidor:", e)
        return "Error"

#1 servidor y 2 clientes 

# 2 clientes -Clente/Servidor