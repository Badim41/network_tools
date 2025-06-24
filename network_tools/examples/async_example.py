import asyncio
import sys

from network_tools import GptModels, ImageModels, AspectRatio
from network_tools.api import AsyncNetworkToolsAPI

API_KEY = "API-KEY"

async def main():
    api = AsyncNetworkToolsAPI(api_key=API_KEY)

    try:
        async for images in api.image_generate_api(
                models=[ImageModels.flux],
                prompt="красивый пейзаж",
                aspect_ratio=AspectRatio.ratio_1x1
        ):
            print(f"Generated images: {images}")

            # Пример использования ChatGPT
        response = await api.chatgpt_api(
            prompt="Привет, как дела?",
            model=GptModels.gpt_4o
        )
        print("gpt", response.response.text)

        # Пример стриминга ChatGPT
        async for chunk in await api.chatgpt_api(
                prompt="Скажи 'Тест'",
                model=GptModels.chatgpt_4o,
                stream=True
        ):
            print(chunk.response.text, end='')
    finally:
        await api.session.close()


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
