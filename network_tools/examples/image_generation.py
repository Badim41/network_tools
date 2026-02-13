from network_tools import NetworkToolsAPI, ImageModels, AspectRatio

api_key = "API_KEY"   # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

models = [ImageModels.nano_banana_pro]
prompt = "A futuristic cityscape with flying cars."
aspect_ratio = AspectRatio.ratio_1x1

# send_url - отправить временную ссылку
for image_group in client.image_generate_api(models, prompt, aspect_ratio, send_url=True):
    print("image_group", image_group)

# models = [ImageModels.flux]
# prompt = "Dark forest"
# aspect_ratio = AspectRatio.ratio_3x2
#
# # return_minimal_images=False - вернуть 4 картинки за раз
# for image_group in client.image_generate_api(models, prompt, aspect_ratio, return_minimal_images=False):
#     print("image_group", image_group)
