## Estructura del Proyecto
GMAO_FACTORY/
│
├── app.py                  # Controlador Principal (Rutas y configuración Flask)
├── database.py             # Modelo de Base de Datos (Conexión y tablas)
├── utils.py                # Lógica de Negocio (Algoritmos de OTs, seguridad)
├── resumen.py              # Blueprint (Módulo) del Dashboard
│
├── static/                 # Archivos Estáticos (CSS, JS, Imágenes)
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   ├── datatables.min.css
│   │   └── all.min.css     # FontAwesome
│   │
│   └── js/
│       ├── bootstrap.bundle.min.js
│       ├── jquery.min.js
│       ├── datatables.min.js
│       ├── es-ES.json      # Traducción de DataTables
│       └── chart.min.js
│
├── templates/              # Vistas HTML (Motor Jinja2)
│   ├── base.html           # Layout Maestro (Menú lateral, cabecera)
│   ├── login.html          # Pantalla de acceso
│   ├── viewer.html         # Visor de archivos adjuntos
│   ├── about.html          # Página "Acerca de"
│   │
│   ├── resumen/
│   │   └── index.html      # Dashboard con gráficas y tablas resumen
│   │
│   ├── inventory/
│   │   ├── index.html      # Tabla de inventario
│   │   └── edit.html       # Formulario de edición
│   │
│   ├── activities/
│   │   ├── index.html      # Tabla de actividades
│   │   └── edit.html       # Formulario de edición
│   │
│   ├── work_orders/
│   │   ├── index.html      # Tabla de Órdenes de Trabajo
│   │   └── cronograma.html # Vista de calendario anual
│   │
│   ├── correctivos/
│   │   ├── index.html      # Tabla de incidencias
│   │   └── edit.html       # Formulario de edición
│   │
│   ├── settings/
│   │   ├── index.html      # Configuración global y usuarios
│   │   └── edit_type.html  # Edición de tipos de equipo
│   │
│   └── print/              # Vistas limpias para imprimir
│       ├── inventory.html
│       ├── all_inventory.html
│       ├── activity.html
│       ├── all_activities.html
│       ├── ot.html
│       ├── all_ots.html
│       ├── cronograma.html
│       ├── correctivo.html
│       └── all_correctivos.html
│
└── mantenimiento_factory.db # Archivo de Base de Datos (Generado automáticamente al arrancar)


## Descripción y funcion princial.
| Archivo | Tipo | Descripción y Función Principal |
| :---- | :---- | :---- |
| **app.py** | Python (Controlador) | **Punto de entrada de la aplicación.** |
• Inicializa el servidor web Flask. 
• Define las rutas URL principales (login, inventario, actividades, etc.). 
• Gestiona la autenticación y las sesiones de usuario. 
• Coordina la comunicación entre la base de datos y las plantillas HTML. 


| Archivo | Tipo | Descripción y Función Principal |
| :---- | :---- | :---- |
| **database.py** | Python (Modelo) | **Gestión de la Base de Datos.** |
• Conecta con el archivo mantenimiento\_factory.db (SQLite). 
• Define la estructura de las tablas (Inventario, Usuarios, OTs, etc.) mediante SQL. 
• Se encarga de crear las tablas si no existen al iniciar el programa. 

| Archivo | Tipo | Descripción y Función Principal |
| :---- | :---- | :---- |
| **utils.py** | Python (Lógica) | **Utilidades y Lógica de Negocio.** |
• Contiene funciones auxiliares de seguridad (login requerido, permisos).
 • Gestiona la conversión de archivos (imágenes/PDF) a formato Base64 para guardarlos en la BD. 
 • **Importante:** Contiene el algoritmo generate\_and\_update\_work\_orders que calcula y crea las Órdenes de Trabajo automáticamente. 


| Archivo | Tipo | Descripción y Función Principal |
| :---- | :---- | :---- |
| **resumen.py** | Python (Módulo) | **Módulo del Dashboard.** |
• Funciona como un "Blueprint" (sub-aplicación) de Flask. 
• Calcula las estadísticas y datos necesarios para las gráficas del panel de control (Resumen Ejecutivo). 
• Gestiona el filtrado por fechas en el resumen. 


| Archivo | Tipo | Descripción y Función Principal |
| :---- | :---- | :---- |
| **templates\_base.py** | Python (Vistas) | **Plantillas HTML Estructurales.** |
• Almacena el código HTML en variables de texto (Strings). 
• Contiene el BASE\_TEMPLATE (menú lateral, cabecera, importación de CSS/JS). 
• Incluye plantillas genéricas como Login, Visor de archivos y formatos de Impresión. 


| Archivo | Tipo | Descripción y Función Principal |
| :---- | :---- | :---- |
| **templates\_modules.py** | Python (Vistas) | **Plantillas HTML de Contenido.** |
• Almacena el código HTML específico de cada sección funcional. 
• Contiene los formularios y tablas para: Inventario, Actividades, Órdenes de Trabajo, Cronograma, Correctivos y Configuración. 
• Se insertan dinámicamente dentro de la plantilla base. 


