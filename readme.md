# **🏭 GMAO Factory v6.00**

**Sistema de Gestión de Mantenimiento Asistido por Ordenador (CMMS)**  
GMAO Factory es una aplicación web ligera y potente construida con **Python (Flask)** y **SQLite**, diseñada para gestionar el mantenimiento integral de activos industriales o instalaciones. Permite el control de inventario, planificación de mantenimientos preventivos, gestión de incidencias (correctivos) y generación automática de órdenes de trabajo.

## **📋 Características Principales**

* **📊 Resumen Ejecutivo:** Dashboard con indicadores clave (KPIs) y gráficas de cumplimiento (Chart.js) sobre Órdenes de Trabajo e Incidencias.  
* **📦 Inventario de Activos:** Registro detallado de equipos con soporte para adjuntar imágenes y documentación técnica (PDFs).  
* **🔄 Mantenimiento Preventivo:** Definición de planes de mantenimiento con periodicidad personalizada y generación automática de Órdenes de Trabajo (OTs).  
* **🛠️ Gestión de Correctivos:** Registro y seguimiento de averías e incidencias imprevistas.  
* **📅 Cronograma Visual:** Vista anual del estado de las tareas (Realizadas, Pendientes, En Curso, etc.).  
* **🖨️ Reportes e Impresión:** Generación de informes en formato amigable para impresión o PDF.  
* **⚙️ Simulación Temporal:** Capacidad para alterar la "Fecha del Sistema" para simulaciones y pruebas de generación de tareas.  
* **🔐 Control de Acceso:** Sistema de usuarios con roles y permisos granulares por módulo.  
* **⚡ Interfaz Reactiva:** Tablas interactivas con búsqueda, filtrado y ordenación (DataTables) sin recargas innecesarias.

## **🚀 Instalación y Despliegue**

Este proyecto está diseñado para funcionar en entornos **Offline** (Intranet/Local), por lo que requiere configurar las librerías estáticas manualmente si no se usan CDNs.

### **1\. Prerrequisitos**

* Python 3.8 o superior.  
* Navegador Web moderno.

### **2\. Clonar el repositorio**

git clone \[https://github.com/tu-usuario/gmao-factory.git\](https://github.com/tu-usuario/gmao-factory.git)  
cd gmao-factory

### **3\. Configurar el Entorno Virtual**

Se recomienda usar un entorno virtual para aislar las dependencias:  
\# Windows  
python \-m venv venv  
venv\\Scripts\\activate

\# Linux/Mac  
python3 \-m venv venv  
source venv/bin/activate

### **4\. Instalar Dependencias**

Instala Flask y las librerías necesarias:  
pip install Flask

*(Nota: El proyecto utiliza principalmente la librería estándar de Python \+ Flask)*

### **5\. Configurar Archivos Estáticos (Modo Local)**

Para que el sistema funcione correctamente sin internet, descarga las siguientes librerías y colócalas en la carpeta static/:  
**En static/css/:**

* bootstrap.min.css (Bootstrap 5\)  
* datatables.min.css (DataTables \+ Bootstrap 5 Theme)  
* all.min.css (FontAwesome 6\)

**En static/js/:**

* bootstrap.bundle.min.js  
* jquery.min.js (jQuery 3.x)  
* datatables.min.js (DataTables Bundle: incluye Buttons, JSZip, PDFMake, HTML5 export, Print)  
* chart.min.js (Chart.js 4.x)  
* es-ES.json (Archivo de traducción de DataTables incluido en el proyecto)

### **6\. Ejecutar la Aplicación**

python app.py

La aplicación se iniciará en http://0.0.0.0:5000 (accesible desde cualquier equipo en la red local).

## **🔑 Credenciales por Defecto**

Al iniciar la aplicación por primera vez, se creará automáticamente un usuario administrador:

* **Usuario:** Administrador  
* **Contraseña:** 123456

**Importante:** Cambie esta contraseña inmediatamente desde el menú "Configuración Global".

## **📂 Estructura del Proyecto**

GMAO\_FACTORY/  
│  
├── app.py                  \# Controlador Principal (Rutas y Lógica)  
├── database.py             \# Modelo de Datos y Conexión SQLite  
├── utils.py                \# Funciones Auxiliares y Seguridad  
├── resumen.py              \# Blueprint del Dashboard  
│  
├── static/                 \# Archivos CSS/JS/Imágenes (Local)  
│   ├── css/  
│   └── js/  
│  
├── templates/              \# Vistas HTML (Jinja2)  
│   ├── base.html           \# Layout Principal  
│   ├── inventory/          \# Módulo de Inventario  
│   ├── work\_orders/        \# Módulo de OTs  
│   ├── ...                 \# Otros módulos  
│   └── print/              \# Vistas para impresión  
│  
└── mantenimiento\_factory.db \# Base de datos (Generada autom.)

## **🛠️ Tecnologías Utilizadas**

* **Backend:** Python 3, Flask.  
* **Base de Datos:** SQLite 3\.  
* **Frontend:** HTML5, Bootstrap 5\.  
* **Scripts:** jQuery, DataTables (Tablas avanzadas), Chart.js (Gráficos).  
* **Iconos:** FontAwesome 6\.

## **📄 Licencia**

Este proyecto está bajo la Licencia **GPL 3.0**. Eres libre de usarlo, modificarlo y distribuirlo manteniendo la autoría original.  
**Autor:** Julio Sánchez Berro.