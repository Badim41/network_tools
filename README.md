# NetworkToolsAPI (Python)

[![Example Usage Bot](https://img.shields.io/badge/Example-Telegram--BOT-0066FF?logo=probot&style=flat)](https://t.me/GPT4_Unlimit_bot?start=git3)
[![Open in Colab](https://img.shields.io/badge/Open%20in-Google%20Colab-F9AB00?logo=googlecolab&style=flat)](https://colab.research.google.com/github/Badim41/network_tools/blob/master/google_colab_notebooks/base.ipynb)

### Нейросети для обработки текста:

- GPT-5-1-high (OpenAI)
- GPT-5-1 (OpenAI)
- GPT-5-high (OpenAI)
- GPT-5 (OpenAI)
- ChatGPT-5 (OpenAI)
- GPT-5-mini (OpenAI)
- GPT-5-nano (OpenAI)
- GPT-oss (OpenAI)
- GLM-4.5 (zAi)
- o4-mini (OpenAI)
- o3-mini-High (OpenAI)
- GPT-4.1 (OpenAI)
- GPT-4.1-mini (OpenAI)
- GPT-4.1-nano (OpenAI)
- o3-mini (OpenAI)
- o1 (OpenAI)
- GPT-4o (OpenAI)
- GPT-4o-mini (OpenAI)
- GPT-3.5 (OpenAI)
- Grok 4 (x-Ai)
- Grok 3 (x-Ai)
- Gemini 3.0 Pro (Google)
- Gemini 2.5 Pro (Google)
- Gemini-2.5 Flash Lite (Google)
- Gemini-2.0 Flash Lite (Google)
- Claude 4.5 Sonnet Thinking (Anthropic)
- Claude 4.5 Sonnet (Anthropic)
- Claude 4.1 Opus (Anthropic)
- Claude 4.1 Opus Thinking (Anthropic)
- Claude 4 Opus (Anthropic)
- Claude 4 Opus Thinking (Anthropic)
- Claude 4 Sonnet (Anthropic)
- Claude 4 Sonnet Thinking (Anthropic)
- Claude 3.7 (Anthropic)
- Claude 3.5 Sonnet (Anthropic)
- Claude 3 Opus (Anthropic)
- Claude 3 Sonnet (Anthropic)
- Claude 3 Haiku (Anthropic)
- DeepSeek R1 (DeepSeek)
- DeepSeek V3 (DeepSeek)
- DeepSeek V3.2 (DeepSeek)
- DeepSeek V3.2 Thinking (DeepSeek)
- Command A Vision (Cohere)
- Command A (Cohere)
- Command R+ (Cohere)
- Reka Flash (Reka)
- Minimax-01 (Minimax)
- Minimax-02 (Minimax)
- Kimi K2 thinking (Moonshot AI)

### Модели для генерации изображений:

- DALL-E-3
- SD Ultra
- SD XL
- Flux
- Recraft V3
- Kandinsky
- ChatGPT Images

## Модели для редактирования изображений:

- Recraft V3
- Stable Diffusion
- ChatGPT Images
- Nano Banana Pro

## Модели для генерации видео:

- Stable video diffusion

## Модели для генерации музыки (generate/cover/extend):

- Suno V3.5
- Suno V4
- Suno V4.5
- Suno V5

## Модели для озвучки текста:
- Elevenlabs multilingual (Elevenlabs)

## Модели для создания аудио:

- Stable Audio

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

- Цены на текстовые модели в **2 раза ниже** официальных
- Цены на модели изображений в **2 раза ниже** официальных
- Цены на модели редактирования изображений в **2 раза ниже** официальных
- Цены на музыку *примерно равны* официальным
- Цены на TTS *примерно равны* официальным

#### Получить ключ

Чтобы получить ключ и бесплатный баланс, перейдите по [ссылке](https://t.me/GPT4_Unlimit_bot?start=api) в бота пи
пропишите /get_api, скопируйте ключ, который пришлёт бот

#### Бесплатный баланс: 1$

## Текстовые модели

# Стоимость использования моделей

## Текстовые модели

| Модель                     | 1M входных токенов (Credit) | 1M выходных токенов (Credit) |
|----------------------------|-----------------------------|------------------------------|
| gpt-5-1-high               | 0.625                       | 5.0                          |
| gpt-5-1                    | 0.625                       | 5.0                          |
| gpt-5-high                 | 0.625                       | 5.0                          |
| gpt-5                      | 0.625                       | 5.0                          |
| gpt-5-mini                 | 0.125                       | 1.0                          |
| gpt-5-nano                 | 0.0025                      | 0.2                          |
| gpt-5-chat-latest          | 0.625                       | 5.0                          |
| gpt-oss                    | 0.075                       | 0.3                          |
| glm-4.6                    | 0.25                        | 1.0                          |
| claude-4-5-sonnet          | 1.50                        | 7.50                         |
| claude-4-5-sonnet-thinking | 1.50                        | 7.50                         |
| claude-4-opus              | 7.50                        | 37.5                         |
| claude-4-opus-thinking     | 7.50                        | 37.5                         |
| claude-4-1-opus            | 7.50                        | 37.5                         |
| claude-4-1-opus-thinking   | 7.50                        | 37.5                         |
| claude-4-sonnet            | 1.50                        | 7.50                         |
| claude-4-sonnet-thinking   | 1.50                        | 7.50                         |
| o4-mini                    | 0.55                        | 2.20                         |
| o3-High                    | 5.00                        | 20.00                        |
| gpt-4.1                    | 1.00                        | 4.00                         |
| gpt-4.1-mini               | 0.20                        | 0.80                         |
| gpt-4.1-nano               | 0.05                        | 0.20                         |
| gpt-4.5                    | 37.50                       | 75.00                        |
| o3-mini                    | 0.55                        | 2.20                         |
| o1                         | 7.50                        | 30.00                        |
| gpt-4o                     | 1.25                        | 5.00                         |
| gpt-4o-mini                | 0.075                       | 0.30                         |
| gpt-3.5                    | 0.50                        | 1.00                         |
| claude-3.7                 | 1.50                        | 7.50                         |
| claude-3.5-sonnet          | 1.50                        | 7.50                         |
| claude-3-opus              | 7.50                        | 37.50                        |
| claude-3-sonnet            | 1.50                        | 7.50                         |
| claude-3-haiku             | 0.125                       | 0.625                        |
| deepseek-r1                | 0.275                       | 1.095                        |
| deepseek-v3                | 0.135                       | 0.55                         |
| deepseek-v3.2              | 0.135                       | 0.205                        |
| deepseek-v3.2 thinking     | 0.135                       | 0.205                        |
| command-r-plus             | 1.25                        | 5.00                         |
| command-a                  | 1.25                        | 5.00                         |
| reka-flash                 | 0.10                        | 0.40                         |
| minimax-01                 | 0.10                        | 0.55                         |
| minimax-02                 | 0.15                        | 0.6                          |
| grok-3                     | 1.50                        | 7.50                         |
| grok-4                     | 1.50                        | 7.50                         |
| gemini-3.0-pro             | 1.0                         | 6.00                         |
| gemini-2.5-pro             | 0.625                       | 5.00                         |
| gemini-2.5-flash           | 0.075                       | 0.30                         |
| gemini-2.0-flash-lite      | 0.075                       | 0.30                         |
| gemini-2.5-flash-lite      | 0.075                       | 0.30                         |
| kimi-k2-thinking           | 0.3                         | 1.25                         |

## Модели изображений

| Модель             | Стоимость (Credit/изображение) |
|--------------------|--------------------------------|
| DALL-E (Light)     | 0.01                           |
| SD Ultra           | 0.04                           |
| SD XL              | 0.0005                         |
| Flux Pro Ultra Row | 0.02                           |
| Flux               | 0.01                           |
| Recraft v3         | 0.02                           |
| ChatGPT Images     | 0.085                          |
| Nano Banana Pro    | 0.03                           |

## Обработка изображений

| Операция                         | Стоимость (Credit/изображение) |
|----------------------------------|--------------------------------|
| Удаление фона                    | 0.01                           |
| Замена фона                      | 0.04                           |
| Дополнение изображения           | 0.02                           |
| Inpaint (Stable Diffusion Ultra) | 0.04                           |
| Inpaint (Recraft V3)             | 0.02                           |
| Inpaint (ChatGPT Images)         | 0.085                          |
| Inpaint (Nano Banana Pro)           | 0.03                           |
| Upscale                          | 0.01                           |
| Добавить текст                   | 0.02                           |
| Сделать в похожем стиле          | 0.02                           |
| Сделать векторным                | 0.01                           |
| Поиск и замена                   | 0.02                           |
| Из изображения в 3D-модель       | 0.01                           |

## Генерация видео

| Модель                 | Стоимость (Credit/видео) |
|------------------------|--------------------------|
| Stable Video Diffusion | 0.2                      |

## Генерация музыки

| Модель    | Стоимость (Credit/2 трека) |
|-----------|----------------------------|
| Suno v5   | 0.1                        |
| Suno v4.5 | 0.1                        |
| Suno v4   | 0.05                       |
| Suno v3   | 0.05                       |

## TTS (озвучить текст)

| Модель     | Стоимость (Credit/1000 символов) |
|------------|----------------------------------|
| Elevenlabs | 0.03                             |

## Audio (создать звук)

| Модель       | Стоимость |
|--------------|-----------|
| Stable audio | 0.01      |

## CURL

### ChatGPT

#### Обычный запрос

```bash
curl --request POST \
  --url https://yellowfire.ru/api/v2/chatgpt \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "gpt-4o", "prompt": "Привет!", "chat_history": [], "file_base64": "", "internet_access": false, "mime_type":""}'
  ```

#### С файлом в base64:

```bash
curl --request POST \
  --url https://yellowfire.ru/api/v2/chatgpt \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "gpt-4o", "prompt": "Что это за текст?", "chat_history": [], "file_base64": "IyMjINCX0LDQs9Cw0LTQutCwINC60L7RiNCw0YfRjNC10Lkg0L/RgNC40YDQvtC00YsNCg0K0JrQvtGC0Ysg4oCTINC+0LTQvdC4INC40Lcg0YHQsNC80YvRhSDQt9Cw0LPQsNC00L7Rh9C90YvRhSDRgdC+0LfQtNCw0L3QuNC5INC90LAg0L3QsNGI0LXQuSDQv9C70LDQvdC10YLQtS4g0J3QtdGB0LzQvtGC0YDRjyDQvdCwINGC0L4sINGH0YLQviDQvtC90Lgg0LbQuNCy0YPRgiDQsdC+0Log0L4g0LHQvtC6INGBINGH0LXQu9C+0LLQtdC60L7QvCDRgtGL0YHRj9GH0LXQu9C10YLQuNGP0LzQuCwg0LIg0LjRhSDQv9C+0LLQtdC00LXQvdC40LgsINC40L3RgdGC0LjQvdC60YLQsNGFINC4INGB0YPRidC90L7RgdGC0Lgg0L7RgdGC0LDQtdGC0YHRjyDRh9GC0L4t0YLQviDQvdC10L7QsdGK0Y/RgdC90LjQvNC+0LUsINC/0YDQuNGC0Y/Qs9C40LLQsNGO0YnQtdC1INCy0L3QuNC80LDQvdC40LUuDQoNCtCf0L7Rh9C10LzRgyDQutC+0YLRiyDRgtCw0Log0LvRjtCx0Y/RgiDQutC+0YDQvtCx0LrQuCwg0LTQsNC20LUg0LXRgdC70Lgg0L7QvdC4INGP0LLQvdC+INC80LDQu9GLINC00LvRjyDQvdC40YU/INCc0L7QttC10YIg0LHRi9GC0YwsINGN0YLQviDRgdCy0Y/Qt9Cw0L3QviDRgSDQuNC90YHRgtC40L3QutGC0LjQstC90YvQvCDQttC10LvQsNC90LjQtdC8INGB0L/RgNGP0YLQsNGC0YzRgdGPINCyINCx0LXQt9C+0L/QsNGB0L3QvtC8INC/0YDQvtGB0YLRgNCw0L3RgdGC0LLQtSwg0LjQu9C4INC20LUg0YLRg9GCINGB0LrRgNGL0YIg0LrQsNC60L7QuS3RgtC+INC00YDRg9Cz0L7QuSwg0L3QtdC40LfQstC10YHRgtC90YvQuSDQvNC+0YLQuNCyPw0KDQrQmNC70Lgg0LLQvtC30YzQvNC10Lwg0LjRhSDRgdC/0L7RgdC+0LHQvdC+0YHRgtGMINCy0YHQtdCz0LTQsCDQv9Cw0LTQsNGC0Ywg0L3QsCDQu9Cw0L/Riy4g0K3RgtC+INGE0LXQvdC+0LzQtdC9LCDQutC+0YLQvtGA0YvQuSDQsdC40L7Qu9C+0LPQuNGPINGH0LDRgdGC0LjRh9C90L4g0L7QsdGK0Y/RgdC90LjQu9CwIOKAkyDRgyDQutC+0YjQtdC6INC90LXQstC10YDQvtGP0YLQvdC+INCz0LjQsdC60LjQuSDQv9C+0LfQstC+0L3QvtGH0L3QuNC6INC4INGA0LDQt9Cy0LjRgtC+0LUg0YfRg9Cy0YHRgtCy0L4g0YDQsNCy0L3QvtCy0LXRgdC40Y8uINCd0L4g0LrQsNC20LTRi9C5INGA0LDQtywg0LrQvtCz0LTQsCDQvNGLINCy0LjQtNC40LwsINC60LDQuiDQvtC90Lgg0LvQvtCy0LrQviDQv9C10YDQtdCy0L7RgNCw0YfQuNCy0LDRjtGC0YHRjyDQsiDQstC+0LfQtNGD0YXQtSwg0LrQsNC20LXRgtGB0Y8sINCx0YPQtNGC0L4g0LfQtNC10YHRjCDQt9Cw0LzQtdGI0LDQvdCwINC80LDQs9C40Y8uDQoNCtCQINC40YUg0LfQsNCz0LDQtNC+0YfQvdGL0LkgItC80YPRgNGA0YAiPyDQrdGC0L4g0L3QtSDQv9GA0L7RgdGC0L4g0LfQstGD0Log4oCTINGN0YLQviDRg9C90LjQstC10YDRgdCw0LvRjNC90YvQuSDRj9C30YvQuiwg0YEg0L/QvtC80L7RidGM0Y4g0LrQvtGC0L7RgNC+0LPQviDQutC+0YIg0LzQvtC20LXRgiDQvtC00L3QvtCy0YDQtdC80LXQvdC90L4g0LLRi9GA0LDQttCw0YLRjCDQutC+0LzRhNC+0YDRgiwg0LTQvtCy0LXRgNC40LUg0LguLi4g0LHQvtC70YwuINCc0YPRgNC70YvQutCw0L3RjNC1INC00LDQttC1INGB0L/QvtGB0L7QsdC90L4g0LfQsNC20LjQstC70Y/RgtGMINGC0LrQsNC90Lgg0LHQu9Cw0LPQvtC00LDRgNGPINCy0LjQsdGA0LDRhtC40Y/QvCDQvtC/0YDQtdC00LXQu9C10L3QvdC+0Lkg0YfQsNGB0YLQvtGC0YssINC90L4g0LrQsNC6INC60L7RgtGLINC90LDRg9GH0LjQu9C40YHRjCDQuNGB0L/QvtC70YzQt9C+0LLQsNGC0Ywg0LXQs9C+INGC0LDQuiDRjdGE0YTQtdC60YLQuNCy0L3Qvj8NCg0K0JgsINC60L7QvdC10YfQvdC+LCDQs9C70LDQstC90YvQuSDQstC+0L/RgNC+0YE6INC/0L7Rh9C10LzRgyDQutC+0YLRiyDRgdC80L7RgtGA0Y/RgiDQsiDQv9GD0YHRgtC+0YLRgz8g0JjQvdC+0LPQtNCwINC60LDQttC10YLRgdGPLCDRh9GC0L4g0L7QvdC4INCy0LjQtNGP0YIg0YLQviwg0YfRgtC+INGB0LrRgNGL0YLQviDQvtGCINGH0LXQu9C+0LLQtdGH0LXRgdC60L7Qs9C+INCz0LvQsNC30LAuINCU0YPRhdC+0LIsINC/0LDRgNCw0LvQu9C10LvRjNC90YvQtSDQvNC40YDRiywg0LjQu9C4LCDQvNC+0LbQtdGCINCx0YvRgtGMLCDQv9GA0L7RgdGC0L4g0L/Ri9C70LjQvdC60Lgg0LIg0YHQvtC70L3QtdGH0L3QvtC8INC70YPRh9C1PyDQkiDQu9GO0LHQvtC8INGB0LvRg9GH0LDQtSDQuNGFINCy0LfQs9C70Y/QtCDRgdC70L7QstC90L4g0LPQvtCy0L7RgNC40YI6ICLQldGB0YLRjCDQstC10YnQuCwg0LrQvtGC0L7RgNGL0LUg0YLQtdCx0LUg0L3QtSDQtNCw0L3QviDQv9C+0L3Rj9GC0YwiLg0KDQrQmtC+0YLRiyDigJMg0Y3RgtC+INC90LUg0L/RgNC+0YHRgtC+INC20LjQstC+0YLQvdGL0LUsINGN0YLQviDRhdC+0LTRj9GH0LjQtSDQt9Cw0LPQsNC00LrQuCwg0LrQvtGC0L7RgNGL0LUg0L3QuNC60L7Qs9C00LAg0L3QtSDQv9C10YDQtdGB0YLQsNGO0YIg0YPQtNC40LLQu9GP0YLRjC4g0JzQvtC20LXRgiDQsdGL0YLRjCwg0LjQvNC10L3QvdC+INCyINGN0YLQvtC8INC40YUg0LLQvtC70YjQtdCx0YHRgtCy0L4g4oCTINC+0L3QuCDQvtGB0YLQsNGO0YLRgdGPINC30LDQs9Cw0LTQutC+0LksINGH0LDRgdGC0YzRjiDQutC+0YLQvtGA0L7QuSDQvNGLINGF0L7RgtC40Lwg0YHRgtCw0YLRjC4=", "internet_access": false, "mime_type":"text/plain"}'
```

### Генерация изображений

```bash
curl --request POST \
  --url https://yellowfire.ru/api/v2/image_generate \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"models": ["sd_xl"], "aspect_ratio": "1:1", "prompt": "A futuristic city with flying cars"}'
```

### Проверка запроса

```bash
curl --request GET \
  --url https://yellowfire.ru/api/v2/status/55081200-929f-4464-97fe-cb5e4dbda2ba \
  --header 'api-key: API_KEY'
  ```

### Получение баланса

```bash
curl --request GET \
  --url https://yellowfire.ru/api/v2/user \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY'
  ```
