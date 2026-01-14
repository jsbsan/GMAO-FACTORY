---
## **Documentación Técnica del Código Fuente: GMAO Factory**
Fecha: 14 de Enero de 2026  
Tecnología: Python (Flask) \+ SQLite  
Arquitectura: Monolito Modular con Vistas Embebidas
---

**1\. Visión General de la Estructura**

El proyecto está estructurado como una aplicación web Flask que integra la lógica de negocio, la persistencia de datos y la interfaz de usuario. A diferencia de las arquitecturas web tradicionales que separan los archivos HTML, este sistema almacena las plantillas en variables de Python para facilitar la portabilidad.

### **Archivos Principales**

* **app.py**: Controlador principal. Gestiona las rutas, la inicialización y la coordinación de módulos.  
* **database.py**: Capa de acceso a datos (DAL). Gestiona la conexión a SQLite y la definición del esquema.  
* **utils.py**: Librería de utilidades, seguridad y **lógica de negocio core** (algoritmos de mantenimiento).  
* **resumen.py**: *Blueprint* (módulo) específico para el cuadro de mando (Dashboard).  
* **templates\_base.py / templates\_modules.py**: Capa de vista. Contienen el código HTML/Jinja2 almacenado en cadenas de texto.

## **2\. Análisis Detallado por Archivo**

### **2.1 app.py (Controlador Principal)**

Es el punto de entrada de la aplicación.

* **Configuración:** Inicializa la app Flask, define la secret\_key para sesiones y registra el *blueprint* de resumen.  
* **Filtros Jinja:** Registra json\_load\_filter para decodificar listas de archivos (imágenes/PDFs) en las vistas.  
* **Rutas de Autenticación:**  
  * /login: Verifica credenciales contra la base de datos usando hash seguro.  
  * /logout: Cierra la sesión del usuario.  
* **Rutas de Inventario (CRUD):**  
  * Gestiona el listado (/inventory), alta (/inventory/add), edición (/inventory/edit) y borrado (/inventory/delete) de equipos.  
  * Maneja la subida de archivos, convirtiéndolos a Base64 antes de guardar.  
* **Rutas de Impresión:**  
  * Genera vistas simplificadas y limpias para imprimir listados o fichas técnicas (/print\_inventory, /print\_all\_inventory).  
* **Inicialización (\_\_main\_\_):**  
  * Verifica si la BD existe; si no, la crea.  
  * Crea el usuario administrador por defecto.  
  * **Sincronización:** Al arrancar, actualiza la fecha del sistema a la fecha real y ejecuta el algoritmo de generación de órdenes de trabajo para asegurar que los datos estén al día.

### **2.2 database.py (Modelo de Datos)**

Encargado de la estructura de la información.

* **get\_db\_connection()**: Establece la conexión con mantenimiento\_factory.db devolviendo filas como diccionarios (sqlite3.Row).  
* **init\_db()**: Contiene el esquema DDL (Data Definition Language).  
  * Crea las tablas si no existen: tipos\_equipo, inventario, actividades, ordenes\_trabajo, correctivos, configuracion, usuarios.  
  * **Migraciones:** Incluye bloques try/except para alterar tablas existentes (añadir columnas) sin perder datos en actualizaciones.  
  * **Datos Semilla:** Inserta tipos de equipo por defecto y la configuración inicial.

### **2.3 utils.py (Lógica de Negocio y Seguridad)**

Este es el "cerebro" de la aplicación.

#### **A. Seguridad**

* **login\_required**: Decorador que protege rutas, redirigiendo al login si no hay sesión.  
* **permission\_required**: Decorador para Control de Acceso Basado en Roles (RBAC), verificando flags específicos (perm\_inventario, etc.) en la base de datos.

#### **B. Gestión de Archivos**

* **file\_to\_base64**: Convierte archivos binarios subidos (imágenes/PDFs) a cadenas de texto Base64 para almacenarlos directamente en la BD SQLite, evitando dependencias del sistema de archivos local.  
* **normalize\_files**: Estandariza la estructura JSON de los archivos para su lectura en el frontend.

#### **C. Motor de Mantenimiento (generate\_and\_update\_work\_orders)**

Esta es la función más crítica.

1. Obtiene la fecha\_sistema y la fecha\_prevista (horizonte de planificación).  
2. Recorre todas las actividades preventivas.  
3. Calcula las fechas teóricas de mantenimiento: Fecha \= Inicio \+ (N \* Periodicidad).  
4. Si la fecha calculada cae dentro del rango de planificación y no existe la OT, la crea.  
5. **Máquina de Estados:** Evalúa las OTs existentes y actualiza su estado (Pendiente, En curso, Prevista) comparando la fecha de la orden con la fecha del sistema.

#### **D. Cronograma (get\_cronograma\_data)**

Prepara una estructura de datos compleja (diccionarios anidados) que cruza **Equipos/Actividades** con **Meses del año** para renderizar la vista de calendario anual.


### **2.4 resumen.py (Dashboard Analytics)**

Módulo dedicado a la inteligencia de negocio.

* Calcula estadísticas agregadas (COUNT) filtradas por un rango de fechas.  
* Prepara los datos (labels y values) para ser consumidos por la librería gráfica Chart.js en el frontend.  
* Permite actualizar dinámicamente el rango de fechas de análisis.

## **3\. Flujo de Datos**

1. **Entrada:** El usuario interactúa con las vistas HTML (generadas por templates\_\*.py).  
2. **Procesamiento:** app.py recibe la petición.  
   * Si implica lógica compleja (ej. generar OTs), delega en utils.py.  
   * Si implica lectura/escritura, usa db.get\_db\_connection().  
3. **Persistencia:** Los datos se guardan en mantenimiento\_factory.db. Los archivos adjuntos se guardan como texto (JSON con Base64) en las columnas de la tabla.  
4. **Salida:** app.py inyecta los datos en las plantillas HTML y devuelve la página renderizada al navegador.

## **4\. Notas de Mantenimiento**

* **Offline-First:** El diseño de usar Base64 para archivos y plantillas embebidas está pensado para que la aplicación sea portable mediante un simple "Copiar y Pegar" de la carpeta, sin necesidad de configurar servidores de archivos estáticos externos.  
* **Simulación:** La aplicación depende de la tabla configuracion para saber "qué día es hoy" (fecha\_sistema). Esto permite simular escenarios futuros cambiando esa fecha desde el panel de ajustes.