import os

from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()

mcp_name = os.environ["LINEAR_MCP_NAME"]

question = input("Pregunta para Linear (Enter = qué herramientas tienes): ") or "What tools do you have available?"

runner = client.beta.messages.tool_runner(
    model="claude-opus-5",
    max_tokens=16000,
    messages=[{"role": "user", "content": question}],
    mcp_servers=[
        {
            "type": "url",
            "url": os.environ["LINEAR_MCP_URL"],
            "name": mcp_name,
            "authorization_token": os.environ["LINEAR_MCP_TOKEN"],
        }
    ],
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": mcp_name,
        }
    ],
    betas=["mcp-client-2025-11-20"],
)

for message in runner:
    for block in message.content:
        if block.type == "mcp_tool_use":
            print(f"=== TOOL: {block.server_name}.{block.name}({block.input}) ===")
        elif block.type == "mcp_tool_result":
            print(f"=== RESULTADO{' (error)' if block.is_error else ''} ===")
        elif block.type == "text":
            print(block.text)
