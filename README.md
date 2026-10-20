# 🤖 Agente de IA con LangChain (Local u Online por API)

Este proyecto implementa un agente autónomo de Inteligencia Artificial en Python con **LangChain** capaz de utilizar herramientas (*tool-calling*) y alternar entre:
1. **Modo Local:** Usando modelos locales mediante [Ollama](https://ollama.com/) (como `llama3`, `llama3.2`, `qwen2.5`, etc.), sin costo y con total privacidad.
2. **Modo API:** Usando proveedores en la nube mediante API como **Groq** (`openai/gpt-oss-120b`) u **OpenAI**, ultra rápidos y con soporte completo de herramientas.

---

## 🛠️ Herramientas y Capacidades del Agente

El agente tiene integradas herramientas para comportarse como un **asistente de programación y desarrollo**:

* 📝 **`create_file`**: Crea o sobreescribe archivos de código (Python, HTML, JS, JSON, etc.) creando carpetas automáticamente.
* 📖 **`read_file`**: Lee e inspecciona el contenido de cualquier archivo del proyecto.
* 📂 **`list_directory`**: Explora los archivos y carpetas existentes.
* 🐍 **`execute_python`**: Ejecuta scripts de Python en un entorno controlado y lee la salida y posibles errores.
* 💻 **`run_command`**: Ejecuta comandos de consola (ej: `pip list`, `git status`, etc.).
* 🧮 **`calculate`**: Calculadora matemática segura para cómputo numérico exacto.
* 🕒 **`get_current_datetime`**: Consulta la fecha y hora en tiempo real.
* ⚙️ **`get_system_status`**: Identifica el sistema operativo y entorno.

---

## 📁 Estructura del Proyecto

```text
agente/
├── .env.example          # Plantilla para variables de entorno
├── .env                  # Archivo de configuración local y claves
├── config.py             # Configuración central (modo local vs api)
├── model_factory.py      # Fábrica que instancia Ollama o Groq/OpenAI
├── tools.py              # Definición de herramientas (archivos, python, terminal, etc.)
├── agent.py              # Definición del agente con LangGraph y memoria
├── main.py               # Consola interactiva para chatear y probar
└── requirements.txt      # Dependencias necesarias
```

---

## ⚙️ ¿Cómo configurar el modo (Local o API)?

### 1. A través del archivo `.env`
Edita la variable `AGENT_MODE` en [.env](file:///c:/Users/PC/Desktop/agente/.env):

```env
# Cambia entre "api" o "local":
AGENT_MODE=api

# Si usas Groq (Recomendado):
GROQ_API_KEY=gsk_...
GROQ_MODEL=openai/gpt-oss-120b

# Si usas Local (Ollama):
OLLAMA_MODEL=llama3
```

### 2. Directamente en el código (`config.py`)
En [config.py](file:///c:/Users/PC/Desktop/agente/config.py):
```python
MODE = "api"  # o "local"
```

---

## 🚀 Puesta en Marcha

Para iniciar el agente ejecuta:

```powershell
.\venv\Scripts\python main.py
```

### Comandos especiales dentro del chat:
- `/mode local`: Cambia en caliente al modelo local de Ollama.
- `/mode api`: Cambia en caliente al modelo en la nube (Groq).
- `/clear`: Limpia la memoria de la conversación actual.
- `salir` o `exit`: Finaliza el programa.

---

## 💡 Ejemplos de lo que le puedes pedir

1. **Crear un script:**
   > *"Crea un script llamado `fibonacci.py` que calcule los primeros 10 números de Fibonacci y pruébalo."*
2. **Explorar el proyecto:**
   > *"Lista los archivos de la carpeta actual y dime qué contiene config.py."*
3. **Ejecutar comandos:**
   > *"Ejecuta un comando para ver qué versión de Python estoy usando."*
