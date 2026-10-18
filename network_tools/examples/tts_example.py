from network_tools import NetworkToolsAPI, TtsModels, GeminiVoices

api_key = "API-KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

text = "Привет! Это пример синтеза речи через Gemini TTS. Вы можете выбрать подходящего спикера и скорость произношения."

# Доступные голоса в GeminiVoices:
# Женские: Fola, Kira, Tavi, Jori, Veda, Lumi
# Мужские: Ludo, Mako, Brio, Rami, Enzo, Riko, Sami, Cruz, Zeno, Varo

for audio_file, status in client.tts_api(
        prompt=text,
        model=TtsModels.gemini_tts,
        voice_id=GeminiVoices.Fola,
        speed=1.0,
        download_stream=False  # скачивать ли промежуточные чанки
):
    if status == "success":
        print("Готовый аудиофайл:", audio_file)
    else:
        print("Потоковый чанк:", audio_file)
