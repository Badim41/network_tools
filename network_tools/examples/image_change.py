from network_tools import NetworkToolsAPI, ImageChangeModels, Upscale_Mode

# Пример картинки. Замените на изображение
image_path = "example_files/cat.png"

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

# Удаление фона
result = client.change_image_api(
    model=ImageChangeModels.remove_background,
    image_path=image_path,
)
print("Изображение без фона:", next(result))

# Изменить фон
result = client.change_image_api(
    model=ImageChangeModels.change_background,
    image_path=image_path,
    prompt="Лесной пейзаж"
)
print("Изображение c изменённым фоном:", next(result))

# Расширение изображения (outpaint)
result = client.change_image_api(
    model=ImageChangeModels.outpaint,
    image_path=image_path
)
print("Расширенное изображение:", next(result))

# Изменение изображения (inpaint) # todo не работает
for stream_result in client.change_image_api(
        model=ImageChangeModels.inpaint,
        image_path=image_path,
        prompt="То, что должно быть на картинке",
        prompt_2="То, чего не должно быть на картинке",
):
    print("Изменённое изображение:", stream_result)

# Увеличение разрешения (upscale)
result = client.change_image_api(
    model=ImageChangeModels.upscale,
    image_path=image_path,
    prompt=Upscale_Mode.quality_HD
)
print("Увеличенное изображение:", next(result))

# Добавить текст (только английские буквы)
result = client.change_image_api(
    model=ImageChangeModels.add_text,
    image_path=image_path,
    prompt="Hello world!"
)
print("Изображение с текстом:", next(result))

# Изображение с таким же стилем
result = client.change_image_api(
    model=ImageChangeModels.style,
    image_path=image_path,
    prompt="Собака"
)
print("Изображение с таким же стилем:", next(result))

# Найти и заменить объект на картинке
result = client.change_image_api(
    model=ImageChangeModels.search_and_replace,
    image_path=image_path,
    prompt="Кот",  # из чего
    prompt_2="Собака"  # во что
)
print("Изображение с таким же стилем:", next(result))

# Сделать 3D модель из картинки # todo не работает
result = client.change_image_api(
    model=ImageChangeModels.model_3d,
    image_path=image_path
)
print("Изображение в 3D:", next(result))
