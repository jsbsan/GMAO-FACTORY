# **🛠️ Documentación Técnica: GMAO Factory v6.00**

Fecha de Actualización: 01/01/2026  
Versión: 6.00 (Stable / Offline Release)  
Autor Original: Julio Sánchez Berro

## **1\. Visión General de la Arquitectura**

GMAO Factory es una aplicación web monolítica desarrollada en **Python** utilizando el micro-framework **Flask**. Sigue un patrón de diseño **MVC (Modelo-Vista-Controlador)** implícito.

* **Backend:** Python 3 \+ Flask.  
* **Base de Datos:** SQLite 3 (Nativa, sin ORM pesado, uso de SQL directo).  
* **Frontend:** HTML5 renderizado por Jinja2 \+ Bootstrap 5\.  
* **Interactividad:** jQuery \+ DataTables (Manejo de datos en cliente) \+ Chart.js.  
* **Persistencia de Archivos:** Almacenamiento BLOB/Base64 directamente en base de datos (Imágenes y PDFs).

## **2\. Pila Tecnológica (Tech Stack)**

### **Backend**

| Componente | Tecnología | Propósito |
| :---- | :---- | :---- |
| **Lenguaje** | Python 3.8+ | Lógica del servidor. |
| **Framework** | Flask 3.x | Enrutamiento, gestión de peticiones y sesiones. |
| **Seguridad** | Werkzeug | Hashing de contraseñas (pbkdf2:sha256). |
| **Base de Datos** | SQLite3 | Almacenamiento relacional ligero (archivo único). |

### **Frontend**

| Componente | Tecnología | Propósito |
| :---- | :---- | :---- |
| **Diseño** | Bootstrap 5.3 | Sistema de rejilla y componentes UI responsivos. |
| **Tablas** | DataTables 1.13 | Paginación, búsqueda y exportación (Excel/PDF) en cliente. |
| **Gráficos** | Chart.js 4.x | Visualización de KPIs en el Dashboard. |
| **Iconos** | FontAwesome 6 | Iconografía vectorial. |

## **3\. Estructura del Proyecto**

La estructura de archivos de la versión 6.00 ha sido modularizada para facilitar el mantenimiento:  
GMAO\_FACTORY/  
│  
├── app.py                  \# \[CONTROLADOR\] Punto de entrada, rutas principales y orquestación.  
├── database.py             \# \[MODELO\] Definición de esquema DDL y conexión a SQLite.  
├── utils.py                \# \[LÓGICA\] Funciones auxiliares, seguridad y algoritmo de OTs.  
├── resumen.py              \# \[BLUEPRINT\] Módulo específico para el Dashboard.  
│  
├── static/                 \# Archivos estáticos (Offline)  
│   ├── css/                \# bootstrap.min.css, datatables.min.css, all.min.css  
│   └── js/                 \# bootstrap.bundle.js, jquery.js, chart.js, datatables.js  
│  
├── templates/              \# \[VISTA\] Plantillas Jinja2  
│   ├── base.html           \# Layout maestro (Sidebar, Navbar, Scripts comunes).  
│   ├── inventory/          \# Vistas CRUD de Inventario.  
│   ├── activities/         \# Vistas CRUD de Actividades.  
│   ├── work\_orders/        \# Listado de OTs y Cronograma.  
│   ├── correctivos/        \# Gestión de Incidencias.  
│   ├── settings/           \# Configuración global y usuarios.  
│   └── print/              \# Plantillas limpias para generación de reportes (window.print).  
│  
├── mantenimiento\_factory.db \# Archivo binario de base de datos (Creado al iniciar).  
└── gmao\_app.log             \# Registro de auditoría (Logging).

## **4\. Modelo de Datos (Esquema de Base de Datos)**

El sistema utiliza 7 tablas principales. La integridad referencial se mantiene mediante FOREIGN KEY.

1. **tipos\_equipo**: Categorización de activos (Ej: Eléctrico, Mecánico).  
2. **inventario**: Tabla maestra de activos.  
   * Campos clave: images y pdfs almacenan arrays JSON con cadenas Base64.  
3. **actividades**: Definición del mantenimiento preventivo.  
   * periodicidad: Entero (días).  
   * fecha\_inicio\_gen: Fecha ancla para el algoritmo de OTs.  
4. **ordenes\_trabajo**: Instancias generadas de mantenimiento.  
   * Estado: En curso, Pendiente, Prevista, Realizada, Aplazada, Rechazada.  
5. **correctivos**: Incidencias no planificadas.  
6. **usuarios**: Control de acceso (RBAC simplificado mediante flags booleanos).  
7. **configuracion**: Tabla *Singleton* (solo 1 fila, ID=1).  
   * Controla la fecha\_sistema (simulación) y fecha\_prevista (horizonte de planificación).

## **5\. Lógica Crítica del Negocio**

### **Algoritmo de Generación de OTs (utils.generate\_and\_update\_work\_orders)**

Este es el núcleo del GMAO. Se ejecuta al pulsar "Generar OTs" o al cambiar fechas en configuración.

1. **Entrada:** fecha\_sistema (simulada) y fecha\_prevista (límite futuro).  
2. **Iteración:** Recorre todas las filas de la tabla actividades.  
3. **Cálculo:**  
   * Calcula fechas futuras sumando periodicidad a la fecha\_inicio.  
   * Si la fecha calculada es futura respecto al sistema \-\> Estado: **Prevista** (Gris).  
   * Si la fecha calculada es hoy o pasada \-\> Estado: **En curso** (Amarillo).  
   * Si la fecha \+ periodicidad \< fecha sistema (vencida) \-\> Estado: **Pendiente** (Rojo).  
4. **Idempotencia:** Verifica si ya existe una OT para esa actividad en esa fecha específica antes de insertar, evitando duplicados.

### **Gestión de Archivos (Base64)**

El sistema **no** guarda archivos en disco (sistema de ficheros), sino en la base de datos.

* **Ventaja:** Portabilidad total (copiar el .db es hacer un backup completo).  
* **Desventaja:** La base de datos crece rápidamente.  
* **Implementación:** Los archivos subidos se leen en memoria, se codifican a Base64 y se guardan en columnas de texto (TEXT) como JSON serializado.

## **6\. Frontend y DataTables**

El renderizado es híbrido:

1. **Server-Side:** Flask consulta la BD y pasa **todos** los datos a la plantilla Jinja2.  
2. **Client-Side:** Jinja2 renderiza una tabla HTML \<table\> estándar con todas las filas.  
3. **Enhancement:** Al cargar el DOM, jQuery inicializa **DataTables** sobre esa tabla. DataTables se encarga de la paginación, el filtrado instantáneo y la ordenación sin realizar nuevas peticiones al servidor.

**Personalización implementada:**

* Traducción al español (es-ES.json).  
* Botones de exportación (Excel/PDF) mediante Buttons extension.  
* Filtro de rango de fechas personalizado (inyectado en el footer de la tabla de OTs).

## **7\. Seguridad**

* **Autenticación:** Decorador @utils.login\_required protege todas las rutas excepto login y static.  
* **Autorización:** Decorador @utils.permission\_required('perm\_nombre') verifica flags booleanos en la sesión del usuario (perm\_inventario, perm\_actividades, etc.).  
* **CSRF:** Protección básica mediante formularios POST directos (sin tokens CSRF explícitos en esta versión, se confía en el entorno de Intranet).

## **8\. Procedimiento de Despliegue**

Para desplegar en un servidor de producción o intranet:

1. **Servidor:** Se recomienda usar **Gunicorn** o **Waitress** en lugar del servidor de desarrollo de Flask (app.run).  
   pip install waitress  
   waitress-serve \--port=5000 app:app  
2. Configuración de Red: Asegurar que el puerto 5000 está abierto en el firewall del host. 
3. Mantenimiento: * Ejecutar VACUUM en SQLite periódicamente si se borran muchos archivos adjuntos para recuperar espacio