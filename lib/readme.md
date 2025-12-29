# Instalación de librerias python
Navega hasta la carpeta donde están los archivos descargados.
Ejecuta el siguiente comando para instalar libreria cada libreria.

``` bash
pip install --no-index --find-links="./" nombre_libreria
```

Nota:
¿Qué significan estos parámetros?
--no-index: Le dice a pip que no intente buscar en PyPI (el servidor oficial en internet).

--find-links="./": Le indica que busque los paquetes en la carpeta actual.
