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
)

print(response.choices[0].message.content)

input("Next? Stream.")

stream = client.chat.completions.create(
    model="gpt-4o",  # GptModels.gpt_4o
    messages=[{"role": "user", "content": "Сгенерируй стих"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

