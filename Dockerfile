# Usar una imagen base de Python 3.10
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación al contenedor
COPY . /app/

# Exponer el puerto en el que FastAPI servirá la aplicación
EXPOSE 8091

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "SmartPot-Middleware.app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8091"]
