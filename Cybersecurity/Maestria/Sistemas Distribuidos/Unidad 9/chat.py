
import sys
import socket
import threading
import os
import base64
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QInputDialog, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QObject
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

# Clave de cifrado (32 bytes). En un sistema real, se debe intercambiar de forma segura.
ENCRYPTION_KEY = b'0123456789abcdef0123456789abcdef'

def encrypt_message(message: str) -> str:
    nonce = get_random_bytes(8)
    cipher = ChaCha20.new(key=ENCRYPTION_KEY, nonce=nonce)
    ciphertext = cipher.encrypt(message.encode('utf-8'))
    combined = nonce + ciphertext
    # Se codifica en base64 y se envuelve con marcador ENC(...)
    return "ENC(" + base64.b64encode(combined).decode('utf-8') + ")"

def decrypt_message(enc_message: str) -> str:
    if enc_message.startswith("ENC(") and enc_message.endswith(")"):
        b64data = enc_message[4:-1]
        combined = base64.b64decode(b64data)
        nonce = combined[:8]
        ciphertext = combined[8:]
        cipher = ChaCha20.new(key=ENCRYPTION_KEY, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode('utf-8')
    else:
        return enc_message

# Funciones de cifrado para archivos (trabajan con bytes)
def encrypt_bytes(data: bytes) -> bytes:
    nonce = get_random_bytes(8)
    cipher = ChaCha20.new(key=ENCRYPTION_KEY, nonce=nonce)
    return nonce + cipher.encrypt(data)

def decrypt_bytes(enc_data: bytes) -> bytes:
    nonce = enc_data[:8]
    ciphertext = enc_data[8:]
    cipher = ChaCha20.new(key=ENCRYPTION_KEY, nonce=nonce)
    return cipher.decrypt(ciphertext)

# --- Clases de red y GUI ---

class MessageSignal(QObject):
    message_received = pyqtSignal(str)

class NetworkHandler:
    def __init__(self, mode, host, port, message_signal):
        self.mode = mode  # 'server' o 'client'
        self.host = host
        self.port = port
        self.message_signal = message_signal
        self.connections = []
        self.socket = None
        if self.mode == 'server':
            self.groups = {}  # { grupo: set(conexiones) }
            self.client_names = {}  # { socket: username }
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

    def broadcast_client_list(self):
        list_str = ",".join(self.client_names.get(c, "") for c in self.connections if c in self.client_names)
        command = "/client_list " + list_str
        for c in self.connections:
            try:
                c.sendall(command.encode('utf-8'))
            except Exception as e:
                print("Error al enviar lista de clientes:", e)

    def handle_client(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                if data:
                    text = data.decode('utf-8', errors='ignore')
                    # Manejo de archivos global cifrado
                    if text.startswith("[ArchivoEncrypted:"):
                        try:
                            file_size = int(text[len("[ArchivoEncrypted:"):text.find("]")])
                        except Exception as e:
                            print("Error parseando header de archivo global encriptado:", e)
                            continue
                        file_data = b""
                        while len(file_data) < file_size:
                            file_data += conn.recv(4096)
                        decrypted_data = decrypt_bytes(file_data)
                        os.makedirs("received_files", exist_ok=True)
                        save_path = os.path.join("received_files", "global_received_file")
                        with open(save_path, "wb") as f:
                            f.write(decrypted_data)
                        self.message_signal.message_received.emit(f"[Archivo: {save_path}]")
                        continue
                    # Manejo de archivos de grupo cifrado
                    elif text.startswith("[GrupoArchivoEncrypted:"):
                        try:
                            inner = text[len("[GrupoArchivoEncrypted:"):text.find("]")]
                            group_name, file_size_str = inner.split(":", 1)
                            file_size = int(file_size_str)
                        except Exception as e:
                            print("Error parseando header de archivo de grupo encriptado:", e)
                            continue
                        file_data = b""
                        while len(file_data) < file_size:
                            file_data += conn.recv(4096)
                        decrypted_data = decrypt_bytes(file_data)
                        os.makedirs("received_files", exist_ok=True)
                        save_path = os.path.join("received_files", f"group_{group_name}_received_file")
                        with open(save_path, "wb") as f:
                            f.write(decrypted_data)
                        self.message_signal.message_received.emit(f"[GrupoArchivo: {group_name} archivo recibido: {save_path}]")
                        continue
                    # Comando de login
                    if text.startswith("/login "):
                        username = text[len("/login "):].strip()
                        self.client_names[conn] = username
                        print(f"Login de {username} desde {conn.getpeername()}")
                        self.broadcast_client_list()
                        continue
                    # Comando de lista de clientes (no se reenvía al chat)
                    if text.startswith("/client_list "):
                        continue
                    # Comandos de grupo (no modificados)
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
                    # Nuevo comando para mensaje uno a uno
                    elif text.startswith("/msg "):
                        parts = text.split(" ", 2)
                        if len(parts) < 3:
                            continue
                        target = parts[1].strip()
                        msg_body = parts[2]
                        found = False
                        for c in self.connections:
                            if c in self.client_names and self.client_names[c] == target:
                                try:
                                    c.sendall(text.encode('utf-8'))
                                    found = True
                                except Exception as e:
                                    print("Error al enviar mensaje uno a uno:", e)
                                break
                        if not found:
                            try:
                                conn.sendall(f"[Sistema] El usuario '{target}' no está conectado.".encode('utf-8'))
                            except Exception as e:
                                print("Error al enviar aviso de usuario no conectado:", e)
                        continue
                    else:
                        conn.sendall("[Sistema] Usa el botón 'Enviar a:' para mensajes uno a uno.".encode('utf-8'))
                else:
                    break
            except Exception as e:
                print("Error en handle_client:", e)
                break
        conn.close()
        if conn in self.connections:
            self.connections.remove(conn)
        if self.mode == 'server':
            if conn in self.client_names:
                del self.client_names[conn]
            for group in list(self.groups.keys()):
                if conn in self.groups[group]:
                    self.groups[group].remove(conn)
                    if not self.groups[group]:
                        del self.groups[group]
            self.broadcast_client_list()

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
                if message.startswith("/"):
                    self.socket.sendall(message.encode('utf-8'))
                else:
                    enc_msg = encrypt_message(message)
                    self.socket.sendall(enc_msg.encode('utf-8'))
        except Exception as e:
            print("Error al enviar mensaje:", e)

    def send_file(self, file_path):
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
            encrypted_data = encrypt_bytes(file_data)
            file_size = len(encrypted_data)
            header = f"[ArchivoEncrypted:{file_size}]"
            self.socket.sendall(header.encode('utf-8'))
            self.socket.sendall(encrypted_data)
        except Exception as e:
            print(f"Error al enviar archivo global: {e}")

    def send_group_file(self, file_path, group_name):
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
            encrypted_data = encrypt_bytes(file_data)
            file_size = len(encrypted_data)
            header = f"[GrupoArchivoEncrypted:{group_name}:{file_size}]"
            self.socket.sendall(header.encode('utf-8'))
            self.socket.sendall(encrypted_data)
        except Exception as e:
            print(f"Error al enviar archivo de grupo: {e}")

class ChatWindow(QMainWindow):
    def __init__(self, mode, host, port):
        super().__init__()
        self.setWindowTitle("Chat P2P - Chat Global")
        self.resize(500, 600)
        self.mode = mode
        self.host = host
        self.port = port
        self.current_target = None  # Destinatario seleccionado para 1 a 1
        self.client_list = []       # Lista de clientes conectados

        username, ok = QInputDialog.getText(self, "Nombre de Nodo", "Ingrese su nombre:")
        self.username = username if ok and username else "Desconocido"

        self.message_signal = MessageSignal()
        self.message_signal.message_received.connect(self.display_message)

        self.network = NetworkHandler(self.mode, self.host, self.port, self.message_signal)

        # Enviar login al servidor (solo en modo cliente)
        if self.mode != 'server':
            self.network.send_message(f"/login {self.username}")

        self.init_ui()
        self.group_windows = {}

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Panel superior con imagen, nombre y botones
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

        # Botón para unirse a grupos
        self.group_input = QLineEdit()
        self.group_input.setPlaceholderText("Nombre del grupo")
        top_panel.addWidget(self.group_input)
        self.join_button = QPushButton("Unirse al grupo")
        self.join_button.clicked.connect(self.join_group)
        top_panel.addWidget(self.join_button)

        # Botón "Enviar a:" para mensajes uno a uno
        self.send_to_button = QPushButton("Enviar a:")
        self.send_to_button.clicked.connect(self.select_target)
        top_panel.addWidget(self.send_to_button)

        # Etiqueta para mostrar el destinatario seleccionado
        self.target_label = QLabel("Destinatario: Ninguno")
        top_panel.addWidget(self.target_label)

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
        # Botón para borrar la conversación
        clear_button = QPushButton("Borrar conversación")
        clear_button.clicked.connect(self.clear_conversation)
        bottom_panel.addWidget(clear_button)
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

    def select_target(self):
        # Mostrar diálogo con la lista de clientes conectados (excluyendo el propio)
        lista = [cliente for cliente in self.client_list if cliente != self.username]
        if not lista:
            QMessageBox.information(self, "Información", "No hay otros clientes conectados.")
            return
        target, ok = QInputDialog.getItem(self, "Seleccionar destinatario", "Enviar a:", lista, 0, False)
        if ok and target:
            self.current_target = target
            self.target_label.setText(f"Destinatario: {target}")

    def display_message(self, message):
        # Actualizar lista de clientes si se recibe el comando
        if message.startswith("/client_list "):
            list_str = message[len("/client_list "):].strip()
            self.client_list = list_str.split(",") if list_str else []
            return
        # Procesar mensajes uno a uno (comando /msg)
        if message.startswith("/msg "):
            parts = message.split(" ", 2)
            if len(parts) >= 3:
                self.chat_area.append(parts[2])
            return
        # Filtrar mensajes de grupo para que no aparezcan en la ventana global
        if message.startswith("[Grupo:") or message.startswith("[GrupoArchivo:"):
            return
        # Desencriptar mensajes cifrados
        if message.startswith("ENC("):
            try:
                plaintext = decrypt_message(message)
                self.chat_area.append(plaintext)
            except Exception as e:
                self.chat_area.append("[Error de cifrado] " + message)
        else:
            self.chat_area.append(message)

    def send_message(self):
        message = self.message_input.text().strip()
        if not message:
            return
        if not self.current_target:
            QMessageBox.warning(self, "Advertencia", "Seleccione un destinatario usando 'Enviar a:'.")
            return
        # Formatear mensaje como comando uno a uno
        command = f"/msg {self.current_target} {self.username}: {message}"
        self.chat_area.append(f"[{self.username} -> {self.current_target}]: {message}")
        self.network.send_message(command)
        self.message_input.clear()

    def insert_emoji(self):
        # Lista de emojis disponibles: enojado, risa, aburrimiento, carita feliz, confusión, mareo
        emojis = ["😠", "😂", "😒", "😊", "😕", "😵"]
        emoji, ok = QInputDialog.getItem(self, "Seleccionar emoji", "Emojis disponibles:", emojis, 0, False)
        if ok and emoji:
            current_text = self.message_input.text()
            self.message_input.setText(current_text + emoji)

    def send_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona Archivo", "",
                                                  "All Files (*)")
        if fileName:
            self.network.send_file(fileName)
            self.chat_area.append(f"[Sistema] Enviando archivo: {os.path.basename(fileName)}...")

    def clear_conversation(self):
        self.chat_area.clear()

class GroupChatWindow(QMainWindow):
    def __init__(self, group_name, network, username):
        super().__init__()
        self.group_name = group_name
        self.network = network
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
        # Botón para borrar conversación en chat grupal
        clear_button = QPushButton("Borrar conversación")
        clear_button.clicked.connect(self.clear_conversation)
        bottom_panel.addWidget(clear_button)
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
            self.chat_area.append(f"[Grupo: {self.group_name}] {self.username}: {message}")
            self.network.send_message(command)
            self.message_input.clear()

    def insert_emoji(self):
        # Lista de emojis disponibles: enojado, risa, aburrimiento, carita feliz, confusión, mareo
        emojis = ["😠", "😂", "😒", "😊", "😕", "😵"]
        emoji, ok = QInputDialog.getItem(self, "Seleccionar emoji", "Emojis disponibles:", emojis, 0, False)
        if ok and emoji:
            current_text = self.message_input.text()
            self.message_input.setText(current_text + emoji)

    def send_group_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona Archivo", "",
                                                  "All Files (*)")
        if fileName:
            self.network.send_group_file(fileName, self.group_name)
            self.chat_area.append(f"[Sistema] Enviando archivo al grupo: {os.path.basename(fileName)}...")

    def clear_conversation(self):
        self.chat_area.clear()

if __name__ == '__main__':
    mode = 'client'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    host = "127.0.0.1" 
    port = 5000
    app = QApplication(sys.argv)
    window = ChatWindow(mode, host, port)
    window.show()
    sys.exit(app.exec_())