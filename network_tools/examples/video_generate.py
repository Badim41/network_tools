from network_tools import NetworkToolsAPI, VideoModels
from network_tools._types import VideoAspectRatio

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

result = client.video_generate_api(
    model=VideoModels.veo_3,
    prompt="cat runs",
    aspect_ratio=VideoAspectRatio.ratio_16x9
    # image_path="example_files/cat_large.png" # kling-1.6 supports only
)
print("Video path:", result)
