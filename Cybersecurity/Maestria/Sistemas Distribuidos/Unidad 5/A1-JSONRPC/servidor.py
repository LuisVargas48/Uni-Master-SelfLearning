from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

# Variables globales
tablero = [["" for _ in range(3)] for _ in range(3)]
turno_actual = "X"

# Función remota: realizar un movimiento
def realizar_movimiento_rpc(i, j, jugador):
    global turno_actual
    if tablero[i][j] == "":
        tablero[i][j] = jugador
        if verificar_ganador():
            return f"¡Ganador: {jugador}!"
        turno_actual = "O" if jugador == "X" else "X"
        return "OK"
    return "Movimiento inválido"

# Función para verificar si hay un ganador
def verificar_ganador():
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != "":
            return True
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != "":
            return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != "":
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != "":
        return True
    return False

# Iniciar servidor JSON-RPC
def iniciar_servidor(ip="0.0.0.0", puerto=5000):
    server = SimpleJSONRPCServer((ip, puerto))
    server.register_function(realizar_movimiento_rpc, "realizar_movimiento")
    print(f"Servidor JSON-RPC escuchando en {ip}:{puerto}...")
    server.serve_forever()

if __name__ == "__main__":
    iniciar_servidor()
