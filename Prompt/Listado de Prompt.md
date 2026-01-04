
## V 0.00 a v 5.11

> Rol: "Actúa como un Arquitecto de Software Senior y Experto en python y desarrollo web."
> Objetivo: "Diseñaremos un sistema de [gestión de mantenimiento e inspección de equipos de una fábrica incluyendo gestión de correctivos]."
> Stack Tecnológico: "Usa Python con Flask, sqlite3 para la base de datos y bootstrap para el frontend."
> Toda la información se almacenará en una base de datos sqlite3
> Debe de tener un visor para los pdf e imágenes almacenadas en la base de datos que se almacena usando el método de base64.
> Los datos se presentarán en tablas con paginación de 10 en 10 elementos.
> El programa debe de estar dividido en módulos:
> ## 1. Inventario. Los datos que almacena son:
> - nombre del equipo. 
> - Tipo de equipo. Inicialmente tendrá los siguientes tipos: Obra civil, Instalaciones Eléctrica e Instalaciones Hidráulicas. Se podrá añadir más tipos 
> - Descripción del equipo
> - 5 imágenes.  Se podrá visualizar
> - 5 documentos pdf. Se podrá visualizar
> El inventario será editable.
> 
> ## 2. Actividades.
> - nombre de la actividad.
> - equipo del inventario. Se eligirá entre los equipos existentes en el inventario
> - Periodicidad.
> - Operaciones a realizar
> - Fecha de inicio de generación de ordenes de trabajo
> 
> ## 3. Ordenes de Trabajo.
> El programa revisirá las actividades y comparará la fecha actual con la periodicidad y fecha de inicio de generación de ordenes de trabajo para generar las ordenes de trabajo.
> Las Ordenes de Trabajo. Tendrán:
> - Nombre de la orden de trabajo coincide con la actividad y se le añade la fecha cuando se ha generado.
> - Un campo de fecha donde se almacena cuando se ha generado
> - Un campo de estado, con valor: Realizada, En curso, y Rechazada
> - Un campo para ver la operaciones de la actividad de referencia
> - Un campo para para observaciones
> - Un campo de fecha para guardar la fecha realizada.
> 
> 
> ## 4. Cronograma
> Se mostrará una tabla con todas las actividades (filas) y en las columna los meses de un año. 
> En la celdas de la tablas se pone el nombre de la orden de trabajo que esten generadas. Color rojo para las que esten "Realizada", amarillo para "en curso" y negro para rechazada.
> 
> > En el inventario, por cada equipo se puede añadir 5 ficheros del tipo imagen y 5 ficheros del tipo pdf.
> El editor del inventario debe de mostrar el nombre de cada imagen y pdf del equipo que este editarndo, poderlos seleccionar para borrarlos
> Quiero que añadas otra pestaña llamada de Configuración, donde pueda ver los Tipos de equipos que existen, editarlos y añadir nuevos.
> 
> En el cronograma si hago click sobre una celda puedo editar la orden de trabajo seleccionada.
> 
> Quiero cambiar el color rojo por verde en las Ordenes de trabajos que esten "realizada"
> 
> Las Actividades (pestaña Actificades) deben de ser editables.
> 
> Quiero que en la pestaña "órdenes de Trabajo" se pueda editar por "Estado", y entre fechas y mostrarlas con el filtro.
> 
> En la pestaña de "Inventario" elimina el botón de "+Nuevo tipo"
> 
> Renombra la pestaña "Configuración" como "Configuración de tipos"
> 
> En la pestaña de Cronograma, quiero que se pueda elegir el año y qu ese actualice el cronograma cuando se cambie de año.
> 
> En la pestaña de "inventario", añade un boton para imprimir en pdf los datos del equipo, incluido imagenes y pdf.
> 
> Añade tambien un boton para imprimir toda la tabla de inventario
> 
> En la pestaña de "actividades", añade un boton para imprimir en pdf los datos de la actividad. Tambien añade un botón para imprimir toda la tabla de actividades
> 
> En la pestaña de "Órdenes de trabajo", añade un boton para imprimir en pdf los datos de la orden de trabajo. Tambien añade un botón para imprimir toda la tabla de ordenes de trabajo.
> 
> El botón de imprimir las "Órdenes de trabajo", debe imprimir las ordenes de trabajos filtradas 
> 
> En la pestaña de "Cronograma" añade un botón de imprimir en pdf el cronograma del año seleccionado.
> 
> Crea una pestaña de "Configuración fecha del sistema". Inicialmente tiene una campo de fecha igual a la fecha actual del sistema, llama este campo "Fecha Sistema", tambien debe de ser almacenado en la base de datos sqlite.
> 
> Pestaña "Ordenes de Trabajo". Lógica de la generación de ordenes de trabajo: Cuando se generan las Ordenes de trabajos , revisa una a una, el resultado de la fecha generada de la orden de trabajo mas la periodicidad de la actividad relacionada con la orden de trabajo con la "Fecha Sistema" .  Si el resultado es menor que cero, el estado de la orden de trabajo pasa a "Pendiente"  y siendo su color rojo. Actualiza tambien el cronograma para que se vean tambien estas ordenes "Pendiente"
> 
> Error: No se han implementado los últimos cambios ¿lo puedes comprobar?
> 
> Añade la siguiente lógica al boton de generar ordenes de trabajo: Revisa una a una todas las ordenes de trabajo cuyo mes de creación sea superior al mes actual de la fecha de sistema. Si es asi pon estado "Prevista" y su color es gris. Actualiza tambien la pestaña de cronograma para que se vean el estado "Prevista" con color gris. Comprueba que se han implementado la lógica de "Prevista" en ordenes de trabajo y cronograma
> Quiero que la aplicación sea accesible a otros dispositivos que esten en la misma red.
> 
> En la pestaña de "Actividades" quiero que el formulario de crear actividad se vea cuando se pulsa un boton y que se oculte este formulario cuando se cree. El boton de "imprimir tabla" se debe de ver siempre en la pestaña de "Actividades".
> 
> Quiero que la pestaña de "Actividades", se  pueda aplicar un filtro, por equipo, por nombre incompleto de actividad, por frecuencia,etc.
> 
> Quiero que la pestaña de "Inventario", se  pueda aplicar un filtro, por Nombre y por Tipo
> 
> Quiero que añadas una nueva pestaña llamada "Correctivos/Incidencias". Donde se gestione los correctivos. Se pueden añadir, editar y borrar. Ademas se podran aplicar filtros e imprimir los que se seleccionen.
> Cada correctivo tiene los siguientes campos:
> - Nombre del Correctivo
> - Nombre del Equipo afectado (a elegir entre el inventario de equipos existente)
> - Comentario: Texto para explicar que ha pasado
> - Solución: texto para explicar que solución se ha dado.
> - Estado: Detectada (en rojo), En curso (en amarillo), Resuelta (en verde)
> - Fecha detectada
> - Fecha resolución
> - Un máximo de 5 fotos se pueden añadir a cada correctivo.
> - Un máximo de 5 pdf se pueden añadir a cada correctivo.
> 
> Error: al ir a la pestaña de "Actividades" me salte el siguiente error. "NameError: name 'ACTIVIDADES_TEMPLATE' is not defined". Comprueba que todas los módulos funcionan correctamente.
> 
> Error: En la pestaña de "Correctivos", no se pueden previsualizar las fotos ni los pdf.
> 
> Error: Los botones interactivos para ver fotos o pdf, no funcionan dan el siguiente error: "AttributeError: 'sqlite3.Row' object has no attribute 'get'
> 
> Error: En edición de Correctivo, falta el texto de "Selecciona para borrar", en la tabla de imágenes y de pdf.
> 
> Quiero que a la pestaña "Cronograma" le cambias el nombre y le pongas "Cronogramas de Ordenes de Trabajo", y la coloques en el menu justo debajo de la pestaña "Órdenes de trabajo"
> 
> Error: A la hora de imprimir un correctivo, no se imprime los nombres de pdf que tiene asociado.
> 
> Error: Al imprimir un cronograma, no sale en color las ordenes de trabajo ni tampoco la leyenda indicando que significa cada color.
> 
>Diseña la aplicación para que sea Responsive Design. Una vez que hayas realizado los cambios, comprueba que todo funciona bien.
>
>Añadir un sistema de logging, para que todo el uso del programa quede registrada y guardada en un fichero de tipo texto. Uso del programa que se debe de registrar en log, por ejemplo: añadir/editar/borrar/imprimir elemento al inventario, actividad, generar ordenes de trabajo, editar ordenes de trabajo, editar y modificar correctivos, imprimir cualquier tipo de informe, etc. Este sistema de logging se podrá activar o desactivar en una nueva pestaña de "Configuración", colocala en la última posición del menu y dentro de esta pestaña añade tambien un botón donde se puedan descargar el archivo donde se guardan de logging.
  >
Error:   La aplicación no se inicia da el siguiente error "Not found"
   > 
Error: Al ejecutar de nuevo la aplicación me da el siguiente error: # TemplateAssertionError
jinja2.exceptions.TemplateAssertionError: No filter named 'json_load'.

> Crea una nueva pestaña (colocala en la ultima posición del menu) llamada "Acerca de...", donde informes de:
>    -> nombre del programa
>    -> version del programa
>    -> autor del programa: "Julio Sánchez Berro"
> 
> Error: genera otra vez el archivo, parece que esta incompleto.
> 
> Error: siguen faltando partes del programa ¿puedes dividir el app.py en varios archivos para que te sea más fácil actualizarlo?

En este momento crear varios archivos, dividiendo el único app.py en:
Tienes toda la razón: el archivo `app.py` se ha vuelto demasiado grande y eso provoca que se corte la respuesta o que sea difícil de mantener.
La mejor solución es refactorizar el código en una **Arquitectura Modular**. Vamos a dividir el programa en 4 archivos distintos. Deberás guardar estos 4 archivos en la misma carpeta para que funcione.
Aquí tienes la nueva estructura:
1. `database.py`: Maneja la conexión y creación de la base de datos.
2. `utils.py`: Contiene funciones de ayuda (fechas, log, manejo de archivos, lógica del cronograma).
3. `ui_templates.py`: Contiene **todo el código HTML** (las plantillas) para limpiar la lógica principal.
4. `app.py`: El archivo principal que ejecuta Flask y gestiona las rutas.


Error: # AttributeError
AttributeError: module 'ui_templates' has no attribute 'CONFIGURACION_TEMPLATE'

Quiero que la pestaña de "Fecha del Sistema" se integre dentro de "Configuración Global"

 Quiero que añadas una nueva sección dentro de la pestaña "Configuración Global", para definir la fecha prevista. Esta fecha debe de ser mayor a la fecha del sistema. Al actualizar esta fecha prevista, genera las ordenes de trabajo desde la fecha del sistema más un dia, hasta la fecha prevista. Las ordenes de trabajo generadas estaran en estado "Prevista"
 
 Quiero añadas una comprobación de que si existe la orden de trabajo no la vuelva a crear cuando se se cambie la fecha prevista.
 
 
 Me da el siguiente error: Error: cuando intento imprimir me da el siguient error: AttributeError
AttributeError: module 'ui_templates' has no attribute 'PRINT_TEMPLATE'

¿puedes comprobar que no hay mas omisiones?

Error: He creado una nueva actividad, y cuando le doy al boton de generar ordenes de trabajo, no se generan las de la nueva actividad. 

Quiero que cada vez que se modifique la fecha de planificación futura, se borren todas las ordenes de trabajo previstas y luego se vuelvan a generar teniendo la nueva fecha de planificación futura.

Quiero que añadas a la pestaña de Gestión de Actividades una acción de Borrar Actividad. Cada vez que se borre una actividad tambien se borrarán todas las ordenes de trabajo de esa actividad. Antes de borrar la actividad pide la confirmación del usurio.

El boton de borrado de actividad debe de desplegar un formulario para que el usuario confirme o cancele el borrado de la actividad y ordenes de trabajo relacionadas a la actividad.
 
 Quiero que incluyas un boton de borrado en las acciones del Inventario de Equipos (pestaña Inventario)
 
 Error: He actualizado los archivos, pero esta alerta no ha salido :" Incluye una alerta de confirmación en JavaScript para evitar borrados accidentales, advirtiendo que se perderán todos los datos relacionados."

Quiero que cuando se inicie el programa se compruebe la fecha actual del ordenador donde se ejecute el programa y que la fecha del sistema se actualice a esta, generandose las ordenes de trabajo.

Añade al programa un sistema de gestión de usuarios y permisos.
Requiero:
Diseña una nueva tabla en la base de datos que incluya usario, contraseñas, roles y permisos. Los permisos serán:
-poder acceder a pestaña inventario
-poder acceder a pestaña Actividades
-poder acceder a pestaña configuración global
Inicialmente hay un usuario llamado "Administrador" con contraseña "123456"
Funciones para registrar usuarios aplicando hash en la constraseñas.
Lógica de verificación. Inicialmente en el navegador web, el programa pedirá usuario y contraseña, lo comprobará y si es correcto seguirá ejecutando la aplicación si no se para de ejecutar la aplicación.
Dentro de la pestaña "Configuración Global", crea un panel para gestionar los usuarios (crear, editar, borrar), contraseñas,roles y permisos que tengan cada rol.
> 
> 
> Comprueba y verifica que todo funciona correctamente. Si encuentras algun error intenta solucionarlo.


Nota. compruebo que se producen varios errorres en páginas que se enlazaban. 
Pongo este prompt:
Cuando intento acceder a la pestaña "Acerca de...", me da el siguiente error: AttributeError AttributeError: module 'ui_templates' has no attribute 'ABOUT_TEMPLATE'
(intenta solucionarlo)
No se soluciona, ¿puedes dividir el archivo ui_templates.py en varios, para hacerlos más pequeños? Actualiza todos los archivos del proyecto.

(divide el archivo de plantillas en varios)

## Version 5.2
Comentario: Paso a otra conversación de gemini-canvas adjuntando los archivos.

Analiza este proyecto
Necesito saber si el programa puede funcionar sin estar conectado al internet solo a una red local
Respuesta:
Estructura que propone:
/static
│
├── /css
│   ├── bootstrap.min.css
│   └── all.min.css      <-- Este archivo busca ../webfonts
│
├── /js
│   └── bootstrap.bundle.min.js
│
└── /webfonts            <-- Carpeta HERMANA de css (no hija)
    ├── fa-solid-900.woff2
    ├── fa-regular-400.woff2
    └── ... (el resto de archivos de fuentes)

¿tengo que copiar la carpeta completa de webfonts en la carpeta css o solo los archivos?
Hazme una tabla donde venga el archivo, numero linea, codigo  original,  codigo nuevo
¿solo hay que cambiar ese archivo? Compruebalo y verificalo con el resto de archivos del proyecto.
Hazme un esquema gráfico de como esta definida las tablas y campos de la base de datos.
Haz un diagrama de flujo del programa.
Me da el siguiente error el diagrama de flujo: 
Error: Error: Parse error on line 11:
...olor:black    Start((Inicio Servidor)):
Crea un documento que explica una a una las funciones y procedimientos del programa completo.
Dime la lógica de las ordenes de trabajo
¿cual es la lógica cuando se crea un actividad?
¿seria sencillo añadir 2 estados más a las ordenes de trabajo, serian "Aplazada" y "Rechazada"

## Version 5.21
¿la fecha prevista tiene algun valor inicial?

Quiero que la fecha prevista coja inicialmente el valor de la fecha del ordenador más 365 dias en la tabla de configuración de la base de datos y que el comportamiento del programa el límite de generacion de ordenes de trabajo sea la fecha prevista . Actualiza el código y revisa todos los archivos que se vean influidos por el cambio.

Aplica los cambios.

Me da error en el menu principal al intentar entrar en la pestaña "Correctivos". Este es el error que sale:  UndefinedError
jinja2.exceptions.UndefinedError: 'item' is undefined

hazme un diagrama de flujo del programa.

En mermaid me da este error: Error: Error: Parse error on line 55:
...> CreateOT[Crear OT (Estado: En Curso/Pr
-----------------------^
Expecting 'SQE', 'DOUBLECIRCLEEND', 'PE', '-)', 'STADIUMEND', 'SUBROUTINEEND', 'PIPE', 'CYLINDEREND', 'DIAMOND_STOP', 'TAGEND', 'TRAPEND', 'INVTRAPEND', 'UNICODE_TEXT', 'TEXT', 'TAGSTART', got 'PS

Me da otro error: Error: Error: Parse error on line 63:
...-> IgnoreOT[Ignorar (No tocar)]:::logic
-----------------------^
Expecting 'SQE', 'DOUBLECIRCLEEND', 'PE', '-)', 'STADIUMEND', 'SUBROUTINEEND', 'PIPE', 'CYLINDEREND', 'DIAMOND_STOP', 'TAGEND', 'TRAPEND', 'INVTRAPEND', 'UNICODE_TEXT', 'TEXT', 'TAGSTART', got 'PS'

## Version 5.22
En gestión de actividades, no aparece la paginación en la tabla. Incluyela para que muestre las actividades de 10 en 10. Actualiza los archivos.

En Correctivos e incidencias, no aparece la paginación en la tabla. Incluyela para que muestre las actividades de 10 en 10.  Actualiza los archivos para que aparezca.

## Version 5.30 -> Nueva Pestaña RESUMEN
Prompt para que gemini-canvas retome el proyecto en una nueva conversación:
"He subido los archivos fuente de mi proyecto en Python. Por favor, realiza las siguientes tareas antes de que empecemos a trabajar:
Analiza la arquitectura: Identifica la función principal de cada archivo y cómo interactúan entre sí.
Resume la lógica: Explica brevemente qué hace el programa, cuál es su entrada de datos y qué resultado genera.
Identifica dependencias: Confirma qué librerías externas utiliza.
Una vez que comprendas la estructura completa, confírmamelo con un breve resumen técnico. Después de eso, te pediré mejoras específicas de rendimiento, refactorización y nuevas funcionalidades."

Nueva funcionalidad: En el menu principal haz una nueva entrada llamada "Resumen", en esta pestaña se debe de ver:
1. Cuadro para elegir fecha inicio resumen (que se lee y almacena en la tabla de configuración de la base de datos). El valor inicial será el dia de hoy menos 365 dias
2. Cuadro para elegir fecha fin resumen (que se lee y almacena en la tabla de configuración de la base de datos). El valor inicial será el dia de hoy.
3. Panel con un gráfico tipo tarta donde se dibuje el porcentaje de las distintas ordenes de trabajo existente en el periodo de fecha inicio resumen y fecha fin resumen. Debe de incluir una leyenda. Los colores deben de coincidir con los tipos de ordenes de trabajo que aparecen en el cronograma.
4. Panel con un gráfico tipo tarta donde se dibuje el porcentaje de los distintos correctivos existente en el periodo de fecha de inicio del resumen y fecha fin resumen. Debe de incluir una leyenda. Los colores deben de coincidir con los tipos de correctivos.
Intenta que todo el nuevo código que generes para esta pestaña, este en un nuevo fichero llamado "resumen.py". 

¿en que linea de codigo se indica que se vea el inventario primero?
(responde que se ve primero el inventario por que esta definido por la ruta raiz)

Quiero que en vez del inventario se vea el resumen.

hazme un diagrama de flujo del programa para mermaid, ten en cuenta problemas que se pueden presentar con caracteres (parentesis, comillas, etc)

## Version 5.99 -> Modular aun más el programa y usar paginas html y 
###Prompt para que gemini-canvas retome el proyecto en una nueva conversación:
"He subido los archivos fuente de mi proyecto en Python. Por favor, realiza las siguientes tareas antes de que empecemos a trabajar:
Analiza la arquitectura: Identifica la función principal de cada archivo y cómo interactúan entre sí.
Resume la lógica: Explica brevemente qué hace el programa, cuál es su entrada de datos y qué resultado genera.
Identifica dependencias: Confirma qué librerías externas utiliza.
Una vez que comprendas la estructura completa, confírmamelo con un breve resumen técnico. Después de eso, te pediré mejoras específicas de rendimiento, refactorización y nuevas funcionalidades."


Actúa como un desarrollador experto en Python Flask. Mi proyecto tiene actualmente todas las plantillas HTML guardadas como variables de texto. Haz una refactorización completa siguiendo estar instrucciones: 
1. Separación de plantillas generando archivos .html reales dentro de una nueva carpeta llamada templates  
2. Revisa el archivo principal (app.py) cambiando las rutas para que dejen de usar render_template_string y pasen a usar render_template.


¿puedes descargarme en un zip todas las carpetas y archivos?
Respuesta: Genera un fichero py que al ejecutarlo crea un zip con todos los archivos generados y estructura de carpetas.

Quiero que refactorice el codigo actual para la representación de las tablas para que uses DataTables para dibujar las tablas, incluye la opciones de paginación, búsqueda, ordenadar por columnas y exportarción a excel de la tabla.

Error: Cuando se ejecuta la aplicación la pantalla se queda congelada en la pestaña resumen.
Respuesta: dice que faltan librerias css y js

No, no puede ser eso, ya que inclui manualmente las librerias en la carpeta static, y de echo las gráficas de generan antes de que se congele la aplicacion ¿cual puede ser el error?
Respuesta: 1) corregir css y 2) corregir enlaces quiere cambiar los enlaces estaticos a online

Solo quiero que apliques la corrección de CSS. No quiero usar CDNs ya que necesito que funciones con librerias locales el programa.


Para la tabla de ordenes de trabajo, necesito añadir un filtro entre fechas en la pestaña de Ordenes de trabajo, ¿lo puedes añadir?

## Version 6.00 -> generación de documentación actualizada
(para el código)
Quiero cambiar el texto de version en vez de la 5.30 que sea la 6.00


### Generación de nueva documentacion:
#### -> Readme para github:
Crea un fichero "readme.md" para añadirlo al repositorio de github sobre el proyecto.

#### -> Documentación para usuario:
Analiza todo el código del proyecto y confírmame cuando estés listo para redactar la documentación
Actúa como un **Technical Writer** experto en software. Tu objetivo es redactar un manual de usuario completo, profesional y fácil de entender para el programa que acabamos de desarrollar en Canvas.
**El manual debe incluir las siguientes secciones:**
 1. **Introducción:** Qué hace el programa y cuál es su objetivo principal.
 2. **Requisitos del Sistema:** Qué necesita el usuario para ejecutarlo (navegador, dependencias, claves de API, etc.).
 3. **Guía de Instalación/Configuración:** Paso a paso para ponerlo en marcha.
 4. **Interfaz de Usuario:** Descripción de los botones, menús y áreas de trabajo.
 5. **Guía de Uso (Paso a Paso):** Ejemplos prácticos de cómo realizar las tareas principales.
 6. **Solución de Problemas (FAQ):** Errores comunes y cómo resolverlos, comentar que la aplicación puede funcionar offline.
 7. **Notas Técnicas:** Breve explicación de las tecnologías usadas.
**Tono y Estilo:**
- Utiliza un lenguaje claro, profesional pero accesible.
- Usa negritas para resaltar botones o acciones importantes.
- Formatea el texto en **Markdown** para que sea fácil de leer.
- Si hay partes del código que requieren una explicación visual, descríbelas detalladamente.
**Público Objetivo:** para los técnicos y operarios

#### -> Documentación para programador
Analiza todo este código y confírmame cuando estés listo para redactar la documentación.
Actúa como un Senior Technical Writer y Arquitecto de Software. Tu tarea es generar la estructura y el contenido detallado de un manual técnico para programadores sobre el sistema GMAO Factory.
El manual debe seguir este esquema obligatorio:
1. **Introducción y Stack Tecnológico:** Breve descripción del propósito del software, lenguajes utilizados, frameworks y dependencias principales.
2. **Arquitectura del Sistema:** Explicación del patrón de diseño (ej. Microservicios, MVC, Hexagonal).
3. **Guía de Configuración (Setup):** Pasos exactos para clonar, instalar dependencias y configurar variables de entorno.
4. **Documentación de la API / Puntos de Entrada:** Detalle de endpoints, tipos de datos, autenticación y manejo de errores.
5. **Flujos de Datos:** Descripción de cómo viaja la información desde el cliente hasta la base de datos.
6. **Diagrama de flujo:** Descripción de  la secuencia lógica y el flujo de ejecución del programa. Describe los procesos y/o algoritmos de forma clara y secuencial.
7. **Guía de Contribución:** Estándares de código (Linting), nombres de ramas y proceso de Pull Request.
#### **Instrucciones para Diagramas:** 
**Por cada sección relevante, incluye una descripción detallada de qué diagrama debería ir allí (ej. Diagrama de Secuencia para la autenticación, Diagrama de Entidad-Relación para la DB, Diagrama de Infraestructura en AWS, diagrama de flujo). **
Diagramas como código (Mermaid.js):** Las descripciones de los diagramas se entreguen en sintaxis **Mermaid**. 
**Instrucciones de formato Mermaid:**
    Usa siempre comillas dobles "" para el contenido de texto dentro de los nodos.
    Estructura: Identificador["Texto del nodo (con paréntesis/símbolos)"].
    No uses el texto descriptivo como ID del nodo.
    Si hay comillas dentro del texto, usa ' (comilla simple) o escapalas.
**Diagramas**
##### Diagramas esenciales que debes incluir
Para que un manual de programador sea realmente útil, no pueden faltar estos apoyos visuales:
###### 1. Diagrama de Arquitectura de Alto Nivel
Muestra cómo interactúan los componentes principales.
- **Qué incluir:** Balanceadores de carga, servidores de aplicaciones, servicios de caché (Redis), bases de datos y servicios externos (APIs de terceros).
###### 2. Diagrama de Entidad-Relación (ERD)
Fundamental para que el programador entienda la persistencia de datos.
- **Qué incluir:** Tablas, llaves primarias/foráneas y el tipo de relación (1:N, N:M).
###### 3. Diagramas de Secuencia (UML)
Ideales para explicar procesos complejos como el flujo de OAuth2 o una transacción de pago.
- **Qué incluir:** Actores (Usuario, Frontend, API, Auth Server) y el orden cronológico de los mensajes/llamadas entre ellos.
###### 4. Diagrama de flujo del programa.    
###### 5. Diagrama de Flujo de CI/CD
Explica qué pasa desde que el programador hace `git push`.
- **Qué incluir:** Ejecución de tests unitarios, análisis de SonarQube, construcción de imagen Docker y despliegue en staging/producción.
- **Usa Swagger/OpenAPI:** Si tienes una API, no escribas los endpoints a mano en el manual; enlaza a la documentación interactiva.

#### **Tono:**
Profesional, técnico, directo y orientado a la eficiencia. Usa bloques de código de ejemplo donde sea necesario.

------
## Version v6.01
------
Cambio en la lógica de generación de ordenes de trabajo:
Revisa el archivo utils.py, en concreto la funcion generate_and_update_work_orders
Revisar todas las ordenes de trabajo de forma que:
1. Estado NULL: ponerlo como "Prevista"
2. Estado "Aplazada": no hacer nada.
3. Estado "Rechazada": no hacer nada.
4. Estado "Realizada": no hacer nada.
5. Estado "En Curso": solo las Ordenes de trabajo cuya fecha de generación pertenece al mes y año actual del sistema
6. Estado "Pendiente": las ordenes de trabajo con fecha anterior (pasado) al mes y año actual del sistema
7. Estado "Prevista": las ordenes de trabajo con fechas posterior (futuro) al mes y año actual del sistema.

Nueva funcionalidad: casillas de verificación para exportación de filtrado
Quiero que añadas una nueva funcionalidad a las datatable , que se puedan marcar las filas usando la propiedad "modifier" y asi tener en las filas casillas de verificación y botones de exportación de filtrado. Quiero que lo añadas en todos los ficheros donde se use datatable. 

-> Error: Revisa el diseño, porque los checkbox de las filas no se ven 
-> Error: cuando intento seleccionar el checkbox, no se selecciona, parece que no hay código asociado.
-> Error: Cuando me muestra la tabla, sale el mensaje la alerta de falta libreria Select, pero si le doy aceptar al mensaje, ya salen la columna de seleccionar y funciona correctemente ¿porque puede ser?

------
## Version v6.08
------
Quiero que añadas en la pestaña "Resumen" dos datatable que estarán debajo de las gráficas:
La primera mostrará las Ordenes de Trabajos filtradas según la fecha de inicio y fecha fin del panel "Configuración del Periodo".
La segunda mostrará los Correctivos filtrados según la fecha de inicio y fecha fin del panel "Configuración del Periodo".
Si hay un cambio en las fechas de inicio y/o fecha fin, se actualizarán las datatables.
Debajo de las datatables, añade un botón para hacer un informe que incluya las gráficas y las datatables de la pestaña "Resumen"

A las datatable que has añadido en resumen, les falta colorear el texto del valor mostrado de la columna estado. Por ejemplo: En la datatable de Orden de Trabajo, las de estado Realizada es de color verde, las "En curso" van en amarillo, etc. Y en la datatable de Incidencias, las "Detectada" van en color rojo, las "Resuelta" van en color verde.


Nueva mejora: en la pestaña de correctivo, añadir un filtro de fecha, "Fecha Desde" y "Fecha Hasta", para filtrar el datatable del listado de Correctivos e incidencias.

Nueva mejora a aplicar en todos los datatable: Si se exporta y no se han seleccionado ninguna fila, se seleccionaran todas las filas.

------
## Version v6.09
------
Cuando en la aplicación y en la pestaña de Ordenes de Trabajo y paso a editar en otra ventana, cuando vuelvo he perdido el filtro que tenía activado en el datatables, como lo puedo recuperar?
Respuesta: aplica propiedad stateSave de las DataTables
Comprueba que no se usan CDN, sino el directorio static donde estarán alamacenadas todas los fichero js y css necesarios para ejecutar la aplicación offline.

------
## Version v6.10
------
P:Me da el siguiente error:
"Error: DataTables warning: table id=tablaOTs - Requested unknown parameter '1' for row 0, column 1. For more information about this error, please see https://datatables.net/tn/4"

------
## Version v6.11
------
P: Ya no da el error, pero vuelvo de la otra ventana no se listan las filas de la datatable.

R:¡Entendido! Si al volver a la página la tabla aparece vacía o no se listan las filas, suele deberse a un conflicto entre el stateSave (que intenta restaurar la tabla tal como la dejaste) y el filtro personalizado de fechas (que se aplica después de cargar la página).
El problema técnico suele ser que DataTables restaura su estado interno, pero el filtro de fecha se aplica "encima" un instante después, y si la tabla no se redibuja en el orden correcto o si los índices de las columnas varían, falla silenciosamente y oculta todo.
He generado la versión v6.11 con una solución robusta:
    Inicialización Diferida: He ajustado el JavaScript para que la configuración de filtros y la restauración de valores (localStorage) ocurra de manera segura.
    Limpieza de Filtros: Antes de añadir el filtro de fechas, limpiamos cualquier filtro previo residual para evitar conflictos.
    Forzado de Redibujado: Se asegura un draw() limpio al cargar la página si hay fechas guardadas.

------
## Version v6.12 y 6.13
------
gmao_factory_v6_12_datatables_fix
Se presentan los siguientes errores:
1. En la pestaña correctivo: Al entrar en dicha pestaña sale el siguiente mensaje:
DataTables warning: table id=tablaCorrectivos - Requested unknown parameter '1' for row 0, column 1. For more information about this error, please see https://datatables.net/tn/4
2. Al entrar en la pestaña "Ordenes de trabajo", sale el siguiente error:
DataTables warning: table id=tablaOTs - Requested unknown parameter '1' for row 0, column 1. For more information about this error, please see https://datatables.net/tn/4
3. En la pestaña "Correctivos", sale el siguiente error:
DataTables warning: table id=tablaCorrectivos - Requested unknown parameter '1' for row 0, column 1. For more information about this error, please see https://datatables.net/tn/4
Nota Importante: Ten en cuenta que la primera columna se usa para seleccionar/deseleccionar con un checkbox la fila.



------
## Version v6.14: 6.13 bug fixes
------
Se producen dos nuevos errores:
1. Al entrar en la pestaña "Inventario", sale el siguiente error:
    TemplateSyntaxError
    jinja2.exceptions.TemplateSyntaxError: Encountered unknown tag 'endfor'. You probably made a nesting mistake. Jinja is expecting this tag, but currently looking for 'elif' or 'else' or 'endif'. The innermost block that needs to be closed is 'if'.
    File "C:\Users\USER\OneDrive\Documentos\GitHub\GMAO-FACTORY\src\templates\inventory\index.html", line 4, in template

2. En la pestaña de "Cronogramas OTs", al pulsar en el botón "Imprimir PDF", sale el siguiente error:
    TemplateSyntaxError
    jinja2.exceptions.TemplateSyntaxError: Encountered unknown tag 'endblock'.
    File "C:\Users\USER\OneDrive\Documentos\GitHub\GMAO-FACTORY\src\templates\print\cronograma.html", line 74, in template



Se produce error al entrar en la pestañal inventario: TemplateSyntaxError
jinja2.exceptions.TemplateSyntaxError: Encountered unknown tag 'endfor'. You probably made a nesting mistake. Jinja is expecting this tag, but currently looking for 'elif' or 'else' or 'endif'. The innermost block that needs to be closed is 'if'. 




------
## Version v6.16
------
P: Te  comento un error que me aparece a veces cuando entro en la pestañ Ordenes de Trabjo: Sale este error: DataTables warning: table id=tablaOTs - Requested unknown parameter '1' for row 0, column 1. For more information about this error, please see https://datatables.net/tn/4
R: Implemente sistema de versionado de estado en la configuración de datatables en base.html