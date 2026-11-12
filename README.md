# Agentes

Agentes generados durante la capacitación de Claude Academy: Claude Platform 101.

## Agentes

| Archivo | Qué hace | Concepto |
|---|---|---|
| `agente_clima.py` | Recomienda qué ropa usar según el clima de una ciudad | Tool use con bucle manual (`stop_reason`, `tool_result`) |
| `agente_pronostico.py` | Da el clima de hoy y el pronóstico de los próximos días | Varias herramientas en un bucle manual |
| `agente_runner.py` | Lo mismo que `agente_pronostico.py`, sin escribir el bucle | Tool runner con `@beta_tool` (esquema generado de la función) |
| `agente_con_pensamiento_extendido.py` | Planea un road trip desde San Francisco según clima y distancia | Pensamiento adaptativo y `effort` |
| `agente_con_herramientas_de_servidor.py` | Responde una pregunta buscando en la web y otra ejecutando código | Herramientas de servidor: web search y code execution |
| `agente_con_skill.py` | Genera un reporte diario de estado a partir de un log de actividad | Agent Skills (skill propia en `skills/`) |
| `agente_con_mcp_linear.py` | Consulta un workspace de Linear | MCP connector |
| `agente_administrado.py` | Crea un archivo en un contenedor en la nube y cuenta sus líneas | Managed Agents: agente, entorno, sesión y event stream |

## Requisitos

- Python 3.10 o superior (probado con 3.15)
- anthropic>=2.3.0
- python-dotenv>=1.2.4

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "anthropic>=2.3.0" "python-dotenv>=1.2.4"
```

Crear un archivo `.env`:

```
ANTHROPIC_API_KEY=
LINEAR_MCP_NAME=linear
LINEAR_MCP_URL=https://mcp.linear.app/mcp
LINEAR_MCP_TOKEN=
```

## Ejecutar

```bash
source .venv/bin/activate
python agente_clima.py
```
