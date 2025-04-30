
import tkinter as tk
import threading
import sys
import time
from p2p import iniciar_servidor_tcp, iniciar_cliente_tcp

# Variables globales
tablero = [["" for _ in range(3)] for _ in range(3)]
turno_actual = "X"
botones = []
mi_ip = "127.0.0.1"
mi_puerto = int(sys.argv[1])  # Tomar el puerto desde la línea de comandos

# Función para actualizar el turno en la interfaz
def actualizar_turno(turno_label):
    turno_label.config(text=f"Turno: {turno_actual}")

# Función para manejar movimientos en el tablero
def realizar_movimiento(i, j, boton, turno_label):
    global turno_actual
    if tablero[i][j] == "":
        tablero[i][j] = turno_actual
        boton.config(text=turno_actual, state="disabled")

        # Enviar movimiento a la red
        mensaje = f"{i},{j},{turno_actual}"
        iniciar_cliente_tcp(mi_ip, mi_puerto, mensaje)

        if verificar_ganador():
            turno_label.config(text=f"¡Ganador: {turno_actual}!")
            deshabilitar_tablero()
        else:
            turno_actual = "O" if turno_actual == "X" else "X"
            actualizar_turno(turno_label)

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

# Función para deshabilitar el tablero cuando hay un ganador
def deshabilitar_tablero():
    for fila in botones:
        for boton in fila:
            boton.config(state="disabled")

# Función para procesar los mensajes recibidos desde la red
def procesar_mensaje(mensaje):
    global turno_actual
    print("Mensaje recibido:", mensaje)
    
    try:
        i, j, jugador = mensaje.split(",")
        i, j = int(i), int(j)
        
        if tablero[i][j] == "":
            tablero[i][j] = jugador
            botones[i][j].config(text=jugador, state="disabled")

            if verificar_ganador():
                turno_label.config(text=f"¡Ganador: {jugador}!")
                deshabilitar_tablero()
            else:
                turno_actual = "O" if turno_actual == "X" else "X"
                actualizar_turno(turno_label)
    except Exception as e:
        print("Error al procesar mensaje:", e)

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

# Iniciar el servidor en un hilo separado
servidor_hilo = threading.Thread(target=iniciar_servidor_tcp, args=(mi_ip, mi_puerto, procesar_mensaje), daemon=True)
servidor_hilo.start()

# Esperar antes de empezar para que ambos servidores estén listos
print(f"Esperando a que el otro jugador inicie...")
time.sleep(5)

# Crear la interfaz
crear_interfaz()
