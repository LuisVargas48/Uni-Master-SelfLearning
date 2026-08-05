# Threat Intelligence Report: Desmantelando una Red Global de Phishing de Retail 

Autor: Luis Alberto Vargas Gonzalez

Fecha: 5 de agosto de 2026

Técnicas utilizadas: OSINT, DNS Enumeration, SSL/TLS Forensics, Infrastructure Fingerprinting.


----------------------------------------------------------------------------------------------------

## 📌 Resumen Ejecutivo

Investigación proactiva y análisis forense de un dominio fraudulento que suplantaba a la marca oficial Bose Corporation en México (bosesmexico.com.mx). A través de técnicas de reconocimiento pasivo y evasión de proxy, se logró desenmascarar la infraestructura real del atacante (Origin IP). El análisis reveló que este dominio no era un incidente aislado, sino parte de una red criminal masiva alojada en un servidor con arbitraje jurisdiccional, operando más de 70 tiendas falsas de marcas globales de retail. Se ejecutaron acciones de Takedown para neutralizar la amenaza.


--------------------------------------------------------------------------------------------

## 🔍 1. Reconocimiento Inicial y Análisis de Dominio (WHOIS)

La investigación comenzó tras detectar tácticas de SEO Poisoning y Typosquatting en motores de búsqueda. Se analizaron los dominios fraudulentos descubriendo un patrón claro de registro masivo:

Dominio Analizado: bosesmexico.com.mx y bosemx.com.mx

Registrador: Openprovider / Registrar.eu (Comúnmente abusado por bajas restricciones).

Fechas de Creación: Junio y julio de 2026 (Infraestructura de vida efímera).

Titularidad: Identidades físicas registradas en Alemania ("egger james", "pfeiffer nadine"), sugiriendo el uso de identidades sintéticas o robadas para dificultar el rastreo legal.

<img width="917" height="410" alt="image" src="https://github.com/user-attachments/assets/5bb6a95e-76ce-4291-a84e-ad9b0dccf0d6" />

<img width="959" height="469" alt="image" src="https://github.com/user-attachments/assets/7c401797-d53c-4244-a78e-615f7c91c912" />

<img width="917" height="365" alt="image" src="https://github.com/user-attachments/assets/78b34934-8fa0-4345-aada-5ac9a7a1c8f9" />



-----------------------------------------------------------------------------------------------------------------------------------

## 🌐 2. Análisis de Infraestructura y Evasión (Uncloaking)

Los atacantes utilizaron la red Anycast de Cloudflare para ocultar la ubicación real de su servidor y obtener certificados SSL gratuitos para generar falsa legitimidad.

Mediante correlación de registros DNS históricos y subdominios no protegidos, se logró realizar un exitoso uncloaking (evasión del proxy inverso), revelando la infraestructura base:

IP de Origen Descubierta: 194.26.231.133

Geolocalización: Los Ángeles, California (EE. UU.)

ASN: AS199242 (Malakmadze Web LLC)

Propietario del Bloque IP: Beijing Ruihao Kai Yuan Technology Co., Ltd.

Conclusión de Red: El atacante utiliza Bulletproof Hosting con arbitraje jurisdiccional (Servidor en EE. UU., IP asignada a China, dominios en Europa) para evadir solicitudes de baja por derechos de autor (DMCA) o Phishing.

<img width="327" height="229" alt="image" src="https://github.com/user-attachments/assets/26c69440-5d0c-40a0-aad3-7527d9fce4bf" />



---------------------------------------------------------------------------------------------

## 🔐 3. Análisis Criptográfico (CT Logs)

Se consultaron las bitácoras de Certificate Transparency (crt.sh). El análisis evidenció la automatización de la campaña:

Uso exclusivo de Autoridades Certificadoras (CA) de Validación de Dominio (DV) gratuitas: Let's Encrypt y Google Trust Services.

Certificados emitidos con vigencia exacta de 90 días mediante el protocolo ACME.

Se detectaron tácticas de Drop Catching (registro de dominios abandonados en el instante en que expiran) para heredar la reputación SEO previa del dominio.

<img width="959" height="470" alt="image" src="https://github.com/user-attachments/assets/b09374be-cf5c-4c96-a9d6-386e1473ec79" />

<img width="956" height="441" alt="image" src="https://github.com/user-attachments/assets/e9ec3360-3b4d-4b5f-ade0-d13d9b136ca2" />



------------------------------------------------------------------------------------------------------------


## ⚙️ 4. Fingerprinting y Escala de la Operación

Se realizó un escaneo pasivo de la IP de origen (194.26.231.133) utilizando motores de búsqueda de infraestructura (Shodan/Censys) para mapear la superficie de ataque, revelando graves fallos en la seguridad operacional (OPSEC) del cibercriminal:

Vulnerabilidad OPSEC: El servidor exponía públicamente el Puerto 21 (FTP - Pure-FTPd). Esto indica que los atacantes utilizan scripts para subir plantillas de tiendas clonadas de forma masiva a través de este protocolo obsoleto.

Pivoteo de Red: Una búsqueda inversa de IP reveló que el servidor aloja actualmente más de 70 dominios fraudulentos activos.

Impacto Global: La red clona tiendas e intercepta pagos de clientes de marcas internacionales como JBL, Marshall, Sonos, Crocs, The North Face, Garmin, entre otras, afectando a usuarios en Norteamérica, Europa y Oceanía.

<img width="959" height="473" alt="image" src="https://github.com/user-attachments/assets/a0b03b1c-3a93-44da-af80-a8706e846bcc" />


<img width="955" height="472" alt="image" src="https://github.com/user-attachments/assets/70c6abfd-becc-430a-8a0a-fa004a5aa600" />


<img width="952" height="467" alt="image" src="https://github.com/user-attachments/assets/9452159a-eef2-452e-b562-1def9a54f489" />




-----------------------------------------------------------------------------------------------------------

## 🛑 5. Respuesta a Incidentes (Takedown Actions)

Con base en la evidencia irrefutable recolectada y preservando una estricta seguridad operacional (reportes anónimos para evitar represalias), se ejecutó el siguiente protocolo de erradicación:

Google Safe Browsing & Microsoft SmartScreen: Se enviaron los reportes de Social Engineering/Phishing para bloquear el acceso de las víctimas a nivel de navegador.

Cloudflare Trust & Safety: Se levantó un ticket oficial demostrando el enmascaramiento del servidor de fraude para solicitar la suspensión del servicio CDN.

Registrador de DNS: Se envió un Takedown Request a abuse@registrar.eu detallando la violación de políticas corporativas y fraude para la suspensión global de los dominios.



--------------------------------------------------------------------------------------------------------------


## 🚨 Indicadores de Compromiso (IoCs)


Tipo    Indicador             Descripción
IPV4    194.26.231.33         Origin Server IP (Malakmadze Web LLC)
URL     bosesmexico.com.mx    Phishing Domain (Cloudflare Cloaked)
URL     bosemx.com.mx         Phishing Domain (Direct IP)
ASN     AS199242              Bulletproof Hosting Infrastructure
