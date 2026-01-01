# **📘 Manual de Usuario: GMAO Factory v6.00**
**Sistema de Gestión de Mantenimiento Asistido por Ordenador**

## **1\. Introducción**
Bienvenido a **GMAO Factory v6.00**. Este software ha sido diseñado para simplificar y optimizar la gestión del mantenimiento en entornos industriales y de instalaciones. Su objetivo principal es permitir a los técnicos y administradores llevar un control riguroso de los activos, planificar mantenimientos preventivos y responder eficazmente a las averías (correctivos).  
**Principales Ventajas:**
* **Funcionamiento Offline:** No requiere conexión a internet para operar.  
* **Gestión Documental:** Permite adjuntar fotos y manuales PDF directamente a los equipos.  
* **Simulación:** Capacidad de simular el paso del tiempo para planificar tareas futuras.  
* **Interfaz Rápida:** Búsquedas y filtrados instantáneos en grandes volúmenes de datos.

## **2\. Requisitos del Sistema**
Para ejecutar GMAO Factory, el equipo informático debe cumplir con los siguientes requisitos mínimos:
* **Sistema Operativo:** Windows 10/11, Linux o macOS.  
* **Navegador Web:** Google Chrome, Microsoft Edge o Mozilla Firefox (Versiones recientes).  
* **Software Base:** Python 3.8 o superior instalado.  
* **Conexión a Red:** Solo necesaria si se accede al programa desde otro ordenador de la misma red local (Intranet). No requiere internet.

## **3\. Guía de Instalación y Configuración**
Siga estos pasos si es la primera vez que inicia el sistema en el servidor o PC principal.
### **Paso 1: Preparación de Archivos**
Asegúrese de tener la carpeta del proyecto descomprimida (gmao\_factory\_local\_fix.zip). La estructura debe contener las carpetas templates, static y el archivo app.py.
### **Paso 2: Configuración de Librerías (Modo Offline)**
Para garantizar que el sistema funcione sin internet, verifique que la carpeta static contiene los archivos necesarios:
1. Vaya a static/css/ y asegúrese de tener: bootstrap.min.css, datatables.min.css, all.min.css.  
2. Vaya a static/js/ y asegúrese de tener: bootstrap.bundle.min.js, jquery.min.js, datatables.min.js, chart.min.js.
**Nota:** Si estos archivos faltan, el sistema funcionará pero se verá visualmente "roto" y las tablas no permitirán ordenar/filtrar.
### **Paso 3: Ejecución**
1. Abra una terminal o consola de comandos en la carpeta del proyecto.  
2. Escriba el siguiente comando y pulse Enter:
``` bash
python app.py
``` 
3. Verá un mensaje indicando: Running on http://0.0.0.0:5000.
### **Paso 4: Acceso** Abra su navegador web y escriba en la barra de direcciones:
* Desde el mismo PC: http://localhost:5000  
* Desde otro PC de la red: http://\<IP\_DEL\_SERVIDOR\>:5000

## **4\. Interfaz de Usuario**
La interfaz está dividida en tres áreas principales:
1. **Barra Lateral (Menú Principal):** Situada a la izquierda (color oscuro). Permite navegar entre los módulos:  
   * **Resumen:** Panel de control con gráficas.  
   * **Inventario:** Listado de máquinas y equipos.  
   * **Actividades:** Definición de tareas preventivas.  
   * **Órdenes de Trabajo (OTs):** Gestión del día a día.  
   * **Cronograma:** Vista de calendario anual.  
   * **Correctivos:** Reporte de averías.  
   * **Configuración:** Gestión de usuarios y fechas (Solo Admin).  
2. **Área de Trabajo (Central):** Donde se muestran las tablas, formularios y gráficos.  
   * **Tablas Interactivas:** Todas las tablas permiten **Buscar** (cuadro arriba a la derecha), **Ordenar** (clic en encabezados) y **Exportar** (botones Excel/PDF/Imprimir).  
3. **Barra Superior (Móvil):** En pantallas pequeñas, el menú se oculta y aparece un botón de "hamburguesa" (tres líneas) arriba a la izquierda.

---

## **5\. Guía de Uso (Paso a Paso)**
###   **A. Gestión de Inventario (Dar de alta una máquina)**
   1. Vaya al menú Inventario.
   2. Haga clic en el botón azul **\+ Nuevo Equipo**.  
   3. Rellene el formulario (Nombre, Tipo, Descripción).  
   4. **Archivos:** Puede seleccionar hasta 5 imágenes y 5 PDFs (manuales, planos).  
   5. Haga clic en **Guardar**.  
   6. **Visualización:** En la tabla, use los botones "Ojo" o iconos de imagen/PDF para ver los adjuntos.

### **B. Configurar Mantenimiento Preventivo**
   1. Vaya al menú Actividades**.**
   2. Haga clic en **\+ Nueva Actividad**.  
   3. Seleccione el **Equipo** del desplegable.  
   4. Defina la **Periodicidad** (ej: 30 días para mensual).  
   5. Indique la **Fecha de Inicio** (a partir de cuándo se debe generar la primera OT).  
   6. Describa las **Operaciones** a realizar.  
   7. Haga clic en **Crear Actividad**.

### **C. Generar y Cerrar Órdenes de Trabajo (OTs)El sistema genera las OTs automáticamente basándose en la fecha del sistem**a.
   1. Vaya a Órdenes de Trabajo.
   2. Haga clic en el botón amarillo **Generar OTs**. El sistema revisará todas las actividades y creará las OTs que toquen hoy o estén pendientes.  
   3. **Para cerrar una OT:**  
      * Localice la OT en la tabla (puede filtrar por "Pendiente" o "En curso").  
      * Haga clic en **Gestionar**.  
      * Cambie el estado a **Realizada**.  
      * Añada observaciones si es necesario y la fecha real de ejecución.  
      * Haga clic en **Actualizar OT**.

### **D. Reportar una Avería (Correctivo)**
   1. Vaya a Correctivos.
   2. Haga clic en **Nueva Incidencia**.  
   3. Seleccione el equipo averiado y describa el problema.  
   4. Puede adjuntar fotos de la rotura.  
   5. Estado inicial: **Detectada**.  
   6. Cuando se repare, edite la incidencia, indique la **Solución** y cambie el estado a **Resuelta**.

---

## **6\. Solución de Problemas (FAQ)**
   **P: La pantalla se queda congelada o en blanco al entrar en "Resumen".**
   **R:** Esto suele ocurrir si hay un problema con el redimensionado de los gráficos. Pruebe a **recargar la página (F5)**. La versión 6.00 incluye una corrección técnica (overflow: hidden) para prevenir esto.

   **P: No veo los iconos o las tablas se ven feas y sin formato.** 
   **R:** El sistema no está encontrando los archivos en la carpeta static. Verifique que bootstrap.min.css y datatables.min.css están en la carpeta correcta dentro del proyecto. Recuerde que este sistema está diseñado para funcionar **sin internet**, por lo que los archivos deben estar descargados localmente.

   **P: No puedo entrar, olvidé la contraseña.** 
   **R:** Por defecto, el usuario es **Administrador** y la contraseña **123456**. Si la cambió y la olvidó, deberá contactar con soporte técnico para resetearla directamente en la base de datos (mantenimiento\_factory.db).

   **P: Las OTs no se generan para el año que viene.** 
   **R:** Vaya a **Configuración Global** \> **Planificación Futura**. Asegúrese de que la "Fecha Prevista (Límite)" sea posterior a la fecha actual.

---

## **7\. Notas Técnicas**
   * **Arquitectura:** Aplicación web monolítica basada en Flask (Python).
   * **Base de Datos:** SQLite 3 (Archivo único: mantenimiento\_factory.db). No requiere servidor SQL dedicado.  
   * **Frontend:** Renderizado en servidor con Jinja2. Usa **DataTables** para la gestión de tablas en el lado del cliente (Client-side processing), lo que permite una respuesta instantánea con datasets de hasta 10,000 registros sin necesidad de recargar la página.  
   * **Seguridad:** Contraseñas almacenadas con hash seguro (werkzeug.security). Control de sesiones basado en cookies firmadas.  
   * **Backup:** Para realizar una copia de seguridad, simplemente copie el archivo mantenimiento\_factory.db y la carpeta static (si contiene imágenes subidas).