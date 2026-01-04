``` mermaid
graph TD
    %% Definición de Estilos (Colores para identificar capas)
    classDef db fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000;
    classDef logic fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#000;
    classDef view fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000;
    classDef user fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#000;
    classDef start fill:#333,stroke:#fff,stroke-width:2px,color:#fff;

    %% --- 1. INICIALIZACIÓN DEL SERVIDOR ---
    Start((Inicio app.py v5.30)):::start --> InitCheck{Existe DB?}
    InitCheck -- No --> InitDB[init_db: Crear Tablas SQLite]:::db
    InitDB --> CreateAdmin[Crear Admin Default]:::db
    InitCheck -- Si --> SyncDate[Sincronizar Fecha Sistema]:::logic
    CreateAdmin --> SyncDate
    SyncDate --> AutoGen[Generar OTs Automáticas al Inicio]:::logic
    AutoGen --> ServerRun[Flask Server Listen 0.0.0.0:5000]

    %% --- 2. FLUJO DE USUARIO Y AUTENTICACIÓN ---
    User((Usuario Web)):::user -->|Petición HTTP| ServerRun
    ServerRun --> AuthDecorator{Decorador @login_required}
    
    AuthDecorator -- No logueado --> ShowLogin[Render Login Template]:::view
    ShowLogin -->|POST Username/Pass| CheckPass{Verificar Hash}:::logic
    CheckPass -- Invalido --> FlashError[Flash: Error Credenciales]:::view
    FlashError --> ShowLogin
    CheckPass -- Valido --> SetSession[Guardar Session User/Permisos]:::logic
    SetSession --> RedirectRoot[Redirigir a /]

    %% --- 3. ENRUTAMIENTO PRINCIPAL ---
    AuthDecorator -- Si logueado --> Router{Router Flask}
    
    %% Ruta Raíz (Redirección nueva)
    Router -->|Ruta /| RedirectRes[Redirigir a /resumen]:::logic
    RedirectRes --> Router

    %% A. Módulo Resumen (Blueprint)
    Router -->|Ruta /resumen| LogicResumen[resumen.py: index]:::logic
    LogicResumen --> QueryStats[DB: Count OTs y Correctivos por Estado]:::db
    QueryStats --> RenderRes[Render Resumen + Chart.js]:::view

    %% B. Módulo Inventario
    Router -->|Ruta /inventory| LogicInv[app.py: inventory]:::logic
    LogicInv --> FilterInv{Hay Filtros?}
    FilterInv -- Si --> QueryInvFilter[DB: SELECT WHERE nombre/tipo]:::db
    FilterInv -- No --> QueryInvAll[DB: SELECT * LIMIT 10]:::db
    QueryInvFilter --> RenderInv[Render INVENTARIO_TEMPLATE]:::view
    QueryInvAll --> RenderInv

    %% C. Módulo Work Orders
    Router -->|Ruta /work_orders| LogicOT[app.py: work_orders]:::logic
    LogicOT --> RenderOT[Render OTS_TEMPLATE]:::view
    RenderOT --> UserActionOT{Acción Usuario}
    
    UserActionOT -->|Click Generar| RouteGenOT[POST /work_orders/generate]:::logic
    UserActionOT -->|Click Editar| RouteEditOT[POST /work_orders/update]:::logic

    %% --- 4. ALGORITMO DE GENERACIÓN DE OTs (Detalle) ---
    subgraph Algoritmo_OTs [Lógica_utils.py:generate_and_update_work_orders]
        direction TB
        RouteGenOT --> GetActs[DB: Leer Actividades Activas]:::db
        GetActs --> LoopActs{Bucle por Actividad}
        LoopActs --> CalcDate[Calc: Fecha = Inicio + N * Periodicidad]:::logic
        CalcDate --> CheckLimit{Fecha <= Limite Config?}
        
        CheckLimit -- Si --> CheckDupe{Existe OT en esa fecha?}
        CheckDupe -- No --> InsertOT[DB: INSERT ordenes_trabajo]:::db
        InsertOT --> CalcState[Logica Estado: Pendiente/Curso/Prevista]:::logic
        CalcState --> LoopActs
        CheckDupe -- Si --> LoopActs
        
        CheckLimit -- No --> UpdateOld[DB: Actualizar Estados Vencidos]:::db
    end

    %% D. Otros Módulos
    Router -->|Ruta /cronograma| LogicCron[app.py: cronograma]:::logic
    LogicCron --> BuildMatrix[Utils: Construir Matriz Mensual]:::logic
    BuildMatrix --> RenderCron[Render CRONOGRAMA_TEMPLATE]:::view

    Router -->|Ruta /correctivos| LogicCorr[app.py: correctivos]:::logic
    LogicCorr --> RenderCorr[Render CORRECTIVOS_TEMPLATE]:::view```