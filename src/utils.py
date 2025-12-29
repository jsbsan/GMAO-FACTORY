import base64
import json
import datetime
import os
from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from database import get_db_connection

LOG_FILE = 'gmao_app.log'

# --- SEGURIDAD ---
def create_default_admin():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM usuarios WHERE username = ?', ('Administrador',)).fetchone()
    if not user:
        pw_hash = generate_password_hash('123456')
        conn.execute('INSERT INTO usuarios (username, password_hash, rol, perm_inventario, perm_actividades, perm_configuracion) VALUES (?, ?, ?, ?, ?, ?)', 
                     ('Administrador', pw_hash, 'Admin', 1, 1, 1))
        conn.commit()
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(perm):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get(perm):
                flash("No tienes permisos para acceder a esta sección.", "danger")
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- UTILIDADES ---
def get_system_date():
    try:
        conn = get_db_connection()
        row = conn.execute('SELECT fecha_sistema FROM configuracion WHERE id=1').fetchone()
        conn.close()
        if row and row['fecha_sistema']:
            return datetime.datetime.strptime(row['fecha_sistema'], '%Y-%m-%d').date()
    except: pass
    return datetime.date.today()

def get_planned_date():
    try:
        conn = get_db_connection()
        row = conn.execute('SELECT fecha_prevista FROM configuracion WHERE id=1').fetchone()
        conn.close()
        if row and row['fecha_prevista']:
            return datetime.datetime.strptime(row['fecha_prevista'], '%Y-%m-%d').date()
    except: pass
    return None

def is_logging_enabled():
    try:
        conn = get_db_connection()
        row = conn.execute('SELECT logging_enabled FROM configuracion WHERE id=1').fetchone()
        conn.close()
        if row: return bool(row['logging_enabled'])
    except: pass
    return False

def log_action(action_message):
    if is_logging_enabled():
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            user = session.get('username', 'Sistema')
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] [{user}] {action_message}\n")
        except: pass

def allowed_file_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

def file_to_base64(file):
    return base64.b64encode(file.read()).decode('utf-8')

def normalize_files(file_list):
    normalized = []
    if not file_list: return []
    for item in file_list:
        if isinstance(item, str): normalized.append({'name': 'Archivo Legacy', 'data': item})
        elif isinstance(item, dict): normalized.append(item)
    return normalized

def json_load_filter(s):
    if not s: return []
    try: return json.loads(s) if isinstance(s, str) else s
    except: return []

def get_cronograma_data(conn, year):
    actividades = conn.execute('SELECT a.id, a.nombre, i.nombre as equipo_nombre FROM actividades a JOIN inventario i ON a.equipo_id = i.id').fetchall()
    cronograma_data = []
    for act in actividades:
        row = {'actividad': act['nombre'], 'equipo': act['equipo_nombre'], 'ots': {}}
        ots = conn.execute('SELECT ot.id, ot.nombre, ot.fecha_generacion, ot.estado, ot.observaciones, ot.fecha_realizada, a.operaciones FROM ordenes_trabajo ot JOIN actividades a ON ot.actividad_id = a.id WHERE ot.actividad_id = ? AND strftime("%Y", ot.fecha_generacion) = ?', (act['id'], str(year))).fetchall()
        for ot in ots:
            fecha = datetime.datetime.strptime(ot['fecha_generacion'], '%Y-%m-%d')
            mes_idx = fecha.month
            if mes_idx not in row['ots']: row['ots'][mes_idx] = []
            row['ots'][mes_idx].append({'id': ot['id'], 'nombre': ot['nombre'], 'estado': ot['estado'], 'day_day': fecha.day, 'fecha': ot['fecha_generacion'], 'operaciones': ot['operaciones'], 'observaciones': ot['observaciones'], 'fecha_realizada': ot['fecha_realizada']})
        cronograma_data.append(row)
    return cronograma_data

def generate_and_update_work_orders(conn, current_system_date):
    row = conn.execute('SELECT fecha_prevista FROM configuracion WHERE id=1').fetchone()
    planned_date = datetime.datetime.strptime(row['fecha_prevista'], '%Y-%m-%d').date() if row and row['fecha_prevista'] else None
    
    generation_limit = current_system_date
    if planned_date and planned_date > current_system_date:
        generation_limit = planned_date

    actividades = conn.execute('SELECT * FROM actividades').fetchall()
    count_generated = 0
    
    for act in actividades:
        f = datetime.datetime.strptime(act['fecha_inicio_gen'], '%Y-%m-%d').date()
        p = act['periodicidad']
        
        while f <= generation_limit:
            if not conn.execute('SELECT id FROM ordenes_trabajo WHERE actividad_id=? AND fecha_generacion=?', (act['id'], f)).fetchone():
                deadline = f + datetime.timedelta(days=p)
                st = 'En curso'
                if f > current_system_date: st = 'Prevista'
                elif deadline < current_system_date: st = 'Pendiente'
                
                conn.execute('INSERT INTO ordenes_trabajo (actividad_id, nombre, fecha_generacion, estado) VALUES (?,?,?,?)', 
                             (act['id'], f"{act['nombre']} - {f.strftime('%d/%m/%Y')}", f, st))
                count_generated += 1
            f += datetime.timedelta(days=p)
            
    active_ots = conn.execute("SELECT ot.id, ot.fecha_generacion, ot.estado, a.periodicidad FROM ordenes_trabajo ot JOIN actividades a ON ot.actividad_id=a.id WHERE ot.estado NOT IN ('Realizada', 'Rechazada')").fetchall()
    
    for ot in active_ots:
        gen = datetime.datetime.strptime(ot['fecha_generacion'], '%Y-%m-%d').date()
        new_state = ot['estado']
        if gen > current_system_date: new_state = 'Prevista'
        else:
            deadline = gen + datetime.timedelta(days=ot['periodicidad'])
            if deadline < current_system_date: new_state = 'Pendiente'
            else: new_state = 'En curso'
        if new_state != ot['estado']:
            conn.execute("UPDATE ordenes_trabajo SET estado = ? WHERE id = ?", (new_state, ot['id']))
            
    return count_generated