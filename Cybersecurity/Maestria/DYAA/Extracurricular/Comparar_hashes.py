import hashlib
import time
import os
import psutil
import shutil

# ------------------------
# Funciones de hash
# ------------------------

def calcular_hash_md5(archivo):
    hash_md5 = hashlib.md5()
    with open(archivo, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_md5.update(bloque)
    return hash_md5.hexdigest()

def calcular_hash_sha256(archivo):
    hash_sha256 = hashlib.sha256()
    with open(archivo, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_sha256.update(bloque)
    return hash_sha256.hexdigest()

# ------------------------
# Medición de rendimiento
# ------------------------

def medir_metricas(funcion_hash, archivo):
    proceso = psutil.Process(os.getpid())
    memoria_inicio = proceso.memory_info().rss

    inicio = time.time()
    resultado = funcion_hash(archivo)
    fin = time.time()

    memoria_fin = proceso.memory_info().rss
    uso_memoria = (memoria_fin - memoria_inicio) / 1024 / 1024  # MB
    duracion = fin - inicio

    return resultado, duracion, uso_memoria

# ------------------------
# Crear copia y modificar 1 byte
# ------------------------

def modificar_archivo(original, modificado):
    shutil.copyfile(original, modificado)
    with open(modificado, "r+b") as f:
        f.seek(0)
        byte = f.read(1)
        if not byte:
            raise ValueError("El archivo está vacío.")
        nuevo_byte = (byte[0] ^ 0x01).to_bytes(1, 'big')  # flip bit
        f.seek(0)
        f.write(nuevo_byte)

# ------------------------
# Ejecutar prueba
# ------------------------

def ejecutar_prueba(ruta_original):
    ruta_modificada = "modificado_" + os.path.basename(ruta_original)
    modificar_archivo(ruta_original, ruta_modificada)

    resultados = {}

    for nombre, funcion in [("MD5", calcular_hash_md5), ("SHA-256", calcular_hash_sha256)]:
        hash_orig, tiempo_orig, mem_orig = medir_metricas(funcion, ruta_original)
        hash_mod, _, _ = medir_metricas(funcion, ruta_modificada)

        resultados[nombre] = {
            "Hash original": hash_orig,
            "Hash modificado": hash_mod,
            "¿Hash diferente?": hash_orig != hash_mod,
            "Tiempo (s)": round(tiempo_orig, 4),
            "Memoria (MB)": round(mem_orig, 4),
            "Longitud del hash": len(hash_orig)
        }

    os.remove(ruta_modificada)
    return resultados

# ------------------------
# Ejemplo de uso
# ------------------------

if __name__ == "__main__":
    ruta = "archivo.txt"
    if os.path.exists(ruta):
        resultado = ejecutar_prueba(ruta)
        for algoritmo, datos in resultado.items():
            print(f"\nAlgoritmo: {algoritmo}")
            for k, v in datos.items():
                print(f"  {k}: {v}")
    else:
        print(" El archivo no existe. Por favor verifica la ruta.")
