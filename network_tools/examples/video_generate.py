from network_tools import NetworkToolsAPI, VideoModels

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

# result = client.video_generate_api(
#     model=VideoModels.hailuo,
#     prompt="cat runs", # или None
#     image_path="example_files/cat.png" # или None
# )
# print("Video path:", result)


result = client.video_generate_api(
    model=VideoModels.stable_video_diffusion, # не поддерживает prompt
    image_path="example_files/cat.png"
)
print("Video path:", result)
