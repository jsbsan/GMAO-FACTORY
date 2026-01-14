# **🏭 GMAO Factory v7.00**

**Sistema de Gestión de Mantenimiento Asistido por Ordenador (CMMS)**

## **1\. Descripción general**

**GMAO Factory** es una solución de software integral, ligera y robusta diseñada para la gestión del mantenimiento en entornos industriales o de servicios. Desarrollada bajo una arquitectura monolítica con **Python (Flask)** y **SQLite**, esta aplicación permite centralizar la información técnica, planificar el mantenimiento preventivo y gestionar incidencias correctivas de manera eficiente.  
Su diseño **"Offline-First"** permite el despliegue en entornos de intranet o aislados (air-gapped) sin dependencia de conexión a internet, garantizando la autonomía operativa de la planta.

## **2\. Características Principales**

* **📊 Dashboard Ejecutivo:** Visualización en tiempo real de KPIs mediante gráficos interactivos (Chart.js) y tablas resumen para la toma de decisiones.  
* **📦 Gestión de Inventario:** Catalogación detallada de activos con soporte para almacenamiento de adjuntos (Imágenes y manuales PDF) directamente en la base de datos.  
* **🔄 Planificación Preventiva:** Motor de generación automática de Órdenes de Trabajo (OTs) basado en periodicidad y fechas de sistema simuladas.  
* **🛠️ Gestión de Correctivos:** Ciclo completo de reporte y resolución de averías e incidencias no planificadas.  
* **📅 Cronograma Visual:** Vista anual matricial para el seguimiento del cumplimiento del plan de mantenimiento.  
* **📅 Calendario Visual:** Vista mensual de las ordenes de trabajo para el seguimiento del cumplimiento del plan de mantenimiento.  
* **⚡ Interfaz Reactiva:** Tablas de datos avanzadas (DataTables) con filtrado, ordenación y exportación (Excel, PDF, Impresión) en el cliente.  
* **🔐 Seguridad y Auditoría:** Sistema de autenticación, control de acceso basado en roles (RBAC) y registro de logs de actividad.

## **3\. Instalación y Despliegue**

Siga estos pasos para desplegar la aplicación en un entorno local o servidor de intranet.

### **Prerrequisitos**

* **Python 3.13** o superior.  
* Navegador web moderno (Chrome, Firefox, Edge).

### **Pasos de Instalación usando el repositorio GitHub**

1. **Clonar el repositorio:**  
   git clone \[https://github.com/jsbsan/GMAO-FACTORY.git\](https://github.com/jsbsan/GMAO-FACTORY.git)  
   cd GMAO-FACTORY

2. **Crear un entorno virtual (Recomendado):**  
   \# Windows  
   python \-m venv venv  
   venv\\Scripts\\activate

   \# Linux/Mac  
   python3 \-m venv venv  
   source venv/bin/activate

3. **Instalar dependencias:**  
   pip install Flask Werkzeug waitress

4. Configuración de Archivos Estáticos (Modo Offline):  
   Para garantizar el funcionamiento sin internet, asegúrese de que la carpeta static/ contenga las librerías necesarias (Bootstrap 5, DataTables, jQuery, Chart.js). Nota: El proyecto está configurado para buscar estos recursos localmente.  

5. Iniciar la aplicación:  
   Al ejecutar el programa por primera vez, se creará automáticamente la base de datos mantenimiento\_factory.db.  
   python app.py

6. Acceso:  
   Abra su navegador y navegue a: http://localhost:5000

*Nota:*
 Tambien se puede crear una imagen docker para ejecutar la aplicación, vease el documento "06 Crear docker.md" en la carpeta docs.

## **4\. Credenciales por defecto**

El sistema genera automáticamente un usuario administrador en el primer despliegue. Se recomienda cambiar la contraseña inmediatamente desde el menú de configuración.

* **Usuario:** Administrador  
* **Contraseña:** 123456

## **5\. Estructura del proyecto**

La arquitectura del proyecto sigue el patrón MVC (Modelo-Vista-Controlador) de forma modular:  
GMAO\_FACTORY/src  
│  
├── app.py                  \# \[Controlador\] Punto de entrada, rutas y orquestación.  
├── database.py             \# \[Modelo\] Esquema de base de datos y conexión.  
├── utils.py                \# \[Lógica\] Algoritmos Core (Generación OTs) y seguridad.  
├── resumen.py              \# \[Blueprint\] Módulo específico del Dashboard.  
│  
├── static/                 \# Recursos estáticos (CSS, JS, Imágenes) para modo Offline.  
│   ├── css/  
│   └── js/  
│  
├── templates/              \# \[Vistas\] Plantillas HTML (Jinja2).  
│   ├── base.html           \# Layout maestro.  
│   ├── inventory/          \# Vistas de Inventario.  
│   ├── activities/         \# Vistas de Actividades.  
│   ├── work\_orders/       \# Vistas de OTs y Cronograma.  
│   ├── calendar/           \# Vistas de OTs en calendario mensual.  
│   ├── correctivos/        \# Vistas de Incidencias.  
│   ├── settings/           \# Configuración y Usuarios.  
│   ├── resumen/            \# Resumen de un periodo: gráficas y tablas de OT y Correctivos.
│   └── print/              \# Plantillas para impresión de reportes.  
│  
├── mantenimiento\_factory.db \# Base de Datos SQLite (Persistencia).  
└── gmao\_app.log             \# Logs del sistema.

## **6\. Tecnologías Utilizadas**

### **Backend**

* **Python:** Lenguaje principal.  
* **Flask:** Framework web ligero y modular.  
* **SQLite:** Base de datos relacional embebida (Zero-configuration).  
* **Werkzeug:** Utilidades WSGI y hashing seguro de contraseñas.

### **Frontend**

* **HTML5 / Jinja2:** Renderizado de vistas en el servidor (SSR).  
* **Bootstrap 5:** Framework CSS para diseño responsivo y componentes UI.  
* **JavaScript:**  
  * **jQuery:** Manipulación del DOM.  
  * **DataTables:** Tablas interactivas avanzadas (Filtrado, Paginación, Exportación).  
  * **Chart.js:** Visualización de datos y gráficas.

## **7\. Licencia**

Este proyecto está bajo la Licencia GPL 3.0.  
Eres libre de usarlo, modificarlo y distribuirlo manteniendo la autoría original.  
**Autor:** Julio Sánchez Berro.