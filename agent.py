import sys
import uuid
from typing import Optional
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from model_factory import get_llm
from tools import AVAILABLE_TOOLS
import config

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SYSTEM_PROMPT = (
    "Eres un asistente de Inteligencia Artificial experto en programación, desarrollo de software y soporte técnico.\n\n"
    "REGLAS OBLIGATORIAS SOBRE EL USO DE HERRAMIENTAS:\n"
    "1. SALUDOS Y CONVERSACIÓN: Si el usuario te saluda ('hola', 'cómo estás', 'buenas', etc.), te hace preguntas generales o simplemente conversa, responde DIRECTAMENTE con texto amable. NUNCA llames a ninguna herramienta para responder a un saludo.\n"
    "2. ACCIONES ESPECÍFICAS: Solo invoca una herramienta cuando el usuario pida explícitamente realizar una acción concreta:\n"
    "   - create_file: Únicamente cuando solicite guardar o crear un archivo.\n"
    "   - read_file: Únicamente para leer un archivo existente.\n"
    "   - list_directory: Únicamente para listar carpetas/archivos.\n"
    "   - execute_python: Únicamente para ejecutar código Python.\n"
    "   - run_command: Únicamente para ejecutar comandos de terminal válidos (ej. pip, git, dir). ¡JAMÁS ejecutes saludos o mensajes del usuario como comandos!\n"
    "   - calculate: Únicamente para operaciones matemáticas numéricas.\n"
    "   - get_current_datetime: Únicamente si preguntan qué hora o fecha es hoy.\n"
    "   - get_system_status: Únicamente si preguntan sobre el sistema operativo o hardware.\n"
    "3. Si no estás seguro de requerir una herramienta, responde directamente al usuario con texto."
)

class AIAgent:
    def __init__(self, mode: Optional[str] = None):
        """
        Inicializa el agente con el modo seleccionado ('local' o 'api').
        """
        self.mode = (mode or config.MODE).lower()
        self.llm = get_llm(self.mode)
        self.tools = AVAILABLE_TOOLS
        
        # Gestor de memoria para conversaciones multi-turno
        self.checkpointer = MemorySaver()
        self.thread_id = str(uuid.uuid4())
        
        # Creacion del agente ReAct (estandar moderno de LangChain / LangGraph)
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=SYSTEM_PROMPT,
            checkpointer=self.checkpointer
        )

    def ask(self, user_input: str) -> str:
        """
        Envia un mensaje al agente, muestra si se invocan herramientas y retorna la respuesta.
        Incluye un fallback automatico si el modelo local no soporta llamadas a herramientas nativas.
        """
        run_config = {"configurable": {"thread_id": self.thread_id}}
        
        try:
            # Intentamos invocar el agente con herramientas
            response = self.agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config=run_config
            )
            
            # Analizar los mensajes para mostrar llamadas a herramientas en consola
            messages = response.get("messages", [])
            for msg in messages:
                # Si el modelo decidio llamar a herramientas:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        print(f"   [HERRAMIENTA]: {tc.get('name')} con argumentos: {tc.get('args')}")
                # Si es el resultado de una herramienta:
                elif hasattr(msg, "name") and msg.name and msg.type == "tool":
                    preview = str(msg.content)[:100] + ("..." if len(str(msg.content)) > 100 else "")
                    print(f"   [RESULTADO]: {preview}")

            # El ultimo mensaje es la respuesta final del agente
            last_message = messages[-1] if messages else None
            if last_message:
                return str(last_message.content)
            return "No se obtuvo respuesta del modelo."

        except Exception as e:
            err_msg = str(e)
            # Manejo amigable si el modelo de Ollama no soporta function calling (ej. llama3:latest)
            if "does not support tools" in err_msg:
                print(f"\n   [AVISO sobre el modelo '{config.LOCAL_MODEL}']:")
                print(f"   El modelo '{config.LOCAL_MODEL}' en Ollama no tiene soporte nativo para herramientas (function calling).")
                print(f"   Para habilitar herramientas locales ejecuta en otra terminal:")
                print(f"      ollama pull llama3.2")
                print(f"   Y en config.py define: LOCAL_MODEL = 'llama3.2'")
                print(f"   -> Respondiendo en modo conversacional directo:")
                
                # Fallback: responde directamente usando el modelo sin herramientas
                direct_response = self.llm.invoke([
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ])
                return str(direct_response.content)
            else:
                raise e

    def clear_history(self):
        """Reinicia el thread_id para comenzar una conversacion limpia."""
        self.thread_id = str(uuid.uuid4())
        print("[Memoria de conversacion reiniciada]")
