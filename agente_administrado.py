from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()

AGENT_NAME = "Line Counter"
ENVIRONMENT_NAME = "line-counter-env"

# 1. AGENTE: modelo, system prompt y herramientas.
agent = next((a for a in client.beta.agents.list() if a.name == AGENT_NAME), None)

if agent is None:
    agent = client.beta.agents.create(
        name=AGENT_NAME,
        model="claude-opus-5",
        system="You are a helpful agent that completes small file tasks.",
        tools=[
            {
                "type": "agent_toolset_20260401",
                "default_config": {"enabled": True, "permission_policy": {"type": "auto"}},
                "configs": [
                    {"name": "web_fetch", "enabled": False},
                    {"name": "web_search", "enabled": False},
                ],
            }
        ],
    )
    print(f"Agente creado: {agent.id}")
else:
    print(f"Agente existente: {agent.id}")

# 2. ENTORNO: el contenedor en la nube donde el agente ejecuta bash y crea archivos.
environment = next(
    (e for e in client.beta.environments.list() if e.name == ENVIRONMENT_NAME), None
)

if environment is None:
    environment = client.beta.environments.create(
        name=ENVIRONMENT_NAME,
        config={
            "type": "cloud",
            "networking": {"type": "limited"},
        },
    )
    print(f"Entorno creado: {environment.id}")
else:
    print(f"Entorno existente: {environment.id}")

# 3. SESIÓN: una ejecución del agente dentro del entorno.
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="Count lines demo",
)
print(f"Sesión: https://platform.claude.com/workspaces/default/sessions/{session.id}\n")

# 4. EVENT STREAM: se abre ANTES de mandar la tarea para no perder ningún evento.
with client.beta.sessions.events.stream(session_id=session.id) as stream:
    client.beta.sessions.events.send(
        session_id=session.id,
        events=[
            {
                "type": "user.message",
                "content": [
                    {
                        "type": "text",
                        "text": "Create a file in the temp directory, "
                                "count its lines, and report back.",
                    }
                ],
            }
        ],
    )

    for event in stream:
        if event.type == "agent.message":
            for block in event.content:
                if block.type == "text":
                    print(block.text)
        elif event.type == "agent.tool_use":
            print(f"=== TOOL: {event.name}({event.input}) ===")
            if event.evaluated_permission == "ask":
                answer = input("¿Permitir esta acción? (s/n): ").strip().lower()
                client.beta.sessions.events.send(
                    session_id=session.id,
                    events=[
                        {
                            "type": "user.tool_confirmation",
                            "tool_use_id": event.id,
                            "result": "allow" if answer == "s" else "deny",
                        }
                    ],
                )
        elif event.type == "session.status_idle":
            if event.stop_reason.type != "requires_action":
                break
        elif event.type == "session.status_terminated":
            break
