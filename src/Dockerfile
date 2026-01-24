# 1. Imagen base: Usamos Python
FROM python:3.13

# 2. Directorio de trabajo: Creamos una carpeta dentro del contenedor
WORKDIR /app

# 3. Copiamos los requerimientos primero (para aprovechar la caché de Docker)
COPY requirements.txt .

# 4. Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto de tu código al contenedor
COPY . .

EXPOSE 5000

# 6. Comando para ejecutar tu app (CAMBIA 'main.py' por el nombre de tu archivo)
CMD ["python", "app.py"]