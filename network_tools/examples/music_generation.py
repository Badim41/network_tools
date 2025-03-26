from network_tools import NetworkToolsAPI, MusicModels

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

music_generator = client.music_generate_api(
    model=MusicModels.riffusion,  # Или MusicModels.riffusion
    lyrics="[Instrumental]",
    music_style="rock",
    instrumental=False
)

stream_urls = next(music_generator)
print("Stream urls:", stream_urls)  # Для riffusion будет [], для suno_v4 может быть список URL

music_clips = next(music_generator)
for clip in music_clips:
    print("Audio path:", clip.audio_path)
    print("Image path:", clip.image_path)
