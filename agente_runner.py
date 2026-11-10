from dotenv import load_dotenv
import anthropic
from anthropic import beta_tool

load_dotenv()

client = anthropic.Anthropic()


@beta_tool
def get_weather(city: str) -> str:
    """Get today's current weather for a city.

    Args:
        city: The city to check
    """
    return f"Weather in {city} today: 95F, sunny"


# @beta_tool convierte esta función en una herramienta y arma el JSON solo:
#   - name:        el nombre de la función -> "get_forecast"
#   - description: la primera línea del docstring
#   - properties:  los parámetros; el tipo sale del type hint (str -> "string")
#   - required:    los parámetros sin valor por defecto (aquí, city)
# Siempre pon type hints, si no el esquema queda incompleto.
@beta_tool
def get_forecast(city: str) -> str:
    # El docstring NO es solo documentación: Claude lo lee como descripción
    # de la herramienta para decidir cuándo usarla. Escríbelo claro.
    """Get the weather forecast for the next few days for a city.

    Args:
        city: The city to check
    """
    # Lo que retorna la función es el tool_result que el runner le devuelve a Claude.
    return f"Forecast for {city}: tomorrow 88F and cloudy, day after 75F with heavy rain"


runner = client.beta.messages.tool_runner(
    model="claude-sonnet-5",
    max_tokens=1024,
    tools=[get_weather, get_forecast],
    messages=[{"role": "user", "content": "I'm in Austin. What should I wear today, and should I pack an umbrella?"}],
)

final = runner.until_done()

for block in final.content:
    if block.type == "text":
        print(block.text)
