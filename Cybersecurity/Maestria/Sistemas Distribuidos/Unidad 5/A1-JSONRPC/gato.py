import tkinter as tk
import threading
import sys
from jsonrpclib import Server
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

# Variables globales
tablero = [["" for _ in range(3)] for _ in range(3)]
turno_actual = "X"
botones = []
mi_puerto = int(sys.argv[1])  # Puerto de este jugador
puerto_remoto = 5001 if mi_puerto == 5000 else 5000  # Puerto del otro jugador

# Servidor JSON-RPC para recibir movimientos
server_rpc = SimpleJSONRPCServer(("127.0.0.1", mi_puerto))

# Cliente JSON-RPC para enviar movimientos al otro jugador
cliente_rpc = Server(f"http://127.0.0.1:{puerto_remoto}")

# Función para manejar movimientos en el tablero
def realizar_movimiento(i, j, boton, turno_label):
    global turno_actual
    if tablero[i][j] == "":
        tablero[i][j] = turno_actual
        boton.config(text=turno_actual, state="disabled")

        # Enviar movimiento al otro jugador
        try:
            cliente_rpc.recibir_movimiento(i, j, turno_actual)
        except Exception as e:
            print(f"⚠️ Error enviando movimiento: {e}")

        if verificar_ganador():
            turno_label.config(text=f"¡Ganador: {turno_actual}!")
            deshabilitar_tablero()
        else:
            turno_actual = "O" if turno_actual == "X" else "X"
            actualizar_turno(turno_label)

# Función para recibir movimientos desde la red
def recibir_movimiento(i, j, jugador):
    global turno_actual
    print(f"✅ Movimiento recibido: ({i}, {j}) - {jugador}")

    if tablero[i][j] == "":
        tablero[i][j] = jugador
        botones[i][j].config(text=jugador, state="disabled")

        if verificar_ganador():
            turno_label.config(text=f"¡Ganador: {jugador}!")
            deshabilitar_tablero()
        else:
            turno_actual = "O" if turno_actual == "X" else "X"
            actualizar_turno(turno_label)

# Registrar la función en el servidor
server_rpc.register_function(recibir_movimiento, "recibir_movimiento")

# Iniciar el servidor en un hilo separado
def iniciar_servidor():
    print(f"🖥️ Servidor escuchando en el puerto {mi_puerto}...")
    server_rpc.serve_forever()

servidor_hilo = threading.Thread(target=iniciar_servidor, daemon=True)
servidor_hilo.start()

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

# Función para actualizar el turno en la interfaz
def actualizar_turno(turno_label):
    turno_label.config(text=f"Turno: {turno_actual}")

# Función para deshabilitar el tablero cuando hay un ganador
def deshabilitar_tablero():
    for fila in botones:
        for boton in fila:
            boton.config(state="disabled")

# Función para crear la interfaz gráfica
def crear_interfaz():
    global botones, turno_label
    ventana = tk.Tk()
    ventana.title(f"Juego del Gato - Jugador {mi_puerto}")
    ventana.geometry("300x350")

    turno_label = tk.Label(ventana, text="Turno: X", font=("Arial", 14))
    turno_label.pack(pady=10)

    marco = tk.Frame(ventana)
    marco.pack()

    botones = []
    for i in range(3):
        fila = []
        for j in range(3):
            boton = tk.Button(marco, text="", font=("Arial", 24), width=5, height=2,
                              command=lambda i=i, j=j: realizar_movimiento(i, j, botones[i][j], turno_label))
            boton.grid(row=i, column=j)
            fila.append(boton)
        botones.append(fila)

    ventana.mainloop()

# Crear la interfaz
crear_interfaz()
