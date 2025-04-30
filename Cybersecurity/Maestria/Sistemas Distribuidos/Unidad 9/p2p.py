import sys
import socket
import threading
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QInputDialog, QFileDialog)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QObject

# Clase para emitir señales de mensajes (para actualizar la GUI desde hilos de red)
class MessageSignal(QObject):
    message_received = pyqtSignal(str)  # Señal para mensajes de texto
    file_received = pyqtSignal(str, str)  # Señal para notificaciones de archivos recibidos

# Clase que maneja la parte de red (servidor o cliente)
class NetworkHandler:
    def __init__(self, mode, host, port, message_signal):
        self.mode = mode  # 'server' o 'client'
        self.host = host
        self.port = port
        self.message_signal = message_signal
        self.connections = []
        self.socket = None
        self.file_transfer = {
            'expecting_header': True,
            'file_name': None,
            'file_size': None,
            'bytes_received': 0,
            'file_data': bytearray()
        }

        if self.mode == 'server':
            self.groups = {}  # Diccionario de grupos

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
                if not data:
                    break

                message = data.decode('utf-8')
                print(f"Mensaje recibido: {message}")  # Depuración

                if message.startswith("/join_group "):
                    group_name = message[len("/join_group "):].strip()
                    if group_name not in self.groups:
                        self.groups[group_name] = set()
                    self.groups[group_name].add(conn)
                    confirmation = f"Te has unido al grupo '{group_name}'."
                    conn.send(confirmation.encode('utf-8'))
                    print(f"Conexión {conn.getpeername()} se unió al grupo '{group_name}'")
                elif message.startswith("/g "):
                    parts = message.split(" ", 2)
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
                                    c.send(full_msg.encode('utf-8'))
                                except Exception as e:
                                    print("Error al enviar a un cliente:", e)
                else:
                    self.message_signal.message_received.emit(message)
                    for c in self.connections:
                        if c != conn:
                            try:
                                c.send(message.encode('utf-8'))
                            except Exception as e:
                                print("Error al enviar a un cliente:", e)
            except Exception as e:
                print("Error en handle_client:", e)
                break
        conn.close()
        self.cleanup_connection(conn)

    def cleanup_connection(self, conn):
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
                if not data:
                    break

                message = data.decode('utf-8')
                print(f"Mensaje recibido: {message}")  # Depuración
                self.message_signal.message_received.emit(message)
            except Exception as e:
                print("Error en receive_messages:", e)
                break
        self.socket.close()

    def send_message(self, message):
        if self.mode == 'server':
            for conn in self.connections:
                try:
                    conn.send(message.encode('utf-8'))
                except Exception as e:
                    print("Error al enviar a un cliente:", e)
        else:
            try:
                self.socket.send(message.encode('utf-8'))
            except Exception as e:
                print("Error al enviar mensaje:", e)

    def send_file_data(self, file_data, header):
        if self.mode == 'server':
            for conn in self.connections:
                try:
                    conn.send(header.encode('utf-8') + file_data)
                except Exception as e:
                    print("Error al enviar archivo:", e)
        else:
            try:
                self.socket.send(header.encode('utf-8') + file_data)
            except Exception as e:
                print("Error al enviar archivo:", e)

# Ventana de chat global
class ChatWindow(QMainWindow):
    def __init__(self, mode, host, port):
        super().__init__()
        self.setWindowTitle("Chat P2P - Chat Global")
        self.resize(500, 600)
        self.mode = mode
        self.host = host
        self.port = port
        self.current_group = None
        self.username = self.get_username()
        self.message_signal = MessageSignal()
        self.network = NetworkHandler(self.mode, self.host, self.port, self.message_signal)
        self.group_windows = {}
        self.init_ui()
        self.message_signal.message_received.connect(self.display_message)
        self.message_signal.file_received.connect(self.display_file)

    def get_username(self):
        username, ok = QInputDialog.getText(self, "Nombre de Nodo", "Ingrese su nombre:")
        return username if ok and username else "Desconocido"

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Panel superior
        top_panel = QHBoxLayout()
        self.profile_pic = QLabel()
        self.profile_pic.setPixmap(QPixmap(50, 50))
        top_panel.addWidget(self.profile_pic)
        top_panel.addWidget(QLabel(self.username))
        self.image_button = QPushButton("Seleccionar Imagen")
        self.image_button.clicked.connect(self.select_image)
        top_panel.addWidget(self.image_button)
        self.group_input = QLineEdit(placeholderText="Nombre del grupo")
        top_panel.addWidget(self.group_input)
        self.join_button = QPushButton("Unirse al grupo")
        self.join_button.clicked.connect(self.join_group)
        top_panel.addWidget(self.join_button)
        layout.addLayout(top_panel)

        # Área de chat
        self.chat_area = QTextEdit(readOnly=True)
        layout.addWidget(self.chat_area)

        # Panel inferior
        bottom_panel = QHBoxLayout()
        self.message_input = QLineEdit()
        bottom_panel.addWidget(self.message_input)

        file_button = QPushButton("📁")
        file_button.clicked.connect(self.send_file)
        bottom_panel.addWidget(file_button)

        send_button = QPushButton("Enviar")
        send_button.clicked.connect(self.send_message)
        bottom_panel.addWidget(send_button)

        emoji_button = QPushButton("😊")
        emoji_button.clicked.connect(self.insert_emoji)
        bottom_panel.addWidget(emoji_button)

        layout.addLayout(bottom_panel)
        central_widget.setLayout(layout)

    def send_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo", "",
            "Todos los archivos (*);;Textos (*.txt);;Videos (*.mp4 *.avi *.mkv)",
            options=options
        )
        if file_path:
            threading.Thread(target=self.handle_file_sending, args=(file_path, None), daemon=True).start()

    def handle_file_sending(self, file_path, group_name):
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()

            file_name = os.path.basename(file_path)
            header = f"/file {file_name} {len(file_data)}\n"

            if group_name:
                header = f"/gfile {group_name} {file_name} {len(file_data)}\n"

            self.network.send_file_data(file_data, header)
            self.chat_area.append(f"[Archivo enviado] {file_name}")

        except Exception as e:
            self.chat_area.append(f"[Error] Fallo al enviar archivo: {str(e)}")

    def display_file(self, notification, file_path):
        self.chat_area.append(f"{notification} [Haz doble clic para abrir]")

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
        if not message.startswith("[Grupo:"):
            self.chat_area.append(message)

    def send_message(self):
        message = self.message_input.text().strip()
        if message:
            formatted_message = f"{self.username}: {message}"
            self.chat_area.append(formatted_message)
            self.network.send_message(formatted_message)
            self.message_input.clear()

    def insert_emoji(self):
        current_text = self.message_input.text()
        self.message_input.setText(current_text + "😊")

# Ventana de chat para grupo
class GroupChatWindow(QMainWindow):
    def __init__(self, group_name, network_handler, username):
        super().__init__()
        self.group_name = group_name
        self.network_handler = network_handler
        self.username = username
        self.init_ui()
        self.network_handler.message_signal.message_received.connect(self.handle_group_message)
        self.network_handler.message_signal.file_received.connect(self.display_group_file)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        self.chat_area = QTextEdit(readOnly=True)
        layout.addWidget(self.chat_area)

        bottom_panel = QHBoxLayout()
        self.message_input = QLineEdit()
        bottom_panel.addWidget(self.message_input)

        file_button = QPushButton("📁")
        file_button.clicked.connect(self.send_file)
        bottom_panel.addWidget(file_button)

        send_button = QPushButton("Enviar")
        send_button.clicked.connect(self.send_group_message)
        bottom_panel.addWidget(send_button)

        layout.addLayout(bottom_panel)
        central_widget.setLayout(layout)

    def send_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo", "",
            "Todos los archivos (*);;Textos (*.txt);;Videos (*.mp4 *.avi *.mkv)",
            options=options
        )
        if file_path:
            threading.Thread(target=self.handle_file_sending, args=(file_path,), daemon=True).start()

    def handle_file_sending(self, file_path):
        self.window().handle_file_sending(file_path, self.group_name)

    def display_group_file(self, notification, file_path):
        if f"[Grupo: {self.group_name}]" in notification:
            self.chat_area.append(f"{notification} [Haz doble clic para abrir]")

    def handle_group_message(self, message):
        prefix = f"[Grupo: {self.group_name}]"
        if message.startswith(prefix):
            self.chat_area.append(message)

    def send_group_message(self):
        message = self.message_input.text().strip()
        if message:
            group_command = f"/g {self.group_name} {self.username}: {message}"
            self.network_handler.send_message(group_command)
            self.chat_area.append(f"[Grupo: {self.group_name}] {self.username}: {message}")
            self.message_input.clear()

if __name__ == '__main__':
    mode = 'client'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    app = QApplication(sys.argv)
    window = ChatWindow(mode, "127.0.0.1", 5000)
    window.show()
    sys.exit(app.exec_())