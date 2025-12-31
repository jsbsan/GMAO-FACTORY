``` mermaid
flowchart TD
    %% Estilos
    classDef startend fill:#f9f,stroke:#333,stroke-width:2px,color:black
    classDef process fill:#e1f5fe,stroke:#0277bd,stroke-width:2px,color:black
    classDef decision fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:black
    classDef db fill:#e0e0e0,stroke:#616161,stroke-width:2px,stroke-dasharray: 5 5,color:black
    classDef logic fill:#dcedc8,stroke:#689f38,stroke-width:2px,color:black

    %% --- BLOQUE 1: INICIO DEL SERVIDOR (app.py) ---
    Start((Inicio Servidor)):::startend --> DBcheck{¿Existe DB?}:::decision
    DBcheck -- No --> InitDB[Crear Tablas SQLite]:::db
    DBcheck -- Sí --> ConnectDB[Conectar a DB]:::db
    
    InitDB --> SetConfig["Configurar: Fecha Sistema=Hoy, Fecha Prevista=Hoy+365"]:::db
    SetConfig --> DefaultUser[Crear Admin Por Defecto]:::process
    ConnectDB --> UpdateConfig{¿Fecha Prevista es NULL?}:::decision
    UpdateConfig -- Sí --> FixConfig[Actualizar Fecha Prevista = Hoy+365]:::db
    UpdateConfig -- No --> DefaultUser
    FixConfig --> DefaultUser
    
    DefaultUser --> SyncDate[Sincronizar con Fecha Real]:::process
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

    %% --- BLOQUE 3: NAVEGACIÓN Y ACCIONES ---
    Dashboard --> UserAction{Acción Usuario}:::decision
    
    UserAction -- Gestión Inventario --> CRUD_Inv[Alta/Baja/Modif. Equipos]:::process
    UserAction -- Gestión Actividades --> CRUD_Act[Definir Planes Mtto.]:::process
    UserAction -- Ver OTs --> ViewOTs[Listado Órdenes Trabajo]:::process
    UserAction -- Cronograma --> ViewCron[Vista Anual]:::process
    UserAction -- Reportar Avería --> CRUD_Corr[Gestión Correctivos]:::process
    UserAction -- Configuración --> ConfigPage[Ajustes Globales]:::process

    %% --- DETALLE MOTOR GENERACIÓN (utils.py) ---
    subgraph Engine [Motor de Generación y Actualización]
        direction TB
        StartEngine((Inicio Motor)):::logic --> GetDates[Leer Fecha Sistema y Fecha Prevista]:::logic
        GetDates --> LoopAct{Recorrer Actividades}:::decision
        
        LoopAct -- Siguiente Actividad --> CalcDate[Calcular Próxima Fecha]:::logic
        CalcDate --> CheckLimit{¿Fecha <= Fecha Prevista?}:::decision
        
        CheckLimit -- Sí --> CheckExist{¿Existe OT ese día?}:::decision
        CheckExist -- Sí --> NextIter[Saltar]:::logic
        CheckExist -- No --> CreateOT["Crear OT (Estado: En Curso/Prevista/Pendiente)"]:::db
        CreateOT --> NextIter
        
        CheckLimit -- No (Fin Actividad) --> LoopAct
        
        LoopAct -- Fin Actividades --> GetActiveOTs[Buscar OTs Activas]:::logic
        GetActiveOTs --> FilterOTs{Filtrar Estados}:::decision
        
        FilterOTs -- Realizada/Rechazada/Aplazada --> IgnoreOT["Ignorar (No tocar)"]:::logic
        FilterOTs -- En Curso/Pendiente/Prevista --> CalcState[Recalcular Estado según Fecha Sistema]:::logic
        
        CalcState --> UpdateDB[Actualizar Estado en DB]:::db
        UpdateDB --> EndEngine((Fin Motor)):::logic
    end

    %% Conexiones
    RunEngine -.-> StartEngine
    ConfigPage -- Cambiar Fechas --> RunEngine
    ViewOTs -- Botón Generar --> RunEngine
```