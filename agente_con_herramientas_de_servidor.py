from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()


def print_blocks(content):
    for block in content:
        if block.type == "server_tool_use":
            print(f"Tool call: {block.name} — {block.input}")
        elif block.type == "web_search_tool_result":
            if isinstance(block.content, list):
                for result in block.content:
                    print(f"  - {result.title}: {result.url}")
            else:
                print(f"Search error: {block.content.error_code}")
        elif block.type == "bash_code_execution_tool_result":
            result = block.content
            if result.type == "bash_code_execution_result":
                if result.return_code == 0:
                    print(f"stdout: {result.stdout}")
                else:
                    print(f"stderr: {result.stderr}")
            else:
                print(f"Tool error: {result.error_code}")
        elif block.type == "text":
            print(block.text)


def run(prompt, tools):
    messages = [{"role": "user", "content": prompt}]

    while True:
        response = client.messages.create(
            model="claude-opus-5",
            max_tokens=16000,
            tools=tools,
            messages=messages,
        )

        print_blocks(response.content)

        if response.stop_reason != "pause_turn":
            return response

        messages.append({"role": "assistant", "content": response.content})


# Llamada 1: búsqueda web — Anthropic ejecuta la búsqueda en el servidor
print("=== BÚSQUEDA WEB ===")
run(
    input("Pregunta para buscar en la web: "),
    [{"type": "web_search_20260209", "name": "web_search"}],
)

# Llamada 2: ejecución de código — Claude escribe y ejecuta Python en un sandbox
print("\n=== EJECUCIÓN DE CÓDIGO ===")
run(
    input("Pregunta para resolver con código: "),
    [{"type": "code_execution_20260120", "name": "code_execution"}],
)
