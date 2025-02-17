import base64
import mimetypes
import os
import time

import requests

from ._types import *

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

    # 3D модели
    '.glb': 'model/gltf-binary',
    '.gltf': 'model/gltf+json',

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


class NetworkToolsAPI:
    def __init__(self, api_key, output_dir="images"):
        self.api_url = "https://yellowfire.ru"
        self.api_key = api_key
        self.output_dir = output_dir

    @staticmethod
    def _file_to_base64(file_path):
        """Конвертирует файл в строку base64"""
        with open(file_path, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode("utf-8")
        return encoded_string

    @staticmethod
    def _get_mime_type(file_path):
        mime_type, encoding = mimetypes.guess_type(file_path)

        if not mime_type:
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
        if not request_id:
            raise NetworkToolsError("Request ID not found in response")
        time.sleep(response_data.get("wait", 5))

        if model == GptModels.o1:
            attempts = 60
        else:
            attempts = 30

        return GptResponse.from_json(self._check_status(request_id, attempts=attempts))

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

    def _check_status(self, request_id, attempts=60, delay=2) -> dict:
        """Запрашивает статус запроса, пока он не станет 'success'."""
        url = f"{self.api_url}/api/v2/status/{request_id}"

        for i in range(attempts):
            response = requests.get(url)

            result = response.json()
            if result.get("error"):
                raise NetworkToolsError(result.get("error"))
            if result["status"] == "success":
                # print(result.get("count_tokens"))
                return result

            time.sleep(delay)  # Ждем 2 секунды перед следующим запросом
        else:
            raise NetworkToolsTimeout(f"Timeout for id {request_id}")

    def image_generate_api(self, models, prompt, aspect_ratio):
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
        if not request_id:
            return {"status": "error", "error": "Request ID not found in response"}
        time.sleep(response_data.get("wait", 10))

        return self._check_status_stream(request_id)

    def change_image_api(self, model, image_path, prompt="", prompt_2=""):
        """
        Отправляет изображение на обработку (удаление фона, апскейл и т. д.).

        :param model: str, тип обработки (использует ImageChangeModels)
        :param image_path: str, путь к файлу изображения
        :param prompt: str, основной текстовый запрос
        :param prompt_2: str, дополнительный текстовый запрос
        :return: список путей обработанных изображений
        """
        url = f"{self.api_url}/api/v2/image_change"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        file_base64 = self._file_to_base64(image_path)
        mime_type = self._get_mime_type(image_path)

        data = {
            "model": model,
            "file_base64": file_base64,
            "mime_type": mime_type,
            "prompt": prompt,
            "prompt_2": prompt_2
        }

        response = requests.post(url, headers=headers, json=data)
        # print(response.text)
        response_data = response.json()

        if response_data.get("error"):
            raise Exception(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        time.sleep(response_data.get("wait", 5))

        return self._check_status_stream(request_id)

    def music_generate_api(self, model, lyrics, file_path=None, music_style="piano", instrumental=False):
        """
        Sends a request to generate music using the specified model and input data.

        :param model: str, type of model for music generation (e.g., 'riffusion', 'suno')
        :param file_path: str, path to an audio file (optional, for models that support file input)
        :param lyrics: str, lyrics to guide the music generation
        :param music_style: str, style of music to generate (e.g., 'piano', 'jazz')
        :param instrumental: bool, whether to generate instrumental music
        :return: audio_urls, audio_paths
        """
        url = f"{self.api_url}/api/v2/music_generate"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        data = {
            "model": model,
            "lyrics": lyrics,
            "music_style": music_style,
            "instrumental": instrumental
        }

        if file_path:
            file_base64 = self._file_to_base64(file_path)
            data["file_base64"] = file_base64

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        if response_data.get("error"):
            raise Exception(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        time.sleep(response_data.get("wait", 5))

        return self._check_music_status(request_id)

    def video_generate_api(self, model, image_path=None, prompt=""):
        """
        Отправляет запрос на генерацию видео.

        :param model: str, модель генерации видео
        :param prompt: [str, None], текстовый запрос
        :param image_path: [str, None], путь к изображению
        :return: video_path
        """
        if prompt and model == VideoModels.stable_video_diffusion:
            raise ValueError("VideoModels.stable_video_diffusion не поддерживает prompt")
        url = f"{self.api_url}/api/v2/video_generate"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        if image_path:
            file_base64 = self._file_to_base64(image_path)
        else:
            file_base64 = ""

        data = {
            "model": model,
            "file_base64": file_base64,
            "prompt": prompt
        }

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        if response_data.get("error"):
            raise Exception(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        time.sleep(response_data.get("wait", 5))

        video_data = self._check_status(request_id, attempts=600, delay=5)
        video_base64 = video_data['response'][model][0]
        return self._save_base64(video_base64, model, "0", request_id)

    def tts_api(self, prompt: str, model: str, speed: int = 0, lang: str = "Auto", voice_id: str = None) -> str:
        """
        Отправляет запрос на генерацию аудио (TTS).

        :param prompt: str, текст для озвучки
        :param model: str, модель генерации голоса
        :param speed: int, скорость речи (по умолчанию 0)
        :param lang: str, язык (по умолчанию "Auto")
        :param voice_id: Optional[str], ID голоса (если None, выбирается по языку)
        :return: List[str], пути к аудиофайлам
        """
        url = f"{self.api_url}/api/v2/tts"
        headers = {"Content-Type": "application/json", "api-key": self.api_key}

        # Получаем голос по умолчанию, если не передан
        if not voice_id:
            voice_id = "226893671006272"

        data = {
            "model": model,
            "prompt": prompt,
            "params": {
                "speed": speed,
                "lang": lang,
                "voice_id": voice_id
            }
        }

        response = requests.post(url, headers=headers, json=data).json()

        if "error" in response:
            raise Exception(response["error"])

        request_id = response.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        audio_data = self._check_status_stream_tts(request_id)
        audio_base64 = audio_data["response"][model][0]
        return self._save_base64(audio_base64, model, request_id, request_id)

    def _check_status_stream(self, request_id, attempts=180):
        """Проверяет статус запроса до получения 'success' и сохраняет изображения."""
        os.makedirs(self.output_dir, exist_ok=True)

        url = f"{self.api_url}/api/v2/status/{request_id}"
        model_was = []

        for i in range(attempts):
            response = requests.get(url)
            status_data = response.json()
            # print(status_data)

            status = status_data.get("status")
            if status_data.get("status") in ["stream", "success"]:
                # сохраняем изображения
                images = status_data.get("response", {})
                image_paths_list = []
                for model, image_paths in images.items():
                    if model in model_was:
                        continue
                    model_was.append(model)
                    for i, file_base64 in enumerate(image_paths):
                        file_path = self._save_base64(file_base64, model, i, request_id)
                        # print(f"Image saved at: {file_path}")
                        image_paths_list.append(file_path)
                    yield image_paths_list
            if status == "success":
                # print(f"Image generation complete! Response: {json.dumps(status_data, indent=2)}")
                return
            elif "error" in status_data:
                raise NetworkToolsError(f"Error occurred: {status_data['error']}")

            time.sleep(5)  # wait
        else:
            raise NetworkToolsTimeout(f"Timeout for id {request_id}")

    def _check_status_stream_tts(self, request_id, attempts=180):
        """
        Проверяет статус запроса TTS.

        - При `stream` получает части аудио.
        - При `success` возвращает объединённое аудио.

        :return: str, путь к итоговому аудиофайлу
        """
        os.makedirs(self.output_dir, exist_ok=True)
        url = f"{self.api_url}/api/v2/status/{request_id}"
        got_parts = 0

        for _ in range(attempts):
            response = requests.get(url)
            status_data = response.json()

            if status_data.get("status") in ["stream", "success"]:
                for model_name, audio_paths in status_data.get("response", {}).items():
                    for i, file_base64 in enumerate(audio_paths):
                        if i < got_parts:
                            continue
                        got_parts+=1
                        file_path = self._save_base64(file_base64, model_name, i, request_id)
                        yield file_path

            if status_data.get("status") == "success":
                return

            elif "error" in status_data:
                raise NetworkToolsError(f"Error occurred: {status_data['error']}")

            if not got_parts:
                time.sleep(3)
            else:
                time.sleep(0.5)
        else:
            raise NetworkToolsTimeout(f"Timeout for request_id {request_id}")

    def _check_music_status(self, request_id, attempts=180):
        """Checks the status of the music generation request."""
        url = f"{self.api_url}/api/v2/status/{request_id}"
        returned_link = False
        for i in range(attempts):
            response = requests.get(url)
            status_data = response.json()
            # print("music status_data", status_data)

            status = status_data.get("status")
            if status == "stream" and not returned_link:
                returned_link = True
                # Возвращаем ссылки на аудио, если статус "stream"
                audio_files = status_data.get("response", {})
                for model, audio_links in audio_files.items():
                    yield audio_links
            elif status == "success":
                # Сохраняем аудио и возвращаем пути к файлам, если статус "success"
                audio_files = status_data.get("response", {})
                file_paths = []
                for model, audio_paths in audio_files.items():
                    for i, file_base64 in enumerate(audio_paths):
                        file_path = self._save_base64(file_base64, model, i, request_id)
                        file_paths.append(file_path)
                if not returned_link:
                    yield ""
                yield file_paths
                return

            if "error" in status_data:
                raise Exception(f"Error occurred: {status_data['error']}")

            time.sleep(5)  # ждем 5 секунд до следующей проверки
        else:
            raise NetworkToolsTimeout(f"Timeout for id {request_id}")

    def _save_base64(self, file_base64, model, index, request_id):
        """Сохраняет файлы из base64 в файл с соответствующим расширением."""
        # Декодируем base64 данные
        img_data = base64.b64decode(file_base64.split(",")[1])

        # Определяем MIME-тип
        mime_type = file_base64.split(",")[0].split(":")[1].split(";")[0]

        # Получаем расширение из mime_type
        file_extension = None
        for ext, mime in extension_to_mime.items():
            if mime == mime_type:
                file_extension = ext
                break

        if not file_extension:
            raise ValueError("Unsupported MIME type")

        # Формируем имя файла
        file_name = f"{model}_{index}_{request_id}{file_extension}"
        file_path = os.path.join(self.output_dir, file_name)

        # Сохраняем файл
        with open(file_path, "wb") as f:
            f.write(img_data)

        return file_path
