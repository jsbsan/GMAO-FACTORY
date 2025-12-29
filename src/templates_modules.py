from flask import url_for

INVENTARIO_TEMPLATE = """
<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">Inventario de Equipos</h1>
    <div>
        <a href="{{ url_for('print_all_inventory', f_nombre=f_nombre, f_tipo=f_tipo) }}" class="btn btn-secondary btn-sm me-2" target="_blank"><i class="fas fa-print"></i> Imprimir Tabla</a>
        {% if session.get('perm_inventario') %}
        <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#addEquipModal">+ Nuevo Equipo</button>
        {% endif %}
    </div>
</div>
<div class="card mb-3"><div class="card-body py-3"><form action="{{ url_for('index') }}" method="GET" class="row g-2 align-items-end"><div class="col-md-4"><label class="form-label small mb-1">Nombre Equipo</label><input type="text" class="form-control form-control-sm" name="f_nombre" value="{{ f_nombre }}" placeholder="Buscar..."></div><div class="col-md-4"><label class="form-label small mb-1">Tipo</label><select class="form-select form-select-sm" name="f_tipo"><option value="">Todos</option>{% for t in tipos %}<option value="{{ t.id }}" {{ 'selected' if f_tipo|string == t.id|string }}>{{ t.nombre }}</option>{% endfor %}</select></div><div class="col-md-4 d-flex gap-2"><button type="submit" class="btn btn-primary btn-sm w-100"><i class="fas fa-filter"></i> Filtrar</button><a href="{{ url_for('index') }}" class="btn btn-outline-secondary btn-sm"><i class="fas fa-times"></i> Limpiar</a></div></form></div></div>
<div class="table-responsive"><table class="table table-striped table-hover"><thead class="table-dark"><tr><th>ID</th><th>Nombre</th><th>Tipo</th><th>Descripción</th><th>Archivos</th><th>Acciones</th></tr></thead><tbody>{% for item in items %}<tr><td>{{ item.id }}</td><td>{{ item.nombre }}</td><td>{{ item.tipo_nombre }}</td><td>{{ item.descripcion }}</td><td>{% set imgs = item.images|json_load %}{% if imgs %}<button class="btn btn-info btn-sm btn-xs" onclick="verGaleria('inventory', 'img', '{{ item.id }}')"><i class="fas fa-images"></i> {{ imgs|length }}</button>{% endif %}{% set pdfs = item.pdfs|json_load %}{% if pdfs %}<button class="btn btn-danger btn-sm btn-xs" onclick="verGaleria('inventory', 'pdf', '{{ item.id }}')"><i class="fas fa-file-pdf"></i> {{ pdfs|length }}</button>{% endif %}</td><td>
    <a href="{{ url_for('print_inventory', id=item.id) }}" class="btn btn-sm btn-secondary mb-1" target="_blank" title="Imprimir PDF"><i class="fas fa-print"></i></a> 
    {% if session.get('perm_inventario') %}
    <a href="{{ url_for('edit_inventory', id=item.id) }}" class="btn btn-sm btn-warning mb-1" title="Editar"><i class="fas fa-edit"></i></a>
    <button type="button" class="btn btn-sm btn-danger mb-1" data-bs-toggle="modal" data-bs-target="#deleteInventoryModal{{ item.id }}" title="Borrar"><i class="fas fa-trash"></i></button>
    <div class="modal fade" id="deleteInventoryModal{{ item.id }}" tabindex="-1" aria-hidden="true"><div class="modal-dialog"><div class="modal-content"><div class="modal-header bg-danger text-white"><h5 class="modal-title">Confirmar Borrado</h5><button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button></div><div class="modal-body text-start"><p>¿Estás seguro de que quieres borrar el equipo <strong>{{ item.nombre }}</strong>?</p><div class="alert alert-warning"><i class="fas fa-exclamation-triangle"></i> <strong>Atención:</strong> Esta acción borrará permanentemente todos sus datos asociados.</div></div><div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button><form action="{{ url_for('delete_inventory', id=item.id) }}" method="POST"><button type="submit" class="btn btn-danger">Sí, borrar todo</button></form></div></div></div></div>
    {% endif %}
</td></tr>{% endfor %}</tbody></table></div>
<nav><ul class="pagination justify-content-center">{% if page > 1 %}<li class="page-item"><a class="page-link" href="{{ url_for('index', page=page-1, f_nombre=f_nombre, f_tipo=f_tipo) }}">Anterior</a></li>{% endif %}<li class="page-item disabled"><span class="page-link">Página {{ page }}</span></li>{% if has_next %}<li class="page-item"><a class="page-link" href="{{ url_for('index', page=page+1, f_nombre=f_nombre, f_tipo=f_tipo) }}">Siguiente</a></li>{% endif %}</ul></nav>
<div class="modal fade" id="addEquipModal" tabindex="-1"><div class="modal-dialog modal-lg"><div class="modal-content"><form action="{{ url_for('add_inventory') }}" method="POST" enctype="multipart/form-data"><div class="modal-header"><h5 class="modal-title">Añadir Equipo</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><div class="mb-3"><label class="form-label">Nombre</label><input type="text" class="form-control" name="nombre" required></div><div class="mb-3"><label class="form-label">Tipo</label><select class="form-select" name="tipo_id" required>{% for t in tipos %}<option value="{{ t.id }}">{{ t.nombre }}</option>{% endfor %}</select></div><div class="mb-3"><label class="form-label">Descripción</label><textarea class="form-control" name="descripcion" rows="3"></textarea></div><div class="mb-3"><label class="form-label">Imágenes (Máx 5)</label><input type="file" class="form-control" name="images" multiple accept="image/*"></div><div class="mb-3"><label class="form-label">PDFs (Máx 5)</label><input type="file" class="form-control" name="pdfs" multiple accept="application/pdf"></div></div><div class="modal-footer"><button type="submit" class="btn btn-primary">Guardar</button></div></form></div></div></div>
<script>function verGaleria(source, tipo, id) {window.location.href = "/view_files/" + source + "/" + tipo + "/" + id;}</script>
"""

EDIT_INVENTORY_TEMPLATE = """
<h2>Editar Equipo: {{ item.nombre }}</h2>
<form action="{{ url_for('update_inventory', id=item.id) }}" method="POST" enctype="multipart/form-data" class="mt-4">
    <div class="row"><div class="col-md-7"><div class="mb-3"><label class="form-label">Nombre</label><input type="text" class="form-control" name="nombre" value="{{ item.nombre }}" required></div><div class="mb-3"><label class="form-label">Tipo</label><select class="form-select" name="tipo_id" required>{% for t in tipos %}<option value="{{ t.id }}" {{ 'selected' if t.id == item.tipo_id }}>{{ t.nombre }}</option>{% endfor %}</select></div><div class="mb-3"><label class="form-label">Descripción</label><textarea class="form-control" name="descripcion" rows="3">{{ item.descripcion }}</textarea></div></div><div class="col-md-5"><div class="card mb-3"><div class="card-header d-flex justify-content-between align-items-center"><span>Imágenes ({{ imgs|length }}/5)</span><small>Selecciona para borrar</small></div><div class="card-body">{% if imgs %}<div class="list-group mb-3">{% for img in imgs %}<div class="list-group-item d-flex justify-content-between align-items-center"><div class="text-truncate" style="max-width: 200px;">{{ img.name }}</div><div class="form-check"><input class="form-check-input" type="checkbox" name="delete_images" value="{{ loop.index0 }}"></div></div>{% endfor %}</div>{% endif %}{% if imgs|length < 5 %}<input type="file" class="form-control form-control-sm" name="images" multiple accept="image/*">{% endif %}</div></div><div class="card"><div class="card-header d-flex justify-content-between align-items-center"><span>PDFs ({{ pdfs|length }}/5)</span><small>Selecciona para borrar</small></div><div class="card-body">{% if pdfs %}<div class="list-group mb-3">{% for pdf in pdfs %}<div class="list-group-item d-flex justify-content-between align-items-center"><div class="text-truncate" style="max-width: 200px;">{{ pdf.name }}</div><div class="form-check"><input class="form-check-input" type="checkbox" name="delete_pdfs" value="{{ loop.index0 }}"></div></div>{% endfor %}</div>{% endif %}{% if pdfs|length < 5 %}<input type="file" class="form-control form-control-sm" name="pdfs" multiple accept="application/pdf">{% endif %}</div></div></div></div>
    <hr><div class="d-flex justify-content-end gap-2"><a href="{{ url_for('index') }}" class="btn btn-secondary">Cancelar</a><button type="submit" class="btn btn-primary">Guardar Cambios</button></div>
</form>
"""

ACTIVIDADES_TEMPLATE = """
<div class="d-flex justify-content-between align-items-center mb-4"><h1 class="h2">Gestión de Actividades</h1><div>{% if session.get('perm_actividades') %}<button class="btn btn-primary btn-sm me-2" type="button" data-bs-toggle="collapse" data-bs-target="#formNuevaActividad"><i class="fas fa-plus"></i> Nueva Actividad</button>{% endif %}<a href="{{ url_for('print_all_activities') }}" class="btn btn-secondary btn-sm" target="_blank"><i class="fas fa-print"></i> Imprimir Tabla</a></div></div>
<div class="collapse mb-4" id="formNuevaActividad"><div class="card card-body bg-light"><h5 class="card-title mb-3">Registrar Nueva Actividad</h5><form action="{{ url_for('add_activity') }}" method="POST" class="row g-3"><div class="col-md-4"><label class="form-label">Nombre Actividad</label><input type="text" class="form-control" name="nombre" required></div><div class="col-md-4"><label class="form-label">Equipo Asociado</label><select class="form-select" name="equipo_id" required>{% for eq in equipos %}<option value="{{ eq.id }}">{{ eq.nombre }} ({{ eq.tipo_nombre }})</option>{% endfor %}</select></div><div class="col-md-2"><label class="form-label">Periodicidad (días)</label><input type="number" class="form-control" name="periodicidad" required min="1"></div><div class="col-md-2"><label class="form-label">Inicio Generación</label><input type="date" class="form-control" name="fecha_inicio" required></div><div class="col-12"><label class="form-label">Operaciones a realizar</label><textarea class="form-control" name="operaciones" rows="2" required></textarea></div><div class="col-12 text-end"><button type="button" class="btn btn-secondary me-2" data-bs-toggle="collapse" data-bs-target="#formNuevaActividad">Cancelar</button><button type="submit" class="btn btn-success">Crear Actividad</button></div></form></div></div>
<div class="card mb-3"><div class="card-body py-3"><form action="{{ url_for('activities') }}" method="GET" class="row g-2 align-items-end"><div class="col-md-3"><label class="form-label small mb-1">Nombre</label><input type="text" class="form-control form-control-sm" name="f_nombre" value="{{ f_nombre }}" placeholder="Buscar..."></div><div class="col-md-3"><label class="form-label small mb-1">Equipo</label><select class="form-select form-select-sm" name="f_equipo"><option value="">Todos</option>{% for eq in equipos %}<option value="{{ eq.id }}" {{ 'selected' if f_equipo|string == eq.id|string }}>{{ eq.nombre }}</option>{% endfor %}</select></div><div class="col-md-2"><label class="form-label small mb-1">Frecuencia</label><input type="number" class="form-control form-control-sm" name="f_periodicidad" value="{{ f_periodicidad }}"></div><div class="col-md-4 d-flex gap-2"><button type="submit" class="btn btn-primary btn-sm w-100"><i class="fas fa-filter"></i> Filtrar</button><a href="{{ url_for('activities') }}" class="btn btn-outline-secondary btn-sm"><i class="fas fa-times"></i> Limpiar</a></div></form></div></div>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-light"><tr><th>Actividad</th><th>Equipo</th><th>Frecuencia</th><th>Inicio</th><th>Operaciones</th><th>Acciones</th></tr></thead><tbody>{% for act in actividades %}<tr><td>{{ act.nombre }}</td><td>{{ act.equipo_nombre }}</td><td>Cada {{ act.periodicidad }} días</td><td>{{ act.fecha_inicio_gen }}</td><td><small>{{ act.operaciones }}</small></td><td>
    <a href="{{ url_for('print_activity_single', id=act.id) }}" class="btn btn-sm btn-secondary mb-1" target="_blank" title="Imprimir PDF"><i class="fas fa-print"></i></a> 
    {% if session.get('perm_actividades') %}
    <a href="{{ url_for('edit_activity', id=act.id) }}" class="btn btn-sm btn-warning mb-1"><i class="fas fa-edit"></i></a>
    <button type="button" class="btn btn-sm btn-danger mb-1" data-bs-toggle="modal" data-bs-target="#deleteActivityModal{{ act.id }}"><i class="fas fa-trash"></i></button>
    <div class="modal fade" id="deleteActivityModal{{ act.id }}" tabindex="-1" aria-labelledby="deleteActivityLabel{{ act.id }}" aria-hidden="true"><div class="modal-dialog"><div class="modal-content"><div class="modal-header bg-danger text-white"><h5 class="modal-title" id="deleteActivityLabel{{ act.id }}">Confirmar Borrado</h5><button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button></div><div class="modal-body text-start"><p>¿Estás seguro de que quieres borrar la actividad <strong>{{ act.nombre }}</strong>?</p><div class="alert alert-warning"><i class="fas fa-exclamation-triangle"></i> <strong>Atención:</strong> Esta acción borrará también todas las <strong>Órdenes de Trabajo</strong> vinculadas a esta actividad. Esta acción no se puede deshacer.</div></div><div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button><form action="{{ url_for('delete_activity', id=act.id) }}" method="POST"><button type="submit" class="btn btn-danger">Sí, borrar todo</button></form></div></div></div></div>
    {% endif %}
</td></tr>{% endfor %}</tbody></table></div>
"""

EDIT_ACTIVITY_TEMPLATE = """
<h2>Editar Actividad: {{ activity.nombre }}</h2>
<form action="{{ url_for('update_activity', id=activity.id) }}" method="POST" class="row g-3 mt-4">
    <div class="col-md-4"><label class="form-label">Nombre</label><input type="text" class="form-control" name="nombre" value="{{ activity.nombre }}" required></div><div class="col-md-4"><label class="form-label">Equipo</label><select class="form-select" name="equipo_id" required>{% for eq in equipos %}<option value="{{ eq.id }}" {{ 'selected' if eq.id == activity.equipo_id }}>{{ eq.nombre }}</option>{% endfor %}</select></div><div class="col-md-2"><label class="form-label">Periodicidad</label><input type="number" class="form-control" name="periodicidad" value="{{ activity.periodicidad }}" required></div><div class="col-md-2"><label class="form-label">Inicio</label><input type="date" class="form-control" name="fecha_inicio" value="{{ activity.fecha_inicio_gen }}" required></div><div class="col-12"><label class="form-label">Operaciones</label><textarea class="form-control" name="operaciones" rows="2" required>{{ activity.operaciones }}</textarea></div><div class="col-12 d-flex justify-content-end gap-2"><a href="{{ url_for('activities') }}" class="btn btn-secondary">Cancelar</a><button type="submit" class="btn btn-primary">Guardar</button></div>
</form>
"""

OTS_TEMPLATE = """
<div class="d-flex justify-content-between align-items-center mb-4"><h1 class="h2">Órdenes de Trabajo</h1><div class="d-flex gap-2"><a href="{{ url_for('print_all_ots', estado=estado_filter, fecha_inicio=fecha_inicio_filter, fecha_fin=fecha_fin_filter) }}" class="btn btn-secondary" target="_blank"><i class="fas fa-print"></i> Imprimir Tabla</a><form action="{{ url_for('generate_work_orders') }}" method="POST"><button type="submit" class="btn btn-warning"><i class="fas fa-sync-alt"></i> Generar OTs</button></form></div></div>
<div class="card mb-3"><div class="card-body"><form action="{{ url_for('work_orders') }}" method="GET" class="row g-3 align-items-end"><div class="col-md-3"><label class="form-label">Estado</label><select class="form-select" name="estado"><option value="">Todos</option><option value="En curso" {{ 'selected' if estado_filter == 'En curso' }}>En curso</option><option value="Pendiente" {{ 'selected' if estado_filter == 'Pendiente' }}>Pendiente</option><option value="Prevista" {{ 'selected' if estado_filter == 'Prevista' }}>Prevista</option><option value="Realizada" {{ 'selected' if estado_filter == 'Realizada' }}>Realizada</option><option value="Rechazada" {{ 'selected' if estado_filter == 'Rechazada' }}>Rechazada</option></select></div><div class="col-md-3"><label class="form-label">Desde</label><input type="date" class="form-control" name="fecha_inicio" value="{{ fecha_inicio_filter }}"></div><div class="col-md-3"><label class="form-label">Hasta</label><input type="date" class="form-control" name="fecha_fin" value="{{ fecha_fin_filter }}"></div><div class="col-md-3"><button type="submit" class="btn btn-primary w-100"><i class="fas fa-filter"></i> Filtrar</button></div></form></div></div>
<div class="table-responsive"><table class="table table-hover align-middle"><thead class="table-dark"><tr><th>ID</th><th>Nombre OT</th><th>Equipo</th><th>Fecha Gen.</th><th>Estado</th><th>Acciones</th></tr></thead><tbody>{% for ot in ots %}<tr><td>{{ ot.id }}</td><td>{{ ot.nombre }}</td><td>{{ ot.equipo_nombre }}</td><td>{{ ot.fecha_generacion }}</td><td>{% if ot.estado == 'Realizada' %}<span class="badge bg-success">Realizada</span>{% elif ot.estado == 'En curso' %}<span class="badge bg-warning text-dark">En curso</span>{% elif ot.estado == 'Pendiente' %}<span class="badge bg-danger">Pendiente</span>{% elif ot.estado == 'Prevista' %}<span class="badge bg-secondary">Prevista</span>{% else %}<span class="badge bg-dark">Rechazada</span>{% endif %}</td><td><a href="{{ url_for('print_ot', id=ot.id) }}" class="btn btn-sm btn-secondary" target="_blank"><i class="fas fa-print"></i></a> <button class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#modalOT{{ ot.id }}">Gestionar</button></td></tr>
<div class="modal fade" id="modalOT{{ ot.id }}" tabindex="-1"><div class="modal-dialog"><div class="modal-content"><form action="{{ url_for('update_ot', id=ot.id) }}" method="POST"><div class="modal-header"><h5 class="modal-title">{{ ot.nombre }}</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><div class="alert alert-secondary"><strong>Operaciones:</strong><br>{{ ot.operaciones }}</div><div class="mb-3"><label class="form-label">Estado</label><select class="form-select" name="estado"><option value="En curso" {{ 'selected' if ot.estado == 'En curso' }}>En curso</option><option value="Pendiente" {{ 'selected' if ot.estado == 'Pendiente' }}>Pendiente</option><option value="Prevista" {{ 'selected' if ot.estado == 'Prevista' }}>Prevista</option><option value="Realizada" {{ 'selected' if ot.estado == 'Realizada' }}>Realizada</option><option value="Rechazada" {{ 'selected' if ot.estado == 'Rechazada' }}>Rechazada</option></select></div><div class="mb-3"><label class="form-label">Observaciones</label><textarea class="form-control" name="observaciones">{{ ot.observaciones }}</textarea></div><div class="mb-3"><label class="form-label">Fecha Realización</label><input type="date" class="form-control" name="fecha_realizada" value="{{ ot.fecha_realizada }}"></div></div><div class="modal-footer"><button type="submit" class="btn btn-primary">Actualizar OT</button></div></form></div></div></div>{% endfor %}</tbody></table></div>
<nav><ul class="pagination justify-content-center">{% if page > 1 %}<li class="page-item"><a class="page-link" href="{{ url_for('work_orders', page=page-1, estado=estado_filter, fecha_inicio=fecha_inicio_filter, fecha_fin=fecha_fin_filter) }}">Anterior</a></li>{% endif %}<li class="page-item disabled"><span class="page-link">Página {{ page }}</span></li>{% if has_next %}<li class="page-item"><a class="page-link" href="{{ url_for('work_orders', page=page+1, estado=estado_filter, fecha_inicio=fecha_inicio_filter, fecha_fin=fecha_fin_filter) }}">Siguiente</a></li>{% endif %}</ul></nav>
"""

CRONOGRAMA_TEMPLATE = """
<div class="d-flex justify-content-between align-items-center mb-4"><h1 class="h2">Cronogramas de Ordenes de Trabajo {{ year }}</h1><div class="d-flex align-items-center gap-3"><form action="{{ url_for('cronograma') }}" method="GET" class="d-flex align-items-center"><label for="yearSelect" class="me-2 fw-bold">Año:</label><input type="number" id="yearSelect" name="year" class="form-control" value="{{ year }}" style="width: 100px;" onchange="this.form.submit()"><button type="submit" class="btn btn-primary btn-sm ms-2">Ir</button></form><a href="{{ url_for('print_cronograma', year=year) }}" target="_blank" class="btn btn-secondary"><i class="fas fa-print"></i> Imprimir PDF</a></div></div>
<div class="table-responsive"><table class="table table-bordered table-sm text-center"><thead class="table-dark"><tr><th style="width: 200px;">Actividad / Equipo</th>{% for m in meses %}<th>{{ m }}</th>{% endfor %}</tr></thead><tbody>{% for row in data %}<tr><td class="text-start bg-light fw-bold">{{ row.actividad }}<br><small class="text-muted">{{ row.equipo }}</small></td>{% for month_idx in range(1, 13) %}<td style="vertical-align: top;">{% if month_idx in row.ots %}{% for ot in row.ots[month_idx] %}<div class="badge-status {% if ot.estado == 'Realizada' %}status-realizada{% elif ot.estado == 'En curso' %}status-en-curso{% elif ot.estado == 'Pendiente' %}status-pendiente{% elif ot.estado == 'Prevista' %}status-prevista{% else %}status-rechazada{% endif %}" title="{{ ot.nombre }} ({{ ot.fecha }})" data-bs-toggle="modal" data-bs-target="#cronModalOT{{ ot.id }}">{{ ot.day_day }}</div><div class="modal fade text-start" id="cronModalOT{{ ot.id }}" tabindex="-1"><div class="modal-dialog"><div class="modal-content"><form action="{{ url_for('update_ot', id=ot.id) }}" method="POST"><div class="modal-header"><h5 class="modal-title">{{ ot.nombre }}</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><input type="hidden" name="redirect_to" value="cronograma"><div class="alert alert-secondary"><strong>Operaciones:</strong><br>{{ ot.operaciones }}</div><div class="mb-3"><label class="form-label">Estado</label><select class="form-select" name="estado"><option value="En curso" {{ 'selected' if ot.estado == 'En curso' }}>En curso</option><option value="Pendiente" {{ 'selected' if ot.estado == 'Pendiente' }}>Pendiente</option><option value="Prevista" {{ 'selected' if ot.estado == 'Prevista' }}>Prevista</option><option value="Realizada" {{ 'selected' if ot.estado == 'Realizada' }}>Realizada</option><option value="Rechazada" {{ 'selected' if ot.estado == 'Rechazada' }}>Rechazada</option></select></div><div class="mb-3"><label class="form-label">Observaciones</label><textarea class="form-control" name="observaciones">{{ ot.observaciones or '' }}</textarea></div><div class="mb-3"><label class="form-label">Fecha Realización</label><input type="date" class="form-control" name="fecha_realizada" value="{{ ot.fecha_realizada or '' }}"></div></div><div class="modal-footer"><button type="submit" class="btn btn-primary">Actualizar OT</button></div></form></div></div></div>{% endfor %}{% endif %}</td>{% endfor %}</tr>{% endfor %}</tbody></table></div>
<div class="mt-3"><small>Leyenda: <span class="badge bg-success">Realizada</span> <span class="badge bg-warning text-dark">En Curso</span> <span class="badge bg-danger">Pendiente</span> <span class="badge bg-secondary">Prevista</span> <span class="badge bg-dark">Rechazada</span>. El número indica el día del mes. Haz click para editar.</small></div>
"""

CORRECTIVOS_TEMPLATE = """
<div class="d-flex justify-content-between align-items-center mb-4"><h1 class="h2">Correctivos e Incidencias</h1><div><button class="btn btn-primary btn-sm me-2" type="button" data-bs-toggle="collapse" data-bs-target="#formNuevoCorrectivo"><i class="fas fa-plus"></i> Nueva Incidencia</button><a href="{{ url_for('print_all_correctivos', f_nombre=f_nombre, f_equipo=f_equipo, f_estado=f_estado, f_fecha_desde=f_fecha_desde, f_fecha_hasta=f_fecha_hasta) }}" class="btn btn-secondary btn-sm" target="_blank"><i class="fas fa-print"></i> Imprimir Tabla</a></div></div>
<div class="collapse mb-4" id="formNuevoCorrectivo"><div class="card card-body bg-light"><h5 class="card-title mb-3">Registrar Nueva Incidencia</h5><form action="{{ url_for('add_correctivo') }}" method="POST" enctype="multipart/form-data" class="row g-3"><div class="col-md-6"><label class="form-label">Nombre del Correctivo</label><input type="text" class="form-control" name="nombre" required></div><div class="col-md-6"><label class="form-label">Equipo Afectado</label><select class="form-select" name="equipo_id" required>{% for eq in equipos %}<option value="{{ eq.id }}">{{ eq.nombre }} ({{ eq.tipo_nombre }})</option>{% endfor %}</select></div><div class="col-12"><label class="form-label">Comentario</label><textarea class="form-control" name="comentario" rows="2"></textarea></div><div class="col-md-3"><label class="form-label">Fecha Detectada</label><input type="date" class="form-control" name="fecha_detectada" value="{{ system_date }}" required></div><div class="col-md-3"><label class="form-label">Estado Inicial</label><select class="form-select" name="estado"><option value="Detectada">Detectada</option><option value="En curso">En curso</option><option value="Resuelta">Resuelta</option></select></div><div class="col-md-3"><label class="form-label">Imágenes</label><input type="file" class="form-control" name="images" multiple accept="image/*"></div><div class="col-md-3"><label class="form-label">PDFs</label><input type="file" class="form-control" name="pdfs" multiple accept="application/pdf"></div><div class="col-12 text-end"><button type="button" class="btn btn-secondary me-2" data-bs-toggle="collapse" data-bs-target="#formNuevoCorrectivo">Cancelar</button><button type="submit" class="btn btn-danger">Guardar Incidencia</button></div></form></div></div>
<div class="card mb-3"><div class="card-body py-3"><form action="{{ url_for('correctivos') }}" method="GET" class="row g-2 align-items-end"><div class="col-md-3"><label class="form-label small mb-1">Nombre</label><input type="text" class="form-control form-control-sm" name="f_nombre" value="{{ f_nombre }}" placeholder="Buscar..."></div><div class="col-md-2"><label class="form-label small mb-1">Equipo</label><select class="form-select form-select-sm" name="f_equipo"><option value="">Todos</option>{% for eq in equipos %}<option value="{{ eq.id }}" {{ 'selected' if f_equipo|string == eq.id|string }}>{{ eq.nombre }}</option>{% endfor %}</select></div><div class="col-md-2"><label class="form-label small mb-1">Estado</label><select class="form-select form-select-sm" name="f_estado"><option value="">Todos</option><option value="Detectada" {{ 'selected' if f_estado == 'Detectada' }}>Detectada</option><option value="En curso" {{ 'selected' if f_estado == 'En curso' }}>En curso</option><option value="Resuelta" {{ 'selected' if f_estado == 'Resuelta' }}>Resuelta</option></select></div><div class="col-md-2"><label class="form-label small mb-1">Desde</label><input type="date" class="form-control form-control-sm" name="f_fecha_desde" value="{{ f_fecha_desde }}"></div><div class="col-md-2 d-flex gap-2"><button type="submit" class="btn btn-primary btn-sm w-100"><i class="fas fa-filter"></i></button><a href="{{ url_for('correctivos') }}" class="btn btn-outline-secondary btn-sm"><i class="fas fa-times"></i></a></div></form></div></div>
<div class="table-responsive"><table class="table table-hover align-middle"><thead class="table-dark"><tr><th>ID</th><th>Incidencia</th><th>Equipo</th><th>Estado</th><th>Detectada</th><th>Resolución</th><th>Archivos</th><th>Acciones</th></tr></thead><tbody>{% for c in correctivos %}<tr><td>{{ c.id }}</td><td>{{ c.nombre }}</td><td>{{ c.equipo_nombre }}</td><td>{% if c.estado == 'Detectada' %}<span class="badge corr-detectada">Detectada</span>{% elif c.estado == 'En curso' %}<span class="badge corr-en-curso">En curso</span>{% elif c.estado == 'Resuelta' %}<span class="badge corr-resuelta">Resuelta</span>{% endif %}</td><td>{{ c.fecha_detectada }}</td><td>{{ c.fecha_resolucion or '-' }}</td><td>{% set imgs = c.images|json_load %}{% set pdfs = c.pdfs|json_load %}{% if imgs or pdfs %}<span class="badge bg-secondary">{{ imgs|length }} <i class="fas fa-image"></i></span> <span class="badge bg-secondary">{{ pdfs|length }} <i class="fas fa-file-pdf"></i></span>{% else %}-{% endif %}</td><td><a href="{{ url_for('print_correctivo', id=c.id) }}" class="btn btn-sm btn-secondary" target="_blank"><i class="fas fa-print"></i></a> <a href="{{ url_for('edit_correctivo', id=c.id) }}" class="btn btn-sm btn-warning"><i class="fas fa-edit"></i></a> <form action="{{ url_for('delete_correctivo', id=c.id) }}" method="POST" class="d-inline" onsubmit="return confirm('¿Borrar?');"><button type="submit" class="btn btn-sm btn-danger"><i class="fas fa-trash"></i></button></form></td></tr>{% endfor %}</tbody></table></div>
<script>function verGaleria(source, tipo, id) {window.location.href = "/view_files/" + source + "/" + tipo + "/" + id;}</script>
"""

EDIT_CORRECTIVO_TEMPLATE = """
<h2>Editar Incidencia: {{ item.nombre }}</h2>
<form action="{{ url_for('update_correctivo', id=item.id) }}" method="POST" enctype="multipart/form-data" class="mt-4"><div class="row"><div class="col-md-6"><div class="mb-3"><label class="form-label">Nombre</label><input type="text" class="form-control" name="nombre" value="{{ item.nombre }}" required></div><div class="mb-3"><label class="form-label">Equipo</label><select class="form-select" name="equipo_id" required>{% for eq in equipos %}<option value="{{ eq.id }}" {{ 'selected' if eq.id == item.equipo_id }}>{{ eq.nombre }}</option>{% endfor %}</select></div><div class="mb-3"><label class="form-label">Comentario</label><textarea class="form-control" name="comentario" rows="3">{{ item.comentario }}</textarea></div><div class="mb-3"><label class="form-label">Solución</label><textarea class="form-control" name="solucion" rows="3">{{ item.solucion }}</textarea></div></div><div class="col-md-6"><div class="row"><div class="col-md-6 mb-3"><label class="form-label">Fecha Detectada</label><input type="date" class="form-control" name="fecha_detectada" value="{{ item.fecha_detectada }}" required></div><div class="col-md-6 mb-3"><label class="form-label">Fecha Resolución</label><input type="date" class="form-control" name="fecha_resolucion" value="{{ item.fecha_resolucion or '' }}"></div><div class="col-12 mb-3"><label class="form-label">Estado</label><select class="form-select" name="estado"><option value="Detectada" {{ 'selected' if item.estado == 'Detectada' }}>Detectada</option><option value="En curso" {{ 'selected' if item.estado == 'En curso' }}>En curso</option><option value="Resuelta" {{ 'selected' if item.estado == 'Resuelta' }}>Resuelta</option></select></div></div><div class="card mb-3"><div class="card-header d-flex justify-content-between align-items-center"><span>Imágenes ({{ imgs|length }}/5)</span><small class="text-muted">Selecciona para borrar</small></div><div class="card-body">{% if imgs %}<div class="list-group mb-2">{% for img in imgs %}<div class="list-group-item d-flex justify-content-between align-items-center p-1"><small class="text-truncate" style="max-width: 200px;">{{ img.name }}</small> <input class="form-check-input" type="checkbox" name="delete_images" value="{{ loop.index0 }}"></div>{% endfor %}</div>{% endif %}{% if imgs|length < 5 %}<input type="file" class="form-control form-control-sm" name="images" multiple accept="image/*">{% endif %}</div></div><div class="card"><div class="card-header d-flex justify-content-between align-items-center"><span>PDFs ({{ pdfs|length }}/5)</span><small class="text-muted">Selecciona para borrar</small></div><div class="card-body">{% if pdfs %}<div class="list-group mb-2">{% for pdf in pdfs %}<div class="list-group-item d-flex justify-content-between align-items-center p-1"><small class="text-truncate" style="max-width: 200px;">{{ pdf.name }}</small> <input class="form-check-input" type="checkbox" name="delete_pdfs" value="{{ loop.index0 }}"></div>{% endfor %}</div>{% endif %}{% if pdfs|length < 5 %}<input type="file" class="form-control form-control-sm" name="pdfs" multiple accept="application/pdf">{% endif %}</div></div></div></div><hr><div class="d-flex justify-content-end gap-2"><a href="{{ url_for('correctivos') }}" class="btn btn-secondary">Cancelar</a><button type="submit" class="btn btn-primary">Guardar Cambios</button></div></form>
"""

GENERAL_SETTINGS_TEMPLATE = """
<h1 class="h2 mb-4">Configuración Global</h1>

<div class="row">
    <div class="col-md-6">
        <div class="card mb-4">
            <div class="card-header bg-light"><h5 class="mb-0"><i class="fas fa-clock me-2"></i> Fecha del Sistema</h5></div>
            <div class="card-body">
                <p>Define la fecha con la que opera el sistema para simulaciones o ajustes temporales.</p>
                <form action="{{ url_for('update_system_date') }}" method="POST">
                    <div class="mb-3"><label class="form-label">Fecha Actual del Sistema</label><input type="date" class="form-control" name="fecha_sistema" value="{{ system_date }}" required><div class="form-text">Todas las operaciones automáticas usarán esta fecha.</div></div>
                    <button type="submit" class="btn btn-primary">Actualizar Fecha</button>
                </form>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header bg-light"><h5 class="mb-0"><i class="fas fa-calendar-plus me-2"></i> Planificación Futura</h5></div>
            <div class="card-body">
                <p>Generar órdenes de trabajo "Previstas" (Grises) desde mañana hasta una fecha futura.</p>
                <form action="{{ url_for('update_planned_date') }}" method="POST">
                    <div class="mb-3">
                        <label class="form-label">Fecha Prevista (Límite)</label>
                        <input type="date" class="form-control" name="fecha_prevista" value="{{ planned_date or '' }}" required>
                        <div class="form-text">Debe ser posterior a la fecha del sistema.</div>
                    </div>
                    <button type="submit" class="btn btn-success">Actualizar y Generar</button>
                </form>
            </div>
        </div>
    </div>
    
    <div class="col-md-6">
        <div class="card mb-4">
            <div class="card-header bg-light"><h5 class="mb-0"><i class="fas fa-file-alt me-2"></i> Registro de Actividad (Logging)</h5></div>
            <div class="card-body">
                <p>Activa el sistema de logging para registrar operaciones críticas.</p>
                <form action="{{ url_for('toggle_logging') }}" method="POST" class="mb-3">
                    <div class="form-check form-switch mb-3"><input class="form-check-input" type="checkbox" role="switch" id="loggingSwitch" name="logging_enabled" onchange="this.form.submit()" {{ 'checked' if logging_enabled else '' }}><label class="form-check-label" for="loggingSwitch"><strong>{{ 'Sistema de Logging ACTIVADO' if logging_enabled else 'Sistema de Logging DESACTIVADO' }}</strong></label></div>
                </form>
                <div class="d-flex justify-content-between align-items-center p-3 border rounded bg-light">
                    <div><strong>Archivo:</strong> <code>gmao_app.log</code><br><small class="text-muted">Tamaño: {{ log_size }}</small></div>
                    <a href="{{ url_for('download_log') }}" class="btn btn-primary {{ 'disabled' if log_size == '0 KB' else '' }}"><i class="fas fa-download me-2"></i> Descargar</a>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header bg-light d-flex justify-content-between align-items-center">
                <h5 class="mb-0"><i class="fas fa-users-cog me-2"></i> Gestión de Usuarios</h5>
                <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#addUserModal">+ Nuevo Usuario</button>
            </div>
            <div class="card-body p-0">
                <table class="table table-striped table-hover mb-0">
                    <thead><tr><th>Usuario</th><th>Rol</th><th>Acciones</th></tr></thead>
                    <tbody>
                        {% for user in users %}
                        <tr>
                            <td>{{ user.username }}</td>
                            <td>{{ user.rol }}</td>
                            <td>
                                <button class="btn btn-sm btn-warning" data-bs-toggle="modal" data-bs-target="#editUserModal{{ user.id }}"><i class="fas fa-edit"></i></button>
                                {% if user.username != 'Administrador' %}
                                <form action="{{ url_for('delete_user', id=user.id) }}" method="POST" class="d-inline" onsubmit="return confirm('¿Borrar usuario?');">
                                    <button type="submit" class="btn btn-sm btn-danger"><i class="fas fa-trash"></i></button>
                                </form>
                                {% endif %}
                                
                                <!-- Edit Modal -->
                                <div class="modal fade" id="editUserModal{{ user.id }}" tabindex="-1">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <form action="{{ url_for('edit_user', id=user.id) }}" method="POST">
                                                <div class="modal-header"><h5 class="modal-title">Editar Usuario</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
                                                <div class="modal-body">
                                                    <div class="mb-3"><label class="form-label">Contraseña (dejar en blanco para no cambiar)</label><input type="password" class="form-control" name="password"></div>
                                                    <div class="mb-3"><label class="form-label">Rol</label><input type="text" class="form-control" name="rol" value="{{ user.rol }}"></div>
                                                    <h6>Permisos</h6>
                                                    <div class="form-check"><input class="form-check-input" type="checkbox" name="perm_inventario" {{ 'checked' if user.perm_inventario else '' }}><label class="form-check-label">Inventario</label></div>
                                                    <div class="form-check"><input class="form-check-input" type="checkbox" name="perm_actividades" {{ 'checked' if user.perm_actividades else '' }}><label class="form-check-label">Actividades</label></div>
                                                    <div class="form-check"><input class="form-check-input" type="checkbox" name="perm_configuracion" {{ 'checked' if user.perm_configuracion else '' }}><label class="form-check-label">Configuración Global</label></div>
                                                </div>
                                                <div class="modal-footer"><button type="submit" class="btn btn-primary">Guardar Cambios</button></div>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center"><span><i class="fas fa-tags me-2"></i> Gestión de Tipos de Equipo</span><button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#addTypeConfigModal">+ Nuevo Tipo</button></div>
            <div class="card-body p-0">
                <table class="table table-striped table-hover mb-0"><thead class="table-light"><tr><th>ID</th><th>Nombre</th><th>Acciones</th></tr></thead><tbody>
                    {% for tipo in tipos %}
                    <tr><td>{{ tipo.id }}</td><td>{{ tipo.nombre }}</td><td><a href="{{ url_for('edit_type', id=tipo.id) }}" class="btn btn-sm btn-outline-primary">Editar</a></td></tr>
                    {% else %}
                    <tr><td colspan="3" class="text-center">No hay tipos definidos.</td></tr>
                    {% endfor %}
                </tbody></table>
            </div>
        </div>
    </div>
</div>

<!-- Modal Add User -->
<div class="modal fade" id="addUserModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <form action="{{ url_for('add_user') }}" method="POST">
                <div class="modal-header"><h5 class="modal-title">Nuevo Usuario</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
                <div class="modal-body">
                    <div class="mb-3"><label class="form-label">Usuario</label><input type="text" class="form-control" name="username" required></div>
                    <div class="mb-3"><label class="form-label">Contraseña</label><input type="password" class="form-control" name="password" required></div>
                    <div class="mb-3"><label class="form-label">Rol</label><input type="text" class="form-control" name="rol" value="Usuario"></div>
                    <h6>Permisos</h6>
                    <div class="form-check"><input class="form-check-input" type="checkbox" name="perm_inventario"><label class="form-check-label">Inventario</label></div>
                    <div class="form-check"><input class="form-check-input" type="checkbox" name="perm_actividades"><label class="form-check-label">Actividades</label></div>
                    <div class="form-check"><input class="form-check-input" type="checkbox" name="perm_configuracion"><label class="form-check-label">Configuración Global</label></div>
                </div>
                <div class="modal-footer"><button type="submit" class="btn btn-primary">Crear</button></div>
            </form>
        </div>
    </div>
</div>

<div class="modal fade" id="addTypeConfigModal" tabindex="-1"><div class="modal-dialog"><div class="modal-content"><form action="{{ url_for('add_type_config') }}" method="POST"><div class="modal-header"><h5 class="modal-title">Nuevo Tipo de Equipo</h5></div><div class="modal-body"><input type="text" class="form-control" name="nombre" placeholder="Ej: Vehículos" required></div><div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button><button type="submit" class="btn btn-primary">Guardar</button></div></form></div></div></div>
"""

VIEWER_TEMPLATE = """
<div class="mb-3"><a href="{{ back_url }}" class="btn btn-secondary">&larr; Volver</a><h3>{{ title_prefix }}: {{ item.nombre }}</h3></div>
<div class="row">
    {% if tipo == 'img' %}{% for file in files %}<div class="col-md-6 mb-4"><div class="card"><img src="data:image/png;base64,{{ file.data }}" class="card-img-top"><div class="card-footer text-muted">{{ file.name }}</div></div></div>{% endfor %}
    {% elif tipo == 'pdf' %}{% for file in files %}<div class="col-12 mb-5"><div class="card h-100"><div class="card-header">{{ file.name }}</div><div class="card-body p-0" style="height: 600px;"><embed src="data:application/pdf;base64,{{ file.data }}" type="application/pdf" width="100%" height="100%"></div></div></div>{% endfor %}
    {% endif %}
</div>
{% if not files %}<div class="alert alert-warning">No hay archivos.</div>{% endif %}
"""
ABOUT_TEMPLATE = """
<div class="container mt-5">
    <div class="card shadow-sm">
        <div class="card-header bg-dark text-white">
            <h3 class="mb-0"><i class="fas fa-info-circle me-2"></i> Acerca de...</h3>
        </div>
        <div class="card-body p-5 text-center">
            <h1 class="display-4 mb-4">GMAO Factory</h1>
            <hr class="w-50 mx-auto mb-4">
            
            <div class="row justify-content-center">
                <div class="col-md-8 text-start">
                    <dl class="row font-monospace fs-5">
                        <dt class="col-sm-4 text-end">Programa:</dt>
                        <dd class="col-sm-8">Sistema de Gestión de Mantenimiento Asistido por Ordenador</dd>

                        <dt class="col-sm-4 text-end">Versión:</dt>
                        <dd class="col-sm-8"><span class="badge bg-primary">v5.0</span></dd>

                        <dt class="col-sm-4 text-end">Autor:</dt>
                        <dd class="col-sm-8">Julio Sánchez Berro</dd>
                        
                        <dt class="col-sm-4 text-end">Licencia:</dt>
                        <dd class="col-sm-8">Uso Interno / Privado</dd>
                    </dl>
                </div>
            </div>
            
            <div class="mt-5">
                <p class="text-muted">Gestión integral de activos, planes de mantenimiento preventivo y control de incidencias.</p>
                <small class="text-muted"> Sevilla, España &copy; {{ system_date.year }}</small>
            </div>
        </div>
    </div>
</div>
"""
PRINT_TEMPLATE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Reporte</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><style>@media print {.no-print {display:none;}} img {max-width:100%;}</style></head><body onload="window.print()"><div class="container"><h1>Ficha Técnica</h1><div class="card mb-3"><div class="card-body"><strong>Nombre:</strong> {{ item.nombre }}<br><strong>Tipo:</strong> {{ item.tipo_nombre }}<br><strong>Desc:</strong> {{ item.descripcion }}</div></div><h3>Imágenes</h3><div class="row">{% for img in imgs %}<div class="col-6 mb-3"><img src="data:image/png;base64,{{ img.data }}"><br><small>{{ img.name }}</small></div>{% endfor %}</div><h3>PDFs</h3><ul>{% for pdf in pdfs %}<li>{{ pdf.name }}</li>{% endfor %}</ul></div></body></html>"""
PRINT_ALL_TEMPLATE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Listado</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><style>@media print {.no-print {display:none;}} table{width:100%;border-collapse:collapse;} th,td{border:1px solid #ddd;padding:8px;}</style></head><body onload="window.print()"><div class="container"><h2>Listado Inventario</h2><table class="table"><thead><tr><th>ID</th><th>Nombre</th><th>Tipo</th><th>Desc</th></tr></thead><tbody>{% for i in items %}<tr><td>{{ i.id }}</td><td>{{ i.nombre }}</td><td>{{ i.tipo_nombre }}</td><td>{{ i.descripcion }}</td></tr>{% endfor %}</tbody></table></div></body></html>"""
PRINT_ACTIVITY_TEMPLATE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Actividad</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><style>@media print {.no-print {display:none;}}</style></head><body onload="window.print()"><div class="container"><h1>Actividad: {{ activity.nombre }}</h1><p>Equipo: {{ activity.equipo_nombre }}</p><p>Periodicidad: {{ activity.periodicidad }}</p><p>Operaciones: {{ activity.operaciones }}</p></div></body></html>"""
PRINT_ALL_ACTIVITIES_TEMPLATE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Actividades</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><style>@media print {.no-print {display:none;}} table{width:100%;border:1px solid #ddd;} th,td{border:1px solid #ddd;padding:5px;}</style></head><body onload="window.print()"><div class="container"><h2>Listado Actividades</h2><table><thead><tr><th>Actividad</th><th>Equipo</th><th>Freq</th><th>Ops</th></tr></thead><tbody>{% for a in activities %}<tr><td>{{ a.nombre }}</td><td>{{ a.equipo_nombre }}</td><td>{{ a.periodicidad }}</td><td>{{ a.operaciones }}</td></tr>{% endfor %}</tbody></table></div></body></html>"""
PRINT_OT_TEMPLATE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>OT</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><style>@media print {.no-print {display:none;}}</style></head><body onload="window.print()"><div class="container"><h1>Orden de Trabajo #{{ ot.id }}</h1><h3>{{ ot.nombre }}</h3><p><strong>Estado:</strong> {{ ot.estado }}</p><p><strong>Equipo:</strong> {{ ot.equipo_nombre }}</p><p><strong>Fecha Gen:</strong> {{ ot.fecha_generacion }}</p><hr><h5>Operaciones</h5><p>{{ ot.operaciones }}</p><h5>Observaciones</h5><p>{{ ot.observaciones }}</p></div></body></html>"""
PRINT_ALL_OTS_TEMPLATE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Listado OTs</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><style>@media print {.no-print {display:none;}} table{width:100%;border:1px solid #ddd;} th,td{border:1px solid #ddd;padding:5px;}</style></head><body onload="window.print()"><div class="container"><h2>Listado Órdenes de Trabajo</h2><table><thead><tr><th>ID</th><th>Nombre</th><th>Equipo</th><th>Fecha</th><th>Estado</th></tr></thead><tbody>{% for ot in ots %}<tr><td>{{ ot.id }}</td><td>{{ ot.nombre }}</td><td>{{ ot.equipo_nombre }}</td><td>{{ ot.fecha_generacion }}</td><td>{{ ot.estado }}</td></tr>{% endfor %}</tbody></table></div></body></html>"""
PRINT_CRONOGRAMA_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Cronograma de Mantenimiento {{ year }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        @media print {
            .no-print { display: none; }
            @page { size: landscape; margin: 1cm; }
            body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
            .badge-status, .badge-legend { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; color-adjust: exact !important; }
        }
        body { padding: 20px; font-family: sans-serif; font-size: 0.8rem; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 4px; text-align: center; vertical-align: middle; }
        th { background-color: #f2f2f2; font-weight: bold; }
        .text-start { text-align: left; }
        .badge-status {
            font-size: 0.75em;
            padding: 2px 4px;
            border-radius: 3px;
            display: inline-block;
            margin: 1px;
            color: #fff; /* Texto blanco por defecto para legibilidad */
            border: 1px solid #ccc;
        }
        /* Definición explícita de colores para impresión */
        .status-realizada { background-color: #198754 !important; color: white !important; border-color: #198754; }
        .status-en-curso { background-color: #ffc107 !important; color: #212529 !important; border-color: #ffc107; }
        .status-rechazada { background-color: #000000 !important; color: white !important; border-color: #000000; }
        .status-pendiente { background-color: #dc3545 !important; color: white !important; border-color: #dc3545; }
        .status-prevista { background-color: #6c757d !important; color: white !important; border-color: #6c757d; }
        
        .badge-legend {
            display: inline-block;
            padding: 3px 6px;
            font-size: 0.8em;
            font-weight: bold;
            border-radius: 4px;
            margin-right: 5px;
            border: 1px solid #999;
            color: white; /* Ensure legend text is white */
        }
    </style>
</head>
<body onload="window.print()">
    <div class="container-fluid">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h2>Cronograma de Mantenimiento - Año {{ year }}</h2>
            <button class="btn btn-secondary no-print" onclick="window.close()">Cerrar</button>
        </div>

        <table class="table table-bordered table-sm">
            <thead>
                <tr>
                    <th style="width: 20%;">Actividad / Equipo</th>
                    {% for m in meses %}
                    <th>{{ m }}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for row in data %}
                <tr>
                    <td class="text-start bg-light">
                        <strong>{{ row.actividad }}</strong><br>
                        <span class="text-muted">{{ row.equipo }}</span>
                    </td>
                    {% for month_idx in range(1, 13) %}
                    <td style="vertical-align: top;">
                        {% if month_idx in row.ots %}
                            {% for ot in row.ots[month_idx] %}
                            <div class="badge-status 
                                {% if ot.estado == 'Realizada' %}status-realizada{% elif ot.estado == 'En curso' %}status-en-curso{% elif ot.estado == 'Pendiente' %}status-pendiente{% elif ot.estado == 'Prevista' %}status-prevista{% else %}status-rechazada{% endif %}">
                                {{ ot.day_day }}
                            </div>
                            {% endfor %}
                        {% endif %}
                    </td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="mt-3">
            <strong>Leyenda:</strong> 
            <span class="badge-legend status-realizada">Realizada</span>
            <span class="badge-legend status-en-curso" style="color: #212529 !important;">En Curso</span>
            <span class="badge-legend status-pendiente">Pendiente (Vencida)</span>
            <span class="badge-legend status-prevista">Prevista</span>
            <span class="badge-legend status-rechazada">Rechazada</span>
            <small class="ms-2 text-muted">El número indica el día del mes.</small>
        </div>
        <div class="mt-2 text-end text-muted">
            <small>Generado: {{ hoy }}</small>
        </div>
    </div>
</body>
</html>
"""
PRINT_CORRECTIVO_TEMPLATE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Incidencia</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><style>@media print {.no-print {display:none;}} img{max-width:100%;}</style></head><body onload="window.print()"><div class="container"><h1>Incidencia: {{ item.nombre }}</h1><p><strong>Estado:</strong> {{ item.estado }}</p><p><strong>Equipo:</strong> {{ item.equipo_nombre }}</p><p><strong>Detectada:</strong> {{ item.fecha_detectada }}</p><p><strong>Comentario:</strong> {{ item.comentario }}</p><p><strong>Solución:</strong> {{ item.solucion }}</p><h3>Fotos</h3><div class="row">{% for img in imgs %}<div class="col-6"><img src="data:image/png;base64,{{ img.data }}"><br>{{ img.name }}</div>{% endfor %}</div><h3>Documentos PDF Adjuntos</h3><ul class="list-group">{% for pdf in pdfs %}<li class="list-group-item d-flex align-items-center"><span style="font-size: 1.5em; color: #dc3545; margin-right: 10px;">📄</span><div><strong>{{ pdf.name }}</strong><br><small class="text-muted">El contenido del PDF se encuentra almacenado digitalmente.</small></div></li>{% else %}<li class="list-group-item">No hay documentos PDF adjuntos.</li>{% endfor %}</ul></div></body></html>"""
PRINT_ALL_CORRECTIVOS_TEMPLATE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Listado Incidencias</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><style>@media print {.no-print {display:none;}} table{width:100%;border:1px solid #ddd;} th,td{border:1px solid #ddd;padding:5px;}</style></head><body onload="window.print()"><div class="container"><h2>Listado Incidencias</h2><table><thead><tr><th>ID</th><th>Nombre</th><th>Equipo</th><th>Estado</th><th>Fecha</th></tr></thead><tbody>{% for c in items %}<tr><td>{{ c.id }}</td><td>{{ c.nombre }}</td><td>{{ c.equipo_nombre }}</td><td>{{ c.estado }}</td><td>{{ c.fecha_detectada }}</td></tr>{% endfor %}</tbody></table></div></body></html>"""

CONFIGURACION_TEMPLATE = """
<div class="d-flex justify-content-between align-items-center mb-4"><h1 class="h2">Configuración de tipos</h1></div>
<div class="row"><div class="col-md-8"><div class="card"><div class="card-header d-flex justify-content-between align-items-center"><span>Tipos de Equipo</span><button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#addTypeConfigModal">+ Nuevo Tipo</button></div><div class="card-body p-0"><table class="table table-striped table-hover mb-0"><thead class="table-light"><tr><th>ID</th><th>Nombre</th><th>Acciones</th></tr></thead><tbody>{% for tipo in tipos %}<tr><td>{{ tipo.id }}</td><td>{{ tipo.nombre }}</td><td><a href="{{ url_for('edit_type', id=tipo.id) }}" class="btn btn-sm btn-outline-primary">Editar</a></td></tr>{% endfor %}</tbody></table></div></div></div></div>
<div class="modal fade" id="addTypeConfigModal" tabindex="-1"><div class="modal-dialog"><div class="modal-content"><form action="{{ url_for('add_type_config') }}" method="POST"><div class="modal-header"><h5 class="modal-title">Nuevo Tipo</h5></div><div class="modal-body"><input type="text" class="form-control" name="nombre" required></div><div class="modal-footer"><button type="submit" class="btn btn-primary">Guardar</button></div></form></div></div></div>
"""
EDIT_TYPE_TEMPLATE = """<h2>Editar Tipo</h2><form action="{{ url_for('update_type', id=tipo.id) }}" method="POST"><div class="mb-3"><input type="text" class="form-control" name="nombre" value="{{ tipo.nombre }}" required></div><div class="d-flex justify-content-end gap-2"><a href="{{ url_for('general_settings') }}" class="btn btn-secondary">Cancelar</a><button type="submit" class="btn btn-primary">Actualizar</button></div></form>"""
SYSTEM_DATE_TEMPLATE = """<h1 class="h2">Fecha del Sistema</h1><form action="{{ url_for('update_system_date') }}" method="POST"><div class="mb-3"><input type="date" class="form-control" name="fecha_sistema" value="{{ fecha_sistema }}" required></div><button type="submit" class="btn btn-primary">Guardar</button></form>"""