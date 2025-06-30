from network_tools import NetworkToolsAPI, TtsModels, HailuoLanguages, HailuoModelIds, ElevenlabsVoices

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

model = TtsModels.hailuo
text = "Привет, это просто пример произношения текста. Вы можете указать скорость, язык и даже id голоса для озвучки. Метод выдаёт аудио потоком, а потом выводит итоговый файл."
for audio_file, status in client.tts_api(prompt=text, model=model, speed=1.0, lang=HailuoLanguages.auto, model_id=HailuoModelIds.speech_02_hd):
    if status == "success":
        print("Готовый аудио:", audio_file)
    else:
        print("Потоковый аудио:", audio_file)


model = TtsModels.elevenlabs
for audio_file, status in client.tts_api(prompt=text, model=model, speed=1.0, voice_id=ElevenlabsVoices.Bea):
    if status == "success":
        print("Готовый аудио:", audio_file)
    else:
        print("Потоковый аудио:", audio_file)