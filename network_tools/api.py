import base64
import mimetypes
import os
import time

import requests

from ._types import *


class NetworkToolsAPI:
    def __init__(self, api_key, output_dir="images"):
        self.api_url = "https://yellowfire.ru"
        self.api_key = api_key
        self.output_dir = output_dir

    def _file_to_base64(self, file_path):
        """Конвертирует файл в строку base64"""
        with open(file_path, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode("utf-8")
        return encoded_string

    @staticmethod
    def _get_mime_type(file_path):
        mime_type, encoding = mimetypes.guess_type(file_path)

        if not mime_type:
            extension_to_mime = {
                # Аудио
                '.mp3': 'audio/mpeg',
                '.wav': 'audio/wav',
                '.ogg': 'audio/ogg',
                '.flac': 'audio/flac',

                # Видео
                '.mp4': 'video/mp4',
                '.avi': 'video/x-msvideo',
                '.mov': 'video/quicktime',
                '.mkv': 'video/x-matroska',

                # Изображения
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp',
                '.svg': 'image/svg+xml',

                # Текстовые файлы
                '.txt': 'text/plain',
                '.csv': 'text/csv',
                '.json': 'application/json',
                '.xml': 'application/xml',

                # Документы
                '.doc': 'application/msword',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                '.pdf': 'application/pdf',
                '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            }

            # Получаем расширение файла
            _, extension = os.path.splitext(file_path)

            # Приводим расширение к нижнему регистру и ищем в словаре
            mime_type = extension_to_mime.get(extension.lower(), None)

        if not mime_type:
            raise UnknownMimetype(f"Не найден mime_type: {file_path}")
        return mime_type

    def chatgpt_api(self, prompt, model=GptModels.gpt_4o, chat_history=[], file_path=None,
                    internet_access=False) -> GptResponse:
        url = f"{self.api_url}/api/v2/chatgpt"

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        # Если файл указан, конвертируем его в base64
        file_base64 = None
        mime_type = None
        if file_path:
            file_base64 = self._file_to_base64(file_path)
            mime_type = self._get_mime_type(file_path)
            # print("mime_type", mime_type)

        payload = {
            "model": model,
            "prompt": prompt,
            "chat_history": chat_history,
            "file_base64": file_base64 or "",  # если нет base64, передаем пустую строку
            "internet_access": internet_access,
            "mime_type": mime_type
        }

        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        # Ожидание и повторный запрос статуса, пока не получим успех

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        time.sleep(response_data.get("wait", 5))
        if not request_id:
            raise NetworkToolsError("Request ID not found in response")

        if model == GptModels.o1:
            attempts = 60
        else:
            attempts = 30

        return self._check_status(request_id, attempts=attempts)

    def get_usage(self) -> UserUsage:
        url = f"{self.api_url}/api/v2/user"

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        response = requests.get(url, headers=headers, json="")
        response_data = response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        return UserUsage.from_dict(response_data)

    def _check_status(self, request_id, attempts=60) -> GptResponse:
        """Запрашивает статус запроса, пока он не станет 'success'."""
        url = f"{self.api_url}/api/v2/status/{request_id}"

        for i in range(attempts):
            response = requests.get(url)

            result = response.json()
            if result.get("error"):
                raise NetworkToolsError(result.get("error"))
            if result["status"] == "success":
                # print(result.get("count_tokens"))
                return GptResponse.from_json(result)

            time.sleep(2)  # Ждем 2 секунды перед следующим запросом
        else:
            raise NetworkToolsTimeout(f"Timeout for id {request_id}")

    def test_image_generate(self, models, prompt, aspect_ratio):
        """
        :param models: List[obj[ImageModels]]
        :param prompt: запрос
        :param aspect_ratio: obj[AspectRatio]
        :return:
        """
        url = f"{self.api_url}/api/v2/image_generate"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        data = {
            "models": models,
            "aspect_ratio": aspect_ratio,
            "prompt": prompt
        }

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        time.sleep(response_data.get("wait", 10))
        if not request_id:
            return {"status": "error", "error": "Request ID not found in response"}

        return self._check_status_stream(request_id)

    def _check_status_stream(self, request_id, attempts=180):
        """Проверяет статус запроса до получения 'success' и сохраняет изображения."""
        os.makedirs(self.output_dir, exist_ok=True)

        url = f"{self.api_url}/api/v2/status/{request_id}"

        for i in range(attempts):
            response = requests.get(url)
            status_data = response.json()
            # print(status_data)

            model_was = []
            status = status_data.get("status")
            if status_data.get("status") in ["stream", "success"]:
                # сохраняем изображения
                images = status_data.get("response", {})
                image_paths_list = []
                for model, image_paths in images.items():
                    if model in model_was:
                        continue
                    model_was.append(model)
                    for i, img_base64 in enumerate(image_paths):
                        file_path = self._save_image(img_base64, model, i, request_id)
                        # print(f"Image saved at: {file_path}")
                        image_paths_list.append(file_path)
                    yield image_paths_list
            if status == "success":
                # print(f"Image generation complete! Response: {json.dumps(status_data, indent=2)}")
                return
            elif "error" in status_data:
                raise NetworkToolsError(f"Error occurred: {status_data['error']}")

            time.sleep(5)  # wait

    def _save_image(self, img_base64, model, index, request_id):
        """Сохраняет изображение из base64 в файл."""
        img_data = base64.b64decode(img_base64.split(",")[1])
        file_name = f"{model}_{index}_{request_id}.png"
        file_path = os.path.join(self.output_dir, file_name)

        with open(file_path, "wb") as f:
            f.write(img_data)

        return file_path