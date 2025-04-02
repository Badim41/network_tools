from network_tools import NetworkToolsAPI, ImageModels, AspectRatio

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

models = [ImageModels.gemini]
prompt = "A futuristic cityscape with flying cars."
aspect_ratio = AspectRatio.ratio_1x1

# send_url - отправить временную ссылку
for image_group in client.image_generate_api(models, prompt, aspect_ratio, send_url=True):
    print("image_group", image_group)
