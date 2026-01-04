from flask import Blueprint, render_template, request, redirect, url_for
import database as db
import utils
import datetime
import json

resumen_bp = Blueprint('resumen', __name__)

@resumen_bp.route('/')
@utils.login_required
def index():
    conn = db.get_db_connection()
    
    config = conn.execute('SELECT fecha_inicio_resumen, fecha_fin_resumen FROM configuracion WHERE id=1').fetchone()
    today = utils.get_system_date()
    
    if config and config['fecha_inicio_resumen']: fecha_inicio = config['fecha_inicio_resumen']
    else: fecha_inicio = (today - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
    if config and config['fecha_fin_resumen']: fecha_fin = config['fecha_fin_resumen']
    else: fecha_fin = today.strftime('%Y-%m-%d')

    estados_ot_orden = ['Realizada', 'En curso', 'Pendiente', 'Prevista', 'Aplazada', 'Rechazada']
    values_ot = []
    total_ots = 0
    for estado in estados_ot_orden:
        count = conn.execute("SELECT COUNT(*) FROM ordenes_trabajo WHERE fecha_generacion BETWEEN ? AND ? AND estado = ?", (fecha_inicio, fecha_fin, estado)).fetchone()[0]
        values_ot.append(count)
        total_ots += count
    
    estados_corr_orden = ['Detectada', 'En curso', 'Resuelta']
    values_corr = []
    total_corr = 0
    for estado in estados_corr_orden:
        count = conn.execute("SELECT COUNT(*) FROM correctivos WHERE fecha_detectada BETWEEN ? AND ? AND estado = ?", (fecha_inicio, fecha_fin, estado)).fetchone()[0]
        values_corr.append(count)
        total_corr += count

    # NEW: Fetch actual data for tables
    ots_query = """
        SELECT ot.id, ot.nombre, ot.fecha_generacion, ot.estado, i.nombre as equipo_nombre
        FROM ordenes_trabajo ot
        JOIN actividades a ON ot.actividad_id = a.id
        JOIN inventario i ON a.equipo_id = i.id
        WHERE ot.fecha_generacion BETWEEN ? AND ?
        ORDER BY ot.fecha_generacion DESC
    """
    ots = conn.execute(ots_query, (fecha_inicio, fecha_fin)).fetchall()

    corr_query = """
        SELECT c.id, c.nombre, c.fecha_detectada, c.estado, i.nombre as equipo_nombre
        FROM correctivos c
        JOIN inventario i ON c.equipo_id = i.id
        WHERE c.fecha_detectada BETWEEN ? AND ?
        ORDER BY c.fecha_detectada DESC
    """
    correctivos = conn.execute(corr_query, (fecha_inicio, fecha_fin)).fetchall()

    conn.close()

    return render_template('resumen/index.html', active_page='resumen', system_date=utils.get_system_date(),
        fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
        labels_ot=json.dumps(estados_ot_orden), values_ot=json.dumps(values_ot),
        labels_corr=json.dumps(estados_corr_orden), values_corr=json.dumps(values_corr),
        total_ots=total_ots, total_corr=total_corr,
        ots=ots, correctivos=correctivos)

@resumen_bp.route('/update_dates', methods=['POST'])
@utils.login_required
def update_dates():
    f_inicio = request.form['fecha_inicio']
    f_fin = request.form['fecha_fin']
    conn = db.get_db_connection()
    conn.execute('UPDATE configuracion SET fecha_inicio_resumen=?, fecha_fin_resumen=? WHERE id=1', (f_inicio, f_fin))
    conn.commit()
    conn.close()
    return redirect(url_for('resumen.index'))