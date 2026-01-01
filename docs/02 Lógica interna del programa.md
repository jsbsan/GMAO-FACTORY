# **🧠 Lógica y Funcionamiento Interno: GMAO Factory**

Este documento describe la arquitectura lógica, el flujo de datos y los algoritmos principales que impulsan la aplicación **GMAO Factory**.

## **1\. Visión General de la Arquitectura**

El sistema es una aplicación web monolítica construida sobre el micro-framework **Flask (Python)**. Sigue un patrón de diseño **MVC (Modelo-Vista-Controlador)** implícito, optimizado para portabilidad y despliegue sencillo (por ejemplo, en intranets industriales sin conexión a internet).

* **Controlador (app.py, resumen.py):** Gestiona las rutas HTTP, la autenticación de usuarios y orquesta el flujo de la aplicación.  
* **Modelo (database.py):** Define la estructura de datos relacional y gestiona la conexión con la base de datos **SQLite**. No utiliza un ORM complejo, sino SQL nativo para mayor control.  
* **Vista (templates\_base.py, templates\_modules.py):** Utiliza el motor de plantillas **Jinja2**. Las vistas no son archivos .html externos, sino que están embebidas como cadenas de texto dentro del código Python, lo que facilita la distribución del software como un "paquete todo incluido".  
* **Lógica de Negocio (utils.py):** Contiene el núcleo algorítmico del sistema, especialmente el motor de generación de órdenes de trabajo.

## **2\. Gestión de Datos y Persistencia**

La aplicación utiliza un único archivo de base de datos (mantenimiento\_factory.db).

### **Entidades Principales**

1. **Inventario:** Activos físicos. Se relacionan con tipos\_equipo.  
   * *Nota técnica:* Las imágenes y manuales PDF no se guardan en el disco duro del servidor. Se codifican en **Base64** y se almacenan directamente en campos de texto (TEXT) dentro de la base de datos como arrays JSON. Esto hace que la base de datos sea totalmente portable.  
2. **Actividades:** Definición de tareas de mantenimiento preventivo. Clave principal: periodicidad (frecuencia en días).  
3. **Órdenes de Trabajo (OTs):** Instancias ejecutables de las actividades.  
4. **Correctivos:** Gestión de incidencias no planificadas (averías).  
5. **Configuración:** Una tabla de una sola fila que almacena variables globales del sistema, como la "Fecha del Sistema" simulada.

## **3\. El Corazón del Sistema: Motor de Mantenimiento Preventivo**

La funcionalidad más crítica reside en la función generate\_and\_update\_work\_orders dentro de utils.py. A diferencia de sistemas que dependen de la fecha real del servidor, este sistema utiliza un concepto de **"Fecha del Sistema Simulada"**.

### **Algoritmo de Generación de OTs**

El sistema permite "viajar en el tiempo" o simular escenarios modificando la fecha del sistema. El algoritmo funciona así:

1. **Inputs:**  
   * fecha\_sistema: La fecha actual virtual configurada por el usuario.  
   * fecha\_prevista: Un horizonte de planificación futuro (ej. planificar los próximos 365 días).  
   * Actividades definidas con su fecha\_inicio y periodicidad.  
2. **Proceso de Generación:**  
   * El sistema itera sobre cada actividad.  
   * Calcula las fechas futuras teóricas: Fecha \= Inicio \+ (N \* Periodicidad).  
   * Si una fecha calculada cae dentro del rango (Fecha Sistema \-\> Fecha Prevista), verifica si ya existe una OT en la base de datos. Si no existe, la crea.  
3. Máquina de Estados de las OTs:  
   Al generar o actualizar una OT, su estado se determina dinámicamente comparando su fecha programada con la fecha\_sistema:  
   * 🔴 **Pendiente (Vencida):** Si Fecha Programada \+ Periodicidad \< Fecha Sistema. Indica que el mantenimiento no se hizo y ya pasó el tiempo límite.  
   * 🟡 **En Curso (Vigente):** Si Fecha Programada \<= Fecha Sistema. La tarea debe realizarse ahora.  
   * ⚪ **Prevista (Futura):** Si Fecha Programada \> Fecha Sistema. Tarea planificada para el futuro, visible en el cronograma pero no ejecutable aún.

## **4\. Flujo de Seguridad y Acceso**

El sistema implementa un control de acceso basado en roles (RBAC) simplificado:

1. **Autenticación:**  
   * Se utiliza werkzeug.security para el hash de contraseñas (pbkdf2:sha256).  
   * Las sesiones se gestionan mediante cookies firmadas de Flask.  
2. **Autorización (utils.permission\_required):**  
   * Decoradores personalizados protegen las rutas críticas.  
   * Los permisos son granulares: perm\_inventario, perm\_actividades, perm\_configuracion. Un usuario puede tener acceso de lectura general pero no permiso para modificar la configuración global.

## **5\. Módulo de Resumen (Dashboard)**

El archivo resumen.py actúa como un módulo independiente (Flask Blueprint).

* **Objetivo:** Proporcionar inteligencia de negocio (BI) rápida.  
* **Lógica:** Calcula estadísticas en tiempo real (conteo de OTs por estado, desglose de correctivos) dentro de un rango de fechas específico.  
* **Visualización:** Prepara los datos en formato JSON para ser consumidos por la librería frontend Chart.js, generando gráficos de anillo y pastel.

## **6\. Frontend y Renderizado**

Aunque es una aplicación web, se comporta casi como una aplicación de escritorio debido a su respuesta.

* **Jinja2:** Inyecta datos de Python en el HTML antes de enviarlo al navegador.  
* **Helpers:** Se utilizan filtros personalizados (como json\_load) para decodificar las estructuras de datos de archivos almacenadas en la base de datos antes de mostrarlas en la vista.