# 🕵️ Analizador de Tráfico de Red con Python y Scapy

## 📄 Descripción del Proyecto

Este proyecto es un analizador de tráfico de red desarrollado en Python, utilizando la potente biblioteca `Scapy`. Su propósito es leer archivos de captura de paquetes (`.pcap`, `.pcapng`) y detectar patrones de tráfico potencialmente sospechosos o de interés para la ciberseguridad.

Ideal para tareas de monitoreo de red, análisis forense básico y como herramienta educativa para comprender el tráfico de red a bajo nivel.

## ✨ Características

* **Lectura de archivos PCAP:** Procesamiento de capturas de red generadas por Wireshark, tcpdump, etc.
* **Detección de Tráfico ICMP (Ping):** Identifica solicitudes y respuestas de ping.
* **Detección de Tráfico No Cifrado:** Localiza paquetes HTTP (Puerto 80) y FTP (Puerto 21), mostrando posibles exposiciones de datos.
* **Búsqueda de Credenciales en Texto Plano:** Analiza la carga útil de paquetes TCP en busca de palabras clave como 'user', 'pass' o 'login'.
* **Detección de Escaneo de Puertos (TCP SYN Scan):** Identifica patrones de múltiples paquetes SYN enviados a diferentes puertos desde un mismo origen hacia un destino, indicando un posible escaneo.
* **Generación de Informe:** Exporta un resumen de los hallazgos a la consola y a un archivo de texto (`informe_analisis.txt`).

## 🚀 Cómo Empezar

### Requisitos

Asegúrate de tener instalado lo siguiente:

* **Python 3.x:** [Descargar Python](https://www.python.org/downloads/)
* **Wireshark / Npcap:** (Npcap es un controlador que permite la captura de paquetes y se instala junto con Wireshark). [Descargar Wireshark](https://www.wireshark.org/download.html)
* **Scapy:** Biblioteca de manipulación de paquetes para Python.

### Instalación

1.  **Clona este repositorio** (una vez que lo subas a GitHub) o descarga los archivos.

2.  **Instala Scapy** usando pip:

    ```bash
    pip install scapy
    ```

3.  (Opcional, para generar capturas de prueba) **Instala Nmap:**

    ```bash
    # Para Windows, descarga el instalador desde nmap.org
    # [https://nmap.org/download.html](https://nmap.org/download.html)
    ```

### Generar una Captura de Prueba (`.pcap`)

Para probar el analizador, puedes generar tu propia captura:

1.  **Abre Wireshark.**
2.  **Inicia la captura** en la interfaz de red que te interese (tu tarjeta Wi-Fi/Ethernet para tráfico web, o el **"Npcap Loopback Adapter"** para tráfico interno como `localhost`).

    **`IMAGEN DE EJEMPLO: Captura de pantalla de Wireshark con la interfaz loopback seleccionada.`**
    (Puedes poner aquí una captura de pantalla de Wireshark con la interfaz de Loopback seleccionada, o simplemente el editor de texto si no quieres añadir imágenes todavía.)

3.  **Genera tráfico:**
    * **Ping (ICMP):** Abre una terminal y ejecuta `ping 8.8.8.8` (o `ping localhost`).
    * **HTTP (no cifrado):** Visita `http://neverssl.com` en tu navegador.
    * **SYN Scan (con Nmap):** En una terminal, ejecuta `nmap -sS localhost`.

4.  **Detén la captura** en Wireshark y **guárdala** como `mi_captura.pcap` (o `captura_datos.pcap` si ese es el nombre que usaste en el script) en la misma carpeta que el script `analizador.py`.

## ⚙️ Uso

1.  Asegúrate de que tu archivo `.pcap` (`mi_captura.pcap` o `captura_datos.pcap`) esté en la misma carpeta que `analizador.py`.
2.  Abre una terminal en esa carpeta.
3.  Ejecuta el script de Python:

    ```bash
    python analizador.py
    ```

El script imprimirá los hallazgos en la consola y generará un archivo `informe_analisis.txt` con los resultados detallados.

## 📊 Ejemplo de Salida


<img width="1919" height="1003" alt="image" src="https://github.com/user-attachments/assets/1a0ef3a7-7f0a-4817-b185-3853ac5f4bdd" />

<img width="1468" height="475" alt="image" src="https://github.com/user-attachments/assets/8437f597-1124-4a17-a444-66a46d43082e" />


## 🧠 Posibles Mejoras

* **Más Reglas de Detección:** Añadir detección de otros tipos de escaneos (UDP scan, XMAS scan), inyecciones SQL, tráfico de malware, etc.
* **Análisis de Flujos:** Agrupar paquetes por sesiones (flujos) para un análisis más contextual.
* **Interfaz Gráfica (GUI):** Desarrollar una interfaz de usuario para facilitar la interacción.
* **Alertas en Tiempo Real:** Adaptar el script para monitorear una interfaz en vivo y generar alertas.
* **Configuración Externa:** Permitir al usuario definir umbrales o reglas en un archivo de configuración.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar este analizador, no dudes en abrir un *issue* o enviar un *pull request*.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---
