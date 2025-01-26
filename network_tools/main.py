from datetime import datetime

from network_tools import NetworkToolsAPI, GptModels, ImageModels, AspectRatio

if __name__ == "__main__":
    api_key = "badim_unlimit_key_1221"  # замените на ваш API ключ

    client = NetworkToolsAPI(api_key)

    input("Next?")

    model = GptModels.gpt_4o  # модель

    prompt = "Что это?"
    chat_history = []
    file_path = r"example_files\cat.png"

    internet_access = False  # Установите True, если требуется доступ к интернету

    response = client.chatgpt_api(prompt, model=model, chat_history=chat_history, file_path=file_path,
                                  internet_access=internet_access)
    print(response.response.text)
    # print(response.chat_history)

    input("Next?")

    # 2 запрос
    prompt = "О чём этот текст? Какого цвета прошлое изображение?"
    chat_history = response.chat_history
    file_path = r"example_files\test.txt"

    response = client.chatgpt_api(prompt, model=model, chat_history=chat_history, file_path=file_path,
                                  internet_access=internet_access)
    print(response.response.text)
    print(response.chat_history)

    input("Next?")

    models = [ImageModels.kandinsky, ImageModels.dalle_light]
    prompt = "A futuristic cityscape with flying cars."
    aspect_ratio = AspectRatio.ratio_1x1

    for image_group in client.test_image_generate(models, prompt, aspect_ratio):
        print(image_group)

    input("Next?")

    user_usage = client.get_usage()

    for request in user_usage.response.usage:
        timestamp = datetime.fromtimestamp(request.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        comment = request.comment
        balance_change = f"{request.balance_change:.8f}"  # Вывод с 8 знаками после запятой
        print(f"{timestamp:<20} {comment:<60} {balance_change:<15}")

    print("Balance left:", user_usage.response.balance)
