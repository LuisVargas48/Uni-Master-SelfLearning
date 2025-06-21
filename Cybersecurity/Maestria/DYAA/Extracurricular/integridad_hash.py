import hashlib
import os

def calcular_hash_sha256(archivo):
    sha256 = hashlib.sha256()
    try:
        with open(archivo, "rb") as f:
            for bloque in iter(lambda: f.read(4096), b""):
                sha256.update(bloque)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def verificar_archivos(directorio):
    hashes = {}
    for root, dirs, files in os.walk(directorio):
        for archivo in files:
            ruta = os.path.join(root, archivo)
            hash_archivo = calcular_hash_sha256(ruta)
            if hash_archivo:
                hashes[ruta] = hash_archivo
    return hashes

def main():
    directorio = input("Ingresa el directorio que deseas verificar: ").strip()
    print("\nCalculando hashes SHA-256...\n")
    resultados = verificar_archivos(directorio)

    for archivo, hash_valor in resultados.items():
        print(f"{archivo}:\n  {hash_valor}\n")

    # Opcional: guardar los hashes en un archivo
    guardar = input("¿Deseas guardar los hashes en un archivo? (s/n): ").lower()
    if guardar == "s":
        with open("hashes_resultados.txt", "w") as f:
            for archivo, hash_valor in resultados.items():
                f.write(f"{archivo}:\n  {hash_valor}\n")
        print("Hashes guardados en 'hashes_resultados.txt'.")

if __name__ == "__main__":
    main()
