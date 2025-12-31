from flask import url_for

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GMAO Factory</title>
    <!-- Usa url_for para offline, o CDN si estás online -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .sidebar-container { background-color: #2c3e50; color: white; min-height: 100vh; }
        .sidebar-link { color: #bdc3c7; text-decoration: none; display: block; padding: 12px 15px; border-bottom: 1px solid #34495e; }
        .sidebar-link:hover, .sidebar-link.active { background-color: #34495e; color: white; border-left: 4px solid #3498db; }
        .sidebar-brand { padding: 20px; text-align: center; background-color: #1a252f; margin-bottom: 10px; }
        .content { padding: 20px; }
        .mobile-navbar { background-color: #2c3e50; }
        
        /* ESTADOS DE OTS */
        .status-realizada { background-color: #198754; color: white; }
        .status-en-curso { background-color: #ffc107; color: #212529; }
        .status-rechazada { background-color: #000000; color: white; }
        .status-pendiente { background-color: #dc3545; color: white; }
        .status-prevista { background-color: #6c757d; color: white; }
        /* NUEVO ESTADO APLAZADA */
        .status-aplazada { background-color: #6f42c1; color: white; } /* Morado */
        
        .corr-detectada { background-color: #dc3545; color: white; }
        .corr-en-curso { background-color: #ffc107; color: #212529; }
        .corr-resuelta { background-color: #198754; color: white; }

        .badge-status { font-size: 0.8em; padding: 5px; border-radius: 4px; display: inline-block; margin-bottom: 2px; cursor: pointer; transition: transform 0.1s; }
        .badge-status:hover { transform: scale(1.1); box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
        .img-thumb { width: 50px; height: 50px; object-fit: cover; cursor: pointer; border: 1px solid #ddd; }
    </style>
</head>
<body>

    {% set navigation %}
        <div class="sidebar-brand">
            <h4>🏭 GMAO</h4>
            <small>Factory v5.1</small>
            <div class="mt-2 small text-muted">Usuario: {{ session.get('username', 'Invitado') }}</div>
        </div>
        <div>
            {% if session.get('perm_inventario') %}
            <a href="{{ url_for('index') }}" class="sidebar-link {{ 'active' if active_page == 'inventario' else '' }}"><i class="fas fa-boxes me-2"></i> Inventario</a>
            {% endif %}
            
            {% if session.get('perm_actividades') %}
            <a href="{{ url_for('activities') }}" class="sidebar-link {{ 'active' if active_page == 'actividades' else '' }}"><i class="fas fa-clipboard-list me-2"></i> Actividades</a>
            {% endif %}
            
            <a href="{{ url_for('work_orders') }}" class="sidebar-link {{ 'active' if active_page == 'ots' else '' }}"><i class="fas fa-tools me-2"></i> Órdenes de Trabajo</a>
            <a href="{{ url_for('cronograma') }}" class="sidebar-link {{ 'active' if active_page == 'cronograma' else '' }}"><i class="fas fa-calendar-alt me-2"></i> Cronogramas OTs</a>
            <a href="{{ url_for('correctivos') }}" class="sidebar-link {{ 'active' if active_page == 'correctivos' else '' }}"><i class="fas fa-exclamation-triangle me-2"></i> Correctivos</a>
            
            {% if session.get('perm_configuracion') %}
            <div class="border-top border-secondary my-2"></div>
            <a href="{{ url_for('general_settings') }}" class="sidebar-link {{ 'active' if active_page == 'ajustes' else '' }}"><i class="fas fa-cog me-2"></i> Configuración Global</a>
            {% endif %}
            
            <div class="border-top border-secondary my-2"></div>
            <a href="{{ url_for('about') }}" class="sidebar-link {{ 'active' if active_page == 'about' else '' }}"><i class="fas fa-info-circle me-2"></i> Acerca de...</a>
            <a href="{{ url_for('logout') }}" class="sidebar-link text-danger"><i class="fas fa-sign-out-alt me-2"></i> Cerrar Sesión</a>
        </div>
    {% endset %}

    <nav class="navbar navbar-dark mobile-navbar d-md-none sticky-top">
      <div class="container-fluid">
        <span class="navbar-brand mb-0 h1">🏭 GMAO Factory</span>
        <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#mobileMenu">
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
    </nav>

    <div class="offcanvas offcanvas-start mobile-navbar text-white d-md-none" tabindex="-1" id="mobileMenu">
      <div class="offcanvas-header"><h5 class="offcanvas-title">Menú</h5><button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"></button></div>
      <div class="offcanvas-body p-0">{{ navigation }}</div>
    </div>

    <div class="container-fluid">
        <div class="row">
            <nav class="col-md-3 col-lg-2 d-none d-md-block sidebar-container p-0">{{ navigation }}</nav>
            <main class="col-md-9 ms-sm-auto col-lg-10 content">
                {% with messages = get_flashed_messages(with_categories=true) %}
                  {% if messages %}
                    {% for category, message in messages %}
                      <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">{{ message }}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>
                    {% endfor %}
                  {% endif %}
                {% endwith %}
                
                <div class="alert alert-secondary py-1 px-3 mb-3 d-flex justify-content-between align-items-center">
                    <small><i class="fas fa-calendar-day"></i> Fecha Sistema: <strong>{{ system_date }}</strong></small>
                </div>
                <!-- CONTENT_PLACEHOLDER -->
            </main>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - GMAO Factory</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body { background-color: #f8f9fa; display: flex; align-items: center; justify-content: center; height: 100vh; } .login-card { max-width: 400px; width: 100%; padding: 20px; }</style>
</head>
<body>
    <div class="card login-card shadow">
        <div class="card-body"><h3 class="text-center mb-4">🏭 GMAO Factory</h3>{% with messages = get_flashed_messages(with_categories=true) %}{% if messages %}{% for category, message in messages %}<div class="alert alert-{{ category }}">{{ message }}</div>{% endfor %}{% endif %}{% endwith %}<form action="{{ url_for('login') }}" method="POST"><div class="mb-3"><label class="form-label">Usuario</label><input type="text" class="form-control" name="username" required autofocus></div><div class="mb-3"><label class="form-label">Contraseña</label><input type="password" class="form-control" name="password" required></div><button type="submit" class="btn btn-primary w-100">Iniciar Sesión</button></form><div class="mt-3 text-center text-muted"><small>Acceso restringido</small></div></div>
    </div>
</body>
</html>
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
                        <dd class="col-sm-8"><span class="badge bg-primary">v5.2</span></dd>

                        <dt class="col-sm-4 text-end">Autor:</dt>
                        <dd class="col-sm-8">Julio Sánchez Berro</dd>
                        
                        <dt class="col-sm-4 text-end">Licencia:</dt>
                        <dd class="col-sm-8">GPL 3.0</dd>
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

# --- PLANTILLAS DE IMPRESIÓN ---

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
        .status-aplazada { background-color: #6f42c1 !important; color: white !important; border-color: #6f42c1; }
        
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
                                {% if ot.estado == 'Realizada' %}status-realizada{% elif ot.estado == 'En curso' %}status-en-curso{% elif ot.estado == 'Pendiente' %}status-pendiente{% elif ot.estado == 'Prevista' %}status-prevista{% elif ot.estado == 'Aplazada' %}status-aplazada{% else %}status-rechazada{% endif %}">
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
            <span class="badge-legend status-aplazada">Aplazada</span>
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