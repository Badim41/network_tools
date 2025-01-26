# NetworkToolsAPI

### Нейросети для обработки текста:
- o1 (OpenAI)
- GPT-4o (OpenAI)
- Claude 3.5 Sonnet (Anthropic)
- Command R+ (Cohere)

### Модели для генерации изображений:
- DALL-E-3
- Flux
- SD Ultra
- Flux Dev
- SD XL
- Recraft
- Kandinsky

## Установка
```bash
pip install git+https://github.com/Badim41/network_tools.git
```

## Использование

### 1. Создание класса
```python
from network_tools import NetworkToolsAPI

api_key = "your_api_key_here"
client = NetworkToolsAPI(api_key)
```

### 2. ChatGPT API
#### Поддерживает файлы .txt, .pdf, .docx, .png
```python
from network_tools import GptModels

model = GptModels.gpt_4o
prompt = "Что это?"
chat_history = []
file_path = "files/cat.png"
# file_path = None

response = client.chatgpt_api(prompt, model=model, chat_history=chat_history, file_path=file_path)
print(response.response.text)
```

### 3. Генерация изображений
```python
from network_tools import ImageModels, AspectRatio

models = [ImageModels.kandinsky, ImageModels.dalle_light]
prompt = "Футуристический городской пейзаж с летающими машинами."
aspect_ratio = AspectRatio.ratio_1x1  # Определите соотношение сторон

for image_group in client.test_image_generate(models, prompt, aspect_ratio):
    print(image_group)  # Печать путей к сгенерированным изображениям
```

### 4. Получение баланса
```python
user_usage = client.get_usage()

for request in user_usage.response.usage:
    timestamp = datetime.fromtimestamp(request.timestamp).strftime('%Y-%m-%d %H:%M:%S')
    comment = request.comment
    balance_change = f"{request.balance_change:.8f}"  # Отображение с 8 знаками после запятой
    print(f"{timestamp:<20} {comment:<60} {balance_change:<15}")

print("Баланс:", user_usage.response.balance)  # Отображение оставшегося баланса
```

## Цена
- Цены на текстовые модели в 4 раза ниже официальных
- Цены на модели изображений в 5 раз ниже официальных

### Claude 3.5 Sonnet:
```
1K input tokens: 0.00075 Credit
1K output tokens: 0.00375 Credit
```

### GPT-4:
```
1K input tokens: 0.0009375 Credit
1K output tokens: 0.00375 Credit
```

### Command R:
```
1K input tokens: 0.0006875 Credit
1K output tokens: 0.0025 Credit
```

### o1:
```
1K input tokens: 0.003 Credit
1K output tokens: 0.012 Credit
```

### Reka Flush:
```
1K input tokens: 0.00004 Credit
1K output tokens: 0.00016 Credit
```

### DALL-E (Light):
```
0.004 Credit/изображение
```

### DALL-E 3:
```
0.008 Credit/изображение
```

### Flux:
```
0.0006 Credit/изображение
```

### SD Ultra:
```
0.016 Credit/изображение
```

### Flux Dev:
```
0.005 Credit/изображение
```
### SD XL:
```
0.0002 Credit/изображение
```

### Recraft:
```
0.008 Credit/изображение
```