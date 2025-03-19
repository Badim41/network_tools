from network_tools import NetworkToolsAPI, GptModels

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

chat_history = [
    {'content': 'Что это?', 'role': 'user'},
    {'content': 'Ваш вопрос очень общий, и мне трудно понять, что именно вы имеете в виду', 'role': 'assistant'}
]  # История запросов

model = GptModels.gpt_4o
prompt = "Перескажи наш диалог"

generator = client.chatgpt_api(prompt, model=model, chat_history=chat_history, stream=True)

for chunk in generator:
    print(chunk.response.text, end='')

print("\n\nchat_history", chunk.chat_history)

