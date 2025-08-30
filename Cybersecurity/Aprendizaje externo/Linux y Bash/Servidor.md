# 🖥️ Proyecto: Configuración de un Servidor Linux en KVM/QEMU

Este pequeño proyecto complementario documenta la configuracion de un servidor Linux basico en **Ubuntu dentro de KVM/QEMU**.  

Incluye los siguientes apartados :  

1. Instalacion de paquetes esenciales  
2. Configuracion de un firewall basico con `ufw`  
3. Automatizacion de un respaldo con un script en Bash  


----------------------------------------------------------------------------

## ⚙️ 1. Instalación de paquetes básicos

Primero actualizamos los repositorios y paquetes existentes:

`sudo apt update && sudo apt upgrade -y`



<img width="2395" height="1416" alt="image" src="https://github.com/user-attachments/assets/e5d9591f-c218-40e4-bf5e-bfacecdc6d7e" />






Instalamos utilidades comunes que facilitan la administración del sistema:

`sudo apt install curl wget net-tools vim -y`



<img width="2395" height="1416" alt="image" src="https://github.com/user-attachments/assets/5c344520-363e-4fe6-bd7a-fd3bfe6b1a21" />




## 🔒 2. Configuración del firewall (UFW)

Instalamos y habilitamos el firewall:


`sudo apt install ufw -y`
`sudo ufw enable`

<img width="2395" height="1416" alt="image" src="https://github.com/user-attachments/assets/487eaa19-1b59-435e-aa7e-f78895c1a1fe" />
<img width="2395" height="1416" alt="image" src="https://github.com/user-attachments/assets/5c06dc38-59ad-41f3-adce-e8a6eeb21111" />







Permitimos el acceso por SSH (importante si se administra de forma remota):

`sudo ufw allow ssh`


<img width="2395" height="1416" alt="image" src="https://github.com/user-attachments/assets/1b595150-c77e-4816-bed9-93eb3bb845d4" />





Verificamos las reglas activas:

`sudo ufw status`

<img width="2395" height="1416" alt="image" src="https://github.com/user-attachments/assets/1e77a6a0-eb5e-4bf3-bb90-ca05b91a292c" />







## 💾 3. Automatizacion de respaldo en Bash

Creamos un script llamado `respaldo.sh`:

```bash
#!/bin/bash
fecha=$(date +%Y%m%d)
destino="/home/usuario/respaldo-$fecha.tar.gz"

tar -czf $destino /home/usuario/

echo "✅ Respaldo generado en: $destino"


```


#



<img width="1920" height="1342" alt="image" src="https://github.com/user-attachments/assets/ad3d1020-927b-48bf-b19f-ec18633cc60c" />



Le damos permisos de ejecucion:

`chmod +x respaldo.sh`



Ejecutamos el script:

`./respaldo.sh`

<img width="1920" height="1342" alt="image" src="https://github.com/user-attachments/assets/a3ae5d25-ae8f-4f41-adb2-de81e528e97a" />




<img width="1920" height="1342" alt="image" src="https://github.com/user-attachments/assets/d2021ac2-65f2-476a-a10a-06151718fe77" />









✅ CONCLUSION

Con esta practica se logra configurar un servidor Linux basico en KVM/QEMU, reforzando conocimientos en:

Instalacion y gestion de paquetes

Seguridad inicial con firewall

Automatizacion de tareas con Bash
