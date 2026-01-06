Aquí tienes una propuesta de guion estructurada para maximizar la retención, el *engagement* y la conversión. Este guion está diseñado para un canal de tecnología/productividad o desarrollo de software con un estilo dinámico (tipo "Dot CSV" o "Nate Gentile" pero enfocado a gestión).

## ---

**📋 Ficha del Vídeo**

* **Título Principal:** ¡Adiós al Excel\! Creé mi propio GMAO Industrial con Python (GRATIS) 🏭  
* **Títulos Alternativos:**  
  * Cómo gestionar una fábrica entera con 4 archivos Python.  
  * El Software de Mantenimiento que las grandes empresas no quieren que conozcas.  
  * GMAO Factory: La solución Offline definitiva.  
* **Duración estimada:** 10-12 minutos.  
* **Tono:** Profesional, Entusiasta, Técnico pero accesible.

## ---

**🎬 Guion del Vídeo**

### **0:00 \- 0:50 | EL GANCHO (The Hook)**

**(Plano: Primer plano tuyo, iluminación dramática o B-Roll de maquinaria industrial funcionando y luego parándose bruscamente).**  
**Host:** "¿Sabes cuánto dinero pierde una fábrica por cada minuto que una máquina está parada? Miles. A veces, millones."  
**(Corte rápido a una hoja de Excel llena de celdas rojas y desordenada).**  
**Host:** "Y sin embargo, el 80% de los jefes de mantenimiento siguen usando hojas de cálculo infinitas, post-its perdidos o software que cuesta 50.000 dólares al año y necesita internet hasta para respirar."  
**(Plano medio, ambiente de estudio tech. Muestras el logo de GMAO Factory en un monitor).**  
**Host:** "Hoy vamos a romper eso. Te presento **GMAO Factory**. Un sistema que he desarrollado desde cero. Es 100% gratuito, Open Source, está hecho en Python y, lo mejor de todo... funciona en un búnker sin internet. Vamos a ver cómo funciona."  
**(Intro del canal con música electrónica suave).**

### ---

**0:50 \- 2:30 | EL PROBLEMA Y LA SOLUCIÓN**

**(Plano: Host sentado frente al ordenador).**  
**Host:** "Vale, seamos sinceros. El software industrial actual tiene dos problemas: o es increíblemente caro y complejo (tipo SAP), o es demasiado simple y no te avisa de nada. Y casi todos fallan en lo mismo: la dependencia de la nube."  
**(Screencast: Mostrando la estructura de carpetas del proyecto \- app.py, database.py, static).**  
**Host:** "GMAO Factory nace con una filosofía distinta: **'Offline-First'**. He utilizado **Flask** como motor y **SQLite** como base de datos. ¿Por qué? Porque significa que todo el sistema vive en un solo archivo. Puedes meter este programa en un USB, llevarlo a una planta petrolífera en medio del océano, enchufarlo y tener el control total del mantenimiento en segundos."

### ---

**2:30 \- 5:00 | TOUR POR LA INTERFAZ: EL CEREBRO DE LA FÁBRICA**

**(Screencast: Pantalla completa navegando por la aplicación. Entras en /login).**  
**Host:** "Entramos. Usuario 'Administrador', contraseña... bueno, la que viene por defecto, '123456' (cambiadla, por favor)."  
**(Click en 'Resumen').**  
**Host:** "Esto es lo primero que ves: El Dashboard Ejecutivo. Gracias a **Chart.js** integrado localmente, tenemos una visión en tiempo real de la salud de la planta.

* A la izquierda: ¿Estamos cumpliendo el preventivo? (Verde es bien, Rojo es... corre).  
* A la derecha: ¿Cuántas máquinas rotas (correctivos) tenemos hoy?  
  Y fijaos en esto: un filtro de fechas dinámico para sacar informes mensuales en un click."

**(Click en 'Inventario').**  
Host: "Pero para mantener algo, primero tienes que saber qué tienes. Aquí en el Inventario, hemos creado un pasaporte digital para cada máquina.  
Mirad esto... (Click en el botón 'Ojo' o archivos). No solo guardamos el nombre y el tipo. El sistema codifica las imágenes y los manuales PDF en Base64 y los guarda dentro de la base de datos. Nada de carpetas perdidas en Windows. Si te llevas la base de datos, te llevas los manuales."

### ---

**5:00 \- 7:30 | LA MAGIA: EL ALGORITMO DE PREVENTIVOS**

**(Plano: Host hablando a cámara, con gráficos superpuestos explicando el algoritmo).**  
**Host:** "Aquí es donde la mayoría de los Excel fallan. ¿Cómo te acuerdas de que al 'Compresor B' le toca cambio de aceite cada 45 días y al 'Torno CNC' revisión cada 6 meses?"  
**(Screencast: Sección 'Actividades' y luego 'Órdenes de Trabajo').**  
Host: "En GMAO Factory, tú defines la Periodicidad en la pestaña de Actividades. Y aquí viene la magia del código...  
Hemos programado un algoritmo en Python (en el archivo utils.py, para los curiosos) que viaja al futuro."  
**(Zoom al botón 'Generar OTs').**  
**Host:** "Cuando pulsas este botón, el sistema:

1. Mira la fecha actual (o la que tú simules).  
2. Calcula matemáticamente cuándo tocan las revisiones.  
3. Te genera las Órdenes de Trabajo automáticamente.  
4. Y te las marca en colores: **Amarillo** si toca hoy, **Rojo** si vas tarde. Es imposible que se te olvide algo."

### ---

**7:30 \- 9:00 | CRONOGRAMA Y CORRECTIVOS**

**(Screencast: Pestaña 'Cronograma').**  
Host: "¿Queréis ver el año entero de un vistazo? Pestaña Cronograma.  
Esto es una matriz generada dinámicamente con Jinja2. Cruza todos tus equipos con los 12 meses del año. Es como tener una bola de cristal para saber qué carga de trabajo tendrán tus técnicos en agosto."  
**(Corte a Pestaña 'Correctivos').**  
**Host:** "Y cuando algo se rompe —porque siempre se rompe algo—, vamos a **Correctivos**. Registramos la avería, subimos la foto del desastre y cambiamos el estado. Simple, rápido y sin burocracia."

### ---

**9:00 \- 10:30 | BAJO EL CAPÓ (TECH STACK)**

**(Plano: Host con el editor de código VS Code abierto).**  
**Host:** "Para mis compañeros programadores, hablemos del stack. Esto es **Python** puro y duro.

* **Backend:** Flask. Ligero, modular con Blueprints (resumen.py).  
* **Frontend:** Bootstrap 5 y DataTables. Pero ojo, he descargado todas las librerías en la carpeta static. Nada de CDNs. Si se cae internet, la fábrica sigue produciendo.  
* **Base de Datos:** SQLite. Un solo archivo .db. Cero configuración.  
* **Seguridad:** Hashing de contraseñas con Werkzeug y decoradores personalizados para los permisos."

**(Muestra brevemente el código de utils.py donde está la función generate\_and\_update\_work\_orders).**  
**Host:** "El código es limpio, comentado y modular. Si queréis añadir un módulo de 'Compras' o 'Personal', la arquitectura MVC ya está lista para escalar."

### ---

**10:30 \- 11:30 | CÓMO CONSEGUIRLO Y CONCLUSIÓN**

**(Plano: Primer plano).**  
**Host:** "GMAO Factory no es solo un proyecto de fin de semana, es una herramienta funcional que puede ahorrar miles de euros a una PYME industrial desde el día uno."  
Host: "¿Lo quieres? Es tuyo. He dejado el enlace al repositorio en la descripción.  
Tenéis el código fuente, el manual de instalación y la documentación técnica. Solo necesitáis Python instalado y ganas de organizar vuestro caos."  
**(Call to Action).**  
**Host:** "Si te ha gustado ver cómo construimos herramientas reales con Python, revienta el botón de like. Suscríbete si quieres que en el próximo vídeo le añadamos una API REST para conectarlo con el móvil. Dejadme en comentarios: ¿Qué funcionalidad le falta? ¡Os leo\!"  
**Host:** "Soy \[Tu Nombre/Canal\], y nos vemos en el siguiente commit. ¡Chao\!"  
**(Outro con música y pantalla final con enlaces a otros vídeos de Python/Proyectos).**

### ---

**📝 Notas de Producción (Assets necesarios):**

1. **Miniatura:** Una cara de sorpresa/éxito, el logo de Python, una captura del Dashboard de GMAO Factory y un texto grande: "TU PROPIO SISTEMA INDUSTRIAL".  
2. **B-Roll:** Necesitas capturas de pantalla fluidas del programa funcionando. Asegúrate de tener datos de prueba (mock data) cargados para que las gráficas se vean bonitas y el cronograma lleno.  
3. **Enlaces:** Link al GitHub o descarga del zip en la descripción.