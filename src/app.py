import sqlite3
import base64
import datetime
from flask import Flask, render_template_string, request, redirect, url_for, flash, send_file, session
import json
import os
from werkzeug.security import check_password_hash, generate_password_hash

# Importamos los módulos locales
import database as db
import utils
import templates_base as tpl_base
import templates_modules as tpl_modules

app = Flask(__name__)
app.secret_key = 'super_secret_key_mantenimiento_factory'

# Registramos el filtro Jinja
@app.template_filter('json_load')
def json_load_filter(s):
    return utils.json_load_filter(s)

# --- RUTAS DE AUTENTICACIÓN ---
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
    return render_template_string(tpl_base.LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    utils.log_action(f"Cierre de sesión: {session.get('username')}")
    session.clear()
    return redirect(url_for('login'))

# --- RUTA PRINCIPAL (INICIO/INVENTARIO) ---
@app.route('/')
@utils.login_required
def index():
    db.init_db()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    f_nombre = request.args.get('f_nombre', '')
    f_tipo = request.args.get('f_tipo', '')
    
    conn = db.get_db_connection()
    tipos = conn.execute('SELECT * FROM tipos_equipo').fetchall()
    
    where_clause = "WHERE 1=1"
    params = []
    if f_nombre: 
        where_clause += " AND i.nombre LIKE ?"
        params.append(f'%{f_nombre}%')
    if f_tipo: 
        where_clause += " AND i.tipo_id = ?"
        params.append(f_tipo)
    
    count = conn.execute(f'SELECT COUNT(*) FROM inventario i {where_clause}', params).fetchone()[0]
    items = conn.execute(f'SELECT i.*, t.nombre as tipo_nombre FROM inventario i LEFT JOIN tipos_equipo t ON i.tipo_id=t.id {where_clause} LIMIT ? OFFSET ?', params + [per_page, offset]).fetchall()
    has_next = (page * per_page) < count
    conn.close()
    
    return render_template_string(
        tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_modules.INVENTARIO_TEMPLATE), 
        items=items, tipos=tipos, page=page, has_next=has_next, 
        active_page='inventario', system_date=utils.get_system_date(), 
        f_nombre=f_nombre, f_tipo=f_tipo
    )

# --- RUTAS DE GESTIÓN DE INVENTARIO ---
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
    except Exception as e: 
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('index'))

@app.route('/inventory/edit/<int:id>')
@utils.login_required
@utils.permission_required('perm_inventario')
def edit_inventory(id):
    conn = db.get_db_connection()
    item = conn.execute('SELECT * FROM inventario WHERE id=?', (id,)).fetchone()
    tipos = conn.execute('SELECT * FROM tipos_equipo').fetchall()
    conn.close()
    if not item: return redirect(url_for('index'))
    imgs = utils.normalize_files(json.loads(item['images']) if item['images'] else [])
    pdfs = utils.normalize_files(json.loads(item['pdfs']) if item['pdfs'] else [])
    return render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_modules.EDIT_INVENTORY_TEMPLATE), item=item, tipos=tipos, imgs=imgs, pdfs=pdfs, active_page='inventario', system_date=utils.get_system_date())

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
    return redirect(url_for('index'))

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
        flash('Equipo y datos asociados eliminados.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al eliminar: {e}', 'danger')
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/inventory/print/<int:id>')
@utils.login_required
def print_inventory(id):
    conn = db.get_db_connection()
    item = conn.execute('SELECT i.*, t.nombre as tipo_nombre FROM inventario i LEFT JOIN tipos_equipo t ON i.tipo_id=t.id WHERE i.id=?', (id,)).fetchone()
    conn.close()
    imgs = utils.normalize_files(json.loads(item['images']) if item['images'] else [])
    pdfs = utils.normalize_files(json.loads(item['pdfs']) if item['pdfs'] else [])
    utils.log_action(f"Impreso inventario individual: ID {id}")
    return render_template_string(tpl_base.PRINT_TEMPLATE, item=item, imgs=imgs, pdfs=pdfs, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/inventory/print_all')
@utils.login_required
def print_all_inventory():
    f_nombre = request.args.get('f_nombre', '')
    f_tipo = request.args.get('f_tipo', '')
    conn = db.get_db_connection()
    where = "WHERE 1=1"
    p = []
    if f_nombre: where += " AND i.nombre LIKE ?"; p.append(f'%{f_nombre}%')
    if f_tipo: where += " AND i.tipo_id = ?"; p.append(f_tipo)
    items = conn.execute(f'SELECT i.*, t.nombre as tipo_nombre FROM inventario i LEFT JOIN tipos_equipo t ON i.tipo_id=t.id {where} ORDER BY i.nombre', p).fetchall()
    conn.close()
    utils.log_action("Impreso listado completo inventario")
    return render_template_string(tpl_base.PRINT_ALL_TEMPLATE, items=items, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/view_files/<source>/<tipo>/<int:id>')
@utils.login_required
def view_files(source, tipo, id):
    conn = db.get_db_connection()
    if source == 'inventory':
        item = conn.execute('SELECT * FROM inventario WHERE id=?', (id,)).fetchone()
        back_url = url_for('index')
        title_prefix = "Archivos de Equipo"
    elif source == 'corrective':
        item = conn.execute('SELECT * FROM correctivos WHERE id=?', (id,)).fetchone()
        back_url = url_for('correctivos')
        title_prefix = "Archivos de Incidencia"
    else:
        item = None
        back_url = url_for('index')
        title_prefix = "Archivos"
    conn.close()
    files = []
    if item:
        content = item['images'] if tipo == 'img' else item['pdfs']
        files = utils.normalize_files(json.loads(content) if content else [])
    return render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_base.VIEWER_TEMPLATE), item=item, files=files, tipo=tipo, back_url=back_url, title_prefix=title_prefix, active_page='inventario', system_date=utils.get_system_date())

# --- RUTAS DE ACTIVIDADES ---
@app.route('/activities')
@utils.login_required
@utils.permission_required('perm_actividades')
def activities():
    f_nombre = request.args.get('f_nombre', '')
    f_equipo = request.args.get('f_equipo', '')
    f_periodicidad = request.args.get('f_periodicidad', '')
    conn = db.get_db_connection()
    query = 'SELECT a.*, i.nombre as equipo_nombre FROM actividades a JOIN inventario i ON a.equipo_id = i.id WHERE 1=1'
    p = []
    if f_nombre: query += " AND a.nombre LIKE ?"; p.append(f'%{f_nombre}%')
    if f_equipo: query += " AND a.equipo_id = ?"; p.append(f_equipo)
    if f_periodicidad: query += " AND a.periodicidad = ?"; p.append(f_periodicidad)
    actividades = conn.execute(query, p).fetchall()
    equipos = conn.execute('SELECT i.id, i.nombre, t.nombre as tipo_nombre FROM inventario i JOIN tipos_equipo t ON i.tipo_id = t.id').fetchall()
    conn.close()
    return render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_modules.ACTIVIDADES_TEMPLATE), actividades=actividades, equipos=equipos, active_page='actividades', f_nombre=f_nombre, f_equipo=f_equipo, f_periodicidad=f_periodicidad, system_date=utils.get_system_date())

@app.route('/activities/add', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_actividades')
def add_activity():
    conn = db.get_db_connection()
    conn.execute('INSERT INTO actividades (nombre, equipo_id, periodicidad, operaciones, fecha_inicio_gen) VALUES (?,?,?,?,?)',
                 (request.form['nombre'], request.form['equipo_id'], request.form['periodicidad'], request.form['operaciones'], request.form['fecha_inicio']))
    conn.commit()
    conn.close()
    utils.log_action(f"Actividad creada: {request.form['nombre']}")
    flash('Actividad creada', 'success')
    return redirect(url_for('activities'))

@app.route('/activities/edit/<int:id>')
@utils.login_required
@utils.permission_required('perm_actividades')
def edit_activity(id):
    conn = db.get_db_connection()
    activity = conn.execute('SELECT * FROM actividades WHERE id=?', (id,)).fetchone()
    equipos = conn.execute('SELECT i.id, i.nombre, t.nombre as tipo_nombre FROM inventario i JOIN tipos_equipo t ON i.tipo_id = t.id').fetchall()
    conn.close()
    return render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_modules.EDIT_ACTIVITY_TEMPLATE), activity=activity, equipos=equipos, active_page='actividades', system_date=utils.get_system_date())

@app.route('/activities/update/<int:id>', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_actividades')
def update_activity(id):
    conn = db.get_db_connection()
    conn.execute('UPDATE actividades SET nombre=?, equipo_id=?, periodicidad=?, operaciones=?, fecha_inicio_gen=? WHERE id=?',
                 (request.form['nombre'], request.form['equipo_id'], request.form['periodicidad'], request.form['operaciones'], request.form['fecha_inicio'], id))
    conn.commit()
    conn.close()
    utils.log_action(f"Actividad actualizada: ID {id}")
    flash('Actividad actualizada', 'success')
    return redirect(url_for('activities'))

@app.route('/activities/delete/<int:id>', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_actividades')
def delete_activity(id):
    conn = db.get_db_connection()
    try:
        conn.execute('DELETE FROM ordenes_trabajo WHERE actividad_id = ?', (id,))
        conn.execute('DELETE FROM actividades WHERE id = ?', (id,))
        conn.commit()
        utils.log_action(f"Actividad eliminada: ID {id} y sus OTs asociadas.")
        flash('Actividad y sus órdenes de trabajo asociadas han sido eliminadas.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al eliminar la actividad: {e}', 'danger')
    finally:
        conn.close()
    return redirect(url_for('activities'))

@app.route('/activities/print/<int:id>')
@utils.login_required
def print_activity_single(id):
    conn = db.get_db_connection()
    activity = conn.execute('SELECT a.*, i.nombre as equipo_nombre, t.nombre as tipo_nombre FROM actividades a JOIN inventario i ON a.equipo_id=i.id JOIN tipos_equipo t ON i.tipo_id=t.id WHERE a.id=?', (id,)).fetchone()
    conn.close()
    utils.log_action(f"Impresa actividad individual: ID {id}")
    return render_template_string(tpl_base.PRINT_ACTIVITY_TEMPLATE, activity=activity, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/activities/print_all')
@utils.login_required
def print_all_activities():
    conn = db.get_db_connection()
    activities = conn.execute('SELECT a.*, i.nombre as equipo_nombre FROM actividades a JOIN inventario i ON a.equipo_id=i.id ORDER BY a.nombre').fetchall()
    conn.close()
    utils.log_action("Impreso listado completo actividades")
    return render_template_string(tpl_base.PRINT_ALL_ACTIVITIES_TEMPLATE, activities=activities, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

# --- RUTAS DE WORK ORDERS ---
@app.route('/work_orders')
@utils.login_required
def work_orders():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    estado = request.args.get('estado', '')
    fecha_inicio = request.args.get('fecha_inicio', '')
    fecha_fin = request.args.get('fecha_fin', '')
    conn = db.get_db_connection()
    q = 'FROM ordenes_trabajo ot JOIN actividades a ON ot.actividad_id = a.id JOIN inventario i ON a.equipo_id = i.id WHERE 1=1'
    p = []
    if estado: q+=" AND ot.estado=?"; p.append(estado)
    if fecha_inicio: q+=" AND ot.fecha_generacion>=?"; p.append(fecha_inicio)
    if fecha_fin: q+=" AND ot.fecha_generacion<=?"; p.append(fecha_fin)
    count = conn.execute(f'SELECT COUNT(*) {q}', p).fetchone()[0]
    ots = conn.execute(f'SELECT ot.*, a.operaciones, i.nombre as equipo_nombre {q} ORDER BY ot.fecha_generacion DESC LIMIT ? OFFSET ?', p+[per_page, offset]).fetchall()
    has_next = (page*per_page)<count
    conn.close()
    return render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_modules.OTS_TEMPLATE), ots=ots, page=page, has_next=has_next, active_page='ots', estado_filter=estado, fecha_inicio_filter=fecha_inicio, fecha_fin_filter=fecha_fin, system_date=utils.get_system_date())

@app.route('/work_orders/generate', methods=['POST'])
@utils.login_required
def generate_work_orders():
    conn = db.get_db_connection()
    current_date = utils.get_system_date()
    count = utils.generate_and_update_work_orders(conn, current_date)
    conn.commit()
    conn.close()
    utils.log_action("Generación manual de OTs ejecutada")
    flash(f'Proceso completado. Se han generado {count} nuevas órdenes.', 'info')
    return redirect(url_for('work_orders'))

@app.route('/work_orders/update/<int:id>', methods=['POST'])
@utils.login_required
def update_ot(id):
    conn = db.get_db_connection()
    conn.execute('UPDATE ordenes_trabajo SET estado=?, observaciones=?, fecha_realizada=? WHERE id=?', (request.form['estado'], request.form['observaciones'], request.form['fecha_realizada'], id))
    conn.commit()
    conn.close()
    utils.log_action(f"OT actualizada: ID {id}")
    flash('OT actualizada', 'success')
    if request.form.get('redirect_to')=='cronograma': return redirect(url_for('cronograma'))
    return redirect(url_for('work_orders'))

@app.route('/work_orders/print/<int:id>')
@utils.login_required
def print_ot(id):
    conn = db.get_db_connection()
    ot = conn.execute('SELECT ot.*, a.operaciones, i.nombre as equipo_nombre, t.nombre as tipo_nombre FROM ordenes_trabajo ot JOIN actividades a ON ot.actividad_id=a.id JOIN inventario i ON a.equipo_id=i.id JOIN tipos_equipo t ON i.tipo_id=t.id WHERE ot.id=?', (id,)).fetchone()
    conn.close()
    utils.log_action(f"Impresa OT individual: ID {id}")
    return render_template_string(tpl_base.PRINT_OT_TEMPLATE, ot=ot, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/work_orders/print_all')
@utils.login_required
def print_all_ots():
    estado = request.args.get('estado', '')
    fecha_inicio = request.args.get('fecha_inicio', '')
    fecha_fin = request.args.get('fecha_fin', '')
    conn = db.get_db_connection()
    q = 'SELECT ot.*, i.nombre as equipo_nombre FROM ordenes_trabajo ot JOIN actividades a ON ot.actividad_id=a.id JOIN inventario i ON a.equipo_id=i.id WHERE 1=1'
    p = []
    if estado: q+=" AND ot.estado=?"; p.append(estado)
    if fecha_inicio: q+=" AND ot.fecha_generacion>=?"; p.append(fecha_inicio)
    if fecha_fin: q+=" AND ot.fecha_generacion<=?"; p.append(fecha_fin)
    q += " ORDER BY ot.fecha_generacion DESC"
    ots = conn.execute(q, p).fetchall()
    conn.close()
    utils.log_action("Impreso listado OTs filtrado")
    return render_template_string(tpl_base.PRINT_ALL_OTS_TEMPLATE, ots=ots, filters=[], hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/cronograma')
@utils.login_required
def cronograma():
    year = request.args.get('year', utils.get_system_date().year, type=int)
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    conn = db.get_db_connection()
    data = utils.get_cronograma_data(conn, year)
    conn.close()
    return render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_modules.CRONOGRAMA_TEMPLATE), data=data, meses=meses, year=year, active_page='cronograma', system_date=utils.get_system_date())

@app.route('/cronograma/print')
@utils.login_required
def print_cronograma():
    year = request.args.get('year', utils.get_system_date().year, type=int)
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    conn = db.get_db_connection()
    data = utils.get_cronograma_data(conn, year)
    conn.close()
    utils.log_action(f"Impreso cronograma año {year}")
    return render_template_string(tpl_base.PRINT_CRONOGRAMA_TEMPLATE, data=data, meses=meses, year=year, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/correctivos')
@utils.login_required
def correctivos():
    f_nombre = request.args.get('f_nombre', '')
    f_equipo = request.args.get('f_equipo', '')
    f_estado = request.args.get('f_estado', '')
    f_fecha_desde = request.args.get('f_fecha_desde', '')
    conn = db.get_db_connection()
    q = 'SELECT c.*, i.nombre as equipo_nombre FROM correctivos c JOIN inventario i ON c.equipo_id=i.id WHERE 1=1'
    p = []
    if f_nombre: q+=" AND c.nombre LIKE ?"; p.append(f'%{f_nombre}%')
    if f_equipo: q+=" AND c.equipo_id=?"; p.append(f_equipo)
    if f_estado: q+=" AND c.estado=?"; p.append(f_estado)
    if f_fecha_desde: q+=" AND c.fecha_detectada>=?"; p.append(f_fecha_desde)
    q += " ORDER BY c.fecha_detectada DESC"
    items = conn.execute(q, p).fetchall()
    equipos = conn.execute('SELECT i.id, i.nombre, t.nombre as tipo_nombre FROM inventario i JOIN tipos_equipo t ON i.tipo_id=t.id').fetchall()
    conn.close()
    return render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_modules.CORRECTIVOS_TEMPLATE), correctivos=items, equipos=equipos, active_page='correctivos', f_nombre=f_nombre, f_equipo=f_equipo, f_estado=f_estado, f_fecha_desde=f_fecha_desde, system_date=utils.get_system_date())

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
    return render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_modules.EDIT_CORRECTIVO_TEMPLATE), item=item, equipos=equipos, imgs=imgs, pdfs=pdfs, active_page='correctivos', system_date=utils.get_system_date())

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
    pdfs = utils.normalize_files(json.loads(item['pdfs']) if item['pdfs'] else []) # Extract PDFs
    utils.log_action(f"Impresa incidencia individual: ID {id}")
    return render_template_string(tpl_base.PRINT_CORRECTIVO_TEMPLATE, item=item, imgs=imgs, pdfs=pdfs, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

@app.route('/correctivos/print_all')
@utils.login_required
def print_all_correctivos():
    f_nombre = request.args.get('f_nombre', '')
    f_equipo = request.args.get('f_equipo', '')
    f_estado = request.args.get('f_estado', '')
    f_fecha_desde = request.args.get('f_fecha_desde', '')
    conn = db.get_db_connection()
    q = 'SELECT c.*, i.nombre as equipo_nombre FROM correctivos c JOIN inventario i ON c.equipo_id=i.id WHERE 1=1'
    p = []
    if f_nombre: q+=" AND c.nombre LIKE ?"; p.append(f'%{f_nombre}%')
    if f_equipo: q+=" AND c.equipo_id=?"; p.append(f_equipo)
    if f_estado: q+=" AND c.estado=?"; p.append(f_estado)
    if f_fecha_desde: q+=" AND c.fecha_detectada>=?"; p.append(f_fecha_desde)
    q += " ORDER BY c.fecha_detectada DESC"
    items = conn.execute(q, p).fetchall()
    conn.close()
    utils.log_action("Impreso listado incidencias")
    return render_template_string(tpl_base.PRINT_ALL_CORRECTIVOS_TEMPLATE, items=items, hoy=utils.get_system_date().strftime('%d/%m/%Y'))

# --- CONFIGURACIÓN GLOBAL (INTEGRADA) ---
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
    
    conn = db.get_db_connection()
    tipos = conn.execute('SELECT * FROM tipos_equipo').fetchall()
    users = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
            
    # Usamos tpl_base para configuraciones
    return render_template_string(tpl_modules.GENERAL_SETTINGS_TEMPLATE, 
                                  BASE_TEMPLATE=tpl_base.BASE_TEMPLATE,
                                  logging_enabled=logging_enabled, log_size=log_size_str, tipos=tipos, users=users,
                                  planned_date=planned_date, active_page='ajustes', system_date=utils.get_system_date())

# FIX: GENERAL_SETTINGS_TEMPLATE in tpl_base was slightly wrong in previous context usage.
# Correction: render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_base.GENERAL_SETTINGS_TEMPLATE), ...)
@app.route('/general_settings')
@utils.login_required
@utils.permission_required('perm_configuracion')
def general_settings_corrected():
    logging_enabled = utils.is_logging_enabled()
    log_size_str = "0 KB"
    if os.path.exists(utils.LOG_FILE):
        size_bytes = os.path.getsize(utils.LOG_FILE)
        log_size_str = f"{size_bytes} bytes" if size_bytes < 1024 else f"{size_bytes / 1024:.2f} KB"
    
    planned_date = utils.get_planned_date()
    
    conn = db.get_db_connection()
    tipos = conn.execute('SELECT * FROM tipos_equipo').fetchall()
    users = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
            
    return render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_modules.GENERAL_SETTINGS_TEMPLATE), 
                                  logging_enabled=logging_enabled, log_size=log_size_str, tipos=tipos, users=users,
                                  planned_date=planned_date, active_page='ajustes', system_date=utils.get_system_date())
# Overwrite the function to remove the duplicate
app.view_functions['general_settings'] = general_settings_corrected

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
        f_inicio = datetime.datetime.strptime(act['fecha_inicio_gen'], '%Y-%m-%d').date()
        periodicity = act['periodicidad']
        
        if f_inicio > system_date:
            current_calc = f_inicio
        else:
            delta_days = (system_date - f_inicio).days
            periods_passed = delta_days // periodicity
            current_calc = f_inicio + datetime.timedelta(days=(periods_passed + 1) * periodicity)
        
        while current_calc <= planned_date:
             if not conn.execute('SELECT id FROM ordenes_trabajo WHERE actividad_id=? AND fecha_generacion=?', (act['id'], current_calc)).fetchone():
                 nombre_ot = f"{act['nombre']} - {current_calc.strftime('%d/%m/%Y')}"
                 conn.execute('INSERT INTO ordenes_trabajo (actividad_id, nombre, fecha_generacion, estado) VALUES (?,?,?,?)', 
                              (act['id'], nombre_ot, current_calc, 'Prevista'))
                 count_generated += 1
             current_calc += datetime.timedelta(days=periodicity)

    conn.commit()
    conn.close()
    
    utils.log_action(f"Fecha prevista actualizada a {planned_str}. Plan regenerado: {count_generated} OTs.")
    flash(f"Plan actualizado. Generadas {count_generated} OTs previstas.", "success")
    return redirect(url_for('general_settings'))

@app.route('/system_date_config/update', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def update_system_date():
    conn = db.get_db_connection()
    conn.execute('UPDATE configuracion SET fecha_sistema=? WHERE id=1', (request.form['fecha_sistema'],))
    conn.commit()
    conn.close()
    utils.log_action(f"Fecha sistema cambiada a {request.form['fecha_sistema']}")
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

# --- USUARIOS ---
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

# --- TIPOS ---
@app.route('/configuration/type/add', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def add_type_config():
    try:
        conn = db.get_db_connection()
        conn.execute('INSERT INTO tipos_equipo (nombre) VALUES (?)', (request.form['nombre'],))
        conn.commit()
        conn.close()
        utils.log_action(f"Tipo de equipo creado: {request.form['nombre']}")
    except: pass
    return redirect(url_for('general_settings'))

@app.route('/configuration/type/edit/<int:id>')
@utils.login_required
@utils.permission_required('perm_configuracion')
def edit_type(id):
    conn = db.get_db_connection()
    tipo = conn.execute('SELECT * FROM tipos_equipo WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_modules.EDIT_TYPE_TEMPLATE), tipo=tipo, active_page='ajustes', system_date=utils.get_system_date())

@app.route('/configuration/type/update/<int:id>', methods=['POST'])
@utils.login_required
@utils.permission_required('perm_configuracion')
def update_type(id):
    try:
        conn = db.get_db_connection()
        conn.execute('UPDATE tipos_equipo SET nombre=? WHERE id=?', (request.form['nombre'], id))
        conn.commit()
        conn.close()
        utils.log_action(f"Tipo actualizado: ID {id}")
    except: pass
    return redirect(url_for('general_settings'))

@app.route('/about')
def about():
    return render_template_string(tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', tpl_base.ABOUT_TEMPLATE), active_page='about', system_date=utils.get_system_date())

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
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('mantenimiento_factory.db'):
        db.init_db()
    # Force DB update
    db.init_db()
    utils.create_default_admin()

    print("Sincronizando fecha del sistema...")
    try:
        conn = db.get_db_connection()
        real_today = datetime.date.today()
        conn.execute('UPDATE configuracion SET fecha_sistema=? WHERE id=1', (real_today,))
        count = utils.generate_and_update_work_orders(conn, real_today)
        conn.commit()
        conn.close()
        print(f"Sistema sincronizado a {real_today}. OTs procesadas: {count}")
    except Exception as e:
        print(f"Error en sincronización inicial: {e}")

    print("Iniciando Sistema GMAO...")
    print("Accesible en tu red local. Busca tu IP (ej: ipconfig o ifconfig)")
    app.run(debug=True, port=5000, host='0.0.0.0')