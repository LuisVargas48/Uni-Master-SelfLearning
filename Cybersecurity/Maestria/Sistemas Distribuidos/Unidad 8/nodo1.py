import socket
import os
import time

# Configuración del nodo
NODOS = [("127.0.0.1", 56433)]  # Nodo 2
TAMANO_PAQUETE = 4096
DESPLAZAMIENTO_CESAR = 7

# Función de cifrado César para archivos binarios
def cifrar_cesar(datos, desplazamiento):
    return bytes((byte + desplazamiento) % 256 for byte in datos)

# Función para enviar un archivo cifrado
def enviar_archivo(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print("El archivo no existe.")
        return

    nombre_archivo = os.path.basename(ruta_archivo)
    tamano_archivo = os.path.getsize(ruta_archivo)
    print(f"Enviando archivo cifrado: {nombre_archivo}, Tamaño: {tamano_archivo} bytes")

    for ip, puerto in NODOS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((ip, puerto))
                print(f"Conectado a {ip}:{puerto}, enviando archivo...")

                # Enviar metadatos del archivo (nombre y tamaño)
                metadatos = f"{nombre_archivo}|{tamano_archivo}\n"
                client_socket.sendall(metadatos.encode())

                # Enviar archivo en fragmentos cifrados
                with open(ruta_archivo, "rb") as archivo:
                    while fragmento := archivo.read(TAMANO_PAQUETE):
                        fragmento_cifrado = cifrar_cesar(fragmento, DESPLAZAMIENTO_CESAR)
                        client_socket.sendall(fragmento_cifrado)

                print(f"Archivo {nombre_archivo} cifrado y enviado con éxito a {ip}:{puerto}")

        except ConnectionRefusedError:
            print(f"No se pudo conectar a {ip}:{puerto}. Reintentando en 2s...")
            time.sleep(2)

# Configuración y ejecución del nodo 1
if __name__ == "__main__":
    time.sleep(3)  # Esperar para iniciar el servidor en el otro nodo
    enviar_archivo("Gatos-Graciosos .mp4")
