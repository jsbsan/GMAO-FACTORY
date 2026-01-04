# **📘 Documentación Técnica: Lógica y Arquitectura de GMAO Factory**

Versión del Software: v6.16 (Referencia)  
Tecnología Base: Python (Flask) \+ SQLite \+ Jinja2 \+ Bootstrap 5

## **1\. Visión General de la Arquitectura**

GMAO Factory es una aplicación web **monolítica** diseñada para la gestión de mantenimiento industrial. Su arquitectura se caracteriza por ser autocontenida y orientada a entornos *offline* (sin conexión a internet).

### **1.1 Patrón de Diseño**

El sistema implementa un patrón **MVC (Modelo-Vista-Controlador)** adaptado al micro-framework Flask:

* **Modelo (Persistencia):** Gestionado mediante **SQLite** nativo (sin ORM complejo). La estructura de datos reside en un único archivo .db.  
* **Vista (Presentación):** Plantillas HTML renderizadas en el servidor (**SSR**) utilizando el motor **Jinja2**. La interfaz visual se apoya en **Bootstrap 5**.  
* **Controlador (Lógica):** Rutas de Flask (app.py y resumen.py) que interceptan las peticiones HTTP, procesan la lógica de negocio (apoyándose en utils.py) y devuelven la vista renderizada.

### **1.2 Características Distintivas**

1. **Simulación Temporal:** El sistema no depende necesariamente del reloj del servidor. Utiliza una "Fecha del Sistema" almacenada en la base de datos, lo que permite simular el paso del tiempo para pruebas o planificaciones futuras.  
2. **Portabilidad Total:** Las imágenes y documentos (PDFs) no se guardan en el sistema de archivos del servidor. Se codifican en **Base64** y se almacenan como cadenas de texto dentro de la base de datos. Esto permite que mover el archivo .db equivalga a mover toda la información del sistema.

## **2\. Modelo de Datos (Database Schema)**

La base de datos relacional (mantenimiento\_factory.db) consta de las siguientes tablas clave:

### **A. Tablas Maestras**

* **configuracion (Singleton):** Tabla de una sola fila (ID=1).  
  * fecha\_sistema: La fecha virtual con la que opera el algoritmo.  
  * fecha\_prevista: El horizonte límite para generar órdenes futuras.  
  * logging\_enabled: Flag para activar/desactivar el registro de actividad.  
* **usuarios:** Gestión de acceso y roles. Contiene *flags* booleanos para el sistema de permisos (perm\_inventario, perm\_actividades, etc.).  
* **tipos\_equipo:** Categorización simple de activos.

### **B. Tablas Operativas**

* **inventario:** El corazón de los activos.  
  * images / pdfs: Campos de tipo TEXT que almacenan arrays JSON. Cada elemento del array contiene el nombre del archivo y la cadena Base64 de los datos binarios.  
* **actividades:** Definición del mantenimiento preventivo (la "plantilla" de la tarea).  
  * periodicidad: Entero que representa los días entre mantenimientos.  
  * fecha\_inicio\_gen: Fecha semilla para el cálculo de recurrencia.  
* **ordenes\_trabajo (OTs):** Instancias concretas generadas a partir de una actividad.  
  * fecha\_generacion: La fecha teórica calculada por el algoritmo.  
  * estado: Cadena de texto que define el ciclo de vida (Pendiente, En curso, Realizada, etc.).  
* **correctivos:** Registro de incidencias no planificadas (averías). Comparte la lógica de almacenamiento de imágenes Base64 con la tabla de inventario.

## **3\. Lógica de Negocio (Core Logic)**

La lógica más compleja del sistema reside en el archivo utils.py, específicamente en la función generate\_and\_update\_work\_orders.

### **3.1 Algoritmo de Generación de Órdenes de Trabajo (OTs)**

Este es un proceso determinista que asegura que existan las órdenes de trabajo necesarias para cumplir con el plan de mantenimiento.  
**Flujo de Ejecución:**

1. **Obtención de Contexto:**  
   * Se recupera la fecha\_sistema (el "hoy" virtual).  
   * Se recupera la fecha\_prevista (el límite futuro hasta donde queremos generar).  
   * *Regla:* Si fecha\_prevista es nula o anterior a fecha\_sistema, el límite de generación es fecha\_sistema (solo genera hasta hoy).  
2. **Iteración de Actividades:**  
   * El sistema recorre cada fila de la tabla actividades.  
   * Para cada actividad, toma su fecha\_inicio\_gen y su periodicidad.  
3. **Proyección de Fechas:**  
   * Utiliza un bucle while para calcular fechas futuras:  
     $$Fecha\_{n} \= Fecha\_{inicio} \+ (n \\times Periodicidad)$$  
   * El bucle continúa mientras Fecha\_n \<= Fecha\_Límite.  
4. **Verificación de Existencia (Idempotencia):**  
   * Antes de crear una OT, consulta la base de datos: SELECT id FROM ordenes\_trabajo WHERE actividad\_id \= X AND fecha\_generacion \= Y.  
   * Si ya existe una OT para esa actividad en esa fecha exacta, **no hace nada** y pasa a la siguiente iteración. Esto evita duplicados.  
5. Determinación del Estado Inicial:  
   Si la OT no existe, se crea. El estado se asigna según la lógica temporal (Versión v6.08):  
   * **Pendiente:** Si la fecha generada es anterior al mes/año actual del sistema (Pasado).  
   * **En Curso:** Si la fecha generada coincide con el mes y año actual del sistema (Presente).  
   * **Prevista:** Si la fecha generada es posterior al mes/año actual del sistema (Futuro).

### **3.2 Actualización de Estados (Máquina de Estados)**

Además de generar nuevas OTs, el sistema revisa las OTs existentes que **no** están en estados terminales (es decir, ignora las que están "Realizada", "Rechazada" o "Aplazada").  
Recalcula el estado basándose en la misma lógica temporal descrita arriba. Esto permite que una OT que el mes pasado estaba "Prevista", al cambiar el mes, pase automáticamente a "En Curso", y si no se hace y pasa el mes, cambie a "Pendiente".

## **4\. Módulo de Resumen (Dashboard)**

El archivo resumen.py utiliza un Flask Blueprint para modularizar esta sección.  
**Lógica de Renderizado:**

1. **Consulta Dinámica:** Al cargar la página, consulta la tabla configuracion para obtener el rango de fechas (fecha\_inicio\_resumen, fecha\_fin\_resumen).  
2. **Agregación de Datos:**  
   * Ejecuta consultas COUNT(\*) agrupadas por estado filtrando por el rango de fechas.  
   * Genera dos conjuntos de datos JSON: uno para OTs y otro para Correctivos.  
   * Realiza consultas SELECT completas para poblar las tablas detalladas (DataTables) que aparecen bajo los gráficos.  
3. **Visualización:** Pasa estos datos JSON al frontend, donde Chart.js renderiza los gráficos de anillo y pastel.

## **5\. Frontend y UX**

### **5.1 Renderizado**

El sistema utiliza **Jinja2** para inyectar datos desde Python al HTML. Sin embargo, para mejorar la experiencia de usuario, se delega gran parte de la interacción al cliente (Navegador).

### **5.2 DataTables (Client-Side Processing)**

Las tablas de datos (\<table\>) se renderizan con todas las filas en el HTML inicial. Inmediatamente después, el script de **DataTables**:

1. Toma el control del DOM de la tabla.  
2. Añade paginación, campo de búsqueda y ordenación por columnas.  
3. **Filtros Personalizados:** En módulos como "Órdenes de Trabajo" y "Correctivos", se inyecta código JavaScript ($.fn.dataTable.ext.search.push) que intercepta el motor de búsqueda de DataTables para permitir filtrar por rangos de fecha sin recargar la página.

### **5.3 Exportación Inteligente**

Se implementa una lógica JS (smartExportConfig) en los botones de exportación:

* Verifica si el usuario ha seleccionado filas (usando la extensión *Select*).  
* Si hay selección $\\rightarrow$ Exporta solo la selección.  
* Si no hay selección $\\rightarrow$ Exporta todas las filas visibles (respetando el filtro actual).

## **6\. Seguridad**

1. **Hashing:** Las contraseñas se almacenan cifradas usando pbkdf2:sha256 (vía werkzeug.security).  
2. **Sesiones:** Se utilizan cookies de sesión firmadas criptográficamente con una SECRET\_KEY definida en app.py.  
3. **Control de Acceso (Decoradores):**  
   * @login\_required: Verifica que exista session\['user\_id'\].  
   * @permission\_required('perm\_x'): Verifica que el flag booleano correspondiente en la sesión del usuario sea True. Si no lo es, redirige y muestra un mensaje de error (Flash message).

## **7\. Infraestructura (Despliegue)**

La aplicación está diseñada para ser agnóstica a la infraestructura, pero se recomienda el uso de **Waitress** como servidor WSGI de producción por su compatibilidad con Windows y simplicidad.  
El ciclo de vida de la aplicación comienza en el bloque if \_\_name\_\_ \== '\_\_main\_\_': de app.py:

1. Verifica si existe el archivo .db.  
2. Si no existe, llama a db.init\_db() para crear el esquema.  
3. Crea el usuario administrador por defecto si no existe.  
4. Realiza una sincronización inicial de fechas y generación de OTs antes de empezar a servir peticiones HTTP.