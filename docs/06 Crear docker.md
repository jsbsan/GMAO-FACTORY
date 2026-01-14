Pasos previos:

1. Crea el fichero requirements.txt
		Si no esta creado el fichero requirements.txt, hay que crearlo. Situate en la carpeta del codigo fuente y escribe:
		``` bash
		pip freeze > requirements.txt
		```

2. Crea el archivo Dockerfile
Si no esta creado, copia estas lineas:
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
		# 6. Comando para ejecutar tu app (CAMBIA 'main.py' por el nombre de tu archivo)
		CMD ["python", "app.py"]

3. Crear el archivo .dockerignore
Si no esta creado, poner el siguiente contenido:
		__pycache__
		venv/
		.git/
		.env
		*.pyc
### 
Necesario para cada vez que se cambie el codigo fuente:
### 

4. Crear imagen docker: 
		``` bash
		docker build -t gmao-factory .
		```

5. Ejecutar contenedor:
		``` bash
		docker run -p 5000:5000 gmao-factory
		```