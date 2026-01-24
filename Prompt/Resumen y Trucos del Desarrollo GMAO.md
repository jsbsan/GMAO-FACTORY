Aquí tienes un resumen estructurado del desarrollo del proyecto **GMAO Factory** basado en el historial de prompts proporcionado, destacando la evolución, los hitos técnicos y una sección de "Trucos" derivados de los problemas resueltos.

### ---

**1\. Resumen del Proyecto: GMAO Factory**

**Objetivo:** Desarrollar un sistema de Gestión de Mantenimiento Asistido por Ordenador (GMAO) para una fábrica.  
**Stack Tecnológico:** Python (Flask), SQLite3, Bootstrap (Frontend), Jinja2 (Templates) y librerías JS (DataTables, FullCalendar).  
**Características Clave:**

* Funciona **100% Offline** (red local), sin dependencias de CDNs externas.  
* Gestión de **Inventario** (con imágenes y PDF en Base64).  
* Gestión de **Actividades** (Preventivos) y **Correctivos** (Incidencias).  
* Generación automática de **Órdenes de Trabajo (OT)** basada en periodicidad.  
* Visualización mediante **Cronogramas** (tabla anual) y **Calendario** (FullCalendar).  
* Tableros de resumen con gráficas y reportes en PDF.

### ---

**2\. Evolución y Hitos del Desarrollo**

El desarrollo se ha dividido en varias fases críticas marcadas por cambios de arquitectura y refinamiento de lógica:

#### **A. Fase de Prototipado y Modularización (v0.00 \- v5.99)**

* **Inicio:** Se comenzó con un solo archivo (app.py), lo que se volvió insostenible.  
* **Refactorización:** Se dividió el proyecto en:  
  * database.py (Modelos y conexión).  
  * utils.py (Lógica de fechas, generación de OTs y herramientas).  
  * app.py (Rutas y controlador).  
  * **Templates:** Se pasó de tener el HTML como strings dentro de Python a usar archivos .html reales en una carpeta /templates.  
* **Lógica de OTs:** Se definió la lógica de colores y estados: *Roja* (Pendiente/Pasada), *Gris* (Prevista/Futura), *Verde* (Realizada).

#### **B. Fase de Estabilización y UI (v6.00 \- v6.16)**

* **Documentación:** Creación de manuales de usuario y técnicos, y diagramas de flujo (Mermaid).  
* **DataTables:** Integración profunda de tablas interactivas con paginación, filtros y exportación. Fue un punto de dolor recurrente (errores de redibujado al volver atrás en el navegador).  
* **Modo Oscuro:** Implementación de temas Claro/Oscuro, resolviendo múltiples problemas de contraste en textos de tablas y formularios.

#### **C. Fase de Funcionalidades Avanzadas (v6.XX \- v7.15)**

* **Calendario:** Integración de FullCalendar con capacidad de edición y lógica de impresión específica para que se vean los 7 días en papel.  
* **Docker:** Preparación del entorno para ser contenerizado.  
* **Backup/Restore:** Funcionalidad para descargar (.bak) y restaurar la base de datos SQLite desde la interfaz.  
* **Lógica de Periodicidad:** Ajuste manual para que periodos de 30 días se traten como "1 mes natural" para evitar desfases en el calendario anual.  
* **Estandarización UI:** Unificación de la posición de botones (Buscar, Exportar, Nuevo) en todas las pantallas (Inventario, Actividades, OTs).

### ---

**3\. Sección de Trucos y Lecciones Aprendidas (Troubleshooting)**

Basado en los errores y soluciones documentados en el chat, aquí tienes los "trucos" técnicos más valiosos extraídos del proceso:

#### **🛠️ Frontend y DataTables**

* **Conflicto StateSave vs. Filtros:** Si usas stateSave: true en DataTables para recordar la página, y además tienes filtros personalizados (como fechas), la tabla puede aparecer vacía al volver atrás.  
  * *Truco:* Usar inicialización diferida o limpiar filtros residuales antes de redibujar (draw()) la tabla al cargar la página.  
* **DataTables "Unknown Parameter":** El error Requested unknown parameter suele ocurrir cuando el número de columnas en el \<thead\> del HTML no coincide exactamente con las columnas de datos o cuando faltan celdas en el \<tbody\>.  
  * *Truco:* Verificar siempre si hay columnas ocultas (como IDs) o columnas de checkbox añadidas dinámicamente.

#### **🖨️ Impresión Web (CSS Print)**

* **FullCalendar cortado:** Al imprimir calendarios web, el navegador suele cortar columnas si el ancho es fluido.  
  * *Truco:* En @media print, forzar min-width: 1024px \!important al contenedor del calendario y usar zoom o escala para que quepa en A4 horizontal.  
  * *Truco:* Para evitar cortes verticales, forzar height: auto y eliminar overflow: scroll en los contenedores internos del calendario.

#### **🐍 Python y Flask**

* **Jinja2 Debugging:** Errores como Encountered unknown tag 'endfor' suelen indicar un anidamiento incorrecto.  
  * *Truco:* Revisar siempre que cada {% if %} tenga su {% endif %} antes de cerrar un {% for %} externo.  
* **Lógica de Fechas (30 días vs 1 mes):** Sumar 30 días matemáticamente provoca que las OTs se desplacen de día cada mes (enero tiene 31, febrero 28).  
  * *Truco:* Implementar lógica condicional: si periodicidad % 30 \== 0, usar relativedelta(months=+X) en lugar de timedelta(days=30).

#### **🎨 UI/UX y Modo Oscuro**

* **Contraste Invisible:** Muchos frameworks (Bootstrap) ponen texto negro por defecto. En modo oscuro, si solo cambias el fondo, el texto desaparece.  
  * *Truco:* Forzar colores explícitos en elementos de tablas (th, td) y inputs, y no confiar en la herencia automática del body.  
* **Consistencia de Botones:**  
  * *Truco:* Al diseñar múltiples módulos (Inventario, OTs), crea una "guía de estilo" para los botones de acción (Buscar a la izquierda, Exportar a la derecha) desde el principio, para evitar tener que refactorizar 4 archivos HTML distintos al final (como ocurrió en la v7.15).

### ---

