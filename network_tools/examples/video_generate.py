from network_tools import NetworkToolsAPI, VideoModels

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

result = client.video_generate_api(
    model=VideoModels.veo_3,
    prompt="cat runs",
    image_path="example_files/cat_large.png"
)
print("Video path:", result)
