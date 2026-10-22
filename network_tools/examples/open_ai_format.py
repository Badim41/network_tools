# TODO
# pip install openai
from openai import OpenAI

api_key = "API_KEY"

client = OpenAI(
    api_key=api_key,
    base_url="https://yellowfire.ru/v1",
)

response = client.chat.completions.create(
    model="gpt-4o",  # GptModels.gpt_4o
    messages=[
        {"role": "user", "content": "Привет!"}
    ],
    temperature=0.7,
)

print(response.choices[0].message.content)

input("Next? Stream.")

stream = client.chat.completions.create(
    model="gpt-4o",  # GptModels.gpt_4o
    messages=[{"role": "user", "content": "Сгенерируй стих"}],
    stream=True,
    temperature=0.7,
)

for chunk in stream:
    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

input("\nNext? Function Calling (tools).")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Получить текущую погоду в городе",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "Город, например: Москва"}
                },
                "required": ["location"],
            },
        },
    }
]

tool_response = client.chat.completions.create(
    model="gemini-3-8-flash",
    messages=[{"role": "user", "content": "Какая погода в Москве?"}],
    tools=tools,
)
print("Message:", response.choices[0].message.content)
print("Tool calls:", tool_response.choices[0].message.tool_calls)

