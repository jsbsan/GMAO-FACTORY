# GMAO Factory v5.1 🏭

GMAO Factory es un Sistema de Gestión de Mantenimiento Asistido por Ordenador diseñado para entornos industriales. Permite la gestión integral de inventarios, planes de mantenimiento preventivo, órdenes de trabajo y control de incidencias (correctivos).

Desarrollado en Python con Flask y SQLite.

## 🚀 Características Principales

- Inventario Digital: Gestión de fichas técnicas de equipos con imágenes y manuales PDF.

- Preventivos: Planificación automática de tareas recurrentes.

- Órdenes de Trabajo (OTs): Ciclo de vida completo (Prevista -> En Curso -> Pendiente/Realizada).

- Correctivos: Gestión de averías e incidencias.

- Simulación: Herramienta de "Fecha del Sistema" para simular escenarios futuros.

- Gestión Documental: Archivos adjuntos almacenados directamente en base de datos (portabilidad total).

- Seguridad: Control de acceso basado en roles (RBAC) y Logs de auditoría.

## 📋 Requisitos

- Python 3.8 o superior.

- Navegador web moderno (Chrome, Edge, Firefox).


## 🛠️ Instalación y Puesta en Marcha

1. Clonar el repositorio o descargar los archivos en una carpeta local.

2. Instalar dependencias:
Abre una terminal en la carpeta del proyecto y ejecuta:

```` bash
pip install flask werkzeug
```` 

3. Iniciar la aplicación:
Ejecuta el archivo principal:

```` bash
python app.py
```` 

4. Acceder:
Abre tu navegador y ve a:
http://localhost:5000

## 🔑 Credenciales por Defecto

El sistema creará automáticamente un usuario administrador en el primer arranque:

- Usuario: Administrador
- Contraseña: 123456

**Importante:** Se recomienda cambiar esta contraseña inmediatamente desde el menú "Configuración Global".

## 📂 Estructura del Proyecto

El proyecto sigue una arquitectura modular en un solo nivel para facilitar el despliegue:

- app.py: Controlador principal y rutas web.

- database.py: Gestión de conexión y esquema de la base de datos SQLite.

- utils.py: Lógica de negocio, algoritmos de generación de OTs y utilidades.

- templates_base.py: Plantillas HTML base (Layout, Login, Impresión).

- templates_modules.py: Plantillas HTML de los módulos funcionales.

- mantenimiento_factory.db: Base de datos (se genera automáticamente al iniciar).

- gmao_app.log: Registro de actividad (si se activa el logging).


## 📖 Documentación Adicional

Para más detalles, consulta los manuales incluidos en el repositorio:

MANUAL_USUARIO.md: Guía paso a paso para el usuario final.

DOCUMENTACION_TECNICA.md: Detalles de arquitectura para desarrolladores.

Autor: Julio Sánchez Berro

Licencia: GPL-3.0