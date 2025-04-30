import tkinter as tk
from tkinter import scrolledtext
import threading
import argparse
import chat_p2p  # Importamos el archivo de lógica P2P

# Crear la interfaz gráfica
def crear_interfaz(mi_ip, mi_puerto):
    ventana = tk.Tk()
    ventana.title("Chat P2P")

    # Crear área de texto para mostrar mensajes
    text_area = scrolledtext.ScrolledText(ventana, width=50, height=15, wrap=tk.WORD)
    text_area.grid(row=0, column=0, padx=10, pady=10)
    text_area.config(state=tk.DISABLED)  # Hacer que el área de texto sea de solo lectura

    # Crear campo de entrada para el mensaje
    entry = tk.Entry(ventana, width=50)
    entry.grid(row=1, column=0, padx=10, pady=10)

    # Crear botón para enviar mensaje
    def enviar_mensaje():
        mensaje = entry.get()  # Obtener el mensaje desde el campo de entrada
        if mensaje:
            text_area.insert(tk.END, f"Tú: {mensaje}\n")
            text_area.yview(tk.END)  # Desplazar hacia abajo automáticamente
            entry.delete(0, tk.END)  # Limpiar el campo de entrada
            threading.Thread(target=chat_p2p.iniciar_cliente_tcp, args=(mi_ip, mi_puerto, mensaje)).start()

    boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_mensaje)
    boton_enviar.grid(row=2, column=0, padx=10, pady=10)

    # Función para recibir mensajes del servidor y actualizarlos en la interfaz
    def recibir_mensaje(mensaje):
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"{mensaje}\n")
        text_area.yview(tk.END)
        text_area.config(state=tk.DISABLED)

    # Crear e iniciar el hilo del servidor
    hilo_servidor = threading.Thread(target=chat_p2p.iniciar_servidor_tcp, args=(mi_ip, mi_puerto, recibir_mensaje), daemon=True)
    hilo_servidor.start()

    # Ejecutar la interfaz gráfica
    ventana.mainloop()

if __name__ == "__main__":
    # Argumentos de línea de comandos para configurar IP y puerto
    parser = argparse.ArgumentParser(description="Nodo P2P tipo chat.")
    parser.add_argument("--puerto", type=int, required=True, help="Puerto en el que este nodo escuchará conexiones.")
    args = parser.parse_args()

    MI_IP = "127.0.0.1"  # Dirección IP fija para este ejemplo
    MI_PUERTO = args.puerto

    # Crear e iniciar la interfaz gráfica
    crear_interfaz(MI_IP, MI_PUERTO)
