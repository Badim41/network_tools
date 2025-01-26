from network_tools import NetworkToolsAPI, GptModels

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

model = GptModels.command_r
prompt = "Перескажи наш диалог"
chat_history = [
    {'content': 'Что это?', 'role': 'user'},
    {'content': 'Ваш вопрос очень общий, и мне трудно понять, что именно вы имеете в виду', 'role': 'assistant'}
]  # История запросов

response = client.chatgpt_api(prompt, model=model, chat_history=chat_history)
print("Ответ 1:", response.response.text)
print("История чата 1:", response.chat_history)


# Второй запрос, с 2 файлами

model = GptModels.gpt_4o
prompt = "Что это?"
chat_history = []
file_path_1 = r"example_files\cat.png"  # Путь к файлу

response = client.chatgpt_api(prompt, model=model, chat_history=chat_history, file_path=file_path_1)
print("Ответ 2:", response.response.text)
print("История чата 2:", response.chat_history)

file_path_2 = r"example_files\test.txt"  # Путь к файлу
prompt = "О чём этот текст? Какого цвета изображение?"
chat_history = response.chat_history

response = client.chatgpt_api(prompt, model=model, chat_history=chat_history, file_path=file_path_2)
print("Ответ 3:", response.response.text)
print("История чата 3:", response.chat_history)
