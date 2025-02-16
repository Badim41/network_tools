from network_tools import NetworkToolsAPI, MusicModels

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

result = client.music_generate_api(
    model=MusicModels.suno_v4,  # Или riffusion
    lyrics="[Instrumental]",
    music_style="rock",
    instrumental=False
)

print("Stream urls:", next(result)) # riffusion не поддерживает их. Будет пустой ответ
print("Audio files:", next(result))
