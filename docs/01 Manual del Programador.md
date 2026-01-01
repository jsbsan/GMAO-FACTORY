# **🛠️ Manual Técnico del Desarrollador: GMAO Factory v6.00**

Estado: Stable Release (Offline Edition)  
Fecha de Revisión: 01/01/2026  
Audiencia: Desarrolladores Backend, Arquitectos de Software, DevOps.

## **1\. Introducción y Stack Tecnológico**

**GMAO Factory** es un sistema de Gestión de Mantenimiento Asistido por Ordenador (CMMS) diseñado bajo una arquitectura monolítica para operar en entornos industriales con conectividad limitada o nula (Intranet/Air-gapped).  
Su núcleo funcional reside en la **generación determinista de Órdenes de Trabajo (OTs)** basada en la periodicidad de activos y una simulación temporal configurable ("Fecha del Sistema").

### **Stack Tecnológico**

| Capa | Tecnología | Versión | Justificación Técnica |
| :---- | :---- | :---- | :---- |
| **Runtime** | Python | 3.8+ | Robustez y facilidad de mantenimiento. |
| **Framework** | Flask | 3.0.0 | Ligereza y flexibilidad mediante Blueprints. |
| **Persistencia** | SQLite | 3.x | Base de datos *serverless* (archivo único), ideal para despliegues portables. |
| **Frontend** | Jinja2 \+ HTML5 | N/A | Renderizado en servidor (SSR) para reducir complejidad de estado en cliente. |
| **UI Framework** | Bootstrap | 5.3 | Diseño responsivo y componentes preconstruidos. |
| **Client-Logic** | jQuery \+ DataTables | 1.13 | Manipulación de DOM y gestión avanzada de tablas en el cliente. |
| **Dataviz** | Chart.js | 4.x | Visualización de KPIs sin dependencias externas pesadas. |

### **Dependencias Principales (requirements.txt)**

Flask==3.0.0       \# Core web framework  
Werkzeug==3.0.0    \# WSGI utilities & Hashing  
waitress==2.1.2    \# Servidor WSGI de producción (recomendado para Windows)

## **2\. Arquitectura del Sistema**

El sistema implementa una **Arquitectura Monolítica Modular** basada en el patrón **MVC (Modelo-Vista-Controlador)**.

### **Patrón de Diseño**

* **Modelo:** Definido en database.py (DDL) y gestionado mediante SQL nativo (sin ORM pesado).  
* **Vista:** Plantillas HTML en templates/ renderizadas por Jinja2.  
* **Controlador:** Rutas en app.py y resumen.py que orquestan la lógica de negocio y retornan las vistas.

### **Diagrama de Arquitectura de Alto Nivel**

Este diagrama muestra la topología física y lógica del despliegue estándar.  
``` mermaid
graph TD
    User["Usuario (Navegador Web)"]

    subgraph Cliente ["Cliente (Front-End)"]
        DOM["HTML5 / CSS3"]
        Static["Assets Locales /static"]
        JS_Engine["Motor JS (DataTables + Chart.js)"]
    end

    subgraph Backend ["Servidor de Aplicaciones (Backend)"]
        WSGI["Servidor WSGI (Waitress)"]
        FlaskRouter["Enrutador Flask (app.py)"]

        subgraph Controladores
            Auth["Módulo Auth"]
            Core["Módulo Core (OTs, Inventario)"]
            Dashboard["Blueprint Resumen"]
        end

        Logic["Lógica de Negocio (utils.py)"]
    end

    subgraph Datos ["Capa de Datos"]
        SQLite[("SQLite DB (.db)")]
        FS["Sistema de Archivos (Logs)"]
    end

    %% Conexiones
    User --> WSGI
    WSGI --> FlaskRouter
    FlaskRouter --> Core
    FlaskRouter --> Dashboard
    Core --> Logic
    Logic --> SQLite
    FlaskRouter --> User
    User --> Static
    User --> JS_Engine
```

## **3\. Guía de Configuración (Setup)**

Pasos para configurar el entorno de desarrollo local.

### **Prerrequisitos**

* **Python 3.8+** instalado y añadido al PATH.  
* **Git** (opcional, para control de versiones).

### **Pasos de Instalación**

1. Clonar/Descomprimir el Proyecto:  
   Extraer el artefacto gmao\_factory\_local\_fix.zip en su directorio de trabajo.  
2. **Crear Entorno Virtual:**  
   python \-m venv venv  
   \# Windows  
   venv\\Scripts\\activate  
   \# Linux/Mac  
   source venv/bin/activate

3. **Instalar Dependencias:**  
   pip install Flask Werkzeug

4. Verificar Assets Estáticos (Modo Offline):  
   Asegúrese de que las carpetas static/css y static/js contienen los archivos .css y .js reales (Bootstrap, DataTables, Chart.js) y no los placeholders de texto.  
5. Inicialización:  
   Ejecutar la aplicación por primera vez creará automáticamente la base de datos mantenimiento\_factory.db.  
   python app.py

6. Acceso:  
   Navegar a http://127.0.0.1:5000.  
   * **Usuario:** Administrador  
   * **Pass:** 123456

## **4\. Documentación de la API / Puntos de Entrada**

El sistema utiliza **Server-Side Rendering (SSR)**. Los endpoints devuelven principalmente HTML, aunque algunos comportamientos pueden considerarse una API interna.

### **Autenticación y Sesión**

* **Mecanismo:** Cookies de sesión firmadas por Flask (session\['user\_id'\]).  
* **Decoradores:**  
  * @utils.login\_required: Protege rutas generales.  
  * @utils.permission\_required('perm\_x'): RBAC granular.

### **Endpoints Principales**

| Método | Endpoint | Descripción | Payload / Params |
| :---- | :---- | :---- | :---- |
| GET | /login | Formulario de acceso. | \- |
| POST | /login | Procesa credenciales. | username, password |
| GET | /resumen/ | Dashboard principal. | \- |
| GET | /inventory | Tabla de activos. | \- |
| POST | /inventory/add | Crea activo. | multipart/form-data (img, pdf) |
| POST | /work\_orders/generate | **Trigger Core:** Genera OTs masivamente. | \- |
| GET | /cronograma | Vista calendario anual. | year (query param) |

### **Diagrama de Secuencia: Flujo de Autenticación**
``` mermaid
sequenceDiagram
    actor User
    participant Browser
    participant Controller as app.py
    participant DB as SQLite

    User->>Browser: Accede a /inventory
    Browser->>Controller: GET /inventory
    Controller->>Controller: Verificar Session['user_id']
    
    alt No Autenticado
        Controller-->>Browser: Redirect 302 -> /login
        Browser->>Controller: GET /login
        Controller-->>Browser: HTML Login Form
    else Autenticado
        Controller->>DB: SELECT * FROM inventario
        DB-->>Controller: Result Set
        Controller-->>Browser: HTML Inventory Table
    end
```

## **5\. Flujos de Datos y Persistencia**

### **Modelo de Datos (ERD)**

La integridad de los datos es crítica. El diseño utiliza FOREIGN KEYS para vincular activos, actividades y órdenes.  
**Nota importante:** Los archivos (Imágenes/PDFs) se almacenan como cadenas Base64 dentro de campos TEXT en la base de datos para mantener la portabilidad del archivo .db.  
``` mermaid
erDiagram
    USUARIOS {
        int id PK
        string username
        string password_hash
        string rol
        bool perms
    }
    INVENTARIO {
        int id PK
        string nombre
        int tipo_id FK
        text images_json_base64
        text pdfs_json_base64
    }
    ACTIVIDADES {
        int id PK
        int equipo_id FK
        int periodicidad
        date fecha_inicio
    }
    ORDENES_TRABAJO {
        int id PK
        int actividad_id FK
        date fecha_generacion
        string estado
    }
    CONFIGURACION {
        int id PK
        date fecha_sistema
        date fecha_prevista_limite
    }

    INVENTARIO ||--o{ ACTIVIDADES : tiene
    ACTIVIDADES ||--o{ ORDENES_TRABAJO : genera
```

## **6\. Diagrama de Flujo (Algoritmo Core)**

El proceso más complejo es la **generación de Órdenes de Trabajo**. Este algoritmo reside en utils.generate\_and\_update\_work\_orders.

### **Lógica del Algoritmo**

1. Obtiene la fecha\_sistema (actual o simulada) y la fecha\_prevista (límite futuro).  
2. Itera sobre cada actividad preventiva definida.  
3. Proyecta fechas futuras (fecha\_inicio \+ n \* periodicidad).  
4. Si la fecha proyectada cae dentro del rango, decide el estado de la OT (Prevista, En Curso, Pendiente) y la inserta si no existe.
``` mermaid
flowchart LR
    Start([Inicio Proceso]) --> GetDates["Obtener:<br/>Fecha Sistema (FS)<br/>Fecha Límite (FL)"]
    GetDates --> GetActivities["Obtener Lista de<br/>Actividades"]

    subgraph Bucle ["Proceso de Generación"]
        GetActivities --> CalcNext["Calcular Próxima Fecha:<br/>F = Inicio + (N * Periodo)"]
        CalcNext --> CheckLimit{¿F <= FL?}
        
        CheckLimit -- No --> EndLoop([Fin Bucle])
        CheckLimit -- Si --> CheckExist{¿Existe OT<br/>para ID + F?}
        
        CheckExist -- Si --> IncN["N = N + 1"]
        IncN --> CalcNext
        
        CheckExist -- No --> DecideState{Comparar<br/>F vs FS}
        
        DecideState -- "F > FS" --> State1["Estado: PREVISTA"]
        DecideState -- "F == FS" --> State2["Estado: EN CURSO"]
        DecideState -- "F < FS" --> State3["Estado: PENDIENTE"]
        
        State1 --> InsertDB
        State2 --> InsertDB
        State3 --> InsertDB
        
        InsertDB["INSERT INTO<br/>ordenes_trabajo"] --> IncN
    end
```

## **7\. Guía de Contribución**

### **Estándares de Código**

* **Linting:** Se recomienda seguir **PEP 8**.  
* **Seguridad:** Nunca commitear claves secretas reales. Usar variables de entorno en producción (aunque el código actual usa hardcoded para simplicidad local).  
* **Imports:** Organizar imports estándar primero, luego flask, luego módulos locales.

### **Gestión de Ramas (Git Flow Simplificado)**

* **main**: Código estable y listo para generar el ZIP de despliegue.  
* **feature/\<nombre\>**: Para nuevas funcionalidades (ej: feature/exportacion-excel).  
* **fix/\<nombre\>**: Para corrección de errores (ej: fix/chartjs-freeze).

### **Proceso de Despliegue (Build)**

Dado el carácter offline, el "despliegue" es la generación del artefacto.

1. Ejecutar python generar\_zip.py.  
2. Este script empaqueta el código y la estructura de directorios necesaria.  
3. El archivo gmao\_factory\_local\_fix.zip resultante es el entregable final (Artifact).

### **Diagrama CI/CD (Pipeline de Construcción Local)**
``` mermaid
graph LR
    Dev["Desarrollador"] -->|Commit| Git["Repositorio Local"]
    Git -->|Ejecuta| Builder["Script:<br/>generar_zip.py"]

    subgraph Build ["Proceso de Build"]
        Builder -->|Lee| Src["Código Fuente (.py)"]
        Builder -->|Lee| Tpl["Templates (.html)"]
        Builder -->|Define| Static["Estructura Static"]
        Static -->|Excluye| Binary["Binarios pesados"]
    end

    Builder -->|Output| Zip["gmao_factory_v6.zip"]
    Zip -->|Instalación| TargetPC["PC de Producción"] 
```
