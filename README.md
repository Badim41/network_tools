# NetworkToolsAPI (Python)

[![Example Usage Bot](https://img.shields.io/badge/Example-Telegram--BOT-0066FF?logo=probot&style=flat)](https://t.me/GPT4_Unlimit_bot)
[![Open in Colab](https://img.shields.io/badge/Open%20in-Google%20Colab-F9AB00?logo=googlecolab&style=flat)](https://colab.research.google.com/github/Badim41/network_tools/blob/master/google_colab_notebooks/base.ipynb)

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
- Recraft V3
- Kandinsky

## Модели для редактирования изображений:
- Recraft V3
- Stable Diffusion
- Flux dev

## Модели для генерации видео:
- T2V-01-Director (Hailuo AI)
- Stable video diffusion

## Модели для генерации музыки:
- Suno (V3, V4)
- Riffusion

## Модели для озвучки текста:
- T2A-01-HD (Hailuo AI)

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

for image_group in client.image_generate_api(models, prompt, aspect_ratio):
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

#### [Остальные примеры](https://github.com/Badim41/network_tools/tree/master/network_tools/examples)

## Цена
- Цены на текстовые модели в **4 раза ниже** официальных
- Цены на модели изображений в **5 раз ниже** официальных
- Цены на модели редактирования изображений в **5 раз ниже** официальных
- Цены на модели видео в **5 раз ниже** официальных
- Цены на музыку *примерно равны* официальным
- Цены на TTS *примерно равны* официальным

#### Получить ключ: https://t.me/@GPT4_Unlimit_bot
#### Бесплатный баланс: 0.5$

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

## Обработка изображений:
```
Удаление фона: 0.004 Credit/изображение
Замена фона: 0.016 Credit/изображение
Дополнение изображения (outpaint): 0.008 Credit/изображение
Восстановление (inpaint): 0.008 и 0.005 Credit/изображение
Увеличение (upscale): 0.004 Credit/изображение
Добавление текста: 0.008 Credit/изображение
Сделать в похожем стиле: 0.008 Credit/изображение
Сделать векторным: 0.004 Credit/изображение
Поиск и замена: 0.008 Credit/изображение
Из изображения в 3D-модель: 0.004 Credit/изображение
```

## Генерация видео:
```
Stable Video Diffusion: 0.04 Credit/видео
Hailuo: 0.086 Credit/видео
```
## Генерация музыки:
```
Suno v4: 0.05 Credit/2 трека
Suno v3: 0.035 Credit/2 трека
Riffusion: 0.01 Credit/трек
```

## TTS (озвучить текст)
```
Hailuo: 0.03 Credit/1000 символов
```

## CURL

### chatgpt
#### Обычный запрос
```bash
curl --request POST \
  --url https://yellowfire.ru/api/v2/chatgpt \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "gpt_4o", "prompt": "Привет!", "chat_history": [], "file_base64": "", "internet_access": false, "mime_type":""}'
  ```
#### С файлом в base64:
```bash
curl --request POST \
  --url https://yellowfire.ru/api/v2/chatgpt \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "gpt_4o", "prompt": "Что это за текст?", "chat_history": [], "file_base64": "IyMjINCX0LDQs9Cw0LTQutCwINC60L7RiNCw0YfRjNC10Lkg0L/RgNC40YDQvtC00YsNCg0K0JrQvtGC0Ysg4oCTINC+0LTQvdC4INC40Lcg0YHQsNC80YvRhSDQt9Cw0LPQsNC00L7Rh9C90YvRhSDRgdC+0LfQtNCw0L3QuNC5INC90LAg0L3QsNGI0LXQuSDQv9C70LDQvdC10YLQtS4g0J3QtdGB0LzQvtGC0YDRjyDQvdCwINGC0L4sINGH0YLQviDQvtC90Lgg0LbQuNCy0YPRgiDQsdC+0Log0L4g0LHQvtC6INGBINGH0LXQu9C+0LLQtdC60L7QvCDRgtGL0YHRj9GH0LXQu9C10YLQuNGP0LzQuCwg0LIg0LjRhSDQv9C+0LLQtdC00LXQvdC40LgsINC40L3RgdGC0LjQvdC60YLQsNGFINC4INGB0YPRidC90L7RgdGC0Lgg0L7RgdGC0LDQtdGC0YHRjyDRh9GC0L4t0YLQviDQvdC10L7QsdGK0Y/RgdC90LjQvNC+0LUsINC/0YDQuNGC0Y/Qs9C40LLQsNGO0YnQtdC1INCy0L3QuNC80LDQvdC40LUuDQoNCtCf0L7Rh9C10LzRgyDQutC+0YLRiyDRgtCw0Log0LvRjtCx0Y/RgiDQutC+0YDQvtCx0LrQuCwg0LTQsNC20LUg0LXRgdC70Lgg0L7QvdC4INGP0LLQvdC+INC80LDQu9GLINC00LvRjyDQvdC40YU/INCc0L7QttC10YIg0LHRi9GC0YwsINGN0YLQviDRgdCy0Y/Qt9Cw0L3QviDRgSDQuNC90YHRgtC40L3QutGC0LjQstC90YvQvCDQttC10LvQsNC90LjQtdC8INGB0L/RgNGP0YLQsNGC0YzRgdGPINCyINCx0LXQt9C+0L/QsNGB0L3QvtC8INC/0YDQvtGB0YLRgNCw0L3RgdGC0LLQtSwg0LjQu9C4INC20LUg0YLRg9GCINGB0LrRgNGL0YIg0LrQsNC60L7QuS3RgtC+INC00YDRg9Cz0L7QuSwg0L3QtdC40LfQstC10YHRgtC90YvQuSDQvNC+0YLQuNCyPw0KDQrQmNC70Lgg0LLQvtC30YzQvNC10Lwg0LjRhSDRgdC/0L7RgdC+0LHQvdC+0YHRgtGMINCy0YHQtdCz0LTQsCDQv9Cw0LTQsNGC0Ywg0L3QsCDQu9Cw0L/Riy4g0K3RgtC+INGE0LXQvdC+0LzQtdC9LCDQutC+0YLQvtGA0YvQuSDQsdC40L7Qu9C+0LPQuNGPINGH0LDRgdGC0LjRh9C90L4g0L7QsdGK0Y/RgdC90LjQu9CwIOKAkyDRgyDQutC+0YjQtdC6INC90LXQstC10YDQvtGP0YLQvdC+INCz0LjQsdC60LjQuSDQv9C+0LfQstC+0L3QvtGH0L3QuNC6INC4INGA0LDQt9Cy0LjRgtC+0LUg0YfRg9Cy0YHRgtCy0L4g0YDQsNCy0L3QvtCy0LXRgdC40Y8uINCd0L4g0LrQsNC20LTRi9C5INGA0LDQtywg0LrQvtCz0LTQsCDQvNGLINCy0LjQtNC40LwsINC60LDQuiDQvtC90Lgg0LvQvtCy0LrQviDQv9C10YDQtdCy0L7RgNCw0YfQuNCy0LDRjtGC0YHRjyDQsiDQstC+0LfQtNGD0YXQtSwg0LrQsNC20LXRgtGB0Y8sINCx0YPQtNGC0L4g0LfQtNC10YHRjCDQt9Cw0LzQtdGI0LDQvdCwINC80LDQs9C40Y8uDQoNCtCQINC40YUg0LfQsNCz0LDQtNC+0YfQvdGL0LkgItC80YPRgNGA0YAiPyDQrdGC0L4g0L3QtSDQv9GA0L7RgdGC0L4g0LfQstGD0Log4oCTINGN0YLQviDRg9C90LjQstC10YDRgdCw0LvRjNC90YvQuSDRj9C30YvQuiwg0YEg0L/QvtC80L7RidGM0Y4g0LrQvtGC0L7RgNC+0LPQviDQutC+0YIg0LzQvtC20LXRgiDQvtC00L3QvtCy0YDQtdC80LXQvdC90L4g0LLRi9GA0LDQttCw0YLRjCDQutC+0LzRhNC+0YDRgiwg0LTQvtCy0LXRgNC40LUg0LguLi4g0LHQvtC70YwuINCc0YPRgNC70YvQutCw0L3RjNC1INC00LDQttC1INGB0L/QvtGB0L7QsdC90L4g0LfQsNC20LjQstC70Y/RgtGMINGC0LrQsNC90Lgg0LHQu9Cw0LPQvtC00LDRgNGPINCy0LjQsdGA0LDRhtC40Y/QvCDQvtC/0YDQtdC00LXQu9C10L3QvdC+0Lkg0YfQsNGB0YLQvtGC0YssINC90L4g0LrQsNC6INC60L7RgtGLINC90LDRg9GH0LjQu9C40YHRjCDQuNGB0L/QvtC70YzQt9C+0LLQsNGC0Ywg0LXQs9C+INGC0LDQuiDRjdGE0YTQtdC60YLQuNCy0L3Qvj8NCg0K0JgsINC60L7QvdC10YfQvdC+LCDQs9C70LDQstC90YvQuSDQstC+0L/RgNC+0YE6INC/0L7Rh9C10LzRgyDQutC+0YLRiyDRgdC80L7RgtGA0Y/RgiDQsiDQv9GD0YHRgtC+0YLRgz8g0JjQvdC+0LPQtNCwINC60LDQttC10YLRgdGPLCDRh9GC0L4g0L7QvdC4INCy0LjQtNGP0YIg0YLQviwg0YfRgtC+INGB0LrRgNGL0YLQviDQvtGCINGH0LXQu9C+0LLQtdGH0LXRgdC60L7Qs9C+INCz0LvQsNC30LAuINCU0YPRhdC+0LIsINC/0LDRgNCw0LvQu9C10LvRjNC90YvQtSDQvNC40YDRiywg0LjQu9C4LCDQvNC+0LbQtdGCINCx0YvRgtGMLCDQv9GA0L7RgdGC0L4g0L/Ri9C70LjQvdC60Lgg0LIg0YHQvtC70L3QtdGH0L3QvtC8INC70YPRh9C1PyDQkiDQu9GO0LHQvtC8INGB0LvRg9GH0LDQtSDQuNGFINCy0LfQs9C70Y/QtCDRgdC70L7QstC90L4g0LPQvtCy0L7RgNC40YI6ICLQldGB0YLRjCDQstC10YnQuCwg0LrQvtGC0L7RgNGL0LUg0YLQtdCx0LUg0L3QtSDQtNCw0L3QviDQv9C+0L3Rj9GC0YwiLg0KDQrQmtC+0YLRiyDigJMg0Y3RgtC+INC90LUg0L/RgNC+0YHRgtC+INC20LjQstC+0YLQvdGL0LUsINGN0YLQviDRhdC+0LTRj9GH0LjQtSDQt9Cw0LPQsNC00LrQuCwg0LrQvtGC0L7RgNGL0LUg0L3QuNC60L7Qs9C00LAg0L3QtSDQv9C10YDQtdGB0YLQsNGO0YIg0YPQtNC40LLQu9GP0YLRjC4g0JzQvtC20LXRgiDQsdGL0YLRjCwg0LjQvNC10L3QvdC+INCyINGN0YLQvtC8INC40YUg0LLQvtC70YjQtdCx0YHRgtCy0L4g4oCTINC+0L3QuCDQvtGB0YLQsNGO0YLRgdGPINC30LDQs9Cw0LTQutC+0LksINGH0LDRgdGC0YzRjiDQutC+0YLQvtGA0L7QuSDQvNGLINGF0L7RgtC40Lwg0YHRgtCw0YLRjC4=", "internet_access": false, "mime_type":"text/plain"}'
```
### Image generate
```bash
curl --request POST \
  --url https://yellowfire.ru/api/v2/image_generate \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"models": ["sd_xl"], "aspect_ratio": "1:1", "prompt": "A futuristic city with flying cars"}'
  ```

### Check request
```bash
curl --request GET \
  --url https://yellowfire.ru/api/v2/status/55081200-929f-4464-97fe-cb5e4dbda2ba \
  --header 'api-key: API_KEY'
  ```

### Balance
```bash
curl --request GET \
  --url https://yellowfire.ru/api/v2/user \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY'
  ```
