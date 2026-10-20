import sys
import config
from agent import AIAgent

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def print_banner(agent: AIAgent):
    print("=" * 65)
    print(" AGENTE DE IA (LANGCHAIN) - HIBRIDO (LOCAL / API)")
    print("=" * 65)
    print(f" Modo actual:     {agent.mode.upper()}")
    if agent.mode == "local":
        print(f" Modelo Ollama:   {config.LOCAL_MODEL}")
        print(f" Servidor Local:  {config.LOCAL_BASE_URL}")
    else:
        print(f" Modelo API:      {config.API_MODEL}")
        print(f" Base URL:        {config.API_BASE_URL or 'OpenAI Oficial'}")
    print("-" * 65)
    print(" Comandos especiales:")
    print("   /mode local   -> Cambiar a modelo local (Ollama)")
    print("   /mode api     -> Cambiar a modelo en la nube (OpenAI/Groq)")
    print("   /clear        -> Limpiar historial de chat")
    print("   salir / exit  -> Salir del programa")
    print("=" * 65 + "\n")

def main():
    # Inicializar agente con la configuracion por defecto
    try:
        agent = AIAgent()
    except Exception as e:
        print(f"\n[Error de inicio]: {e}", file=sys.stderr)
        print("Revisa tu archivo config.py o .env y asegurate de tener Ollama o tu API Key listos.")
        return

    print_banner(agent)

    while True:
        try:
            user_input = input("\nTu: ").strip()
            
            if not user_input:
                continue

            if user_input.lower() in ["salir", "exit", "quit"]:
                print("Hasta luego!")
                break

            if user_input.lower() == "/clear":
                agent.clear_history()
                continue

            if user_input.lower().startswith("/mode"):
                parts = user_input.split()
                if len(parts) == 2 and parts[1].lower() in ["local", "api"]:
                    new_mode = parts[1].lower()
                    print(f"\n[Cambiando modo a: {new_mode.upper()}...]")
                    try:
                        agent = AIAgent(mode=new_mode)
                        print_banner(agent)
                    except Exception as e:
                        print(f"[Error al cambiar de modo]: {e}")
                else:
                    print("Uso: /mode local  o  /mode api")
                continue

            print("\n[Pensando...]")
            response = agent.ask(user_input)
            print(f"\nAgente: {response}")

        except KeyboardInterrupt:
            print("\nSesion finalizada.")
            break
        except Exception as e:
            print(f"\n[Error durante la ejecucion]: {e}")

if __name__ == "__main__":
    main()
