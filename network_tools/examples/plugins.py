from network_tools._types import ALL_VISION_MODELS
from network_tools import NetworkToolsAPI, GptModels

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

print("Модели со зрением:", ALL_VISION_MODELS)

chat_history = [
    {'content': 'Что это?', 'role': 'user'},
    {'content': 'Ваш вопрос очень общий, и мне трудно понять, что именно вы имеете в виду', 'role': 'assistant'}
]  # История запросов

model = GptModels.deepseek_r1
prompt = "Что на картинке?"
file_path_1 = r"example_files\cat.png"

# Используется плагин на распознавание изображений, если модель не поддерживает изображения
response = client.chatgpt_api(prompt, model=model, chat_history=chat_history, file_path=file_path_1)
print("Ответ:", response.response.text)
print("История чата:", response.chat_history)
print("Использованные плагины:", response.plugins)
print("Описание картинки от ChatGPT-4o:", response.image_description)