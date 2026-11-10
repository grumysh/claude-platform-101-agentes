from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get today's current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city to check"}
            },
            "required": ["city"],
        },
    },
    {
        "name": "get_forecast",
        "description": "Get the weather forecast for the next few days for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city to check"}
            },
            "required": ["city"],
        },
    },
]


def get_weather(city):
    return f"Weather in {city} today: 95F, sunny"


def get_forecast(city):
    return (
        f"Forecast for {city}: "
        "tomorrow 88F and cloudy, "
        "day after 75F with heavy rain, "
        "then 80F and sunny"
    )


def run_tool(name, tool_input):
    match name:
        case "get_weather":
            return get_weather(tool_input["city"])
        case "get_forecast":
            return get_forecast(tool_input["city"])
    raise ValueError(f"Unknown tool: {name}")


messages = [
    {
        "role": "user",
        "content": "I'm in Austin. What should I wear today, and should I pack an umbrella for the next few days?",
    }
]

while True:
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=messages,
        tools=tools,
    )

    if response.stop_reason != "tool_use":
        break

    messages.append({"role": "assistant", "content": response.content})

    tool_results = [
        {
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": run_tool(block.name, block.input),
        }
        for block in response.content
        if block.type == "tool_use"
    ]

    messages.append({"role": "user", "content": tool_results})

for block in response.content:
    if block.type == "text":
        print(block.text)
