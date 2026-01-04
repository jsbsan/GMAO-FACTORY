# **🛠️ Manual Técnico del Desarrollador: GMAO Factory**

Versión del Software: v6.16 (Stable / Offline)  
Fecha de Revisión: 04/01/2026  
Audiencia: Desarrolladores Backend, Arquitectos de Software, DevOps.

## **1\. Introducción y Stack Tecnológico**

**GMAO Factory** es una plataforma monolítica de gestión de mantenimiento industrial diseñada específicamente para operar en entornos **Air-gapped** (sin conexión a internet/Intranet aislada). Su arquitectura prioriza la portabilidad, permitiendo que todo el sistema (código, base de datos y assets) se distribuya mediante un único artefacto comprimido.

### **Propósito del Sistema**

Gestionar el ciclo de vida de activos industriales, incluyendo la catalogación (Inventario), la planificación determinista de mantenimientos preventivos (Generación de OTs) y la gestión reactiva de incidencias (Correctivos).

### **Stack Tecnológico**

| Capa | Tecnología | Versión | Justificación Técnica |
| :---- | :---- | :---- | :---- |
| **Backend** | Python | 3.8+ | Lógica de servidor robusta y multiplataforma. |
| **Framework** | Flask | 3.0.0 | Micro-framework WSGI ligero y modular. |
| **Persistencia** | SQLite | 3.x | Base de datos relacional embebida (Zero-conf). |
| **Frontend** | Jinja2 \+ HTML5 | N/A | Renderizado en servidor (SSR) para reducir la complejidad del cliente. |
| **UI Framework** | Bootstrap | 5.3 | Sistema de diseño responsivo. |
| **Client-Scripting** | jQuery \+ DataTables | 1.13 | Gestión de datos tabulares, filtrado y exportación en el cliente. |
| **Dataviz** | Chart.js | 4.x | Visualización de KPIs sin dependencias externas pesadas. |

### **Dependencias Principales (requirements.txt)**

Flask==3.0.0  
Werkzeug==3.0.0  
waitress==2.1.2  \# Servidor de producción WSGI recomendado

## **2\. Arquitectura del Sistema**

El sistema sigue un patrón arquitectónico **Monolítico Modular** basado en **MVC (Modelo-Vista-Controlador)**.

* **Vista:** Plantillas HTML (templates/) renderizadas por Jinja2.  
* **Controlador:** Rutas Flask (app.py, resumen.py) que manejan la petición HTTP.  
* **Modelo:** Definición de esquema (database.py) y lógica de negocio (utils.py).

### **Diagrama de Arquitectura de Alto Nivel**
``` mermaid
graph TD  
    User["Usuario (Navegador Web)"]  
      
    subgraph "Cliente (Front-End)"  
        Browser["Motor de Renderizado HTML/CSS"]  
        Static["Assets Locales (static/js, static/css)"]  
        JS_Engine["Motor JS (DataTables + Chart.js)"]  
    end

    subgraph "Servidor de Aplicaciones (Backend)"  
        WSGI["Servidor WSGI (Waitress/Gunicorn)"]  
        FlaskCore["Flask App Router (app.py)"]  
          
        subgraph "Controladores"  
            Auth["Módulo Auth"]  
            Core["Módulo Inventario/OTs"]  
            Dashboard["Blueprint Resumen"]  
        end  
          
        Logic["Lógica de Negocio (utils.py)"]  
    end

    subgraph "Capa de Datos"  
        SQLite[("SQLite DB (.db)")]  
        FS["Sistema de Archivos (Logs)"]  
    end

    User -- "HTTP Request (Port 5000)" --> WSGI  
    WSGI -- "Proxy Pass" --> FlaskCore  
    FlaskCore -- "Dispatch" --> Core & Dashboard  
    Core -- "Invoca" --> Logic  
    Logic -- "SQL Query" --> SQLite  
    FlaskCore -- "HTML Response" --> User  
    User -- "Load Assets" --> Static  
    User -- "Render & Interact" --> JS_Engine
```

## **3\. Guía de Configuración (Setup)**

Pasos exactos para levantar el entorno de desarrollo.

### **Prerrequisitos**

* Python 3.8 o superior.  
* Entorno virtual (venv) recomendado.  
* **Importante:** Descargar librerías estáticas manualmente para desarrollo offline.

### **Instalación**

1. **Clonar el Proyecto:**  
   git clone \<repositorio\>  
   cd gmao-factory

2. **Configurar Entorno Virtual:**  
   python \-m venv venv  
   \# Windows:  
   venv\\Scripts\\activate  
   \# Linux/Mac:  
   source venv/bin/activate

3. **Instalar Dependencias:**  
   pip install Flask Werkzeug waitress

4. Configuración de Assets Estáticos (Offline):  
   Para el funcionamiento correcto de DataTables (checkboxes y exportación), asegúrese de poblar la carpeta static/ con:  
   * **CSS:** bootstrap.min.css, datatables.min.css, all.min.css (FontAwesome).  
   * **JS:** bootstrap.bundle.min.js, jquery.min.js, chart.min.js, datatables.min.js (Bundle con extensiones Buttons, HTML5 Export, Print y **Select**).  
5. **Ejecución:**  
   python app.py

   *La base de datos mantenimiento\_factory.db se creará automáticamente en el primer inicio.*

## **4\. Documentación de la API / Puntos de Entrada**

Aunque es una aplicación SSR, los controladores actúan como endpoints funcionales.

### **Autenticación**

Se utilizan cookies de sesión firmadas (session\['user\_id'\]).

### **Puntos de Entrada Clave**

| Método | Ruta | Descripción | Payload Relevante |
| :---- | :---- | :---- | :---- |
| POST | /login | Autenticación de usuario. | username, password |
| POST | /inventory/add | Creación de activo. | multipart/form-data (imágenes, pdfs) |
| POST | /work\_orders/generate | **Trigger Core:** Generación masiva de OTs. | Ninguno (usa fecha sistema) |
| GET | /resumen/ | Dashboard (Blueprint). | \- |

### **Diagrama de Secuencia: Autenticación**
``` mermaid
sequenceDiagram  
    actor User as Usuario  
    participant Browser as Navegador  
    participant Controller as Flask (app.py)  
    participant DB as SQLite

    User->>Browser: Accede a /inventory  
    Browser->>Controller: GET /inventory  
    Controller->>Controller: Verificar Session Cookie  
      
    alt No Autenticado  
        Controller-->>Browser: Redirect 302 -> /login  
        Browser->>Controller: GET /login  
        Controller-->>Browser: HTML Login Form  
    else Autenticado  
        Controller->>DB: SELECT * FROM inventario  
        DB-->>Controller: Result Set  
        Controller-->>Browser: HTML Renderizado (Inventory Table)  
    end
```

## **5\. Flujos de Datos**

La información fluye desde formularios HTML hacia la base de datos SQLite. Los archivos binarios (imágenes/PDFs) reciben un tratamiento especial para mantener la portabilidad.

### **Persistencia de Archivos**

* **No** se usa sistema de archivos (/uploads).  
* **Sí** se usa codificación **Base64**. Los archivos se convierten a string y se almacenan en columnas TEXT dentro de la base de datos como arrays JSON.

### **Diagrama de Entidad-Relación (ERD)**
``` mermaid
erDiagram
    USUARIOS {
        int id PK
        string username
        string password_hash
        boolean perm_inventario
        boolean perm_actividades
    }
    INVENTARIO {
        int id PK
        string nombre
        int tipo_id FK
        text images "JSON Array (Base64)"
        text pdfs "JSON Array (Base64)"
    }
    ACTIVIDADES {
        int id PK
        int equipo_id FK
        int periodicidad "Días"
        date fecha_inicio_gen
    }
    ORDENES_TRABAJO {
        int id PK
        int actividad_id FK
        date fecha_generacion
        string estado "Enum: Pendiente, EnCurso..."
    }
    CORRECTIVOS {
        int id PK
        int equipo_id FK
        date fecha_detectada
        string estado
        text images "JSON Array (Base64)"
    }
    CONFIGURACION {
        int id PK
        date fecha_sistema "Simulación"
        date fecha_prevista "Horizonte"
    }

    INVENTARIO ||--o{ ACTIVIDADES : tiene
    ACTIVIDADES ||--o{ ORDENES_TRABAJO : genera
    INVENTARIO ||--o{ CORRECTIVOS : reporta
```

## **6\. Diagrama de Flujo (Lógica Core)**

El algoritmo más complejo del sistema es la **Generación y Actualización de Órdenes de Trabajo** (utils.generate\_and\_update\_work\_orders). Este proceso determina qué tareas preventivas deben lanzarse y actualiza los estados de las existentes.

### **Reglas de Negocio (v6.16)**

1. **En Curso:** Fecha OT \== Mes/Año actual del sistema.  
2. **Pendiente:** Fecha OT \< Mes/Año actual del sistema.  
3. **Prevista:** Fecha OT \> Mes/Año actual del sistema.

``` mermaid
flowchart TD  
    Start([Inicio Proceso]) --> GetContext[Obtener Fecha Sistema FS y Fecha Límite FL]  
    GetContext --> GetActs[SELECT * FROM actividades]  
      
    subgraph "Bucle de Generación"  
        GetActs --> CalcDate[Calcular Fecha Objetivo: F = Inicio + N * Periodo]  
        CalcDate --> CheckLimit{¿F <= FL?}  
          
        CheckLimit -- No --> EndGen([Fin Generación])  
        CheckLimit -- Si --> CheckDB{¿Existe OT para ID+F?}  
          
        CheckDB -- Si --> IncN[N = N + 1]  
        IncN --> CalcDate  
          
        CheckDB -- No --> DetermineState{Comparar Mes/Año F vs FS}  
          
        DetermineState -- "F > FS" --> StPrev[Estado: PREVISTA]  
        DetermineState -- "F == FS" --> StCurso[Estado: EN CURSO]  
        DetermineState -- "F < FS" --> StPend[Estado: PENDIENTE]  
          
        StPrev & StCurso & StPend --> InsertDB[INSERT INTO ordenes_trabajo]  
        InsertDB --> IncN  
    end  
      
    EndGen --> UpdateLoop[Bucle Actualización OTs Existentes]  
    UpdateLoop --> ApplyLogic[Aplicar misma lógica de Estado por Mes/Año]  
    ApplyLogic --> End([Fin Proceso])
```

## **7\. Guía de Contribución**
### **Estándares de Código**
* **Python:** Seguir **PEP 8**. Usar Snake Case para variables (mi\_variable).  
* **SQL:** Palabras clave en mayúsculas (SELECT, WHERE). Evitar ORM para mantener el rendimiento en consultas masivas.  
* **Frontend:** No usar estilos inline; utilizar clases de utilidad de Bootstrap.

### **Proceso de CI/CD (Pipeline de Construcción)**
Dado el despliegue offline, el pipeline finaliza en la creación de un artefacto .zip.  
``` mermaid
graph LR  
    Dev["Desarrollador"] -->|Commit| Git[Repositorio]  
    Git -->|Pull| BuildServer[Entorno de Build]  
      
    subgraph "Pipeline de Build (generar_zip.py)"  
        BuildServer -->|Inyecta| PyCode[Código Python]  
        BuildServer -->|Inyecta| Templates[Plantillas HTML]  
        BuildServer -->|Define| Static[Estructura Static]  
        Static -->|Empaqueta| Zip[Artefacto .zip]  
    end  
      
    Zip -->|Copia Manual/USB| Prod[Servidor Producción Offline]  
    Prod -->|Unzip & Run| AppRunning[GMAO Factory Live]
```

### **Gestión de Ramas**
* `main`: Código de producción listo para generar ZIP.  
* `develop`: Rama de integración principal.  
* `feature/<nombre>`: Nuevas funcionalidades (ej. `feature/exportacion-excel`).  
* `fix/<nombre>`: Corrección de errores (ej. `fix/datatable-checkbox`).

