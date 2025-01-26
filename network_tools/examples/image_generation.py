from network_tools import NetworkToolsAPI, ImageModels, AspectRatio

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

models = [ImageModels.sd_xl, ImageModels.dalle_light]
prompt = "A futuristic cityscape with flying cars."
aspect_ratio = AspectRatio.ratio_1x1

for image_group in client.test_image_generate(models, prompt, aspect_ratio):
    print(image_group)
