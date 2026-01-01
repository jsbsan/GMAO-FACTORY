# Manual de Usuario - GMAO Factory v5.0

Bienvenido al sistema de **GMAO Factory**. Este documento le guiará a través de la instalación, configuración y uso diario de su nueva herramienta de Gestión de Mantenimiento Asistido por Ordenador.

## 1. Introducción

**GMAO Factory** es una solución integral diseñada para digitalizar y simplificar el mantenimiento en entornos industriales. Su objetivo principal es eliminar el uso de papel y hojas de cálculo dispersas, centralizando toda la información técnica en una única plataforma accesible.

**Funcionalidades Principales:**

- **Inventario Digital:** Fichas técnicas de equipos con imágenes y manuales PDF adjuntos.
    
- **Mantenimiento Preventivo:** Planificación automática de tareas recurrentes.
    
- **Órdenes de Trabajo (OTs):** Gestión del ciclo de vida de las tareas (pendientes, en curso, realizadas).
    
- **Correctivos:** Registro y seguimiento de averías imprevistas.
    
- **Simulación Temporal:** Capacidad para simular fechas futuras o pasadas para auditorías y planificación.
    

## 2. Requisitos del Sistema

Para ejecutar **GMAO Factory**, su equipo debe cumplir con los siguientes requisitos mínimos:

- **Sistema Operativo:** Windows 10/11, macOS o Linux.
    
- **Software Base:** Tener instalado **Python 3.8** o superior.
    
- **Navegador Web:** Google Chrome, Microsoft Edge, Firefox o Safari (versiones recientes).
    
- **Red:** Conexión a red local (LAN/WiFi) si desea acceder desde múltiples dispositivos (móviles/tablets).
    

## 3. Guía de Instalación y Configuración

Siga estos pasos para poner en marcha el sistema por primera vez:

### Paso 1: Preparación de Archivos

Asegúrese de tener los siguientes 4 archivos en una misma carpeta (por ejemplo, `C:\GMAO_Factory`):

1. `app.py`
    
2. `database.py`
    
3. `utils.py`
    
4. `ui_templates.py`
    

### Paso 2: Instalación de Dependencias

Abra la terminal o consola de comandos, navegue hasta la carpeta y ejecute el siguiente comando para instalar las librerías necesarias:

```
pip install flask werkzeug

```

### Paso 3: Ejecución del Servidor

Inicie la aplicación ejecutando el archivo principal:

```
python app.py

```

Verá un mensaje indicando que el sistema está funcionando en `http://0.0.0.0:5000`.

### Paso 4: Acceso Inicial

1. Abra su navegador web.
    
2. Escriba en la barra de direcciones: `http://localhost:5000`.
    
3. Inicie sesión con las credenciales de administrador predeterminadas:
    
    - **Usuario:** `Administrador`
        
    - **Contraseña:** `123456`
        

> **Nota:** Por seguridad, cambie esta contraseña inmediatamente desde la sección de Configuración Global.

## 4. Interfaz de Usuario

La interfaz está diseñada para ser intuitiva y limpia. Se divide en dos áreas principales:

1. **Menú Lateral (Sidebar):**
    
    - Situado a la izquierda (en escritorio) o accesible mediante el botón de menú (en móviles).
        
    - Contiene el acceso a todos los módulos: Inventario, Actividades, OTs, Cronograma, Correctivos y Configuración.
        
    - Muestra el usuario conectado actual.
        
2. **Área de Trabajo Principal:**
    
    - Muestra la información del módulo seleccionado.
        
    - En la parte superior, siempre verá un **Aviso de Fecha del Sistema**. Esto indica en qué "día virtual" está operando el programa (útil para simulaciones).
        

## 5. Guía de Uso (Paso a Paso)

### 5.1. Gestión de Usuarios y Tipos (Configuración Inicial)

Antes de empezar, configure los básicos:

1. Vaya a **Configuración Global**.
    
2. En **Gestión de Usuarios**, cree cuentas para sus operarios. Puede asignar permisos específicos (ej: solo ver OTs, pero no borrar inventario).
    
3. En **Gestión de Tipos de Equipo**, defina las categorías (ej: "Compresores", "Cintas Transportadoras").
    

### 5.2. Creación del Inventario

1. Vaya a la pestaña **Inventario**.
    
2. Pulse el botón azul **+ Nuevo Equipo**.
    
3. Rellene el nombre, seleccione el tipo y añada una descripción.
    
4. Puede subir hasta **5 fotos** y **5 manuales PDF** directamente en la ficha.
    
5. Pulse **Guardar**.
    

### 5.3. Definición del Mantenimiento Preventivo

Para que el sistema genere trabajo automáticamente:

1. Vaya a **Actividades**.
    
2. Pulse **Nueva Actividad**.
    
3. Seleccione el Equipo, defina qué hay que hacer (Operaciones) y la frecuencia en días (Periodicidad).
    
4. Establezca la **Fecha de Inicio**.
    

### 5.4. Gestión de Órdenes de Trabajo (OTs)

Este es el corazón del sistema:

1. Vaya a **Órdenes de Trabajo**.
    
2. Pulse el botón naranja **Generar OTs**. El sistema calculará qué tareas tocan hoy basándose en la periodicidad.
    
3. **Estados de colores:**
    
    - 🟡 **Amarillo (En curso):** Tareas activas que están dentro de plazo.
        
    - 🔴 **Rojo (Pendiente):** Tareas cuya fecha límite ha vencido. ¡Prioridad alta!
        
    - 🟢 **Verde (Realizada):** Tareas completadas.
        
    - ⚪ **Gris (Prevista):** Tareas futuras (ver Planificación Futura).
        
4. Para cerrar una orden, pulse **Gestionar**, cambie el estado a "Realizada", añada observaciones y la fecha real de ejecución.
    

### 5.5. Gestión de Correctivos (Averías)

Si algo se rompe inesperadamente:

1. Vaya a **Correctivos**.
    
2. Pulse **Nueva Incidencia**.
    
3. Registre el equipo y la avería. Estado inicial: **Detectada (Rojo)**.
    
4. A medida que se repara, edite la incidencia para cambiar a **En curso (Amarillo)** y finalmente **Resuelta (Verde)**, añadiendo la solución aplicada.
    

### 5.6. Planificación Futura

¿Quiere ver la carga de trabajo del próximo mes?

1. Vaya a **Configuración Global**.
    
2. En la tarjeta "Planificación Futura", seleccione una fecha límite (ej: dentro de 3 meses).
    
3. Pulse **Actualizar y Generar**.
    
4. Vaya al **Cronograma**. Verá las tareas futuras marcadas en **Gris (Prevista)**. Estas se convertirán automáticamente en **Amarillas** cuando llegue el día correspondiente.
    

### 5.7. Impresión de Informes

En cualquier módulo (Inventario, OTs, etc.), encontrará botones grises con un icono de impresora:

- **Imprimir Tabla (Cabecera):** Genera un PDF con el listado completo visible en pantalla (respeta los filtros aplicados).
    
- **Imprimir Ficha (Fila):** Genera un informe detallado del elemento específico, incluyendo imágenes.
    

## 6. Solución de Problemas (FAQ)

**P: Al imprimir, no se ven los colores de los estados (rojo, verde, amarillo).**

- **R:** Asegúrese de que en las opciones de impresión de su navegador, la casilla **"Gráficos de fondo"** (Background graphics) esté activada. El sistema intenta forzarlo, pero algunos navegadores requieren activación manual.
    

**P: He cambiado la fecha del sistema, pero las órdenes antiguas no se actualizan.**

- **R:** Pulse el botón **Generar OTs** en la pestaña de Órdenes de Trabajo. Esto fuerza al sistema a recalcular el estado (Vencido/En curso) de todas las órdenes abiertas basándose en la nueva fecha.
    

**P: ¿Dónde se guardan las fotos y los datos?**

- **R:** Todo se guarda en el archivo `mantenimiento_factory.db`. **Haga copias de seguridad de este archivo regularmente**. Si lo pierde, perderá todos los datos.
    

**P: No puedo acceder desde mi móvil.**

- **R:** Asegúrese de que su móvil está en la misma WiFi que el ordenador principal. Debe escribir la dirección IP del ordenador seguida del puerto, no "localhost" (ej: `http://192.168.1.35:5000`). Compruebe que el firewall de Windows no esté bloqueando el puerto 5000 o el programa Python.
    

**P: ¿Cómo averiguo la dirección IP del ordenador que está ejecutando la aplicación?**

- **R:** Necesita esta dirección para poder conectarse desde otros dispositivos (móviles, tablets) en la misma red.
    
    - **En Windows:** Pulse la tecla `Windows`, escriba **cmd** y pulse Enter. En la ventana negra que aparece, escriba el comando `ipconfig` y pulse Enter. Busque la línea que dice **"Dirección IPv4"**; ese número (ej: `192.168.1.45`) es su IP.
        
    - **En Mac/Linux:** Abra el Terminal y escriba `ifconfig` o `ip a`. Busque la dirección `inet` (generalmente empieza por 192.168...).
        
    - **Nota:** Consulta al administrador del sistema si no tiene acceso al ordenador donde se ejecuta la aplicación.
        

## 7. Notas Técnicas

- **Tecnología:** Python 3 + Flask (Backend), HTML5/Bootstrap 5 (Frontend), SQLite (Base de datos).
    
- **Almacenamiento de Archivos:** Las imágenes y PDFs se convierten a cadena de texto (Base64) y se almacenan directamente dentro de la base de datos SQLite para facilitar la portabilidad (un solo archivo `.db` contiene todo).
    
- **Logging:** El sistema incluye un registro de auditoría (`gmao_app.log`) activable desde la configuración global para rastrear quién crea, edita o borra elementos.