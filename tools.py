import datetime
import os
import platform
import subprocess
import sys
from langchain_core.tools import tool

# ==============================================================================
# HERRAMIENTAS DE SISTEMA Y MATEMÁTICAS
# ==============================================================================

@tool
def get_current_datetime() -> str:
    """Retorna la fecha y hora actual del sistema.
    Útil cuando el usuario pregunta la hora, fecha o día actual."""
    now = datetime.datetime.now()
    return now.strftime("Fecha y hora actual: %Y-%m-%d %H:%M:%S (Día: %A)")

@tool
def calculate(expression: str) -> str:
    """Evalúa una expresión matemática simple (por ejemplo: '25 * 4 + 10' o 'sqrt(144)').
    Útil para cálculos numéricos precisos."""
    import math
    safe_dict = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "pow": pow,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "pi": math.pi,
        "e": math.e,
    }
    try:
        result = eval(expression, {"__builtins__": None}, safe_dict)
        return f"Resultado de '{expression}': {result}"
    except Exception as e:
        return f"Error al calcular '{expression}': {str(e)}"

@tool
def get_system_status() -> str:
    """Retorna información básica sobre el sistema operativo y entorno de la máquina donde corre el agente."""
    return (
        f"Sistema Operativo: {platform.system()} {platform.release()} "
        f"({platform.version()}), Arquitectura: {platform.machine()}"
    )

# ==============================================================================
# HERRAMIENTAS DE PROGRAMACIÓN Y GESTIÓN DE ARCHIVOS
# ==============================================================================

@tool
def create_file(file_path: str, content: str) -> str:
    """Crea o sobreescribe un archivo en el disco con el contenido especificado.
    Crea las carpetas intermedias automáticamente si no existen.
    Útil para escribir scripts de Python, HTML, JavaScript, JSON, etc.
    
    :param file_path: Ruta relativa o absoluta del archivo a crear (ej: 'app.py' o 'src/index.html').
    :param content: El código o texto completo que contendrá el archivo.
    """
    try:
        parent_dir = os.path.dirname(file_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        byte_count = len(content.encode("utf-8"))
        return f"Archivo creado exitosamente en: '{file_path}' ({byte_count} bytes escritos)."
    except Exception as e:
        return f"Error al crear el archivo '{file_path}': {str(e)}"

@tool
def read_file(file_path: str) -> str:
    """Lee y retorna el contenido de un archivo de texto existente.
    Útil para inspeccionar código, archivos de configuración o datos.
    
    :param file_path: Ruta del archivo que se desea leer.
    """
    try:
        if not os.path.exists(file_path):
            return f"El archivo '{file_path}' no existe."
            
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
            
        return f"--- Contenido de '{file_path}' ---\n{content}"
    except Exception as e:
        return f"Error al leer el archivo '{file_path}': {str(e)}"

@tool
def list_directory(directory_path: str = ".") -> str:
    """Lista los archivos y subcarpetas dentro de un directorio.
    Útil para explorar el proyecto o verificar qué archivos existen.
    
    :param directory_path: Ruta de la carpeta a inspeccionar (por defecto '.' es la carpeta actual).
    """
    try:
        if not os.path.exists(directory_path):
            return f"La carpeta '{directory_path}' no existe."
            
        entries = os.listdir(directory_path)
        if not entries:
            return f"La carpeta '{directory_path}' está vacía."
            
        result = [f"Archivos y carpetas en '{directory_path}':"]
        for entry in sorted(entries):
            full_path = os.path.join(directory_path, entry)
            is_dir = "[CARPETA]" if os.path.isdir(full_path) else "[ARCHIVO]"
            result.append(f"  {is_dir} {entry}")
            
        return "\n".join(result)
    except Exception as e:
        return f"Error al listar la carpeta '{directory_path}': {str(e)}"

@tool
def execute_python(code: str) -> str:
    """Ejecuta un script o fragmento de código Python en un subproceso aislado
    y captura la salida por consola (stdout) y los posibles errores (stderr).
    Útil para probar algoritmos, resolver cálculos complejos o validar scripts.
    
    :param code: Código en Python a ejecutar.
    """
    try:
        # Usamos el mismo ejecutable de python del entorno virtual
        python_executable = sys.executable
        process = subprocess.run(
            [python_executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8"
        )
        
        output = process.stdout
        errors = process.stderr
        
        res = []
        if output:
            res.append(f"Salida estándar (stdout):\n{output.strip()}")
        if errors:
            res.append(f"Errores (stderr):\n{errors.strip()}")
        if not output and not errors:
            res.append("El código se ejecutó exitosamente sin salida por consola.")
            
        res.append(f"Código de salida: {process.returncode}")
        return "\n".join(res)
    except subprocess.TimeoutExpired:
        return "Error: La ejecución del código excedió el tiempo límite de 30 segundos."
    except Exception as e:
        return f"Error al ejecutar código Python: {str(e)}"

@tool
def run_command(command: str) -> str:
    """Ejecuta un comando real de consola en la terminal del sistema (PowerShell/CMD) y retorna el resultado.
    SOLO debe usarse para comandos válidos como 'pip install ...', 'git status', 'dir', etc.
    PROHIBIDO usar esta herramienta para saludos, preguntas, charlas o texto conversacional del usuario.
    
    :param command: El comando exacto de terminal a ejecutar.
    """
    try:
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="replace"
        )
        
        out = process.stdout
        err = process.stderr
        
        res = [f"Comando ejecutado: '{command}'"]
        if out:
            res.append(f"Salida:\n{out.strip()}")
        if err:
            res.append(f"Errores / Advertencias:\n{err.strip()}")
        if not out and not err:
            res.append("El comando finalizó sin salida de texto.")
        res.append(f"Código de retorno: {process.returncode}")
        return "\n".join(res)
    except subprocess.TimeoutExpired:
        return f"Error: El comando '{command}' tardó más de 30 segundos y fue cancelado."
    except Exception as e:
        return f"Error al ejecutar el comando: {str(e)}"

# ==============================================================================
# LISTA DE HERRAMIENTAS ACTIVAS
# ==============================================================================
AVAILABLE_TOOLS = [
    get_current_datetime,
    calculate,
    get_system_status,
    create_file,
    read_file,
    list_directory,
    execute_python,
    run_command,
]


