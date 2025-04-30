import socket
import os
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading

# Configuración del nodo receptor
MI_IP = "127.0.0.1"
MI_PUERTO = 56433  # Nodo 2
CARPETA_DESTINO = "./videos_recibidos"
os.makedirs(CARPETA_DESTINO, exist_ok=True)

TAMANO_PAQUETE = 4096
DESPLAZAMIENTO_CESAR = 7

# Función de descifrado César para archivos binarios
def descifrar_cesar(datos, desplazamiento):
    return bytes((byte - desplazamiento) % 256 for byte in datos)

# Función para recibir archivos y descifrarlos
def iniciar_servidor_tcp():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((MI_IP, MI_PUERTO))
    server_socket.listen()
    print(f"Servidor TCP escuchando en {MI_IP}:{MI_PUERTO}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Conexión establecida con {addr}")

        try:
            metadata = conn.recv(1024).decode().strip()
            if "|" not in metadata:
                raise ValueError(f"Formato de metadatos incorrecto: {metadata}")

            nombre_archivo, tamano_archivo = metadata.split("|", 1)
            tamano_archivo = int(tamano_archivo.strip())

            print(f"Recibiendo archivo cifrado: {nombre_archivo}, Tamaño: {tamano_archivo} bytes")

            ruta_completa = os.path.join(CARPETA_DESTINO, nombre_archivo)
            with open(ruta_completa, "wb") as archivo:
                bytes_recibidos = 0
                while bytes_recibidos < tamano_archivo:
                    fragmento_cifrado = conn.recv(TAMANO_PAQUETE)
                    if not fragmento_cifrado:
                        break
                    fragmento_descifrado = descifrar_cesar(fragmento_cifrado, DESPLAZAMIENTO_CESAR)
                    archivo.write(fragmento_descifrado)
                    bytes_recibidos += len(fragmento_cifrado)

            print(f"Archivo {nombre_archivo} recibido y descifrado con éxito. Guardado en {ruta_completa}")

            # Iniciar la reproducción del video
            reproductor = VideoPlayer(ruta_completa)
            reproductor.run()

        except Exception as e:
            print(f"Error al recibir archivo: {e}")

# Clase para la GUI del reproductor de video
class VideoPlayer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.paused = False
        self.cap = cv2.VideoCapture(video_path)

        self.root = tk.Tk()
        self.root.title("Reproductor de Video")
        self.root.geometry("800x600")

        self.panel = tk.Label(self.root)
        self.panel.pack()

        self.btn_play_pause = tk.Button(self.root, text="Play/Pause", command=self.toggle_play)
        self.btn_play_pause.pack(side=tk.LEFT)

        self.btn_rewind = tk.Button(self.root, text="<<", command=self.rewind)
        self.btn_rewind.pack(side=tk.LEFT)

        self.btn_forward = tk.Button(self.root, text=">>", command=self.forward)
        self.btn_forward.pack(side=tk.LEFT)

        self.update_video()

    def toggle_play(self):
        self.paused = not self.paused

    def rewind(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, self.cap.get(cv2.CAP_PROP_POS_FRAMES) - 30))

    def forward(self):
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        new_pos = min(total_frames, self.cap.get(cv2.CAP_PROP_POS_FRAMES) + 30)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_pos)

    def update_video(self):
        if not self.paused:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)
                self.panel.config(image=frame)
                self.panel.image = frame
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reiniciar el video
        self.root.after(30, self.update_video)

    def run(self):
        self.root.mainloop()

# Iniciar el servidor en un hilo
if __name__ == "__main__":
    servidor = threading.Thread(target=iniciar_servidor_tcp)
    servidor.start()
