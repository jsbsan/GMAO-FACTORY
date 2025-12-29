---------------------------
Pasar de online a offline
---------------------------

# En templates_base.py, busca la sección <head> y el final del <body>

# CAMBIA ESTO:
# <link href="https://cdn.jsdelivr.net/..." ...>

# POR ESTO:
# <link href="{{ url_for('static', filename='css/bootstrap.min.css') }}" rel="stylesheet">
# <link href="{{ url_for('static', filename='css/all.min.css') }}" rel="stylesheet">

# Y EL SCRIPT AL FINAL:
# <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>


Archivo,Ubicación (Variable),Aprox. Línea,Código Original (Requiere Internet),Código Nuevo (Offline / Local)
templates_base.py,BASE_TEMPLATE (Head),10,"<link href=""https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"" rel=""stylesheet"">","<link href=""{{ url_for('static', filename='css/bootstrap.min.css') }}"" rel=""stylesheet"">"
templates_base.py,BASE_TEMPLATE (Head),11,"<link rel=""stylesheet"" href=""https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"">","<link href=""{{ url_for('static', filename='css/all.min.css') }}"" rel=""stylesheet"">"
templates_base.py,BASE_TEMPLATE (Final Body),73,"<script src=""https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js""></script>","<script src=""{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}""></script>"
templates_base.py,LOGIN_TEMPLATE (Head),82,"<link href=""https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"" rel=""stylesheet"">","<link href=""{{ url_for('static', filename='css/bootstrap.min.css') }}"" rel=""stylesheet"">"
templates_base.py,PRINT_... (Todas las de impresión),100+,"<link href=""https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"" rel=""stylesheet"">","<link href=""{{ url_for('static', filename='css/bootstrap.min.css') }}"" rel=""stylesheet"">"