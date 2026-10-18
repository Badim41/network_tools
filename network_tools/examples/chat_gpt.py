from network_tools import NetworkToolsAPI, GptModels

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

model = GptModels.command_a
prompt = "Перескажи наш диалог"
chat_history = [
    {'content': 'Что это?', 'role': 'user'},
    {'content': 'Ваш вопрос очень общий, и мне трудно понять, что именно вы имеете в виду', 'role': 'assistant'}
]  # История запросов

response = client.chatgpt_api(prompt, model=model, chat_history=chat_history, temperature=0.7)
print("Ответ 1:", response.response.text)
print("История чата 1:", response.chat_history)
print("response.cost:", response.cost) # Credits. 1 Credit = 100₽


# Второй запрос, с одной или несколькими картинками

model = GptModels.gemini_3_8_flash
prompt = "Что это?"
chat_history = []
file_path_1 = [r"example_files\cat.png"]  # Путь к файлу

response = client.chatgpt_api(prompt, model=model, chat_history=chat_history, file_path=file_path_1, temperature=0.7)
print("Ответ 2:", response.response.text)
print("История чата 2:", response.chat_history)

# Третий запрос, со списком файлов (или одним файлом) и историей чата

file_path_2 = [r"example_files\test.txt"]  # Можно передавать как str, так и list[str]
prompt = "О чём этот текст? Какого цвета изображение?"
chat_history = response.chat_history

response = client.chatgpt_api(prompt, model=model, chat_history=chat_history, file_path=file_path_2)
print("Ответ 3:", response.response.text)
print("История чата 3:", response.chat_history)
