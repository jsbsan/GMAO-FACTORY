import os

def pack_project(output_file="contexto_proyecto.txt"):
    # Directorios y archivos que queremos ignorar para no saturar a la IA
    ignore_list = {
        '__pycache__', '.git', '.venv', 'venv', 'env', 
        '.pytest_cache', '.vscode', '.idea', 'dist', 'build',
        'node_modules', '.DS_Store'
    }
    
    # Extensiones de archivos que queremos incluir
    include_extensions = {'.py', '.md', '.txt', '.html', '.css', '.js', '.json', '.yaml', '.yml', '.sql'}

    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write("ESTRUCTURA DEL PROYECTO:\n")
        
        # Primero generamos un árbol visual rápido de las carpetas
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in ignore_list]
            level = root.replace('.', '').count(os.sep)
            indent = ' ' * 4 * level
            f_out.write(f"{indent}{os.path.basename(root)}/\n")
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                if any(f.endswith(ext) for ext in include_extensions):
                    f_out.write(f"{sub_indent}{f}\n")
        
        f_out.write("\n" + "="*50 + "\n")
        f_out.write("CONTENIDO DE LOS ARCHIVOS:\n")
        f_out.write("="*50 + "\n\n")

        # Ahora recorremos y volcamos el contenido de cada archivo
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in ignore_list]
            
            for file in files:
                if any(file.endswith(ext) for ext in include_extensions):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, '.')
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f_in:
                            content = f_in.read()
                            f_out.write(f"--- INICIO ARCHIVO: {relative_path} ---\n")
                            f_out.write(content)
                            f_out.write(f"\n--- FIN ARCHIVO: {relative_path} ---\n\n")
                    except Exception as e:
                        f_out.write(f"Error leyendo {relative_path}: {e}\n")

    print(f"✅ Proyecto empaquetado con éxito en: {output_file}")

if __name__ == "__main__":
    pack_project()