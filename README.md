# NetworkToolsAPI (Python)

[![Example Usage Bot](https://img.shields.io/badge/Example-Telegram--BOT-0066FF?logo=probot&style=flat)](https://t.me/GPT4_Unlimit_bot?start=git3)
[![Open in Colab](https://img.shields.io/badge/Open%20in-Google%20Colab-F9AB00?logo=googlecolab&style=flat)](https://colab.research.google.com/github/Badim41/network_tools/blob/master/google_colab_notebooks/base.ipynb)

**OpenAI endpoint: `https://sert.yellowfire.ru:444/v1`** (самый стабильный) / `https://ru.yellowfire.ru/v1` (RU (нестабилен из-за РКН)) / `https://yellowfire.ru/v1` (Cloudflare)

---

#### При использовании агентов

Если вы используете **ИИ-АГЕНТА ДЛЯ НАПИСАНИЯ КОДА**, то вставьте в чат [README](https://raw.githubusercontent.com/Badim41/network_tools/refs/heads/master/README.md), чтобы агент мог воспользовать этой библиотекой:
- **[README](https://raw.githubusercontent.com/Badim41/network_tools/refs/heads/master/README.md)**

---

## Получить ключ

Чтобы получить ключ и бесплатный баланс, перейдите по [ссылке](https://t.me/GPT4_Unlimit_bot?start=api) в бота пи
пропишите, скопируйте ключ, который пришлёт бот

#### Бесплатный баланс: 1 Credit

1 Credit = 100₽

## 📑 Оглавление
- [🧠 Поддерживаемые модели](#-нейросети-для-обработки-текста)
- [📦 Установка](#установка)
- [💻 Использование (Python)](#использование)
  - [1. Инициализация клиента](#1-инициализация-клиента)
  - [2. ChatGPT API](#2-chatgpt-api)
  - [3. Генерация изображений](#3-генерация-изображений)
  - [4. Получение баланса](#4-получение-баланса)
  - [5. Редактирование изображений](#5-редактирование-изображений)
  - [6. Генерация видео](#6-генерация-видео)
  - [7. Генерация музыки](#7-генерация-музыки)
  - [8. Озвучка текста (TTS)](#8-озвучка-текста-tts)
  - [9. Генерация звуковых эффектов (Audio)](#9-генерация-звуковых-эффектов-audio)
  - [10. Распознавание речи (STT)](#10-распознавание-речи-stt)
- [💰 Стоимость использования](#-стоимость-использования-моделей)
- [🌐 CURL Примеры](#curl-примеры)

### 💬 Нейросети для обработки текста:

> 💡 **Для работы с длинным контекстом** лучше всего использовать модели **Gemini 4 Argon**, **Gemini 3.5 Flash**, **Gemini 3.5 Flash Lite** или **Gemini 3.0 Pro**.

**OpenAI**
- GPT-5.6-sol / GPT-5.6-terra / GPT-5.6-luna **(временно недоступны)**
- GPT-5 / GPT-5-mini / GPT-5-nano
- GPT-oss
- GPT-4.1 / GPT-4.1-mini / GPT-4.1-nano
- GPT-4o / GPT-4o-mini

**Anthropic (Claude)**
- Claude 5 Opus / Claude 5 Sonnet / Claude 5 Fable **(временно недоступны)**
- Claude 4.5 Sonnet

**Google (Gemini)**
> (на данный момент самые стабильные + поддержка до 800к символов)

- Gemini 4 Argon
- Gemini 3.8 (Flash)
- Gemini 3.0 (Pro, Flash)
- Gemini 3.5 (Flash, Flash Lite)

**DeepSeek**
- DeepSeek V4 (Pro, Flash)
- DeepSeek V3.2 / V3.2 Thinking

**X-Ai (Grok)**
- Grok 4 / Grok 4 Fast

**Другие**
- Cohere: Command R+, Command A
- Moonshot AI: Kimi K2.5 **(временно недоступны)**

### 🎨 Модели для генерации изображений:
- Flux
- Recraft V3
- ChatGPT Images
- Nano Banana 2

### 🖼️ Модели для редактирования изображений:
- Recraft V3
- ChatGPT Images
- Nano Banana 2

### 🎬 Модели для генерации видео:
- Kling 3 (поддержка аудио и видео до 10 секунд)

### 🎵 Модели для генерации музыки (generate/cover/extend):
- Suno V5 / V4.5

### 🗣️ Модели для озвучки текста:
- Gemini TTS (16 голосов: Fola, Kira, Tavi, Ludo, Mako, Riko, Enzo, Rami, Lumi, Veda и др.)

### 🔊 Модели для создания аудио:
- Stable Audio

### 🎙️ Распознавание речи (STT):
- Поддержка `.mp3`, `.wav`, `.ogg`, `.m4a`, `.flac`, `.webm` и других аудиоформатов

## Установка

```bash
pip install git+https://github.com/Badim41/network_tools.git
```

## Использование

### 1. Инициализация клиента

Вы можете использовать как синхронный, так и асинхронный клиент:

```python
from network_tools import NetworkToolsAPI, AsyncNetworkToolsAPI

api_key = "your_api_key_here"

# Синхронный клиент
client = NetworkToolsAPI(api_key)

# Асинхронный клиент
# async_client = AsyncNetworkToolsAPI(api_key)
```

### 2. ChatGPT API

#### Поддерживает файлы .txt, .docx, .pdf, .png, .jpg (как один путь `str`, так и список путей `list[str]`)

```python
from network_tools import GptModels

model = GptModels.gpt_5
prompt = "Что изображено на этих картинках?"
chat_history = []
file_path = "files/cat.png"
# Или несколько файлов сразу:
# file_path = ["files/cat.png", "files/dog.png"]
# file_path = None

response = client.chatgpt_api(prompt, model=model, chat_history=chat_history, file_path=file_path, temperature=0.7)
print(response.response.text)
print(response.cost) # Стоимость запроса, Credits
# 1 Credit = 100₽
```

### 3. Генерация изображений

```python
from network_tools import ImageModels, AspectRatio

models = [ImageModels.nano_banana, ImageModels.flux]
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

### 5. Редактирование изображений

Метод поддерживает удаление фона, inpaint, upscale и многое другое.

```python
from network_tools import ImageChangeModels, Upscale_Mode, ImageModels

image_path = "images/example.png"

# Удаление фона
result_bg = client.change_image_api(
    model=ImageChangeModels.remove_background,
    image_path=image_path,
)
print("Изображение без фона:", next(result_bg))

# Inpaint (изменение части изображения по текстовому запросу)
for stream_result in client.change_image_api(
        model=ImageChangeModels.inpaint,
        image_path=image_path,
        prompt="Сделай кота синим",
        strength=0.5, 
        inpaint_models=[ImageModels.nano_banana]
):
    print("Изменённое изображение (Inpaint):", stream_result)

# Увеличение разрешения (Upscale)
result_upscale = client.change_image_api(
    model=ImageChangeModels.upscale,
    image_path=image_path,
    prompt=Upscale_Mode.quality_HD
)
print("Увеличенное изображение:", next(result_upscale))
```

### 6. Генерация видео

Генерация видео по тексту или изображению (доступна настройка длительности и аудио).

```python
from network_tools import VideoModels

video_path = client.video_generate_api(
    model=VideoModels.kling_3,
    prompt="cat runs",
    image_path="images/example.png",  # Опционально
    duration=5,                       # Длительность: 5 или 10 (секунд)
    with_audio=True                   # С генерацией аудио: True или False
)
print("Путь к видео:", video_path)
```

### 7. Генерация музыки

Создание полноценных треков (с вокалом или инструментальных) с использованием Suno.

```python
from network_tools import MusicModels, SunoMode

music_generator = client.music_generate_api(
    model=MusicModels.suno_v5,
    lyrics="[Instrumental]\n\n[end]",  # Слова песни
    music_style="piano, pop-music, drums, quiet, calm",  # Жанр
    instrumental=False,
    mode=SunoMode.extend  # Или SunoMode.cover
)

# 1. Сначала возвращаются временные ссылки на стрим (если поддерживается)
stream_urls = next(music_generator)
print("Stream URLs:", stream_urls)

# 2. Затем возвращаются скачанные медиафайлы
music_clips = next(music_generator)
for clip in music_clips:
    print("Audio path:", clip.audio_path)
    print("Image path:", clip.image_path)
```

### 8. Озвучка текста (TTS)

```python
from network_tools import TtsModels, GeminiVoices

text = "Привет, это пример озвучки текста через нейросеть Gemini TTS."

for audio_file, status in client.tts_api(
        prompt=text,
        model=TtsModels.gemini_tts,
        voice_id=GeminiVoices.Fola,  # Или Kira, Ludo, Mako, Riko, Enzo и др.
        speed=1.0,
        download_stream=False  # Скачивать ли промежуточные результаты
):
    if status == "success":
        print("Готовый аудиофайл:", audio_file)
    else:
        print("Потоковый аудиофайл (часть):", audio_file)
```

### 9. Генерация звуковых эффектов (Audio)

Создание звуков и эффектов по текстовому описанию.

```python
from network_tools import AudioModels

audio_path = client.audio_generate_api(
    prompt="guitar sound",
    duration=90,
    model=AudioModels.stable_audio,
)
print("Сгенерированный звук:", audio_path)
```

### 10. Распознавание речи (STT)

Перевод голосовых сообщений и аудиофайлов в текст.

```python
stt_result = client.stt_api(
    audio_path="files/voice.ogg",
    lang="ru"  # Опционально (например, "ru", "en"; если None — автоопределение)
)
print("Распознанный текст:", stt_result.text)
```

## Цены

- Цены на текстовые модели в **2 раза ниже** официальных
- Цены на модели изображений в **2 раза ниже** официальных
- Цены на модели редактирования изображений в **2 раза ниже** официальных
- Цены на музыку **до 2 раз ниже** официальных
- Цены на TTS *примерно равны* официальным
- Цены на распознавание речи (STT) в **2 раза ниже** официальных
- Цены на генерацию видео **до 2 раз ниже** официальных


## 💰 Стоимость использования моделей (с учетом скидки 50%)

### Текстовые модели

| Модель                     | 1M входных токенов (Credit) | 1M выходных токенов (Credit) |
|----------------------------|-----------------------------|------------------------------|
| gpt-5.6-sol                | 0.75                        | 4.50                         |
| gpt-5.6-terra              | 0.375                       | 2.25                         |
| gpt-5.6-luna               | 0.15                        | 0.90                         |
| gpt-5-5                    | 2.50                        | 15.00                        |
| gpt-5-4                    | 0.625                       | 7.00                         |
| gpt-5-4-mini               | 0.375                       | 2.25                         |
| gpt-5-3-codex              | 0.625                       | 7.00                         |
| gpt-5-2-pro                | 84.00                       | 10.50                        |
| gpt-5-2                    | 0.625                       | 7.00                         |
| gpt-5-2-high               | 0.625                       | 7.00                         |
| gpt-5-1-high               | 0.875                       | 5.00                         |
| chatgpt-5-1                | 0.625                       | 5.00                         |
| gpt-5-1                    | 0.625                       | 5.00                         |
| gpt-5-high                 | 0.625                       | 5.00                         |
| chatgpt-5                  | 0.625                       | 5.00                         |
| gpt-5                      | 0.625                       | 5.00                         |
| gpt-5-mini                 | 0.125                       | 1.00                         |
| gpt-5-nano                 | 0.0025                      | 0.20                         |
| gpt-5-chat-latest          | 0.625                       | 5.00                         |
| gpt-oss                    | 0.075                       | 0.30                         |
| glm-4.6                    | 0.25                        | 1.00                         |
| claude-5-opus              | 0.75                        | 3.75                         |
| claude-5-sonnet            | 1.00                        | 5.00                         |
| claude-5-fable             | 12.50                       | 62.50                        |
| claude-4-8-opus            | 2.50                        | 12.50                        |
| claude-4-7-opus            | 2.50                        | 12.50                        |
| claude-4-6-opus            | 2.50                        | 12.50                        |
| claude-4-6-sonnet          | 2.50                        | 12.50                        |
| claude-4-5-haiku           | 0.15                        | 0.75                         |
| claude-4-5-opus            | 2.50                        | 12.50                        |
| claude-4-5-opus-thinking   | 2.50                        | 12.50                        |
| claude-4-5-sonnet          | 1.50                        | 7.50                         |
| claude-4-5-sonnet-thinking | 2.50                        | 12.50                        |
| claude-4-opus              | 7.50                        | 37.50                        |
| claude-4-opus-thinking     | 7.50                        | 37.50                        |
| claude-4-1-opus            | 7.50                        | 37.50                        |
| claude-4-1-opus-thinking   | 7.50                        | 37.50                        |
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
| chatgpt-4o                 | 1.25                        | 5.00                         |
| gpt-4o                     | 1.25                        | 5.00                         |
| gpt-4o-mini                | 0.075                       | 0.30                         |
| gpt-3.5                    | 0.50                        | 1.00                         |
| claude-3.7                 | 1.50                        | 7.50                         |
| deepseek-v4-pro            | 0.2175                      | 0.435                        |
| deepseek-v4-flash          | 0.07                        | 0.14                         |
| deepseek-r1                | 0.275                       | 1.095                        |
| deepseek-v3                | 0.135                       | 0.55                         |
| deepseek-v3.2              | 0.135                       | 0.205                        |
| deepseek-v3.2 thinking     | 0.135                       | 0.205                        |
| command-r-plus             | 1.25                        | 5.00                         |
| command-a                  | 1.25                        | 5.00                         |
| command-a-vision           | 1.25                        | 5.00                         |
| c4ai-aya-vision-32b        | 1.25                        | 5.00                         |
| deep-ai-model              | 0.50                        | 1.00                         |
| reka-flash                 | 0.10                        | 0.40                         |
| minimax-01                 | 0.10                        | 0.55                         |
| minimax-02                 | 0.15                        | 0.60                         |
| grok-3                     | 1.50                        | 7.50                         |
| grok-4                     | 1.50                        | 7.50                         |
| grok-4-fast                | 1.50                        | 7.50                         |
| gemini-4-argon             | 1.00                        | 5.00                         |
| gemini-3.8-flash           | 1.50                        | 9.00                         |
| gemini-3.0-pro             | 1.00                        | 6.00                         |
| gemini-3.5-flash           | 1.50                        | 9.00                         |
| gemini-3.5-flash-lite      | 0.15                        | 1.25                         |
| gemini-3.0-flash           | 0.25                        | 1.50                         |
| gemini-2.5-pro             | 0.625                       | 5.00                         |
| gemini-2.5-flash           | 0.075                       | 0.30                         |
| gemini-2.0-flash-lite      | 0.075                       | 0.30                         |
| gemini-2.5-flash-lite      | 0.075                       | 0.30                         |
| kimi-k2-thinking           | 0.30                        | 1.25                         |
| kimi-k2-5                  | 0.30                        | 1.25                         |

## Модели изображений

| Модель         | Стоимость (Credit/изображение) |
|----------------|--------------------------------|
| Flux           | 0.02                           |
| Recraft v3     | 0.02                           |
| ChatGPT Images | 0.085                          |
| Nano Banana 2  | 0.03                           |

## Обработка изображений

| Операция                         | Стоимость (Credit/изображение) |
|----------------------------------|--------------------------------|
| Удаление фона                    | 0.01                           |
| Замена фона                      | 0.04                           |
| Дополнение изображения           | 0.02                           |
| Inpaint (Recraft V3)             | 0.02                           |
| Inpaint (ChatGPT Images)         | 0.085                          |
| Inpaint (Nano Banana 2)          | 0.03                           |
| Upscale                          | 0.01                           |
| Сделать векторным                | 0.01                           |
| Из изображения в 3D-модель       | 0.01                           |

## Генерация видео

| Модель                     | Стоимость (Credit/видео) |
|----------------------------|--------------------------|
| Kling 3 (5s)               | 0.5                      |
| Kling 3 (10s)              | 1.0                      |
| Kling 3 (5s + audio)       | 0.7                      |
| Kling 3 (10s + audio)      | 1.4                      |

## Генерация музыки

| Модель    | Стоимость (Credit/2 трека) |
|-----------|----------------------------|
| Suno v5   | 0.1                        |
| Suno v4.5 | 0.1                        |

## TTS (озвучить текст)

| Модель     | Стоимость (Credit/1000 символов) |
|------------|----------------------------------|
| gemini_tts | 0.03                             |

## Audio (создать звук)

| Модель       | Стоимость |
|--------------|-----------|
| Stable audio | 0.01      |

## STT (распознать речь)

| Операция                 | Стоимость (Credit/запрос) |
|--------------------------|---------------------------|
| Распознавание речи (STT) | 0.003                     |

## CURL Примеры

### 💬 ChatGPT

#### Обычный запрос (при передаче нескольких файлов `file_base64` и `mime_type` могут быть массивами `list[str]`)

```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/chatgpt \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "gpt-4o", "prompt": "Привет!", "chat_history": [], "file_base64": "", "internet_access": false, "mime_type":"", "temperature": 0.7}'
```

#### С текстовым файлом в base64:

```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/chatgpt \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "gpt-4o", "prompt": "Что это за текст?", "chat_history": [], "file_base64": "IyMjINCX0LDQs9Cw0LTQutCwINC60L7RiNCw0YfRjNC10Lkg0L/RgNC40YDQvtC00YsNCg0K0JrQvtGC0Ysg4oCTINC+0LTQvdC4INC40Lcg0YHQsNC80YvRhSDQt9Cw0LPQsNC00L7Rh9C90YvRhSDRgdC+0LfQtNCw0L3QuNC5INC90LAg0L3QsNGI0LXQuSDQv9C70LDQvdC10YLQtS4g0J3QtdGB0LzQvtGC0YDRjyDQvdCwINGC0L4sINGH0YLQviDQvtC90Lgg0LbQuNCy0YPRgiDQsdC+0Log0L4g0LHQvtC6INGBINGH0LXQu9C+0LLQtdC60L7QvCDRgtGL0YHRj9GH0LXQu9C10YLQuNGP0LzQuCwg0LIg0LjRhSDQv9C+0LLQtdC00LXQvdC40LgsINC40L3RgdGC0LjQvdC60YLQsNGFINC4INGB0YPRidC90L7RgdGC0Lgg0L7RgdGC0LDQtdGC0YHRjyDRh9GC0L4t0YLQviDQvdC10L7QsdGK0Y/RgdC90LjQvNC+0LUsINC/0YDQuNGC0Y/Qs9C40LLQsNGO0YnQtdC1INCy0L3QuNC80LDQvdC40LUuDQoNCtCf0L7Rh9C10LzRgyDQutC+0YLRiyDRgtCw0Log0LvRjtCx0Y/RgiDQutC+0YDQvtCx0LrQuCwg0LTQsNC20LUg0LXRgdC70Lgg0L7QvdC4INGP0LLQvdC+INC80LDQu9GLINC00LvRjyDQvdC40YU/INCc0L7QttC10YIg0LHRi9GC0YwsINGN0YLQviDRgdCy0Y/Qt9Cw0L3QviDRgSDQuNC90YHRgtC40L3QutGC0LjQstC90YvQvCDQttC10LvQsNC90LjQtdC8INGB0L/RgNGP0YLQsNGC0YzRgdGPINCyINCx0LXQt9C+0L/QsNGB0L3QvtC8INC/0YDQvtGB0YLRgNCw0L3RgdGC0LLQtSwg0LjQu9C4INC20LUg0YLRg9GCINGB0LrRgNGL0YIg0LrQsNC60L7QuS3RgtC+INC00YDRg9Cz0L7QuSwg0L3QtdC40LfQstC10YHRgtC90YvQuSDQvNC+0YLQuNCyPw0KDQrQmNC70Lgg0LLQvtC30YzQvNC10Lwg0LjRhSDRgdC/0L7RgdC+0LHQvdC+0YHRgtGMINCy0YHQtdCz0LTQsCDQv9Cw0LTQsNGC0Ywg0L3QsCDQu9Cw0L/Riy4g0K3RgtC+INGE0LXQvdC+0LzQtdC9LCDQutC+0YLQvtGA0YvQuSDQsdC40L7Qu9C+0LPQuNGPINGH0LDRgdGC0LjRh9C90L4g0L7QsdGK0Y/RgdC90LjQu9CwIOKAkyDRgyDQutC+0YjQtdC6INC90LXQstC10YDQvtGP0YLQvdC+INCz0LjQsdC60LjQuSDQv9C+0LfQstC+0L3QvtGH0L3QuNC6INC4INGA0LDQt9Cy0LjRgtC+0LUg0YfRg9Cy0YHRgtCy0L4g0YDQsNCy0L3QvtCy0LXRgdC40Y8uINCd0L4g0LrQsNC20LTRi9C5INGA0LDQtywg0LrQvtCz0LTQsCDQvNGLINCy0LjQtNC40LwsINC60LDQuiDQvtC90Lgg0LvQvtCy0LrQviDQv9C10YDQtdCy0L7RgNCw0YfQuNCy0LDRjtGC0YHRjyDQsiDQstC+0LfQtNGD0YXQtSwg0LrQsNC20LXRgtGB0Y8sINCx0YPQtNGC0L4g0LfQtNC10YHRjCDQt9Cw0LzQtdGI0LDQvdCwINC80LDQs9C40Y8uDQoNCtCQINC40YUg0LfQsNCz0LDQtNC+0YfQvdGL0LkgItC80YPRgNGA0YAiPyDQrdGC0L4g0L3QtSDQv9GA0L7RgdGC0L4g0LfQstGD0Log4oCTINGN0YLQviDRg9C90LjQstC10YDRgdCw0LvRjNC90YvQuSDRj9C30YvQuiwg0YEg0L/QvtC80L7RidGM0Y4g0LrQvtGC0L7RgNC+0LPQviDQutC+0YIg0LzQvtC20LXRgiDQvtC00L3QvtCy0YDQtdC80LXQvdC90L4g0LLRi9GA0LDQttCw0YLRjCDQutC+0LzRhNC+0YDRgiwg0LTQvtCy0LXRgNC40LUg0LguLi4g0LHQvtC70YwuINCc0YPRgNC70YvQutCw0L3RjNC1INC00LDQttC1INGB0L/QvtGB0L7QsdC90L4g0LfQsNC20LjQstC70Y/RgtGMINGC0LrQsNC90Lgg0LHQu9Cw0LPQvtC00LDRgNGPINCy0LjQsdGA0LDRhtC40Y/QvCDQvtC/0YDQtdC00LXQu9C10L3QvdC+0Lkg0YfQsNGB0YLQvtGC0YssINC90L4g0LrQsNC6INC60L7RgtGLINC90LDRg9GH0LjQu9C40YHRjCDQuNGB0L/QvtC70YzQt9C+0LLQsNGC0Ywg0LXQs9C+INGC0LDQuiDRjdGE0YTQtdC60YLQuNCy0L3Qvj8NCg0K0JgsINC60L7QvdC10YfQvdC+LCDQs9C70LDQstC90YvQuSDQstC+0L/RgNC+0YE6INC/0L7Rh9C10LzRgyDQutC+0YLRiyDRgdC80L7RgtGA0Y/RgiDQsiDQv9GD0YHRgtC+0YLRgz8g0JjQvdC+0LPQtNCwINC60LDQttC10YLRgdGPLCDRh9GC0L4g0L7QvdC4INCy0LjQtNGP0YIg0YLQviwg0YfRgtC+INGB0LrRgNGL0YLQviDQvtGCINGH0LXQu9C+0LLQtdGH0LXRgdC60L7Qs9C+INCz0LvQsNC30LAuINCU0YPRhdC+0LIsINC/0LDRgNCw0LvQu9C10LvRjNC90YvQtSDQvNC40YDRiywg0LjQu9C4LCDQvNC+0LbQtdGCINCx0YvRgtGMLCDQv9GA0L7RgdGC0L4g0L/Ri9C70LjQvdC60Lgg0LIg0YHQvtC70L3QtdGH0L3QvtC8INC70YPRh9C1PyDQkiDQu9GO0LHQvtC8INGB0LvRg9GH0LDQtSDQuNGFINCy0LfQs9C70Y/QtCDRgdC70L7QstC90L4g0LPQvtCy0L7RgNC40YI6ICLQldGB0YLRjCDQstC10YnQuCwg0LrQvtGC0L7RgNGL0LUg0YLQtdCx0LUg0L3QtSDQtNCw0L3QviDQv9C+0L3Rj9GC0YwiLg0KDQrQmtC+0YLRiyDigJMg0Y3RgtC+INC90LUg0L/RgNC+0YHRgtC+INC20LjQstC+0YLQvdGL0LUsINGN0YLQviDRhdC+0LTRj9GH0LjQtSDQt9Cw0LPQsNC00LrQuCwg0LrQvtGC0L7RgNGL0LUg0L3QuNC60L7Qs9C00LAg0L3QtSDQv9C10YDQtdGB0YLQsNGO0YIg0YPQtNC40LLQu9GP0YLRjC4g0JzQvtC20LXRgiDQsdGL0YLRjCwg0LjQvNC10L3QvdC+INCyINGN0YLQvtC8INC40YUg0LLQvtC70YjQtdCx0YHRgtCy0L4g4oCTINC+0L3QuCDQvtGB0YLQsNGO0YLRgdGPINC30LDQs9Cw0LTQutC+0LksINGH0LDRgdGC0YzRjiDQutC+0YLQvtGA0L7QuSDQvNGLINGF0L7RgtC40Lwg0YHRgtCw0YLRjC4=", "internet_access": false, "mime_type":"text/plain"}'
```

### 🎨 Генерация изображений

```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/image_generate \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"models": ["nano_banana"], "aspect_ratio": "1:1", "prompt": "A futuristic city with flying cars"}'
```

### 🖼️ Редактирование изображений

#### Удаление фона
```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/image_change \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "remove_background", "file_base64": "iVBORw0KGgo...", "mime_type": "image/png", "prompt": "", "prompt_2": "", "strength": 0.5, "inpaint_models": [], "send_url": false}'
```

#### Апскейл (увеличение разрешения)
```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/image_change \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "upscale", "file_base64": "iVBORw0KGgo...", "mime_type": "image/jpeg", "prompt": "HD", "prompt_2": "", "strength": 0.5, "inpaint_models": [], "send_url": false}'
```

#### Изменение части изображения (Inpaint)
```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/image_change \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "inpaint", "file_base64": "iVBORw0KGgo...", "mime_type": "image/jpeg", "prompt": "Сделай кота синим", "prompt_2": "", "strength": 0.5, "inpaint_models": ["nano_banana"], "send_url": false}'
```

### 🎬 Генерация видео

#### По текстовому промпту
```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/video_generate \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "kling-3", "file_base64": "", "prompt": "A cat running in a futuristic city", "aspect_ratio": "16:9", "duration": 5, "with_audio": false, "send_url": false}'
```

#### На основе изображения (Kling 3)
```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/video_generate \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "kling-3", "file_base64": "iVBORw0KGgo...", "prompt": "A cat running", "aspect_ratio": "16:9", "duration": 10, "with_audio": true, "send_url": false}'
```

### 🎵 Генерация музыки

#### Создание трека (Suno v5)
```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/music_generate \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "suno_v5", "lyrics": "[Verse] Hello world!", "music_style": "pop", "instrumental": false, "return_images": true, "mode": "extend", "send_url": false}'
```

### 🗣️ Озвучка текста (TTS)

```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/tts \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "gemini_tts", "prompt": "Привет, это тест озвучки через Gemini TTS!", "params": {"speed": 1.0, "voice_id": "Fola"}}'
```

### 🔊 Генерация звука (Audio)

```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/audio_generate \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"model": "stable_audio", "prompt": "guitar solo, acoustic", "file_base64": "", "duration": 90, "steps": 50, "cfg_scale": 7.0, "strength": 1.0, "seed": 0, "send_url": false}'
```

### 🎙️ Распознавание речи (STT)

#### Передача аудио в Base64 (JSON)
```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/stt \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY' \
  --data '{"file_base64": "UklGRiQAAABXQVZFZm10...", "mime_type": "audio/wav", "lang": "ru"}'
```

#### Передача файла напрямую (multipart/form-data)
```bash
curl --request POST \
  --url https://sert.yellowfire.ru:444/api/v2/stt \
  --header 'api-key: API_KEY' \
  --form 'file=@voice.ogg' \
  --form 'lang=ru'
```

### 🔄 Проверка статуса (для всех асинхронных задач)

После отправки POST-запроса вы получите `request_id`. Используйте его для опроса статуса выполнения задачи:

```bash
curl --request GET \
  --url https://sert.yellowfire.ru:444/api/v2/status/ВАШ_REQUEST_ID \
  --header 'api-key: API_KEY'
```

### 💳 Получение баланса

```bash
curl --request GET \
  --url https://sert.yellowfire.ru:444/api/v2/user \
  --header 'Content-Type: application/json' \
  --header 'api-key: API_KEY'
```
