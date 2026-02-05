# Imagen base ligera de Python
FROM python:3.9-slim

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalarlas
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la app
COPY app/ .

# Exponer el puerto de Flask
EXPOSE 5000

# Comando para ejecutar
CMD ["python", "app.py"]