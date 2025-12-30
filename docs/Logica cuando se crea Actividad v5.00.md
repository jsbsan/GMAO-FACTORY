Según el código actual (app.py y utils.py), la lógica cuando un usuario crea una **Nueva Actividad** es, sorprendentemente, muy simple y "perezosa" (lazy).  
Aquí tienes el desglose exacto de lo que ocurre:

### **1\. El Registro de la Definición (Lo que hace add\_activity)**

Cuando pulsas el botón "Crear Actividad", el sistema **NO genera las Órdenes de Trabajo (OTs) inmediatamente**. Lo único que hace en ese preciso instante es guardar la "receta" o definición en la base de datos.  
El flujo es:

1. **Recogida de Datos:** El sistema toma:  
   * **Qué:** Nombre y Operaciones.  
   * **Dónde:** Equipo asociado.  
   * **Cuándo (Reglas):** Periodicidad (cada X días) y Fecha de Inicio.  
2. **Inserción SQL:** Ejecuta un INSERT INTO actividades.  
3. **Redirección:** Te devuelve al listado de actividades.

**En este punto, aunque la actividad existe, su lista de Órdenes de Trabajo está vacía.**

### ---

**2\. La Generación de OTs (El paso diferido)**

Para que aparezcan las OTs (las tareas con fecha concreta) de esa nueva actividad, tiene que ejecutarse el **Motor de Generación** (utils.generate\_and\_update\_work\_orders).  
En tu código actual, este motor se activa en tres momentos:

1. **Manualmente:** Si vas a "Órdenes de Trabajo" y pulsas el botón amarillo **"Generar OTs"**.  
2. **Al Reiniciar:** Cada vez que apagas y enciendes el servidor (if \_\_name\_\_ \== '\_\_main\_\_').  
3. **Al Configurar:** Si cambias la "Fecha del Sistema" o la "Fecha Prevista" en la configuración global.

### **3\. Ejemplo Práctico del Flujo**

Imagina que hoy es **10 de Enero**.

1. **Creas Actividad:** "Engrasar cadena", cada **5 días**, empezando el **1 de Enero**.  
   * *Resultado inmediato:* La actividad aparece en la lista de Actividades. En la lista de OTs **no hay nada aún**.  
2. **Ejecutas el Motor (Pulsas "Generar OTs"):**  
   * El sistema ve la nueva actividad.  
   * Lee: Inicio 1 Ene, Frecuencia 5 días.  
   * Calcula fechas:  
     * 1 Ene (Pasada) \-\> Crea OT \-\> Calcula estado \-\> **PENDIENTE** (Vencida).  
     * 6 Ene (Pasada) \-\> Crea OT \-\> Calcula estado \-\> **PENDIENTE** (Vencida).  
     * 11 Ene (Futura) \-\> Crea OT \-\> Calcula estado \-\> **PREVISTA**.

### **Resumen**

La lógica es de **"Definición ahora, Generación después"**.  
Si quisieras que las OTs aparecieran *automáticamente* justo al dar de alta la actividad, habría que añadir una pequeña línea de código en app.py, dentro de la función add\_activity:

Python

\# En app.py, función add\_activity  
def add\_activity():  
    \# ... (código de inserción existente) ...  
    conn.commit()  
      
    \# LÍNEA EXTRA QUE FALTARÍA PARA QUE SEA INSTANTÁNEO:  
    utils.generate\_and\_update\_work\_orders(conn, utils.get\_system\_date())   
    conn.commit() \# Guardar las OTs generadas  
      
    conn.close()  
    \# ...

Tal y como está ahora el programa, **el usuario debe recordar pulsar "Generar OTs"** después de crear una nueva actividad para ver las tareas reflejadas en el calendario.