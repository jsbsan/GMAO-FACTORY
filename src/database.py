import sqlite3
import datetime

DB_NAME = 'mantenimiento_factory.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tipos_equipo (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventario (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, tipo_id INTEGER NOT NULL, descripcion TEXT, images TEXT, pdfs TEXT, FOREIGN KEY (tipo_id) REFERENCES tipos_equipo (id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS actividades (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, equipo_id INTEGER NOT NULL, periodicidad INTEGER NOT NULL, operaciones TEXT, fecha_inicio_gen DATE NOT NULL, FOREIGN KEY (equipo_id) REFERENCES inventario (id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS ordenes_trabajo (id INTEGER PRIMARY KEY AUTOINCREMENT, actividad_id INTEGER NOT NULL, nombre TEXT NOT NULL, fecha_generacion DATE NOT NULL, estado TEXT NOT NULL DEFAULT 'En curso', observaciones TEXT, fecha_realizada DATE, FOREIGN KEY (actividad_id) REFERENCES actividades (id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS correctivos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, equipo_id INTEGER NOT NULL, comentario TEXT, solucion TEXT, estado TEXT NOT NULL DEFAULT 'Detectada', fecha_detectada DATE NOT NULL, fecha_resolucion DATE, images TEXT, pdfs TEXT, FOREIGN KEY (equipo_id) REFERENCES inventario (id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS configuracion (id INTEGER PRIMARY KEY, fecha_sistema DATE, logging_enabled INTEGER DEFAULT 0, fecha_prevista DATE, fecha_inicio_resumen DATE, fecha_fin_resumen DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, rol TEXT, perm_inventario INTEGER DEFAULT 0, perm_actividades INTEGER DEFAULT 0, perm_configuracion INTEGER DEFAULT 0)''')
    
    try: c.execute("ALTER TABLE configuracion ADD COLUMN logging_enabled INTEGER DEFAULT 0")
    except: pass 
    try: c.execute("ALTER TABLE configuracion ADD COLUMN fecha_prevista DATE")
    except: pass
    try: c.execute("ALTER TABLE configuracion ADD COLUMN fecha_inicio_resumen DATE")
    except: pass
    try: c.execute("ALTER TABLE configuracion ADD COLUMN fecha_fin_resumen DATE")
    except: pass

    today = datetime.date.today()
    next_year = today + datetime.timedelta(days=365)
    try: c.execute("UPDATE configuracion SET fecha_prevista = ? WHERE id=1 AND fecha_prevista IS NULL", (next_year,))
    except: pass
    try: c.execute("INSERT INTO configuracion (id, fecha_sistema, logging_enabled, fecha_prevista) VALUES (1, ?, 0, ?)", (today, next_year))
    except sqlite3.IntegrityError: pass
    
    defaults = ['Obra Civil', 'Instalaciones Eléctricas', 'Instalaciones Hidráulicas']
    for d in defaults:
        try: c.execute("INSERT INTO tipos_equipo (nombre) VALUES (?)", (d,))
        except: pass
    conn.commit()
    conn.close()