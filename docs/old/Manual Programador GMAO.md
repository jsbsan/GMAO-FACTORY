# Manual Técnico del Desarrollador - GMAO Factory v5.1

Este documento sirve como referencia técnica exhaustiva para desarrolladores encargados del mantenimiento, extensión y refactorización del sistema **GMAO Factory**.

## 1. Introducción y Stack Tecnológico

**GMAO Factory** es una aplicación monolítica modular diseñada para la gestión integral del mantenimiento industrial. Su objetivo es centralizar la gestión de activos, la planificación de mantenimiento preventivo y la resolución de incidencias correctivas.

### Stack Tecnológico

|   |   |   |
|---|---|---|
|**Capa**|**Tecnología**|**Descripción**|
|**Backend**|Python 3.8+|Lenguaje principal.|
|**Framework Web**|Flask|Microframework para el manejo de rutas y peticiones HTTP.|
|**Base de Datos**|SQLite|Base de datos relacional ligera (archivo único: `mantenimiento_factory.db`).|
|**Seguridad**|Werkzeug|Hashing de contraseñas (`pbkdf2:sha256`).|
|**Frontend**|Jinja2 + Bootstrap 5|Renderizado de plantillas en servidor (SSR) y estilos responsivos.|
|**Motor de Plantillas**|Jinja2|Lógica de presentación integrada en Python (modularizada).|

**Dependencias Principales (`requirements.txt`):**

- `Flask`
    
- `werkzeug`
    

## 2. Arquitectura del Sistema

El sistema sigue un patrón de **Arquitectura Modular Monolítica** con una separación lógica de responsabilidades, aunque físicamente reside en una estructura plana para facilitar el despliegue en entornos restringidos.

### Estructura de Módulos

El código fuente se divide en 5 ficheros principales que actúan como capas lógicas:

1. **`app.py` (Controlador / Enrutador):**
    
    - Punto de entrada (`entry point`).
        
    - Inicializa la instancia `Flask`.
        
    - Define los _endpoints_ y gestiona los verbos HTTP.
        
    - Orquesta las llamadas a la lógica de negocio y renderiza las vistas.
        
2. **`database.py` (Capa de Persistencia):**
    
    - Gestiona la conexión con SQLite (`sqlite3`).
        
    - Contiene el DDL (Data Definition Language) para la creación de tablas.
        
    - Maneja migraciones básicas (e.g., `ALTER TABLE` controlados).
        
3. **`utils.py` (Capa de Lógica de Negocio y Servicios):**
    
    - Contiene la lógica "pesada" de la aplicación.
        
    - Algoritmos de generación de órdenes de trabajo (`generate_and_update_work_orders`).
        
    - Gestión de fechas (Sistema vs. Real).
        
    - Decoradores de seguridad (`@login_required`, `@permission_required`).
        
    - Utilidades de archivos (conversión Base64) y logging.
        
4. **`templates_base.py` y `templates_modules.py` (Capa de Vista):**
    
    - Almacenan el código HTML/Jinja2 en variables de cadena para evitar la dependencia de sistemas de archivos externos en entornos _sandbox_.
        
    - `templates_base.py`: Layouts maestros, login, navegación.
        
    - `templates_modules.py`: Vistas específicas de cada dominio (Inventario, OTs, etc.).
        

### Diagrama de Arquitectura de Alto Nivel

Este diagrama ilustra cómo interactúan los componentes dentro del entorno de ejecución.

``` mermaid
graph TD
    User[Cliente / Navegador] -->|HTTP Request| Flask[Servidor Flask app.py]
    
    subgraph Backend_Core [Backend Core]
        Flask -->|Verifica Auth| Utils[Servicios y Lógica utils.py]
        Flask -->|Consulta Datos| DB_Mod[Módulo DB database.py]
        Utils -->|Lógica Negocio| DB_Mod
        Utils -->|Escribe Logs| LogFile["gmao_app.log"]
    end
    
    subgraph Persistencia
        DB_Mod -->|SQL| SQLite[(SQLite DB)]
        SQLite -->|Resultados| DB_Mod
    end
    
    subgraph Presentacion [Capa de Presentación]
        Flask -->|Renderiza| Templates["Plantillas templates_*.py"]
        Templates -->|HTML| User
    end
```

## 3. Guía de Configuración (Setup)

Sigue estos pasos para configurar el entorno de desarrollo local.

### Prerrequisitos

- Python 3.8 o superior instalado.
    
- Git (opcional, para control de versiones).
    

### Pasos de Instalación

1. **Clonar el repositorio (o descargar fuentes):**
    
    ```
    git clone https://repo-url/gmao-factory.git
    cd gmao-factory
    ```
    
2. **Crear entorno virtual (Recomendado):**
    
    ```
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```
    
3. **Instalar dependencias:**
    
    ```
    pip install flask werkzeug
    ```
    
4. **Inicialización de la Base de Datos:** El sistema crea automáticamente el archivo `mantenimiento_factory.db` y el usuario administrador al arrancar por primera vez. No se requiere script SQL manual.
    
5. **Ejecutar la aplicación:**
    
    ```
    python app.py
    ```
    
    La aplicación estará disponible en `http://localhost:5000`.
    
6. **Credenciales Iniciales:**
    
    - User: `Administrador`
        
    - Pass: `123456`
        

## 4. Documentación de la API / Puntos de Entrada

Dado que es una aplicación renderizada en servidor (SSR), los endpoints devuelven HTML. Sin embargo, la estructura de rutas es RESTful en su nomenclatura.

### Autenticación y Sistema

|   |   |   |
|---|---|---|
|**Método**|**Endpoint**|**Descripción**|
|`GET/POST`|`/login`|Gestión de inicio de sesión. Crea la sesión de usuario.|
|`GET`|`/logout`|Destruye la sesión.|
|`GET`|`/`|Dashboard principal (redirecciona a Inventario).|
|`GET`|`/system_date_config`|Panel de configuración de fecha simulada.|

### Inventario (`/inventory`)

|            |                          |                                                              |
| ---------- | ------------------------ | ------------------------------------------------------------ |
| **Método** | **Endpoint**             | **Descripción**                                              |
| `POST`     | `/inventory/add`         | Crea un nuevo equipo. Payload: `Multipart/form-data`.        |
| `GET`      | `/inventory/edit/<id>`   | Formulario de edición.                                       |
| `POST`     | `/inventory/update/<id>` | Procesa la actualización del equipo.                         |
| `POST`     | `/inventory/delete/<id>` | **Borrado en cascada**. Elimina equipo y datos relacionados. |

### Órdenes de Trabajo (`/work_orders`)

|   |   |   |
|---|---|---|
|**Método**|**Endpoint**|**Descripción**|
|`GET`|`/work_orders`|Listado de OTs con filtros.|
|`POST`|`/work_orders/generate`|Dispara el algoritmo de generación masiva de OTs.|
|`POST`|`/work_orders/update/<id>`|Actualiza el estado (Realizada/Rechazada) de una OT.|

### Diagrama de Secuencia: Generación de Órdenes de Trabajo

Este diagrama explica la lógica crítica de generación de OTs.

``` mermaid
sequenceDiagram
    actor Admin
    participant App as app.py
    participant Utils as utils.py
    participant DB as SQLite

    Admin->>App: POST /work_orders/generate
    App->>Utils: get_system_date()
    Utils-->>App: fecha_sistema
    App->>Utils: generate_and_update_work_orders(conn, fecha)
    
    loop Para cada Actividad
        Utils->>DB: SELECT * FROM actividades
        Note over Utils: Calcular próximas fechas: Inicio + Periodicidad
        
        alt Fecha <= Límite
            Utils->>DB: Check if OT exists
            alt OT no existe
                Note over Utils: Determinar estado: Prevista/EnCurso/Pendiente
                Utils->>DB: INSERT orden_trabajo
            end
        end
    end

    Utils-->>App: Retorna contador OTs generadas
    App-->>Admin: Flash Message + Redirect
```

## 5. Flujos de Datos

La aplicación sigue un flujo síncrono bloqueante típico de Flask.

1. **Recepción:** `app.py` intercepta la petición.
    
2. **Middleware:** Los decoradores `@login_required` y `@permission_required` (en `utils.py`) validan la sesión (`flask.session`). Si falla, redirige a `/login` o al índice.
    
3. **Procesamiento:**
    
    - Se abre conexión a BD (`db.get_db_connection()`).
        
    - Se ejecuta la lógica de negocio (ej: cálculos de fechas, validación de archivos).
        
    - Se ejecutan las queries SQL.
        
    - Si es una modificación crítica, se invoca `utils.log_action()` para auditoría.
        
4. **Respuesta:** Se inyectan los objetos de datos en las cadenas de plantillas (`render_template_string`) y se devuelve HTML al cliente.
    

### Diagrama de Entidad-Relación (ERD)

Estructura de la base de datos `mantenimiento_factory.db`.

``` mermaid
erDiagram
    TIPOS_EQUIPO ||--o{ INVENTARIO : clasifica
    INVENTARIO ||--o{ ACTIVIDADES : tiene
    INVENTARIO ||--o{ CORRECTIVOS : sufre
    ACTIVIDADES ||--o{ ORDENES_TRABAJO : genera
    
    USUARIOS {
        int id PK
        string username
        string password_hash
        string rol
        int perm_inventario
    }

    INVENTARIO {
        int id PK
        string nombre
        text images "JSON Base64"
        text pdfs "JSON Base64"
    }

    ORDENES_TRABAJO {
        int id PK
        date fecha_generacion
        string estado "En curso, Pendiente, Prevista..."
    }

    CONFIGURACION {
        int id PK
        date fecha_sistema
        date fecha_prevista
        bool logging_enabled
    }
```

## 6. Guía de Contribución

### Estándares de Código

- **Estilo:** PEP 8.
    
- **Indentación:** 4 espacios.
    
- **Imports:** Agrupados (Librerías estándar, Terceros, Locales).
    
- **Manejo de Errores:** Bloques `try-except` obligatorios en operaciones de base de datos y manejo de archivos.
    

### Gestión de Ramas (Git Flow Simplificado)

- `main`: Código estable y producción.
    
- `develop`: Integración de nuevas funcionalidades.
    
- `feature/<nombre-feature>`: Desarrollo de nuevas características (ej: `feature/nuevos-reportes`).
    
- `fix/<nombre-bug>`: Corrección de errores.
    

### Proceso de Pull Request

1. Asegurar que `python app.py` arranca sin errores de sintaxis.
    
2. Verificar que las migraciones de base de datos en `init_db()` son idempotentes (no fallan si la tabla ya existe).
    
3. Si se modifican plantillas, actualizar tanto `templates_base.py` como `templates_modules.py`.
    

### Diagrama de Flujo CI/CD (Propuesto)

Flujo recomendado para la integración continua.

``` mermaid
flowchart LR
    Dev[Desarrollador] -->|Push| Repo[Repositorio Git]
    Repo -->|Webhook| CI[Servidor CI: GitHub Actions/Jenkins]
    
    subgraph "Pipeline CI"
        CI --> Lint[Linter: Flake8]
        Lint --> Test[Unit Tests :PyTest]
        Test --> Build[Build Docker Image]
    end
    
    Build -->|Success| Registry[Container Registry]
    Registry -->|Deploy| Server[Servidor Producción]
```
