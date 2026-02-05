# 🏗️ CTF Build: Laboratorio de Microservicios Vulnerables

Este documento detalla la arquitectura, el despliegue y la configuración técnica del laboratorio de seguridad basado en contenedores. Este entorno ha sido diseñado para simular vulnerabilidades comunes en aplicaciones modernas y entornos de microservicios.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.9 (Flask Framework)
* **Orquestación:** Docker & Docker Compose
* **Vulnerabilidades:** Command Injection & Insecure Deserialization (Pickle)
* **SO Base:** Debian-based (Python-slim)

---

## 🚀 Despliegue del Laboratorio

Para levantar el entorno, asegúrate de tener instalado **Docker** y **Docker Compose**. Sigue estos pasos en tu terminal:

1. **Clonar el repositorio:**
   ```bash
   git clone <https://github.com/LuisVargas48/Uni-Master-SelfLearning/new/main/Cybersecurity/Aprendizaje%20externo/Docker_Ciberseguridad>
   cd Uni-Master-SelfLearning
   cd Cybersecurity
   cd Aprendizaje externo
   cd Docker_Cibersrguridad
   cd CTF_build


2. **Construir e iniciar los contenedores.**
    ```bash
    docker-compose up --build

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/a5065aa4-3621-47a2-8061-04888017d53b" />



3. **Verificación:**
   ```bash
     El laboratorio debe de estar disponible en: http::localhost:8080




<img width="1919" height="1015" alt="image" src="https://github.com/user-attachments/assets/8da98065-d187-402b-b963-619c88bd4b1e" />





# 🏗️ Arquitectura de Construcción


1. **Aplicación (app/app.py)**
La aplicación web utiliza Flask para exponer dos puntos de entrada principales con fines educativos:

       **/ping:** Simula una herramienta de red que, por un diseño inseguro, permite la concatenación de comandos del sistema operativo.

       **/profile:** Implementa un sistema de sesiones basado en la serialización de objetos con la librería pickle.

2. **Dockerización**
El Dockerfile utiliza una imagen slim para minimizar la superficie de ataque, aunque se mantienen las herramientas necesarias para la explotación. El archivo docker-compose.yml gestiona la red aislada (bridge) y las variables de entorno donde se ocultan las "Flags".

<img width="1400" height="886" alt="image" src="https://github.com/user-attachments/assets/28f2995d-fcfa-47be-bb86-aab577ec3ecf" />


  # 🎯 Objetivos del CTF (Flags)
  
El reto consiste en obtener dos banderas (flags) ocultas en el sistema:

**User Flag:** Localizada en las variables de entorno del contenedor. Requiere la explotación del endpoint /ping.

**Root Flag:** Localizada en el sistema de archivos del servidor. Requiere comprometer la integridad de la sesión mediante la deserialización de objetos en /profile.




# Aviso de Seguridad: 

Este entorno se proporciona únicamente con fines educativos y de investigación. No debe ser desplegado en redes públicas ni en entornos de producción.
