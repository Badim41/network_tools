from network_tools import NetworkToolsAPI, MusicModels, SunoMode

api_key = "API_KEY"   # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

music_generator = client.music_generate_api(
    model=MusicModels.suno_v4,
    lyrics="[Instrumental]\n\n[end]",  # слова песни
    music_style="piano, pop-music, drums, quite, calm",  # жанр музыки
    instrumental=False,
)

stream_urls = next(music_generator)
print("Stream urls:", stream_urls)

music_clips = next(music_generator)
for clip in music_clips:
    print("Audio path:", clip.audio_path)
    print("Image path:", clip.image_path)
    print("lyric timestamps:", clip.lyric_timestamps)

