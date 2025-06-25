from network_tools import NetworkToolsAPI, AudioModels

api_key = "API-KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

audio_path = client.audio_generate_api(
    prompt="gitar sound",
    duration=90,
    # audio_path="audio_path.mp3",  # input audio file
    model=AudioModels.stable_audio,
)

print("audio_path", audio_path)
