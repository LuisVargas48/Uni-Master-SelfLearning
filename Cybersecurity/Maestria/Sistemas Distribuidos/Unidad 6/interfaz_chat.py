# interfaz_chat.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import argparse
import chat_p2p

# ======== INTERFAZ DE AUTENTICACIÓN ========
def crear_interfaz_autenticacion(mi_ip, mi_puerto, callback):
    ventana = tk.Tk()
    ventana.title("Autenticación")

    tk.Label(ventana, text="Usuario:").grid(row=0, column=0, padx=10, pady=5)
    usuario_entry = tk.Entry(ventana, width=30)
    usuario_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Contraseña:").grid(row=1, column=0, padx=10, pady=5)
    contraseña_entry = tk.Entry(ventana, width=30, show="*")
    contraseña_entry.grid(row=1, column=1, padx=10, pady=5)

    def autenticar():
        usuario = usuario_entry.get()
        contraseña = contraseña_entry.get()
        if chat_p2p.autenticar_usuario(usuario, contraseña):
            ventana.destroy()
            callback(mi_ip, mi_puerto, usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    tk.Button(ventana, text="Iniciar Sesión", command=autenticar).grid(row=2, column=0, columnspan=2, pady=10)
    ventana.mainloop()

# ======== INTERFAZ DE CHAT ========
def crear_interfaz_chat(mi_ip, mi_puerto, usuario):
    ventana = tk.Tk()
    ventana.title(f"Chat P2P - {usuario}")

    text_area = scrolledtext.ScrolledText(ventana, width=50, height=15, wrap=tk.WORD)
    text_area.grid(row=0, column=0, padx=10, pady=10)
    text_area.config(state=tk.DISABLED)

    entry = tk.Entry(ventana, width=50)
    entry.grid(row=1, column=0, padx=10, pady=5)

    def enviar_mensaje():
        mensaje = entry.get()
        if mensaje:
            # Mostrar mensaje cifrado en la interfaz antes de enviarlo
            mensaje_cifrado = chat_p2p.cifrar_cesar(mensaje, 3)
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, f"Tú (cifrado): {mensaje_cifrado}\n")
            text_area.config(state=tk.DISABLED)
            entry.delete(0, tk.END)

            # Enviar mensaje cifrado
            threading.Thread(target=chat_p2p.iniciar_cliente_tcp, args=(mi_ip, mi_puerto, usuario, mensaje, 3)).start()

    tk.Button(ventana, text="Enviar", command=enviar_mensaje).grid(row=2, column=0, padx=10, pady=10)

    # Función para recibir mensajes
    def recibir_mensaje(mensaje):
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"{mensaje}\n")
        text_area.config(state=tk.DISABLED)

    # Hilo para escuchar mensajes
    hilo_servidor = threading.Thread(
        target=chat_p2p.iniciar_servidor_tcp,
        args=(mi_ip, mi_puerto, recibir_mensaje, 3),
        daemon=True
    )
    hilo_servidor.start()

    ventana.mainloop()

# ======== EJECUCIÓN PRINCIPAL ========
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat P2P con autenticación y cifrado César.")
    parser.add_argument("--puerto", type=int, required=True, help="Puerto del nodo.")
    args = parser.parse_args()

    MI_IP = "127.0.0.1"
    MI_PUERTO = args.puerto

    crear_interfaz_autenticacion(MI_IP, MI_PUERTO, crear_interfaz_chat)
