import sqlite3
import base64
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
import json
import os
import shutil
from werkzeug.security import check_password_hash, generate_password_hash
import database as db
import utils
from resumen import resumen_bp
from waitress import serve

app = Flask(__name__)
app.secret_key = 'super_secret_key_mantenimiento_factory'
app.register_blueprint(resumen_bp, url_prefix='/resumen')

@app.template_filter('json_load')
def json_load_filter(s):
    return utils.json_load_filter(s)

# Context Processor para inyectar el nombre del mantenimiento en todas las vistas
@app.context_processor
def inject_maintenance_name():
    return dict(maintenance_name=utils.get_maintenance_name())

# ==========================================
# AUTENTICACIÓN
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = db.get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['rol'] = user['rol']
            session['perm_inventario'] = user['perm_inventario']
            session['perm_actividades'] = user['perm_actividades']
            session['perm_configuracion'] = user['perm_configuracion']
            utils.log_action(f"Inicio de sesión exitoso: {username}")
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    utils.log_action(f"Cierre de sesión: {session.get('username')}")
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@utils.login_required
def index():
    return redirect(url_for('resumen.index'))

# ==========================================
# INVENTARIO
# ==========================================

@app.route('/inventory')
@utils.login_required
def inventory():
    db.init_db()
    conn = db.get_db_connection()
    tipos = conn.execute('SELECT * FROM tipos_equipo').fetchall()
    items = conn.execute('SELECT i.*, t.nombre as tipo_nombre FROM inventario i LEFT JOIN tipos_equipo t ON i.tipo_id=t.id').fetchall()
    conn.close()
    return render_template('inventory/index.html', items=items, tipos=tipos, active_page='inventario', system_date=utils.get_system_date())

@app.route('/inventory/add', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_inventario')
def add_inventory():
    try:
        images_list = []
        for f in request.files.getlist('images')[:5]:
             if f and utils.allowed_file_image(f.filename): images_list.append({'name': f.filename, 'data': utils.file_to_base64(f)})
        pdfs_list = []
        for f in request.files.getlist('pdfs')[:5]:
             if f and utils.allowed_file_pdf(f.filename): pdfs_list.append({'name': f.filename, 'data': utils.file_to_base64(f)})
        conn = db.get_db_connection()
        conn.execute('INSERT INTO inventario (nombre, tipo_id, descripcion, images, pdfs) VALUES (?, ?, ?, ?, ?)',
                     (request.form['nombre'], request.form['tipo_id'], request.form['descripcion'], json.dumps(images_list), json.dumps(pdfs_list)))
        conn.commit()
        conn.close()
        utils.log_action(f"Inventario añadido: {request.form['nombre']}")
        flash('Equipo añadido', 'success')
    except Exception as e: flash(f'Error: {e}', 'danger')
    return redirect(url_for('inventory'))

@app.route('/inventory/edit/<int:id>')
@utils.login_required
@utils.permission_required('perm_inventario')
def edit_inventory(id):
    conn = db.get_db_connection()
    item = conn.execute('SELECT * FROM inventario WHERE id=?', (id,)).fetchone()
    tipos = conn.execute('SELECT * FROM tipos_equipo').fetchall()
    conn.close()
    if not item: return redirect(url_for('inventory'))
    imgs = utils.normalize_files(json.loads(item['images']) if item['images'] else [])
    pdfs = utils.normalize_files(json.loads(item['pdfs']) if item['pdfs'] else [])
    return render_template('inventory/edit.html', item=item, tipos=tipos, imgs=imgs, pdfs=pdfs, active_page='inventario', system_date=utils.get_system_date())

@app.route('/inventory/update/<int:id>', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_inventario')
def update_inventory(id):
    conn = db.get_db_connection()
    curr = conn.execute('SELECT images, pdfs FROM inventario WHERE id=?', (id,)).fetchone()
    curr_imgs = utils.normalize_files(json.loads(curr['images']) if curr['images'] else [])
    curr_pdfs = utils.normalize_files(json.loads(curr['pdfs']) if curr['pdfs'] else [])
    del_imgs = [int(x) for x in request.form.getlist('delete_images')]
    kept_imgs = [x for i, x in enumerate(curr_imgs) if i not in del_imgs]
    for f in request.files.getlist('images'):
        if f and utils.allowed_file_image(f.filename): kept_imgs.append({'name': f.filename, 'data': utils.file_to_base64(f)})
    if len(kept_imgs)>5: kept_imgs=kept_imgs[:5]
    del_pdfs = [int(x) for x in request.form.getlist('delete_pdfs')]
    kept_pdfs = [x for i, x in enumerate(curr_pdfs) if i not in del_pdfs]
    for f in request.files.getlist('pdfs'):
        if f and utils.allowed_file_pdf(f.filename): kept_pdfs.append({'name': f.filename, 'data': utils.file_to_base64(f)})
    if len(kept_pdfs)>5: kept_pdfs=kept_pdfs[:5]
    conn.execute('UPDATE inventario SET nombre=?, tipo_id=?, descripcion=?, images=?, pdfs=? WHERE id=?',
                 (request.form['nombre'], request.form['tipo_id'], request.form['descripcion'], json.dumps(kept_imgs), json.dumps(kept_pdfs), id))
    conn.commit()
    conn.close()
    utils.log_action(f"Inventario actualizado: ID {id}")
    flash('Actualizado', 'success')
    return redirect(url_for('inventory'))

@app.route('/inventory/delete/<int:id>', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_inventario')
def delete_inventory(id):
    conn = db.get_db_connection()
    try:
        conn.execute('DELETE FROM ordenes_trabajo WHERE actividad_id IN (SELECT id FROM actividades WHERE equipo_id = ?)', (id,))
        conn.execute('DELETE FROM actividades WHERE equipo_id = ?', (id,))
        conn.execute('DELETE FROM correctivos WHERE equipo_id = ?', (id,))
        conn.execute('DELETE FROM inventario WHERE id = ?', (id,))
        conn.commit()
        utils.log_action(f"Equipo eliminado: ID {id}")
        flash('Equipo eliminado.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al eliminar: {e}', 'danger')
    finally: conn.close()
    return redirect(url_for('inventory'))

@app.route('/inventory/print/<int:id>')
@utils.login_required
def print_inventory(id):
    conn = db.get_db_connection()
    item = conn.execute('SELECT i.*, t.nombre as tipo_nombre FROM inventario i LEFT JOIN tipos_equipo t ON i.tipo_id=t.id WHERE i.id=?', (id,)).fetchone()
    conn.close()
    imgs = utils.normalize_files(json.loads(item['images']) if item['images'] else [])
    pdfs = utils.normalize_files(json.loads(item['pdfs']) if item['pdfs'] else [])
    utils.log_action(f"Impreso inventario: ID {id}")
    return render_template('print/inventory.html', item=item, imgs=imgs, pdfs=pdfs, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/inventory/print_all')
@utils.login_required
def print_all_inventory():
    conn = db.get_db_connection()
    items = conn.execute('SELECT i.*, t.nombre as tipo_nombre FROM inventario i LEFT JOIN tipos_equipo t ON i.tipo_id=t.id ORDER BY i.nombre').fetchall()
    conn.close()
    utils.log_action("Impreso listado inventario")
    return render_template('print/all_inventory.html', items=items, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/view_files/<source>/<tipo>/<int:id>')
@utils.login_required
def view_files(source, tipo, id):
    conn = db.get_db_connection()
    if source == 'inventory':
        item = conn.execute('SELECT * FROM inventario WHERE id=?', (id,)).fetchone()
        back_url = url_for('inventory')
        title_prefix = "Archivos de Equipo"
    elif source == 'corrective':
        item = conn.execute('SELECT * FROM correctivos WHERE id=?', (id,)).fetchone()
        back_url = url_for('correctivos')
        title_prefix = "Archivos de Incidencia"
    else:
        item = None
        back_url = url_for('inventory')
        title_prefix = "Archivos"
    conn.close()
    files = []
    if item:
        content = item['images'] if tipo == 'img' else item['pdfs']
        files = utils.normalize_files(json.loads(content) if content else [])
    return render_template('viewer.html', item=item, files=files, tipo=tipo, back_url=back_url, title_prefix=title_prefix, active_page='inventario', system_date=utils.get_system_date())

# ==========================================
# ACTIVIDADES (CON LÓGICA DE GENERACIÓN AUTOMÁTICA)
# ==========================================

@app.route('/activities')
@utils.login_required
@utils.permission_required('perm_actividades')
def activities():
    conn = db.get_db_connection()
    actividades = conn.execute('SELECT a.*, i.nombre as equipo_nombre FROM actividades a JOIN inventario i ON a.equipo_id = i.id').fetchall()
    equipos = conn.execute('SELECT i.id, i.nombre, t.nombre as tipo_nombre FROM inventario i JOIN tipos_equipo t ON i.tipo_id = t.id').fetchall()
    conn.close()
    return render_template('activities/index.html', actividades=actividades, equipos=equipos, active_page='actividades', system_date=utils.get_system_date())

@app.route('/activities/add', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_actividades')
def add_activity():
    conn = db.get_db_connection()
    # Leemos si el usuario quiere generar OTs (checkbox en formulario)
    generar_ot = 1 if 'generar_ot' in request.form else 0
    
    conn.execute('INSERT INTO actividades (nombre, equipo_id, periodicidad, operaciones, fecha_inicio_gen, generar_ot) VALUES (?,?,?,?,?,?)',
                 (request.form['nombre'], request.form['equipo_id'], request.form['periodicidad'], request.form['operaciones'], request.form['fecha_inicio'], generar_ot))
    
    # IMPORTANTE: Commit para guardar la actividad ANTES de generar las OTs
    conn.commit() 
    
    # Si la actividad se crea con el check activo, generamos sus primeras OTs inmediatamente
    if generar_ot:
        utils.generate_and_update_work_orders(conn, utils.get_system_date())
        conn.commit()
    
    conn.close()
    utils.log_action(f"Actividad creada: {request.form['nombre']}")
    flash('Actividad creada y plan generado', 'success')
    return redirect(url_for('activities'))

@app.route('/activities/edit/<int:id>')
@utils.login_required
@utils.permission_required('perm_actividades')
def edit_activity(id):
    conn = db.get_db_connection()
    activity = conn.execute('SELECT * FROM actividades WHERE id=?', (id,)).fetchone()
    equipos = conn.execute('SELECT i.id, i.nombre, t.nombre as tipo_nombre FROM inventario i JOIN tipos_equipo t ON i.tipo_id = t.id').fetchall()
    conn.close()
    return render_template('activities/edit.html', activity=activity, equipos=equipos, active_page='actividades', system_date=utils.get_system_date())

@app.route('/activities/update/<int:id>', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_actividades')
def update_activity(id):
    conn = db.get_db_connection()
    generar_ot = 1 if 'generar_ot' in request.form else 0
    
    conn.execute('UPDATE actividades SET nombre=?, equipo_id=?, periodicidad=?, operaciones=?, fecha_inicio_gen=?, generar_ot=? WHERE id=?',
                 (request.form['nombre'], request.form['equipo_id'], request.form['periodicidad'], request.form['operaciones'], request.form['fecha_inicio'], generar_ot, id))
    
    # LÓGICA DE ACTUALIZACIÓN DE OTS:
    # 1. Borramos las OTs futuras ('Prevista') porque la periodicidad o fecha pudo haber cambiado
    #    o porque el usuario desactivó la generación de OTs.
    conn.execute("DELETE FROM ordenes_trabajo WHERE actividad_id=? AND estado='Prevista'", (id,))
    
    # 2. Guardamos cambios
    conn.commit()
    
    # 3. Regeneramos el plan. La función generate_and_update_work_orders respetará el flag generar_ot.
    #    Si generar_ot es 1, rellenará los huecos borrados con las nuevas fechas.
    #    Si generar_ot es 0, no creará nada nuevo (y las 'Prevista' ya fueron borradas).
    utils.generate_and_update_work_orders(conn, utils.get_system_date())
    conn.commit()
    
    conn.close()
    utils.log_action(f"Actividad actualizada: ID {id}")
    flash('Actividad actualizada y plan recalculado', 'success')
    return redirect(url_for('activities'))

@app.route('/activities/delete/<int:id>', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_actividades')
def delete_activity(id):
    conn = db.get_db_connection()
    try:
        # Aquí se borran TODAS las OTs (incluidas historial) al borrar la actividad madre
        conn.execute('DELETE FROM ordenes_trabajo WHERE actividad_id = ?', (id,))
        conn.execute('DELETE FROM actividades WHERE id = ?', (id,))
        conn.commit()
        utils.log_action(f"Actividad eliminada: ID {id}")
        flash('Actividad eliminada.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al eliminar: {e}', 'danger')
    finally: conn.close()
    return redirect(url_for('activities'))

@app.route('/activities/print/<int:id>')
@utils.login_required
def print_activity_single(id):
    conn = db.get_db_connection()
    activity = conn.execute('SELECT a.*, i.nombre as equipo_nombre, t.nombre as tipo_nombre FROM actividades a JOIN inventario i ON a.equipo_id=i.id JOIN tipos_equipo t ON i.tipo_id=t.id WHERE a.id=?', (id,)).fetchone()
    conn.close()
    utils.log_action(f"Impresa actividad: ID {id}")
    return render_template('print/activity.html', activity=activity, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/activities/print_all')
@utils.login_required
def print_all_activities():
    conn = db.get_db_connection()
    activities = conn.execute('SELECT a.*, i.nombre as equipo_nombre FROM actividades a JOIN inventario i ON a.equipo_id=i.id ORDER BY a.nombre').fetchall()
    conn.close()
    utils.log_action("Impreso listado actividades")
    return render_template('print/all_activities.html', activities=activities, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

# ==========================================
# ÓRDENES DE TRABAJO
# ==========================================

@app.route('/work_orders')
@utils.login_required
def work_orders():
    conn = db.get_db_connection()
    q = 'SELECT ot.*, a.operaciones, i.nombre as equipo_nombre FROM ordenes_trabajo ot JOIN actividades a ON ot.actividad_id = a.id JOIN inventario i ON a.equipo_id = i.id ORDER BY ot.fecha_generacion DESC'
    ots = conn.execute(q).fetchall()
    conn.close()
    return render_template('work_orders/index.html', ots=ots, active_page='ots', system_date=utils.get_system_date())

@app.route('/work_orders/generate', methods=['POST'])
@utils.login_required
def generate_work_orders():
    conn = db.get_db_connection()
    current_date = utils.get_system_date()
    # Esta función en utils ya debe incluir la lógica de ignorar actividades con generar_ot=0
    count = utils.generate_and_update_work_orders(conn, current_date)
    conn.commit()
    conn.close()
    utils.log_action("Generación manual de OTs")
    flash(f'Generadas {count} nuevas órdenes.', 'info')
    return redirect(url_for('work_orders'))

@app.route('/work_orders/update/<int:id>', methods=['POST'])
@utils.login_required
def update_ot(id):
    conn = db.get_db_connection()
    redirect_target = 'calendar_view' if request.form.get('redirect_to') == 'calendar' else 'work_orders'
    if request.form.get('redirect_to') == 'cronograma': redirect_target = 'cronograma'
    
    # NEW: Capturamos la fecha del calendario si existe
    calendar_date = request.form.get('current_calendar_date')
    # NEW: Capturamos el año del cronograma si existe
    cronograma_year = request.form.get('cronograma_year')
    
    conn.execute('UPDATE ordenes_trabajo SET estado=?, observaciones=?, fecha_realizada=? WHERE id=?', (request.form['estado'], request.form['observaciones'], request.form['fecha_realizada'], id))
    conn.commit()
    conn.close()
    utils.log_action(f"OT actualizada: ID {id}")
    flash('OT actualizada', 'success')
    
    # Si volvemos al calendario y tenemos una fecha, la pasamos como parámetro
    if redirect_target == 'calendar_view' and calendar_date:
        return redirect(url_for('calendar_view', date=calendar_date))
    
    # Si volvemos al cronograma y tenemos un año, lo pasamos como parámetro
    if redirect_target == 'cronograma' and cronograma_year:
        return redirect(url_for('cronograma', year=cronograma_year))
        
    return redirect(url_for(redirect_target))

@app.route('/work_orders/print/<int:id>')
@utils.login_required
def print_ot(id):
    conn = db.get_db_connection()
    ot = conn.execute('SELECT ot.*, a.operaciones, i.nombre as equipo_nombre, t.nombre as tipo_nombre FROM ordenes_trabajo ot JOIN actividades a ON ot.actividad_id=a.id JOIN inventario i ON a.equipo_id=i.id JOIN tipos_equipo t ON i.tipo_id=t.id WHERE ot.id=?', (id,)).fetchone()
    conn.close()
    utils.log_action(f"Impresa OT: ID {id}")
    return render_template('print/ot.html', ot=ot, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/work_orders/print_all')
@utils.login_required
def print_all_ots():
    conn = db.get_db_connection()
    q = 'SELECT ot.*, i.nombre as equipo_nombre FROM ordenes_trabajo ot JOIN actividades a ON ot.actividad_id=a.id JOIN inventario i ON a.equipo_id=i.id ORDER BY ot.fecha_generacion DESC'
    ots = conn.execute(q).fetchall()
    conn.close()
    utils.log_action("Impreso listado OTs")
    return render_template('print/all_ots.html', ots=ots, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/cronograma')
@utils.login_required
def cronograma():
    year = request.args.get('year', utils.get_system_date().year, type=int)
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    conn = db.get_db_connection()
    data = utils.get_cronograma_data(conn, year)
    conn.close()
    return render_template('work_orders/cronograma.html', data=data, meses=meses, year=year, active_page='cronograma', system_date=utils.get_system_date())

@app.route('/cronograma/print')
@utils.login_required
def print_cronograma():
    year = request.args.get('year', utils.get_system_date().year, type=int)
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    conn = db.get_db_connection()
    data = utils.get_cronograma_data(conn, year)
    conn.close()
    utils.log_action(f"Impreso cronograma año {year}")
    return render_template('print/cronograma.html', data=data, meses=meses, year=year, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

# ==========================================
# CORRECTIVOS
# ==========================================

@app.route('/correctivos')
@utils.login_required
def correctivos():
    conn = db.get_db_connection()
    items = conn.execute('SELECT c.*, i.nombre as equipo_nombre FROM correctivos c JOIN inventario i ON c.equipo_id=i.id ORDER BY c.fecha_detectada DESC').fetchall()
    equipos = conn.execute('SELECT i.id, i.nombre, t.nombre as tipo_nombre FROM inventario i JOIN tipos_equipo t ON i.tipo_id=t.id').fetchall()
    conn.close()
    return render_template('correctivos/index.html', correctivos=items, equipos=equipos, active_page='correctivos', system_date=utils.get_system_date())

@app.route('/correctivos/add', methods=['POST'])
@utils.login_required
def add_correctivo():
    images_list = []
    for f in request.files.getlist('images')[:5]:
        if f and utils.allowed_file_image(f.filename): images_list.append({'name': f.filename, 'data': utils.file_to_base64(f)})
    pdfs_list = []
    for f in request.files.getlist('pdfs')[:5]:
        if f and utils.allowed_file_pdf(f.filename): pdfs_list.append({'name': f.filename, 'data': utils.file_to_base64(f)})
    conn = db.get_db_connection()
    conn.execute('INSERT INTO correctivos (nombre, equipo_id, comentario, fecha_detectada, estado, images, pdfs) VALUES (?,?,?,?,?,?,?)',
                 (request.form['nombre'], request.form['equipo_id'], request.form['comentario'], request.form['fecha_detectada'], request.form['estado'], json.dumps(images_list), json.dumps(pdfs_list)))
    conn.commit()
    conn.close()
    utils.log_action(f"Incidencia creada: {request.form['nombre']}")
    flash('Incidencia registrada', 'success')
    return redirect(url_for('correctivos'))

@app.route('/correctivos/edit/<int:id>')
@utils.login_required
def edit_correctivo(id):
    conn = db.get_db_connection()
    item = conn.execute('SELECT * FROM correctivos WHERE id=?', (id,)).fetchone()
    equipos = conn.execute('SELECT i.id, i.nombre, t.nombre as tipo_nombre FROM inventario i JOIN tipos_equipo t ON i.tipo_id=t.id').fetchall()
    conn.close()
    imgs = utils.normalize_files(json.loads(item['images']) if item['images'] else [])
    pdfs = utils.normalize_files(json.loads(item['pdfs']) if item['pdfs'] else [])
    return render_template('correctivos/edit.html', item=item, equipos=equipos, imgs=imgs, pdfs=pdfs, active_page='correctivos', system_date=utils.get_system_date())

@app.route('/correctivos/update/<int:id>', methods=['POST'])
@utils.login_required
def update_correctivo(id):
    conn = db.get_db_connection()
    curr = conn.execute('SELECT images, pdfs FROM correctivos WHERE id=?', (id,)).fetchone()
    curr_imgs = utils.normalize_files(json.loads(curr['images']) if curr['images'] else [])
    curr_pdfs = utils.normalize_files(json.loads(curr['pdfs']) if curr['pdfs'] else [])
    del_imgs = [int(x) for x in request.form.getlist('delete_images')]
    kept_imgs = [x for i, x in enumerate(curr_imgs) if i not in del_imgs]
    for f in request.files.getlist('images'):
        if f and utils.allowed_file_image(f.filename): kept_imgs.append({'name': f.filename, 'data': utils.file_to_base64(f)})
    if len(kept_imgs)>5: kept_imgs=kept_imgs[:5]
    del_pdfs = [int(x) for x in request.form.getlist('delete_pdfs')]
    kept_pdfs = [x for i, x in enumerate(curr_pdfs) if i not in del_pdfs]
    for f in request.files.getlist('pdfs'):
        if f and utils.allowed_file_pdf(f.filename): kept_pdfs.append({'name': f.filename, 'data': utils.file_to_base64(f)})
    if len(kept_pdfs)>5: kept_pdfs=kept_pdfs[:5]
    conn.execute('UPDATE correctivos SET nombre=?, equipo_id=?, comentario=?, solucion=?, fecha_detectada=?, fecha_resolucion=?, estado=?, images=?, pdfs=? WHERE id=?',
                 (request.form['nombre'], request.form['equipo_id'], request.form['comentario'], request.form['solucion'], request.form['fecha_detectada'], request.form['fecha_resolucion'], request.form['estado'], json.dumps(kept_imgs), json.dumps(kept_pdfs), id))
    conn.commit()
    conn.close()
    utils.log_action(f"Incidencia actualizada: ID {id}")
    flash('Incidencia actualizada', 'success')
    return redirect(url_for('correctivos'))

@app.route('/correctivos/delete/<int:id>', methods=['POST'])
@utils.login_required
def delete_correctivo(id):
    conn = db.get_db_connection()
    conn.execute('DELETE FROM correctivos WHERE id=?', (id,))
    conn.commit()
    conn.close()
    utils.log_action(f"Incidencia eliminada: ID {id}")
    flash('Eliminado', 'success')
    return redirect(url_for('correctivos'))

@app.route('/correctivos/print/<int:id>')
@utils.login_required
def print_correctivo(id):
    conn = db.get_db_connection()
    item = conn.execute('SELECT c.*, i.nombre as equipo_nombre FROM correctivos c JOIN inventario i ON c.equipo_id=i.id WHERE c.id=?', (id,)).fetchone()
    conn.close()
    imgs = utils.normalize_files(json.loads(item['images']) if item['images'] else [])
    pdfs = utils.normalize_files(json.loads(item['pdfs']) if item['pdfs'] else []) 
    utils.log_action(f"Impresa incidencia: ID {id}")
    return render_template('print/correctivo.html', item=item, imgs=imgs, pdfs=pdfs, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/correctivos/print_all')
@utils.login_required
def print_all_correctivos():
    conn = db.get_db_connection()
    items = conn.execute('SELECT c.*, i.nombre as equipo_nombre FROM correctivos c JOIN inventario i ON c.equipo_id=i.id ORDER BY c.fecha_detectada DESC').fetchall()
    conn.close()
    utils.log_action("Impreso listado incidencias")
    return render_template('print/all_correctivos.html', items=items, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

@app.route('/general_settings')
@utils.login_required
@utils.permission_required('perm_configuracion')
def general_settings():
    logging_enabled = utils.is_logging_enabled()
    log_size_str = "0 KB"
    if os.path.exists(utils.LOG_FILE):
        size_bytes = os.path.getsize(utils.LOG_FILE)
        log_size_str = f"{size_bytes} bytes" if size_bytes < 1024 else f"{size_bytes / 1024:.2f} KB"
    planned_date = utils.get_planned_date()
    # Obtenemos nombre del mantenimiento, aunque ya lo tenemos por context_processor, lo pasamos explícitamente si se desea
    maintenance_name = utils.get_maintenance_name()
    
    conn = db.get_db_connection()
    tipos = conn.execute('SELECT * FROM tipos_equipo').fetchall()
    users = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('settings/index.html', logging_enabled=logging_enabled, log_size=log_size_str, tipos=tipos, users=users, planned_date=planned_date, maintenance_name=maintenance_name, active_page='ajustes', system_date=utils.get_system_date())

# RUTA NUEVA: ACTUALIZAR NOMBRE DEL MANTENIMIENTO
@app.route('/settings/update_maintenance_name', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def update_maintenance_name():
    name = request.form['nombre_mantenimiento']
    conn = db.get_db_connection()
    conn.execute('UPDATE configuracion SET nombre_mantenimiento=? WHERE id=1', (name,))
    conn.commit()
    conn.close()
    utils.log_action(f"Nombre del mantenimiento actualizado a: {name}")
    flash('Nombre del mantenimiento actualizado', 'success')
    return redirect(url_for('general_settings'))

@app.route('/settings/update_planned_date', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def update_planned_date():
    planned_str = request.form['fecha_prevista']
    planned_date = datetime.datetime.strptime(planned_str, '%Y-%m-%d').date()
    system_date = utils.get_system_date()
    if planned_date <= system_date:
        flash("La fecha prevista debe ser posterior a la fecha del sistema.", "danger")
        return redirect(url_for('general_settings'))
    conn = db.get_db_connection()
    conn.execute('UPDATE configuracion SET fecha_prevista = ? WHERE id = 1', (planned_str,))
    conn.execute("DELETE FROM ordenes_trabajo WHERE estado = 'Prevista'")
    actividades = conn.execute('SELECT * FROM actividades').fetchall()
    count_generated = 0
    for act in actividades:
        # LÓGICA DE CONTROL: Si la actividad tiene generar_ot desactivado, saltamos
        if not act['generar_ot']:
            continue

        f_inicio = datetime.datetime.strptime(act['fecha_inicio_gen'], '%Y-%m-%d').date()
        periodicity = act['periodicidad']
        if f_inicio > system_date: current_calc = f_inicio
        else:
            delta_days = (system_date - f_inicio).days
            periods_passed = delta_days // periodicity
            current_calc = f_inicio + datetime.timedelta(days=(periods_passed + 1) * periodicity)
        while current_calc <= planned_date:
             if not conn.execute('SELECT id FROM ordenes_trabajo WHERE actividad_id=? AND fecha_generacion=?', (act['id'], current_calc)).fetchone():
                 nombre_ot = f"{act['nombre']} - {current_calc.strftime('%d/%m/%Y')}"
                 # Modified Logic: Based on Month/Year strict comparison
                 if current_calc.year < system_date.year or (current_calc.year == system_date.year and current_calc.month < system_date.month):
                     st = 'Pendiente'
                 elif current_calc.year == system_date.year and current_calc.month == system_date.month:
                     st = 'En curso'
                 else:
                     st = 'Prevista'
                     
                 conn.execute('INSERT INTO ordenes_trabajo (actividad_id, nombre, fecha_generacion, estado) VALUES (?,?,?,?)', 
                              (act['id'], nombre_ot, current_calc, st))
                 count_generated += 1
             current_calc += datetime.timedelta(days=periodicity)
    conn.commit()
    conn.close()
    utils.log_action(f"Plan regenerado: {count_generated} OTs.")
    flash(f"Plan actualizado. Generadas {count_generated} OTs.", "success")
    return redirect(url_for('general_settings'))

@app.route('/system_date_config/update', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def update_system_date():
    conn = db.get_db_connection()
    conn.execute('UPDATE configuracion SET fecha_sistema=? WHERE id=1', (request.form['fecha_sistema'],))
    conn.commit()
    conn.close()
    return redirect(url_for('general_settings'))

@app.route('/settings/toggle_logging', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def toggle_logging():
    enabled = 1 if 'logging_enabled' in request.form else 0
    conn = db.get_db_connection()
    conn.execute('UPDATE configuracion SET logging_enabled = ? WHERE id = 1', (enabled,))
    conn.commit()
    conn.close()
    flash(f"Logging {'activado' if enabled else 'desactivado'}", "success")
    return redirect(url_for('general_settings'))

@app.route('/settings/download_log')
@utils.login_required
@utils.permission_required('perm_configuracion')
def download_log():
    if os.path.exists(utils.LOG_FILE): return send_file(utils.LOG_FILE, as_attachment=True)
    flash("Log vacío.", "warning"); return redirect(url_for('general_settings'))

@app.route('/settings/backup_db')
@utils.login_required
@utils.permission_required('perm_configuracion')
def backup_db():
    db_file = db.DB_NAME # 'mantenimiento_factory.db'
    if not os.path.exists(db_file):
        flash("No se encuentra la base de datos.", "danger")
        return redirect(url_for('general_settings'))
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_name = f"backup_mantenimiento_{timestamp}.bak"
    
    utils.log_action("Descargada copia de seguridad de la BD")
    return send_file(db_file, as_attachment=True, download_name=backup_name)

# RUTA NUEVA: RESTAURAR COPIA DE SEGURIDAD
@app.route('/settings/restore_db', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def restore_db():
    if 'db_file' not in request.files:
        flash('No se seleccionó ningún archivo', 'danger')
        return redirect(url_for('general_settings'))
    
    file = request.files['db_file']
    if file.filename == '':
        flash('No se seleccionó ningún archivo', 'danger')
        return redirect(url_for('general_settings'))

    if file and utils.allowed_file_db(file.filename):
        try:
            # 1. Guardar archivo temporal
            temp_path = "restore_temp.db"
            file.save(temp_path)
            
            # 2. Verificar que es una BD SQLite válida
            try:
                verify_conn = sqlite3.connect(temp_path)
                verify_conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                verify_conn.close()
            except sqlite3.Error:
                os.remove(temp_path)
                flash('El archivo subido no es una base de datos SQLite válida o está corrupto.', 'danger')
                return redirect(url_for('general_settings'))

            # 3. Sustituir la base de datos actual
            # Hacemos un backup rápido de la actual por si falla el move (solo un renombrado)
            current_db = db.DB_NAME
            backup_fail_safe = current_db + ".restore_backup"
            
            if os.path.exists(current_db):
                shutil.move(current_db, backup_fail_safe)
            
            try:
                shutil.move(temp_path, current_db)
                # Si todo ha ido bien, borramos el backup de seguridad
                if os.path.exists(backup_fail_safe):
                    os.remove(backup_fail_safe)
                    
                utils.log_action("Base de datos restaurada desde copia de seguridad")
                flash('Base de datos restaurada con éxito. Por seguridad, inicie sesión nuevamente.', 'success')
                return redirect(url_for('logout'))
                
            except Exception as e:
                # Si falla mover el nuevo archivo, restauramos el original
                if os.path.exists(backup_fail_safe):
                    shutil.move(backup_fail_safe, current_db)
                raise e

        except Exception as e:
            flash(f'Error al restaurar la base de datos: {str(e)}', 'danger')
            return redirect(url_for('general_settings'))
    else:
        flash('Formato de archivo no válido. Use .db, .sqlite o .bak', 'danger')
        return redirect(url_for('general_settings'))

@app.route('/users/add', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def add_user():
    try:
        pw_hash = generate_password_hash(request.form['password'])
        p_inv = 1 if 'perm_inventario' in request.form else 0
        p_act = 1 if 'perm_actividades' in request.form else 0
        p_conf = 1 if 'perm_configuracion' in request.form else 0
        conn = db.get_db_connection()
        conn.execute('INSERT INTO usuarios (username, password_hash, rol, perm_inventario, perm_actividades, perm_configuracion) VALUES (?,?,?,?,?,?)',
                     (request.form['username'], pw_hash, request.form['rol'], p_inv, p_act, p_conf))
        conn.commit()
        conn.close()
        utils.log_action(f"Usuario creado: {request.form['username']}")
        flash('Usuario creado', 'success')
    except: flash('Error al crear usuario', 'danger')
    return redirect(url_for('general_settings'))

@app.route('/users/edit/<int:id>', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def edit_user(id):
    p_inv = 1 if 'perm_inventario' in request.form else 0
    p_act = 1 if 'perm_actividades' in request.form else 0
    p_conf = 1 if 'perm_configuracion' in request.form else 0
    conn = db.get_db_connection()
    if request.form['password']:
        pw = generate_password_hash(request.form['password'])
        conn.execute('UPDATE usuarios SET rol=?, perm_inventario=?, perm_actividades=?, perm_configuracion=?, password_hash=? WHERE id=?', (request.form['rol'], p_inv, p_act, p_conf, pw, id))
    else:
        conn.execute('UPDATE usuarios SET rol=?, perm_inventario=?, perm_actividades=?, perm_configuracion=? WHERE id=?', (request.form['rol'], p_inv, p_act, p_conf, id))
    conn.commit()
    conn.close()
    utils.log_action(f"Usuario editado: ID {id}")
    flash('Usuario actualizado', 'success')
    return redirect(url_for('general_settings'))

@app.route('/users/delete/<int:id>', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def delete_user(id):
    conn = db.get_db_connection()
    conn.execute('DELETE FROM usuarios WHERE id=?', (id,))
    conn.commit()
    conn.close()
    utils.log_action(f"Usuario eliminado: ID {id}")
    flash('Usuario eliminado', 'success')
    return redirect(url_for('general_settings'))

@app.route('/configuration/type/add', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def add_type_config():
    try:
        conn = db.get_db_connection()
        conn.execute('INSERT INTO tipos_equipo (nombre) VALUES (?)', (request.form['nombre'],))
        conn.commit()
        conn.close()
        utils.log_action(f"Tipo creado: {request.form['nombre']}")
    except: pass
    return redirect(url_for('general_settings'))

@app.route('/configuration/type/edit/<int:id>')
@utils.login_required
@utils.permission_required('perm_configuracion')
def edit_type(id):
    conn = db.get_db_connection()
    tipo = conn.execute('SELECT * FROM tipos_equipo WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('settings/edit_type.html', tipo=tipo, active_page='ajustes', system_date=utils.get_system_date())

@app.route('/configuration/type/update/<int:id>', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def update_type(id):
    try:
        conn = db.get_db_connection()
        conn.execute('UPDATE tipos_equipo SET nombre=? WHERE id=?', (request.form['nombre'], id))
        conn.commit()
        conn.close()
    except: pass
    return redirect(url_for('general_settings'))

@app.route('/about')
def about():
    return render_template('about.html', active_page='about', system_date=utils.get_system_date())

@app.route('/types/add', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_inventario')
def add_type():
    try:
        conn = db.get_db_connection()
        conn.execute('INSERT INTO tipos_equipo (nombre) VALUES (?)', (request.form['nombre'],))
        conn.commit()
        conn.close()
    except: pass
    return redirect(url_for('inventory'))

# ==========================================
# RUTAS NUEVAS PARA EL CALENDARIO (COLORES ACTUALIZADOS)
# ==========================================

@app.route('/calendar')
@utils.login_required
def calendar_view():
    return render_template('calendar/index.html', active_page='calendario', system_date=utils.get_system_date())

@app.route('/api/calendar_events')
@utils.login_required
def get_calendar_events():
    conn = db.get_db_connection()
    ots = conn.execute('SELECT id, nombre, fecha_generacion, estado, observaciones FROM ordenes_trabajo').fetchall()
    conn.close()
    
    events = []
    for ot in ots:
        color = '#6c757d' # Default
        estado = ot['estado']
        
        if estado == 'Pendiente': color = '#dc3545'      # Rojo
        elif estado == 'En curso': color = '#ffc107'     # Amarillo
        elif estado == 'Realizada': color = '#28a745'    # Verde
        elif estado == 'Prevista': color = '#6c757d'     # Gris
        elif estado == 'Aplazada': color = '#6f42c1'     # Violeta
        elif estado == 'Rechazada': color = '#000000'    # Negra
        
        events.append({
            'id': ot['id'],
            'title': ot['nombre'],
            'start': ot['fecha_generacion'],
            'color': color,
            'url': url_for('work_orders'),
            'extendedProps': {
                'estado': estado,
                'observaciones': ot['observaciones'] or ''
            }
        })
        
    return json.dumps(events)

if __name__ == '__main__':
    if not os.path.exists('mantenimiento_factory.db'):
        db.init_db()
    db.init_db()
    utils.create_default_admin()
    print("Sincronizando fecha del sistema...")
    try:
        conn = db.get_db_connection()
        real_today = datetime.date.today()
        # Usamos .isoformat() para convertir el objeto fecha a texto "YYYY-MM-DD"
        conn.execute('UPDATE configuracion SET fecha_sistema=? WHERE id=1', (real_today.isoformat(),))
        count = utils.generate_and_update_work_orders(conn, real_today)
        conn.commit()
        conn.close()
        print(f"Sistema sincronizado a {real_today}. OTs procesadas: {count}")
    except Exception as e: print(f"Error en sincronización inicial: {e}")
    print("Iniciando Sistema GMAO...")
    print("Accesible en tu red local. Busca tu IP (ej: ipconfig o ifconfig)")
    ## app.run(debug=True, port=5000, host='0.0.0.0')
    serve(app, port=5000, host='0.0.0.0')