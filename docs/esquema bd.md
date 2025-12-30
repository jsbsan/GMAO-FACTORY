``` mermaid
erDiagram
    %% --- TABLAS PRINCIPALES ---

    TIPOS_EQUIPO {
        INTEGER id PK "Identificador único"
        TEXT nombre "Nombre único (Ej: Vehículos)"
    }

    INVENTARIO {
        INTEGER id PK "Identificador único"
        TEXT nombre "Nombre del equipo"
        INTEGER tipo_id FK "Relación con Tipos"
        TEXT descripcion
        TEXT images "JSON/Base64"
        TEXT pdfs "JSON/Base64"
    }

    ACTIVIDADES {
        INTEGER id PK "Identificador único"
        TEXT nombre "Nombre (Ej: Cambio Aceite)"
        INTEGER equipo_id FK "Relación con Inventario"
        INTEGER periodicidad "Días"
        TEXT operaciones "Instrucciones"
        DATE fecha_inicio_gen "Fecha base cálculo"
    }

    ORDENES_TRABAJO {
        INTEGER id PK "Identificador único"
        INTEGER actividad_id FK "Relación con Actividad"
        TEXT nombre "Nombre generado"
        DATE fecha_generacion "Fecha planificada"
        TEXT estado "En curso, Pendiente, etc."
        TEXT observaciones
        DATE fecha_realizada
    }

    CORRECTIVOS {
        INTEGER id PK "Identificador único"
        TEXT nombre "Nombre de la avería"
        INTEGER equipo_id FK "Relación con Inventario"
        TEXT comentario
        TEXT solucion
        TEXT estado "Detectada, Resuelta"
        DATE fecha_detectada
        DATE fecha_resolucion
        TEXT images "JSON/Base64"
        TEXT pdfs "JSON/Base64"
    }

    %% --- TABLAS DE SISTEMA ---

    CONFIGURACION {
        INTEGER id PK "Solo existe fila ID=1"
        DATE fecha_sistema "Fecha virtual del sistema"
        INTEGER logging_enabled "0=No, 1=Sí"
        DATE fecha_prevista "Límite planificación futura"
    }

    USUARIOS {
        INTEGER id PK
        TEXT username "Único"
        TEXT password_hash "Encriptada"
        TEXT rol "Admin, Usuario"
        INTEGER perm_inventario "Permiso bool"
        INTEGER perm_actividades "Permiso bool"
        INTEGER perm_configuracion "Permiso bool"
    }

    %% --- RELACIONES ---

    TIPOS_EQUIPO ||--|{ INVENTARIO : "Clasifica a"
    INVENTARIO ||--|{ ACTIVIDADES : "Tiene planificadas"
    INVENTARIO ||--|{ CORRECTIVOS : "Sufre incidencias"
    ACTIVIDADES ||--|{ ORDENES_TRABAJO : "Genera múltiples"
 ```