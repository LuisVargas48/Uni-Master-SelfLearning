import socket
import threading
import os
import time


# Configuración de nodos (debes cambiar los puertos en cada nodo)
NODOS = [
    ("127.0.0.1", 56432),  # Nodo 1
    ("127.0.0.1", 56433),  # Nodo 2
]

# Tamaño del paquete (bytes)
TAMANO_PAQUETE = 1024

# Función para cifrar el texto con el método Césas
def cifrar_cesar(texto, desplazamiento):
    resultado = []
    for char in texto:
        if char.isalpha():
            # Desplazar solo las letras
            ascii_offset = 65 if char.isupper() else 97
            resultado.append(chr((ord(char) - ascii_offset + desplazamiento) % 26 + ascii_offset))
        else:
            resultado.append(char)  # No cambiar caracteres no alfabéticos
    return ''.join(resultado)

# Función para descifrar el texto con el método César
def descifrar_cesar(texto, desplazamiento):
    return cifrar_cesar(texto, -desplazamiento)

# Función para enviar un archivo en fragmentos (con cifrado)
def enviar_archivo(mi_ip, mi_puerto, ruta_archivo, desplazamiento_cesar=3):
    if not os.path.exists(ruta_archivo):
        print("El archivo no existe.")
        return

    nombre_archivo = os.path.basename(ruta_archivo)
    tamano_archivo = os.path.getsize(ruta_archivo)

    print(f"Tamaño del archivo a enviar: {tamano_archivo} bytes")

    for ip, puerto in NODOS:
        if (ip, puerto) == (mi_ip, mi_puerto):
            continue  # No enviarse a sí mismo

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((ip, puerto))
                print(f"Conectado a {ip}:{puerto}, enviando archivo...")

                # Enviar metadatos del archivo (nombre y tamaño) como una línea separada
                metadatos = f"{nombre_archivo}|{tamano_archivo}\n"
                client_socket.sendall(metadatos.encode())

                # Leer y cifrar el archivo en fragmentos antes de enviarlo
                with open(ruta_archivo, "rb") as archivo:
                    while fragmento := archivo.read(TAMANO_PAQUETE):
                        # Cifrar cada fragmento (convertir bytes a texto cifrado)
                        fragmento_texto = fragmento.decode(errors='ignore')  # Convertir a texto
                        fragmento_cifrado = cifrar_cesar(fragmento_texto, desplazamiento_cesar)
                        client_socket.sendall(fragmento_cifrado.encode())

                print(f"Archivo {nombre_archivo} enviado con éxito a {ip}:{puerto}")

        except ConnectionRefusedError:
            print(f"No se pudo conectar a {ip}:{puerto}. Reintentando en 2s...")
            time.sleep(2)

# Servidor TCP para recibir archivos (con descifrado)
def iniciar_servidor_tcp(mi_ip, mi_puerto, carpeta_destino, desplazamiento_cesar=3):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((mi_ip, mi_puerto))
    server_socket.listen()
    print(f"Servidor TCP escuchando en {mi_ip}:{mi_puerto}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Conexión establecida con {addr}")

        try:
            # Primero, recibir los metadatos del archivo
            metadata = conn.recv(1024).decode().strip()
            if "|" not in metadata:
                raise ValueError(f"Formato de metadatos incorrecto: {metadata}")

            nombre_archivo, tamano_archivo = metadata.split("|", 1)
            tamano_archivo = int(tamano_archivo.strip())

            print(f"Tamaño del archivo recibido: {tamano_archivo} bytes")

            # Guardar el archivo en la carpeta de destino
            ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
            with open(ruta_completa, "wb") as archivo:
                bytes_recibidos = 0
                while bytes_recibidos < tamano_archivo:
                    fragmento = conn.recv(TAMANO_PAQUETE)
                    if not fragmento:
                        break
                    # Descifrar el fragmento antes de escribirlo en el archivo
                    fragmento_texto = fragmento.decode(errors='ignore')
                    fragmento_descifrado = descifrar_cesar(fragmento_texto, desplazamiento_cesar)
                    archivo.write(fragmento_descifrado.encode())
                    bytes_recibidos += len(fragmento)

            print(f"Archivo {nombre_archivo} recibido y guardado en {ruta_completa}")

        except Exception as e:
            print(f"Error al recibir archivo: {e}")

# Configuración y ejecución de los nodos
if __name__ == "__main__":
    # Define si este nodo es el emisor o receptor
    mi_ip = "127.0.0.1"
    mi_puerto = 56432  # Cambia este puerto a 56433 en el otro nodo

    # Carpeta donde se guardarán los archivos recibidos
    carpeta_destino = "./archivos_recibidos"
    os.makedirs(carpeta_destino, exist_ok=True)

    # Iniciar el servidor en un hilo
    servidor = threading.Thread(target=iniciar_servidor_tcp, args=(mi_ip, mi_puerto, carpeta_destino))
    servidor.start()

    # Simular envío de archivo desde un nodo
    time.sleep(3)  # Esperar a que el servidor se inicie
    if mi_puerto == 56432:  # Solo el nodo 1 enviará un archivo de prueba
        enviar_archivo(mi_ip, mi_puerto, "archivo_prueba.txt")
