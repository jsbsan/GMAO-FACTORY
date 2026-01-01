Claro, la lógica de las **Órdenes de Trabajo (OTs)** es el corazón de este sistema GMAO. Se encuentra principalmente en el archivo utils.py, dentro de la función generate\_and\_update\_work\_orders.  
Aquí te explico paso a paso cómo funciona el algoritmo:

### **1\. Conceptos Clave**

Antes de la lógica, el sistema maneja tres fechas fundamentales para calcular todo:

* **Fecha de Inicio:** Definida en la *Actividad* (cuándo empieza el plan).  
* **Periodicidad:** Definida en la *Actividad* (cada cuántos días se repite).  
* **Fecha del Sistema:** La fecha "virtual" que tú controlas en configuración (por defecto es hoy).

### **2\. El Algoritmo de Generación (Paso a Paso)**

El sistema no espera a que llegue el día para crear la OT. Las calcula matemáticamente en bucle.  
Paso A: Determinar el límite temporal  
El sistema se pregunta: "¿Hasta qué fecha debo generar OTs?"

* Por defecto: Hasta la **Fecha del Sistema** (hoy).  
* Si has configurado una "Planificación Futura": Hasta la **Fecha Prevista**.

Paso B: Recorrer las Actividades  
Para cada actividad de mantenimiento definida (ej: "Revisión Aceite \- Cada 30 días"), el sistema hace lo siguiente:

1. Toma la **Fecha de Inicio** original.  
2. Empieza a sumar la **Periodicidad** en un bucle (Fecha Inicio \+ 30, \+ 60, \+ 90...).  
3. **Verificación de Existencia:** Antes de crear nada, comprueba en la base de datos: *"¿Ya existe una OT para esta actividad en esta fecha exacta?"*  
   * Si **SÍ** existe: Salta y sigue calculando la siguiente fecha.  
   * Si **NO** existe y la fecha es menor o igual al límite (Paso A): **CREA LA OT**.

### **3\. La Lógica de los Estados (El "Semáforo")**

Una vez que la OT existe (o se acaba de crear), el sistema decide qué **Estado** ponerle. Esto es dinámico y cambia según avanza la fecha del sistema.

| Estado | Color | Lógica Matemática | Significado |
| :---- | :---- | :---- | :---- |
| **PREVISTA** | Gris | Fecha OT \> Fecha Sistema | Es una tarea futura. Todavía no toca hacerla. |
| **EN CURSO** | Amarillo | Fecha OT \<= Fecha Sistema | Ya ha llegado el día (o ya pasó), pero aún estás a tiempo de hacerla. |
| **PENDIENTE** | Rojo | Fecha OT \+ Periodicidad \< Fecha Sistema | **¡Vencida\!** Se te ha pasado el plazo. Ya deberías haber generado la siguiente OT, por lo que esta se considera "caducada" o no atendida a tiempo. |
| **REALIZADA** | Verde | Manual | Un operario ha entrado y marcado que la hizo. El sistema ya no toca esta OT. |

### **4\. Ejemplo Práctico**

Imagina una actividad: **"Limpieza Filtros"** cada **7 días**.

* Inicio: 1 de Enero.  
* Fecha Sistema (Hoy): 10 de Enero.

**El sistema hace:**

1. Calcula 1 de Enero \+ 7 días \= **8 de Enero**.  
2. ¿8 de Enero \<= 10 de Enero? **Sí**.  
3. Crea la OT para el día 8\.  
4. Calcula el estado:  
   * El día 8 ya pasó (estamos a 10).  
   * ¿Ha vencido? El límite es 8 \+ 7 días \= día 15\. Como estamos a 10, aún no ha llegado al 15\.  
   * **Resultado:** Estado **"EN CURSO"**.

**Si avanzas la Fecha del Sistema al 20 de Enero:**

1. El sistema recalcula esa OT del día 8\.  
2. Límite: 8 \+ 7 \= 15\.  
3. Como estamos a 20 (y 20 \> 15), el sistema cambia el estado automáticamente a **"PENDIENTE"** (Vencida).

### **Resumen Técnico**

La función generate\_and\_update\_work\_orders hace dos cosas:

1. **INSERT:** Rellena los huecos en el calendario creando las filas que faltan en la base de datos.  
2. **UPDATE:** Repasa todas las OTs que no estén "Realizadas" y actualiza su estado (En curso vs Pendiente vs Prevista) comparando su fecha con la del sistema actual.