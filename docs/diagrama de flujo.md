``` mermaid
flowchart TD
    %% Estilos - Eliminados los punto y coma finales para evitar errores de parseo
    classDef startend fill:#f9f,stroke:#333,stroke-width:2px,color:black
    classDef process fill:#e1f5fe,stroke:#0277bd,stroke-width:2px,color:black
    classDef decision fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:black
    classDef db fill:#e0e0e0,stroke:#616161,stroke-width:2px,stroke-dasharray: 5 5,color:black
    classDef logic fill:#dcedc8,stroke:#689f38,stroke-width:2px,color:black

    %% --- BLOQUE 1: INICIO DEL SERVIDOR ---
    Start((Inicio Servidor)):::startend --> DBcheck{¿Existe DB?}:::decision
    DBcheck -- No --> InitDB[Crear Tablas SQLite]:::db
    DBcheck -- Sí --> ConnectDB[Conectar a DB]:::db
    InitDB --> DefaultUser[Crear Admin Por Defecto]:::process
    ConnectDB --> DefaultUser
    DefaultUser --> SyncDate[Sincronizar Fecha Sistema = Hoy]:::process
    SyncDate --> RunEngine[[Ejecutar Motor OTs]]:::logic
    RunEngine --> ServerReady((Servidor Listo)):::startend

    %% --- BLOQUE 2: FLUJO DE USUARIO ---
    ServerReady --> LoginPage[Página Login]:::process
    LoginPage --> InputCreds[/Usuario introduce credenciales/]:::process
    InputCreds --> CheckAuth{¿Credenciales OK?}:::decision
    CheckAuth -- No --> FlashError[Mostrar Error]:::process
    FlashError --> LoginPage
    CheckAuth -- Sí --> SetSession[Guardar Sesión y Permisos]:::process
    SetSession --> Dashboard[Panel Principal / Inventario]:::process

    %% --- BLOQUE 3: NAVEGACIÓN ---
    Dashboard --> UserAction{Acción Usuario}:::decision
    
    UserAction -- Gestión Inventario --> CRUD_Inv[Alta/Baja/Modif. Equipos]:::process
    UserAction -- Gestión Actividades --> CRUD_Act[Definir Planes Mtto.]:::process
    UserAction -- Ver OTs --> ViewOTs[Listado Órdenes Trabajo]:::process
    UserAction -- Reportar Avería --> CRUD_Corr[Gestión Correctivos]:::process
    UserAction -- Configuración --> ConfigPage[Ajustes Globales]:::process

    %% --- DETALLE LÓGICA GENERACIÓN OTs (utils.py) ---
    subgraph Engine [Motor de Generación Automática]
        direction TB
        StartEngine((Inicio Motor)):::logic --> GetDates[Obtener Fecha Sistema y Fecha Límite]:::logic
        GetDates --> LoopAct{Recorrer Actividades}:::decision
        
        LoopAct -- Siguiente Actividad --> CalcDate[Calcular Próxima Fecha]:::logic
        CalcDate --> CheckLimit{¿Fecha <= Límite?}:::decision
        
        CheckLimit -- Sí --> CheckExist{¿Existe OT?}:::decision
        CheckExist -- Sí --> NextIter[Saltar]:::logic
        CheckExist -- No --> DefineState{Comparar con Hoy}:::decision
        
        DefineState -- Fecha > Hoy --> StPrev[Estado: PREVISTA]:::logic
        DefineState -- Fecha + Periodo < Hoy --> StPend[Estado: PENDIENTE]:::logic
        DefineState -- Fecha == Hoy --> StCurso[Estado: EN CURSO]:::logic
        
        StPrev --> InsertOT[Insertar OT en DB]:::db
        StPend --> InsertOT
        StCurso --> InsertOT
        InsertOT --> NextIter
        
        CheckLimit -- No --> UpdateStates[Actualizar Estados OTs existentes]:::logic
        UpdateStates --> EndEngine((Fin Motor)):::logic
        
        NextIter --> LoopAct
    end

    %% Conexiones entre bloques
    RunEngine -.-> StartEngine
    ConfigPage -- Cambiar Fecha Sistema --> SyncDate
    ConfigPage -- Forzar Generación --> RunEngine
    CRUD_Act -- Nueva Actividad --> RunEngine
```