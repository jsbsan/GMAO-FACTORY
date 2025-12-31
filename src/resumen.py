from flask import Blueprint, render_template_string, request, redirect, url_for
import database as db
import utils
import templates_base as tpl_base
import datetime
import json

# Definimos el Blueprint
resumen_bp = Blueprint('resumen', __name__)

RESUMEN_TEMPLATE = """
<script src="{{ url_for('static', filename='js/chart.min.js') }}"></script>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h2">Resumen Ejecutivo</h1>
    <span class="text-muted">Estadísticas del periodo seleccionado</span>
</div>

<div class="card mb-4 border-primary">
    <div class="card-header bg-primary text-white">
        <h5 class="mb-0"><i class="fas fa-calendar-alt me-2"></i> Configuración del Periodo</h5>
    </div>
    <div class="card-body bg-light">
        <form action="{{ url_for('resumen.update_dates') }}" method="POST" class="row align-items-end g-3">
            <div class="col-md-5">
                <label class="form-label fw-bold">Fecha Inicio Resumen</label>
                <input type="date" class="form-control" name="fecha_inicio" value="{{ fecha_inicio }}" required>
            </div>
            <div class="col-md-5">
                <label class="form-label fw-bold">Fecha Fin Resumen</label>
                <input type="date" class="form-control" name="fecha_fin" value="{{ fecha_fin }}" required>
            </div>
            <div class="col-md-2">
                <button type="submit" class="btn btn-primary w-100"><i class="fas fa-sync-alt"></i> Actualizar</button>
            </div>
        </form>
    </div>
</div>

<div class="row">
    <!-- Panel OTs -->
    <div class="col-md-6 mb-4">
        <div class="card h-100 shadow-sm">
            <div class="card-header fw-bold text-center bg-light">Distribución de Órdenes de Trabajo</div>
            <div class="card-body">
                <div style="position: relative; height: 300px; width: 100%;">
                    <canvas id="chartOTs"></canvas>
                </div>
                <div class="mt-3 text-center small text-muted">Total OTs en el periodo: {{ total_ots }}</div>
            </div>
        </div>
    </div>

    <!-- Panel Correctivos -->
    <div class="col-md-6 mb-4">
        <div class="card h-100 shadow-sm">
            <div class="card-header fw-bold text-center bg-light">Distribución de Incidencias (Correctivos)</div>
            <div class="card-body">
                <div style="position: relative; height: 300px; width: 100%;">
                    <canvas id="chartCorrectivos"></canvas>
                </div>
                 <div class="mt-3 text-center small text-muted">Total Incidencias en el periodo: {{ total_corr }}</div>
            </div>
        </div>
    </div>
</div>

<script>
    // Configuración Gráfico OTs
    const ctxOT = document.getElementById('chartOTs').getContext('2d');
    const dataOT = {
        labels: {{ labels_ot | safe }},
        datasets: [{
            data: {{ values_ot | safe }},
            backgroundColor: [
                '#198754', // Realizada (Verde)
                '#ffc107', // En curso (Amarillo)
                '#dc3545', // Pendiente (Rojo)
                '#6c757d', // Prevista (Gris)
                '#6f42c1', // Aplazada (Morado)
                '#000000'  // Rechazada (Negro)
            ],
            borderWidth: 1
        }]
    };
    new Chart(ctxOT, {
        type: 'doughnut',
        data: dataOT,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            if (label) label += ': ';
                            let value = context.raw;
                            let total = context.chart._metasets[context.datasetIndex].total;
                            let percentage = Math.round((value / total) * 100) + '%';
                            return label + value + ' (' + percentage + ')';
                        }
                    }
                }
            }
        }
    });

    // Configuración Gráfico Correctivos
    const ctxCorr = document.getElementById('chartCorrectivos').getContext('2d');
    const dataCorr = {
        labels: {{ labels_corr | safe }},
        datasets: [{
            data: {{ values_corr | safe }},
            backgroundColor: [
                '#dc3545', // Detectada (Rojo)
                '#ffc107', // En curso (Amarillo)
                '#198754'  // Resuelta (Verde)
            ],
            borderWidth: 1
        }]
    };
    new Chart(ctxCorr, {
        type: 'pie',
        data: dataCorr,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            if (label) label += ': ';
                            let value = context.raw;
                            let total = context.chart._metasets[context.datasetIndex].total;
                            let percentage = Math.round((value / total) * 100) + '%';
                            return label + value + ' (' + percentage + ')';
                        }
                    }
                }
            }
        }
    });
</script>
"""

@resumen_bp.route('/')
@utils.login_required
def index():
    conn = db.get_db_connection()
    
    # 1. Obtener Configuración de Fechas
    config = conn.execute('SELECT fecha_inicio_resumen, fecha_fin_resumen FROM configuracion WHERE id=1').fetchone()
    
    today = utils.get_system_date()
    
    # Lógica de fechas por defecto
    if config and config['fecha_inicio_resumen']:
        fecha_inicio = config['fecha_inicio_resumen']
    else:
        fecha_inicio = (today - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        
    if config and config['fecha_fin_resumen']:
        fecha_fin = config['fecha_fin_resumen']
    else:
        fecha_fin = today.strftime('%Y-%m-%d')

    # 2. Datos para OTs (Coincidencia exacta de colores requiere orden fijo)
    # Orden deseado: Realizada, En curso, Pendiente, Prevista, Aplazada, Rechazada
    estados_ot_orden = ['Realizada', 'En curso', 'Pendiente', 'Prevista', 'Aplazada', 'Rechazada']
    values_ot = []
    
    total_ots = 0
    for estado in estados_ot_orden:
        count = conn.execute(
            "SELECT COUNT(*) FROM ordenes_trabajo WHERE fecha_generacion BETWEEN ? AND ? AND estado = ?", 
            (fecha_inicio, fecha_fin, estado)
        ).fetchone()[0]
        values_ot.append(count)
        total_ots += count
    
    # 3. Datos para Correctivos
    # Orden deseado: Detectada, En curso, Resuelta
    estados_corr_orden = ['Detectada', 'En curso', 'Resuelta']
    values_corr = []
    
    total_corr = 0
    for estado in estados_corr_orden:
        # Usamos fecha_detectada como criterio
        count = conn.execute(
            "SELECT COUNT(*) FROM correctivos WHERE fecha_detectada BETWEEN ? AND ? AND estado = ?", 
            (fecha_inicio, fecha_fin, estado)
        ).fetchone()[0]
        values_corr.append(count)
        total_corr += count
        
    conn.close()

    return render_template_string(
        tpl_base.BASE_TEMPLATE.replace('<!-- CONTENT_PLACEHOLDER -->', RESUMEN_TEMPLATE),
        active_page='resumen',
        system_date=utils.get_system_date(),
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        labels_ot=json.dumps(estados_ot_orden),
        values_ot=json.dumps(values_ot),
        labels_corr=json.dumps(estados_corr_orden),
        values_corr=json.dumps(values_corr),
        total_ots=total_ots,
        total_corr=total_corr
    )

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