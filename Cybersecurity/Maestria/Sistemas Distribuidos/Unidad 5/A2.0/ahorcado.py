# ahorcado.py
import tkinter as tk
from tkinter import messagebox
import threading
from p2p import iniciar_servidor_tcp, iniciar_cliente_tcp
import sys

class Ahorcado:
    def __init__(self, root, mi_ip, mi_puerto):
        self.root = root
        self.root.title("Juego del Ahorcado")

        self.mi_ip = mi_ip
        self.mi_puerto = mi_puerto

        # Palabra fija directamente en ahorcado.py
        self.palabra = "seguridad"  # Cambia esta palabra si deseas otra
        self.intentos = 6
        self.letras_usadas = []
        self.letras_correctas = []

        # Iniciar servidor en un hilo separado
        threading.Thread(target=iniciar_servidor_tcp, args=(mi_ip, mi_puerto, self.recibir_mensaje), daemon=True).start()

        # Interfaz gráfica
        self.label_palabra = tk.Label(self.root, text="_ " * len(self.palabra), font=("Helvetica", 18))
        self.label_palabra.pack(pady=20)

        self.entry_letra = tk.Entry(self.root, font=("Helvetica", 18))
        self.entry_letra.pack(pady=20)
        self.entry_letra.bind("<Return>", self.verificar_letra)

        self.label_intentos = tk.Label(self.root, text=f"Intentos restantes: {self.intentos}", font=("Helvetica", 18))
        self.label_intentos.pack(pady=20)

    def recibir_mensaje(self, mensaje):
        """Recibe una letra de otro nodo y actualiza el estado."""
        letra = mensaje.strip().lower()
        if letra in self.letras_usadas:
            return
        self.letras_usadas.append(letra)
        self.actualizar_estado(letra)

    def verificar_letra(self, event):
        """Envía la letra ingresada a todos los nodos y actualiza localmente."""
        letra = self.entry_letra.get().lower()
        self.entry_letra.delete(0, tk.END)

        if letra in self.letras_usadas:
            messagebox.showinfo("Ahorcado", "Ya has usado esta letra.")
            return

        self.letras_usadas.append(letra)
        iniciar_cliente_tcp(self.mi_ip, self.mi_puerto, letra)
        self.actualizar_estado(letra)

    def actualizar_estado(self, letra):
        """Actualiza la interfaz según la letra recibida."""
        if letra in self.palabra:
            self.letras_correctas.append(letra)
            self.actualizar_palabra()
            if all(l in self.letras_correctas for l in self.palabra):
                messagebox.showinfo("Ahorcado", "¡Ganaste!")
                self.root.quit()
        else:
            self.intentos -= 1
            self.label_intentos.config(text=f"Intentos restantes: {self.intentos}")
            if self.intentos == 0:
                messagebox.showinfo("Ahorcado", f"¡Perdiste! La palabra era '{self.palabra}'")
                self.root.quit()

    def actualizar_palabra(self):
        """Muestra la palabra con las letras adivinadas."""
        texto = " ".join([l if l in self.letras_correctas else "_" for l in self.palabra])
        self.label_palabra.config(text=texto)

if __name__ == "__main__":
    mi_ip = sys.argv[1]
    mi_puerto = int(sys.argv[2])

    root = tk.Tk()
    juego = Ahorcado(root, mi_ip, mi_puerto)
    root.mainloop()
