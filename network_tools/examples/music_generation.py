from network_tools import NetworkToolsAPI, MusicModels, SunoMode

api_key = "API_KEY"   # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

test_lyrics = """[Verse 1]
Утренний свет падает на стекло,
Город молчит, вокруг легко и тепло.
Клавиши мягко звучат в тишине,
Мысли плывут в спокойной волне.

[Chorus]
Сквозь суету и шум дорог,
Пусть этот ритм согреет вечер.
Звуки рояля развеют тревог,
Даря покой при нашей встрече.

[Verse 2]
Время замедлит привычный бег,
Падает с неба кружащийся снег.
Каждая нота ложится в строку,
Я этот миг для тебя сберегу.

[Outro]
Музыка тает в ночной тиши...
Слушай дыханье своей души.
[End]"""

music_generator = client.music_generate_api(
    model=MusicModels.suno_v4,
    lyrics=test_lyrics,  # слова песни
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

