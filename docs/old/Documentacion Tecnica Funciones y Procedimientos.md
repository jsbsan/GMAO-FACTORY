# **Documentación Técnica: Funciones y Procedimientos GMAO Factory**

Este documento detalla la arquitectura lógica del sistema, desglosando cada archivo y explicando el propósito de sus funciones y rutas.

## **1\. Módulo de Base de Datos (database.py)**

Este archivo gestiona la persistencia de datos usando SQLite. No utiliza ORM (como SQLAlchemy), sino consultas SQL directas para mayor ligereza.

### **Funciones**

* **get\_db\_connection()**  
  * **Propósito:** Establece la conexión con el archivo mantenimiento\_factory.db.  
  * **Detalle:** Configura row\_factory \= sqlite3.Row, lo que permite acceder a los resultados de la base de datos como si fueran diccionarios (por nombre de columna) en lugar de tuplas numéricas.  
  * **Retorno:** Objeto de conexión SQLite.  
* **init\_db()**  
  * **Propósito:** Inicializa el esquema de la base de datos. Se ejecuta al iniciar la aplicación.  
  * **Procedimiento:**  
    1. Crea las tablas si no existen (CREATE TABLE IF NOT EXISTS): tipos\_equipo, inventario, actividades, ordenes\_trabajo, correctivos, configuracion, usuarios.  
    2. **Migraciones Seguras:** Intenta añadir columnas nuevas (logging\_enabled, fecha\_prevista) a tablas existentes dentro de bloques try/except para no romper bases de datos antiguas.  
    3. **Datos Semilla:** Inserta la configuración inicial (ID=1) y tipos de equipo por defecto (Obra Civil, Eléctricas, etc.) si la base de datos está vacía.

## **2\. Módulo de Utilidades y Lógica de Negocio (utils.py)**

Contiene la lógica central del programa, seguridad y funciones auxiliares.

### **A. Seguridad y Usuarios**

* **create\_default\_admin()**  
  * Comprueba si existe el usuario "Administrador". Si no, lo crea con contraseña "123456" (hasheada) y todos los permisos activados.  
* **login\_required(f)**  
  * **Decorador:** Protege las rutas de Flask. Si el usuario no tiene user\_id en la sesión, lo redirige al Login.  
* **permission\_required(perm)**  
  * **Decorador:** Verifica si el usuario actual tiene un permiso específico (perm\_inventario, etc.). Si no, muestra un error y redirige al inicio.

### **B. Gestión de Fechas y Configuración**

* **get\_system\_date()**  
  * Recupera la "Fecha Virtual" almacenada en la tabla configuracion. Si falla, devuelve la fecha real del servidor. Esto permite simular el paso del tiempo.  
* **get\_planned\_date()**  
  * Recupera la fecha límite hasta la cual se deben pre-generar órdenes de trabajo futuras (Estado "Prevista").  
* **is\_logging\_enabled() / log\_action(action\_message)**  
  * Verifica si el logging está activo en la DB. Si es así, escribe la acción del usuario en el archivo de texto gmao\_app.log con una marca de tiempo.

### **C. Gestión de Archivos (Imágenes/PDFs)**

* **allowed\_file\_image(filename) / allowed\_file\_pdf(filename)**  
  * Valida que las extensiones de los archivos subidos sean seguras y del tipo correcto (png, jpg, pdf).  
* **file\_to\_base64(file)**  
  * Lee el archivo binario subido por el usuario y lo convierte a una cadena de texto Base64 para poder guardarlo dentro de un campo de texto en la base de datos SQLite.  
* **normalize\_files(file\_list)**  
  * Estandariza la estructura de los archivos para que el frontend pueda leerlos, ya vengan de JSON o de formatos antiguos (Legacy).  
* **json\_load\_filter(s)**  
  * Filtro personalizado para Jinja2 que permite decodificar cadenas JSON (listas de archivos) directamente en las plantillas HTML.

### **D. Motor de Mantenimiento (El Núcleo)**

* **get\_cronograma\_data(conn, year)**  
  * **Propósito:** Prepara la matriz de datos para la vista de Cronograma anual.  
  * **Lógica:**  
    1. Obtiene todas las actividades.  
    2. Para cada actividad, busca sus OTs del año seleccionado.  
    3. Agrupa las OTs por mes para pintar la tabla visualmente.  
* **generate\_and\_update\_work\_orders(conn, current\_system\_date)**  
  * **Propósito:** Es el algoritmo principal que genera y actualiza las Órdenes de Trabajo (OTs).  
  * **Flujo:**  
    1. **Generación:** Recorre todas las actividades. Calcula fechas futuras sumando la periodicidad a la fecha de inicio. Si una fecha cae dentro del rango permitido (hasta hoy o hasta la fecha planificada), crea una nueva fila en ordenes\_trabajo.  
    2. **Actualización de Estados:** Revisa las OTs existentes que no están finalizadas y recalcula su estado basándose en la fecha actual del sistema:  
       * **Prevista:** Fecha de OT \> Fecha Sistema.  
       * **En curso:** Fecha de OT \<= Fecha Sistema (y dentro del plazo).  
       * **Pendiente:** Fecha límite (Fecha OT \+ Periodicidad) \< Fecha Sistema.

## **3\. Controlador Principal (app.py)**

Gestiona las rutas HTTP, recibe las peticiones del navegador y decide qué respuesta enviar.

### **A. Autenticación e Inicio**

* **/login (GET/POST):** Valida usuario y contraseña (hash). Si es correcto, guarda los datos y permisos en session.  
* **/logout:** Limpia la sesión y redirige al login.  
* **/ (Index):** Muestra el listado de Inventario. Aplica filtros de búsqueda y paginación.

### **B. Rutas de Inventario**

* **/inventory/add (POST):** Recibe el formulario, procesa imágenes/PDFs a Base64 e inserta el nuevo equipo en la DB.  
* **/inventory/edit/\<id\> y /update/\<id\>:** Muestra formulario de edición y procesa la actualización. Maneja la lógica de "borrar imágenes seleccionadas" y "añadir nuevas".  
* **/inventory/delete/\<id\>:** Borrado en cascada. Elimina el equipo y **también** sus actividades, OTs y correctivos asociados para mantener la integridad referencial.  
* **/inventory/print...:** Genera vistas simplificadas HTML para impresión (ficha individual o listado).

### **C. Rutas de Actividades**

* **/activities:** Lista las definiciones de mantenimiento preventivo.  
* **/activities/add, /edit, /update:** CRUD estándar para actividades.  
* **/activities/delete/\<id\>:** Al borrar una actividad, elimina todas las OTs históricas asociadas a ella.

### **D. Rutas de Órdenes de Trabajo (Work Orders)**

* **/work\_orders:** Listado de OTs. Muestra estados con colores (badges). Permite filtrar por estado y fechas.  
* **/work\_orders/generate (POST):** Botón de pánico/manual que fuerza la ejecución de utils.generate\_and\_update\_work\_orders inmediatamente.  
* **/work\_orders/update/\<id\>:** Permite al operario cambiar el estado (ej: a "Realizada"), añadir observaciones y fecha real de ejecución.

### **E. Rutas de Cronograma**

* **/cronograma:** Llama a utils.get\_cronograma\_data y renderiza la tabla visual de Actividad vs Meses.

### **F. Rutas de Correctivos (Incidencias)**

* **/correctivos:** Gestión de averías no planificadas.  
* **/correctivos/add, /update:** Similar al inventario, permite subir fotos de la avería y cambiar el estado (Detectada \-\> En curso \-\> Resuelta).

### **G. Configuración Global (/general\_settings)**

* **Gestión de Usuarios:** CRUD de usuarios y asignación de permisos booleanos.  
* **Fecha del Sistema:** Permite cambiar la fecha con la que opera el motor lógico (para simulaciones).  
* **Planificación Futura:** Define hasta cuándo se deben pre-calcular las OTs "Previstas".  
* **Logs:** Permite activar/desactivar el registro en archivo y descargarlo.  
* **Tipos de Equipo:** CRUD para las categorías de los equipos.

### **H. Inicialización (if \_\_name\_\_ \== '\_\_main\_\_':)**

* Al arrancar el script:  
  1. Llama a db.init\_db() para asegurar tablas.  
  2. Llama a utils.create\_default\_admin() para asegurar acceso.  
  3. **Sincronización:** Fuerza una actualización de la fecha del sistema a la fecha real del servidor y ejecuta el motor de OTs para asegurar que los datos estén frescos al iniciar.  
  4. Arranca el servidor web Flask en el puerto 5000, accesible desde la red (host='0.0.0.0').

## **4\. Archivos de Vistas (templates\_base.py y templates\_modules.py)**

No contienen lógica de ejecución, sino cadenas de texto multilínea que representan el HTML.

* **BASE\_TEMPLATE:** Contiene la estructura \<html\>\<head\>...\<body\>, la barra lateral (sidebar), la barra de navegación móvil y la importación de librerías CSS/JS (Bootstrap). Define bloques donde se inyectará el contenido dinámico.  
* **Templates en templates\_modules.py:** Son fragmentos HTML específicos (ej: tabla de inventario, formulario de usuario) que Flask inyecta dentro del BASE\_TEMPLATE según la ruta que se visite.