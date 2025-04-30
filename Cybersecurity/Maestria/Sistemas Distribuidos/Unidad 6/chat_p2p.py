# chat_p2p.py
import socket
import threading

# Lista de nodos (IP, Puerto) en la red P2P
NODOS = [
    ("127.0.0.1", 56432),  # Nodo 1
    ("127.0.0.1", 56433),  # Nodo 2
    
]

# Diccionario de usuarios y contraseñas (puedes ampliarlo)
USUARIOS = {
    "Luis": "DragonDorado5512",
    "Alejandro": "StoneMarizca12973"
}

# ======== Cifrado y Descifrado César ========
def cifrar_cesar(mensaje, clave):
    """Cifra un mensaje usando el cifrado César."""
    mensaje_cifrado = ""
    for char in mensaje:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            mensaje_cifrado += chr((ord(char) - shift + clave) % 26 + shift)
        else:
            mensaje_cifrado += char
    return mensaje_cifrado 

def descifrar_cesar(mensaje, clave):
    """Descifra un mensaje usando el cifrado César."""
    return cifrar_cesar(mensaje, -clave)

# ======== SERVIDOR TCP PARA MENSAJES ========
def iniciar_servidor_tcp(mi_ip, mi_puerto, callback_recibir_mensaje, clave):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((mi_ip, mi_puerto))
        server_socket.listen()
        print(f"Servidor TCP escuchando en {mi_ip}:{mi_puerto}")

        while True:
            conn, addr = server_socket.accept()
            print(f"Conexión recibida desde {addr}")
            with conn:
                data = conn.recv(1024)
                if not data:
                    break
                mensaje_cifrado = data.decode('utf-8')
                mensaje = descifrar_cesar(mensaje_cifrado, clave)
                callback_recibir_mensaje(f"{mensaje}")

# ======== CLIENTE TCP PARA ENVIAR MENSAJES ========
def iniciar_cliente_tcp(mi_ip, mi_puerto, usuario, mensaje, clave):
    mensaje_cifrado = cifrar_cesar(mensaje, clave)
    print(f"Mensaje cifrado: {mensaje_cifrado}")  # Mostrar mensaje cifrado

    for ip, puerto in NODOS:
        if (ip, puerto) != (mi_ip, mi_puerto):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((ip, puerto))
                    client_socket.sendall(mensaje_cifrado.encode('utf-8'))
                    print(f"Mensaje enviado a {ip}:{puerto}")
            except ConnectionRefusedError:
                print(f"No se pudo conectar a {ip}:{puerto}")

# ======== FUNCIÓN DE AUTENTICACIÓN ========
def autenticar_usuario(usuario, contraseña):
    if usuario in USUARIOS and USUARIOS[usuario] == contraseña:
        print(f"✅ Autenticación exitosa: {usuario}")
        return True
    else:
        print("❌ Error de autenticación")
        return False
