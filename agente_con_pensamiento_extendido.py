from dotenv import load_dotenv
import anthropic
from anthropic import beta_tool

load_dotenv()

client = anthropic.Anthropic()

fake_weather = {
    "San Francisco": "62F, foggy",
    "Monterey": "68F, sunny",
    "Napa": "85F, sunny",
    "Lake Tahoe": "45F, snow showers",
    "Santa Cruz": "66F, partly cloudy",
    "Yosemite": "55F, rain",
}


@beta_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: City name
    """
    return f"Weather in {city}: {fake_weather.get(city, '72F, clear')}"


runner = client.beta.messages.tool_runner(
    model="claude-opus-5",
    max_tokens=16000,
    thinking={"type": "adaptive", "display": "summarized"},  # summarized = return the reasoning text
    output_config={"effort": "high"},  # low | medium | high | xhigh | max
    tools=[get_weather],
    messages=[
        {
            "role": "user",
            "content": "Plan a road trip out of San Francisco with two stops, "
                       "weighing weather and drive time.",
        }
    ],
)

for message in runner:
    for block in message.content:
        if block.type == "thinking":
            print("=== THINKING ===")
            print(block.thinking)
        elif block.type == "tool_use":
            print(f"=== TOOL: {block.name}({block.input}) ===")
        elif block.type == "text":
            print("=== RESPUESTA ===")
            print(block.text)
