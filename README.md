# Agentes

Agentes generados durante la capacitación de Claude Academy: Claude Platform 101.

## Requisitos

- Python 3.10 o superior (probado con 3.15)

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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
