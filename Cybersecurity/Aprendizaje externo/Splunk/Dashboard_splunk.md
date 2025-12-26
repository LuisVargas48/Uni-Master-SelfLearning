# 🛡️ Monitor de Seguridad Linux con Splunk

## 📄 Descripción del Proyecto

Este proyecto es una implementación de monitoreo de seguridad (SIEM) desarrollada en **Splunk Enterprise**. Su propósito es ingestar y analizar logs críticos de un servidor **Ubuntu Linux** en tiempo real mediante el uso de un **Universal Forwarder**.

El dashboard permite detectar patrones de intrusión, auditar el uso de privilegios elevados y visualizar la salud de los procesos del sistema, sirviendo como una herramienta esencial para tareas de **Blue Teaming** y **Análisis Forense**.

## ✨ Características Principales

* **Ingesta de Datos Distribuidos:** Configuración de arquitectura Cliente-Servidor usando Splunk Universal Forwarder para el envío seguro de logs (`/var/log/auth.log`, `syslog`).
* **Auditoría de Privilegios (SUDO):** Extracción personalizada de campos mediante **Regex (SPL)** para identificar exactamente qué comandos se ejecutan con permisos de `root`.
* **Detección de Fuerza Bruta (SSH):** Identificación visual de intentos de login fallidos repetitivos, alertando sobre posibles ataques de diccionario hacia el puerto 22.
* **Monitorización de Procesos:** Visualización estadística de los demonios y servicios (`systemd`, `CRON`, etc.) que más recursos o actividad generan en el sistema.
* **Dashboard Interactivo:** Paneles dinámicos con selectores de tiempo para filtrar eventos históricos o visualizar amenazas en tiempo real.

## 🛠️ Tecnologías Utilizadas

* **SIEM:** Splunk Enterprise
* **Agente:** Splunk Universal Forwarder
* **OS:** Ubuntu Linux (Server/Desktop)
* **Lenguaje:** SPL (Search Processing Language) & Regex


## 🔍 Consultas SPL Clave

Estas son las consultas técnicas desarrolladas para generar los paneles del dashboard:


### Auditoría de comandos SUDO (tabla)

```splunk
index="pruebas" host="luisv-VMware-Virtual-Platform" "sudo" "COMMAND="
| rex field=_raw "COMMAND=(?<comando_ejecutado>.*)$"
| table _time, comando_ejecutado
```


### Detección de fuerza bruta por medio de SSH (Gráfico)


```splunk
index="pruebas" "Failed password"
| rex field=_raw "for (invalid user )?(?<usuario_atacante>\S+) from"
| timechart count by usuario_atacante
```


### TOP procesos del sistema (Grafica de pastel )

```splunk
index="pruebas" host="luisv-VMware-Virtual-Platform"
| top limit=10 process
```







## 📸 Capturas de Pantalla


<img width="1919" height="720" alt="image" src="https://github.com/user-attachments/assets/85c8a3c9-2310-4a71-a938-2e2c18e40952" />

<img width="1919" height="974" alt="image" src="https://github.com/user-attachments/assets/e07b9bdd-8228-4229-a684-8cb71a812b1b" />



<img width="1832" height="334" alt="image" src="https://github.com/user-attachments/assets/10cb02b2-ed46-45a2-9d61-31211d0d7963" />


