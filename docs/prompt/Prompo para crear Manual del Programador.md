#### -> Documentación para programador
Analiza todo este código y confírmame cuando estés listo para redactar la documentación tecnica del proyecto.
Actúa como un Senior Technical Writer y Arquitecto de Software. Tu tarea es generar la estructura y el contenido detallado de un manual técnico para programadores sobre el sistema GMAO Factory.

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

El primer punto del manual es:
1. **Introducción y Stack Tecnológico:** Breve descripción del propósito del software, lenguajes utilizados, frameworks y dependencias principales.


El segundo punto del manual es:
2. **Arquitectura del Sistema:** Explicación del patrón de diseño (ej. Microservicios, MVC, Hexagonal).

El tercer punto del manual es:
3. **Guía de Configuración (Setup):** Pasos exactos para clonar, instalar dependencias y configurar variables de entorno.



4. **Documentación de la API / Puntos de Entrada:** Detalle de endpoints, tipos de datos, autenticación y manejo de errores.
5. **Flujos de Datos:** Descripción de cómo viaja la información desde el cliente hasta la base de datos.
6. **Diagrama de flujo:** Descripción de  la secuencia lógica y el flujo de ejecución del programa. Describe los procesos y/o algoritmos de forma clara y secuencial.
7. **Guía de Contribución:** Estándares de código (Linting), nombres de ramas y proceso de Pull Request.