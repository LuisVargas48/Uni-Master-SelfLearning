import socket
import threading
import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QInputDialog, QFileDialog)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QObject

# --- Protocolo:
# Global: el archivo se envía con header "[Archivo:<file_size>]"
# Grupo: se envía con header "[GrupoArchivo:<group_name>:<file_size>]"
# El receptor detecta el header, lee los bytes indicados y reenvía según corresponda.
# ------------------------------------------------------------------------------

# Clase para emitir señales de mensajes (para actualizar la GUI desde hilos de red)
class MessageSignal(QObject):
    message_received = pyqtSignal(str)

# Clase que maneja la parte de red (servidor o cliente)
class NetworkHandler:
    def __init__(self, mode, host, port, message_signal):
        self.mode = mode  # 'server' o 'client'
        self.host = host
        self.port = port
        self.message_signal = message_signal
        self.connections = []
        self.socket = None

        # Para el servidor: diccionario de grupos: nombre -> conjunto de conexiones
        if self.mode == 'server':
            self.groups = {}  # { grupo: set(conexiones) }

        if self.mode == 'server':
            self.start_server()
        else:
            self.start_client()

    def start_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Servidor iniciado en {self.host}:{self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            conn, addr = self.socket.accept()
            print(f"Conexión aceptada de {addr}")
            self.connections.append(conn)
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                if data:
                    # Revisar si se trata de envío de archivo global o de grupo
                    header = data.decode('utf-8', errors='ignore')
                    if header.startswith("[Archivo:"):
                        try:
                            file_size = int(header[len("[Archivo:"):header.find("]")])
                        except Exception as e:
                            print("Error parseando header de archivo global:", e)
                            continue
                        file_data = b""
                        while len(file_data) < file_size:
                            file_data += conn.recv(4096)
                        save_path = os.path.join("received_files", "global_received_file")
                        os.makedirs("received_files", exist_ok=True)
                        with open(save_path, "wb") as f:
                            f.write(file_data)
                        self.message_signal.message_received.emit(f"[Archivo: {save_path}]")
                        continue
                    elif header.startswith("[GrupoArchivo:"):
                        try:
                            inner = header[len("[GrupoArchivo:"):header.find("]")]
                            group_name, file_size_str = inner.split(":", 1)
                            file_size = int(file_size_str)
                        except Exception as e:
                            print("Error parseando header de archivo de grupo:", e)
                            continue
                        file_data = b""
                        while len(file_data) < file_size:
                            file_data += conn.recv(4096)
                        full_data = header[:header.find("]")+1].encode('utf-8') + file_data
                        if group_name in self.groups:
                            for c in self.groups[group_name]:
                                if c != conn:
                                    try:
                                        c.sendall(full_data)
                                    except Exception as e:
                                        print("Error al enviar archivo de grupo:", e)
                        self.message_signal.message_received.emit(f"[GrupoArchivo: {group_name} archivo recibido]")
                        continue
                    # Procesar comandos de grupos
                    text = data.decode('utf-8')
                    if text.startswith("/join_group "):
                        group_name = text[len("/join_group "):].strip()
                        if group_name not in self.groups:
                            self.groups[group_name] = set()
                        self.groups[group_name].add(conn)
                        confirmation = f"Te has unido al grupo '{group_name}'."
                        conn.sendall(confirmation.encode('utf-8'))
                        print(f"Conexión {conn.getpeername()} se unió al grupo '{group_name}'")
                        continue
                    elif text.startswith("/g "):
                        parts = text.split(" ", 2)
                        if len(parts) < 3:
                            continue
                        group_name = parts[1].strip()
                        group_msg = parts[2].strip()
                        full_msg = f"[Grupo: {group_name}] {group_msg}"
                        self.message_signal.message_received.emit(full_msg)
                        if group_name in self.groups:
                            for c in self.groups[group_name]:
                                if c != conn:
                                    try:
                                        c.sendall(full_msg.encode('utf-8'))
                                    except Exception as e:
                                        print("Error al enviar mensaje de grupo:", e)
                        continue
                    else:
                        # Mensaje global
                        self.message_signal.message_received.emit(text)
                        for c in self.connections:
                            if c != conn:
                                try:
                                    c.sendall(data)
                                except Exception as e:
                                    print("Error al enviar mensaje global:", e)
                else:
                    break
            except Exception as e:
                print("Error en handle_client:", e)
                break
        conn.close()
        if conn in self.connections:
            self.connections.remove(conn)
        if self.mode == 'server':
            for group in list(self.groups.keys()):
                if conn in self.groups[group]:
                    self.groups[group].remove(conn)
                    if not self.groups[group]:
                        del self.groups[group]

    def start_client(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            print(f"Conectado al servidor en {self.host}:{self.port}")
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print("Error al conectar:", e)

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(4096)
                if data:
                    self.message_signal.message_received.emit(data.decode('utf-8', errors='ignore'))
                else:
                    break
            except Exception as e:
                print("Error en receive_messages:", e)
                break
        self.socket.close()

    def send_message(self, message):
        try:
            if self.mode == 'server':
                for conn in self.connections:
                    conn.sendall(message.encode('utf-8'))
            else:
                self.socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print("Error al enviar mensaje:", e)

    def send_file(self, file_path):
        try:
            file_size = os.path.getsize(file_path)
            header = f"[Archivo:{file_size}]"
            self.socket.sendall(header.encode('utf-8'))
            with open(file_path, "rb") as f:
                while (chunk := f.read(4096)):
                    self.socket.sendall(chunk)
        except Exception as e:
            print(f"Error al enviar archivo global: {e}")

    def send_group_file(self, file_path, group_name):
        try:
            file_size = os.path.getsize(file_path)
            header = f"[GrupoArchivo:{group_name}:{file_size}]"
            self.socket.sendall(header.encode('utf-8'))
            with open(file_path, "rb") as f:
                while (chunk := f.read(4096)):
                    self.socket.sendall(chunk)
        except Exception as e:
            print(f"Error al enviar archivo de grupo: {e}")

# Ventana de chat global
class ChatWindow(QMainWindow):
    def __init__(self, mode, host, port):
        super().__init__()
        self.setWindowTitle("Chat P2P - Chat Global")
        self.resize(500, 600)
        self.mode = mode
        self.host = host
        self.port = port

        username, ok = QInputDialog.getText(self, "Nombre de Nodo", "Ingrese su nombre:")
        self.username = username if ok and username else "Desconocido"

        self.message_signal = MessageSignal()
        self.message_signal.message_received.connect(self.display_message)

        self.network = NetworkHandler(self.mode, self.host, self.port, self.message_signal)

        self.init_ui()
        self.group_windows = {}

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        top_panel = QHBoxLayout()
        self.profile_pic = QLabel()
        pixmap = QPixmap(50, 50)
        pixmap.fill()
        self.profile_pic.setPixmap(pixmap)
        top_panel.addWidget(self.profile_pic)

        self.contact_label = QLabel(self.username)
        top_panel.addWidget(self.contact_label)

        self.image_button = QPushButton("Seleccionar Imagen")
        self.image_button.clicked.connect(self.select_image)
        top_panel.addWidget(self.image_button)

        self.group_input = QLineEdit()
        self.group_input.setPlaceholderText("Nombre del grupo")
        top_panel.addWidget(self.group_input)
        self.join_button = QPushButton("Unirse al grupo")
        self.join_button.clicked.connect(self.join_group)
        top_panel.addWidget(self.join_button)

        top_panel.addStretch()
        layout.addLayout(top_panel)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        layout.addWidget(self.chat_area)

        bottom_panel = QHBoxLayout()
        self.message_input = QLineEdit()
        bottom_panel.addWidget(self.message_input)
        send_button = QPushButton("Enviar")
        send_button.clicked.connect(self.send_message)
        bottom_panel.addWidget(send_button)
        emoji_button = QPushButton("😊")
        emoji_button.clicked.connect(self.insert_emoji)
        bottom_panel.addWidget(emoji_button)
        file_button = QPushButton("Enviar Archivo")
        file_button.clicked.connect(self.send_file)
        bottom_panel.addWidget(file_button)
        layout.addLayout(bottom_panel)

        central_widget.setLayout(layout)

    def select_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona Imagen", "",
                                                  "Images (*.png *.jpg *.bmp *.gif);;All Files (*)",
                                                  options=options)
        if fileName:
            pixmap = QPixmap(fileName).scaled(50, 50)
            self.profile_pic.setPixmap(pixmap)

    def join_group(self):
        group_name = self.group_input.text().strip()
        if group_name:
            self.network.send_message(f"/join_group {group_name}")
            self.chat_area.append(f"[Sistema] Te has unido al grupo '{group_name}'.")
            self.group_input.clear()
            if group_name not in self.group_windows:
                group_window = GroupChatWindow(group_name, self.network, self.username)
                self.group_windows[group_name] = group_window
                group_window.show()

    def display_message(self, message):
        # Mostrar en chat global (incluye echo)
        if not message.startswith("[Grupo:"):
            self.chat_area.append(message)

    def send_message(self):
        message = self.message_input.text().strip()
        if message:
            formatted_message = f"{self.username}: {message}"
            # Agregamos el mensaje en la ventana del remitente
            self.chat_area.append(formatted_message)
            self.network.send_message(formatted_message)
            self.message_input.clear()

    def insert_emoji(self):
        current_text = self.message_input.text()
        self.message_input.setText(current_text + "😊")

    def send_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona Archivo", "",
                                                  "All Files (*)")
        if fileName:
            self.network.send_file(fileName)
            self.chat_area.append(f"[Sistema] Enviando archivo: {os.path.basename(fileName)}...")

# Ventana de chat para grupo
class GroupChatWindow(QMainWindow):
    def __init__(self, group_name, network_handler, username):
        super().__init__()
        self.group_name = group_name
        self.network = network_handler
        self.username = username
        self.setWindowTitle(f"Chat Grupo: {group_name}")
        self.resize(500, 600)

        self.init_ui()
        self.network.message_signal.message_received.connect(self.handle_group_message)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        layout.addWidget(self.chat_area)

        bottom_panel = QHBoxLayout()
        self.message_input = QLineEdit()
        bottom_panel.addWidget(self.message_input)
        send_button = QPushButton("Enviar")
        send_button.clicked.connect(self.send_message)
        bottom_panel.addWidget(send_button)
        emoji_button = QPushButton("😊")
        emoji_button.clicked.connect(self.insert_emoji)
        bottom_panel.addWidget(emoji_button)
        file_button = QPushButton("Enviar Archivo")
        file_button.clicked.connect(self.send_group_file)
        bottom_panel.addWidget(file_button)
        layout.addLayout(bottom_panel)

        central_widget.setLayout(layout)

    def handle_group_message(self, message):
        prefix = f"[Grupo: {self.group_name}]"
        if message.startswith(prefix):
            self.chat_area.append(message)

    def send_message(self):
        message = self.message_input.text().strip()
        if message:
            command = f"/g {self.group_name} {self.username}: {message}"
            # Mostrar el mensaje en la ventana del remitente
            self.chat_area.append(f"[Grupo: {self.group_name}] {self.username}: {message}")
            self.network.send_message(command)
            self.message_input.clear()

    def insert_emoji(self):
        current_text = self.message_input.text()
        self.message_input.setText(current_text + "😊")

    def send_group_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona Archivo", "",
                                                  "All Files (*)")
        if fileName:
            self.network.send_group_file(fileName, self.group_name)
            self.chat_area.append(f"[Sistema] Enviando archivo al grupo: {os.path.basename(fileName)}...")

if __name__ == '__main__':
    mode = 'client'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    host = "127.0.0.1"  # Para pruebas en la misma máquina
    port = 5000
    app = QApplication(sys.argv)
    window = ChatWindow(mode, host, port)
    window.show()
    sys.exit(app.exec_())