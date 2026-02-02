from network_tools import NetworkToolsAPI, TtsModels, ModelV3Voices, ModelV3Languages

api_key = "API-KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

text = "Привет, это просто пример произношения текста. Вы можете указать скорость, язык и даже id голоса для озвучки. Метод выдаёт аудио потоком, а потом выводит итоговый файл."

model = TtsModels.voice_model_v3

# (voice clone)
reference_audio_file = "example_files/file.wav" # only WAV file supported

for audio_file, status in client.tts_api(
        prompt=text,
        model=model,
        speed=1.0,
        voice_id=ModelV3Voices.ru_RU_MALE,
        lang=ModelV3Languages.Russian_Russia,
        reference_audio_wav=reference_audio_file,
        download_stream=False # скачивать промежуточные результаты
):
    if status == "success":
        print("Готовый аудио:", audio_file)
    else:
        print("Потоковый аудио:", audio_file)