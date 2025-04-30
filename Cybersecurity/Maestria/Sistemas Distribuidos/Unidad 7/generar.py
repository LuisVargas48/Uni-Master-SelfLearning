import random
import string

# Función para generar una cadena aleatoria de una longitud específica
def generar_texto_aleatorio(longitud):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation + ' ', k=longitud))

# Generar un archivo de texto de 50 MB o más
tamano_objetivo = 50 * 1024 * 1024  # 50 MB en bytes
tamano_actual = 0

ruta_archivo = "archivo_prueba.txt"

# Abrir el archivo para escribir
with open(ruta_archivo, "w") as archivo:
    while tamano_actual < tamano_objetivo:
        # Generar un bloque de texto aleatorio de tamaño 1 MB
        bloque_aleatorio = generar_texto_aleatorio(1024 * 1024)  # 1 MB de texto
        archivo.write(bloque_aleatorio)
        tamano_actual += len(bloque_aleatorio)

print(f"Archivo {ruta_archivo} generado con éxito. Tamaño: {tamano_actual} bytes")
