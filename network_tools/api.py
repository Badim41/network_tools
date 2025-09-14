import base64
import mimetypes
import os
import time
from typing import Union, Generator, AsyncGenerator

import aiofiles
import asyncio
import requests
from aiohttp import ClientTimeout, TCPConnector, ClientSession
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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
        self.api_url = "https://sert.yellowfire.ru:444"
        self.api_key = api_key
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.session = requests.Session()

        retries = Retry(total=10, backoff_factor=3, status_forcelist=[502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

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
                    internet_access=False, stream=False) -> Union[GptResponse, Generator[GptResponse, None, None]]:
        url = f"{self.api_url}/api/v2/chatgpt"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        # Если указан файл — конвертируем его в base64
        file_base64 = None
        mime_type = None
        if file_path:
            file_base64 = self._file_to_base64(file_path)
            mime_type = self._get_mime_type(file_path)

        payload = {
            "model": model,
            "prompt": prompt,
            "chat_history": chat_history,
            "file_base64": file_base64 or "",  # если нет base64, передаем пустую строку
            "internet_access": internet_access,
            "mime_type": mime_type,
            "stream": stream,
        }

        response = self.session.post(url, headers=headers, json=payload)
        response_data = response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise NetworkToolsError("Request ID not found in response")

        if stream:
            return self._check_status_stream_gpt(request_id)
        else:
            # Ждем время, указанное сервером
            time.sleep(response_data.get("wait", 1))
            # Не стримовый режим: опрашиваем статус до успешного завершения
            attempts = 300

            result = self._check_status(request_id, attempts=attempts, delay=0.1)
            return GptResponse.from_json(result)

    def get_usage(self) -> UserUsage:
        url = f"{self.api_url}/api/v2/user"

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        response = self.session.get(url, headers=headers, json="")
        response_data = response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        return UserUsage.from_dict(response_data)

    def _check_status(self, request_id, attempts=1200, delay=2.0) -> dict:
        """Запрашивает статус запроса, пока он не станет 'success'."""
        url = f"{self.api_url}/api/v2/status/{request_id}"

        for i in range(attempts):
            response = self.session.get(url)

            result = response.json()
            if result.get("error"):
                raise NetworkToolsError(result.get("error"))
            if result["status"] == "success":
                # print(result.get("count_tokens"))
                return result

            time.sleep(delay)
        else:
            raise NetworkToolsTimeout(f"Timeout for id {request_id}")

    def image_generate_api(self, models, prompt, aspect_ratio, send_url=False, return_minimal_images=True, width=None, height=None, allow_nsfw=True):
        """
        :param models: List[obj[ImageModels]]
        :param prompt: запрос
        :param aspect_ratio: obj[AspectRatio]
        :param send_url: отправить картинку ссылкой
        :param return_minimal_images: вернуть минимальное число картинок (1). False - вернуть 4 картинки
        :param width: Указать ширину (будет игнорироваться aspect_ratio)
        :param height: Указать высоту (будет игнорироваться aspect_ratio)
        :param allow_nsfw: фильтр NSFW (работает только на 'Flux')
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
            "prompt": prompt,
            "send_url": send_url,
            "return_minimal_images": return_minimal_images,
            "width": width,
            "height": height,
            "allow_nsfw": allow_nsfw,
        }

        response = self.session.post(url, headers=headers, json=data)
        response_data = response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            return {"status": "error", "error": "Request ID not found in response"}

        time.sleep(response_data.get("wait", 2))

        return self._check_status_stream_images(request_id)

    def change_image_api(self, model, image_path, prompt="", prompt_2="", strength=None, inpaint_models=None,
                         send_url=False):
        """
        Отправляет изображение на обработку (удаление фона, апскейл и т. д.).

        :param model: str, тип обработки (использует ImageChangeModels)
        :param image_path: str, путь к файлу изображения
        :param prompt: str, основной текстовый запрос
        :param prompt_2: str, дополнительный текстовый запрос
        :param strength: float, сила изменения изображения для inpaint
        :return: список путей обработанных изображений
        """
        if strength and not model == ImageChangeModels.inpaint:
            print("strength supports only with ImageChangeModels.inpaint, so strength will be ignored")
        elif not strength:
            strength = 0.5

        if not inpaint_models:
            inpaint_models = []
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
            "prompt_2": prompt_2,
            "strength": strength,
            "inpaint_models": inpaint_models,
            "send_url": send_url
        }

        response = self.session.post(url, headers=headers, json=data)
        # print(response.text)
        response_data = response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        time.sleep(response_data.get("wait", 5))

        return self._check_status_stream_images(request_id)

    def music_generate_api(
            self,
            model,
            lyrics,
            file_path=None,
            music_style="piano",
            instrumental=False,
            mode=SunoMode.extend,
            send_url=False
    ) -> Generator:
        url = f"{self.api_url}/api/v2/music_generate"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        data = {
            "model": model,
            "lyrics": lyrics,
            "music_style": music_style,
            "instrumental": instrumental,
            "return_images": True,
            "mode": mode,
            "send_url": send_url
        }

        if file_path:
            file_base64 = self._file_to_base64(file_path)
            data["file_base64"] = file_base64

        response = self.session.post(url, headers=headers, json=data)
        response_data = response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        time.sleep(response_data.get("wait", 5))

        return self._check_music_status(request_id, model)

    def video_generate_api(self, model, image_path=None, prompt="", send_url=False, aspect_ratio="16:9"):
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
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "send_url": send_url
        }

        response = self.session.post(url, headers=headers, json=data)
        # print("response", response.text)
        response_data = response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        time.sleep(response_data.get("wait", 10))

        video_data = self._check_status(request_id, attempts=6000, delay=10)
        video_base64 = video_data['response'][model][0]
        return self._save_base64(video_base64, model, "0", request_id)

    def tts_api(self, prompt: str, model: str, speed: float = 1, lang: str = "Auto", voice_id: str = None,
                model_id: str = HailuoModelIds.speech_02_hd):
        """
        Отправляет запрос на генерацию аудио (TTS).

        :param prompt: str, текст для озвучки
        :param model: str, модель генерации голоса
        :param speed: float, скорость речи (по умолчанию 1)
        :param lang: str, язык (по умолчанию "Auto")
        :param voice_id: Optional[str], ID голоса (если None, выбирается по языку)
        :return: List[str], пути к аудиофайлам
        """
        url = f"{self.api_url}/api/v2/tts"
        headers = {"Content-Type": "application/json", "api-key": self.api_key}

        # голос по умолчанию
        if not voice_id:
            voice_id = "226893671006272"

        data = {
            "model": model,
            "prompt": prompt,
            "params": {
                "speed": speed,
                "lang": lang,
                "voice_id": voice_id,
                "model_id": model_id
            }
        }

        response = self.session.post(url, headers=headers, json=data).json()

        if "error" in response:
            raise NetworkToolsBadRequest(response["error"])

        request_id = response.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        return self._check_status_stream_tts(request_id)

    def audio_generate_api(
            self,
            prompt: str,
            model=AudioModels.stable_audio,
            audio_path: str = None,
            duration=90,
            steps=50,
            cfg_scale=7.0,
            strength=1.0,
            seed=0,
            send_url=False
    ):
        """
        Отправляет запрос на генерацию видео.

        :param prompt: str, текстовый запрос
        :param model: str, модель генерации аудио
        :param audio_path: str, путь к входному аудио
        :param duration: int, длительность аудио
        :param steps: int, шаги генерации
        :param cfg_scale: float, ?
        :param strength: float, сила изменения входного аудио
        :param seed: int, сид
        :param send_url: bool, отпрвить ссылку в результате
        :return: audio_path
        """

        url = f"{self.api_url}/api/v2/audio_generate"

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        if audio_path:
            file_base64 = self._file_to_base64(audio_path)
        else:
            file_base64 = ""

        data = {
            "prompt": prompt,
            "model": model,
            "file_base64": file_base64,
            "duration": duration,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "strength": strength,
            "seed": seed,
            "send_url": send_url
        }

        with self.session.post(url, headers=headers, json=data) as response:
            response_data = response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        time.sleep(response_data.get("wait", 3))

        audio_data = self._check_status(request_id, attempts=60, delay=1)

        audio_base64 = audio_data['response'][model][0]
        return self._save_base64(audio_base64, model, "0", request_id)

    def _check_status_stream_images(self, request_id, attempts=1200):
        """Проверяет статус запроса до получения 'success' и сохраняет изображения."""

        url = f"{self.api_url}/api/v2/status/{request_id}"
        model_was = []

        for _ in range(attempts):
            response = self.session.get(url)
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

            # time.sleep(3)  # wait
        else:
            raise NetworkToolsTimeout(f"Timeout for id {request_id}")

    def _check_status_stream_tts(self, request_id, attempts=300):
        """
        :return: str, путь к итоговому аудиофайлу
        """
        url = f"{self.api_url}/api/v2/status/{request_id}"
        got_parts = 0

        for _ in range(attempts):
            response = self.session.get(url)
            status_data = response.json()
            # print("status_data", status_data)

            status = status_data.get("status")
            # print("status(1)", status)
            if status in ["stream", "success"]:
                for model_name, audio_paths in status_data.get("stream_parts", status_data.get("response")).items():
                    for i, file_base64 in enumerate(audio_paths):
                        if i < got_parts:  # если success, то возвращается 1 аудиофайл
                            print("continue", i, got_parts)
                            continue
                        got_parts += 1
                        file_path = self._save_base64(file_base64, model_name, f"{status}-{i}", request_id)
                        yield file_path, "stream"  # последний файл - полное аудио

            if status == "success":
                for model_name, audio_paths in status_data.get("response").items():
                    file_path = self._save_base64(audio_paths[0], model_name, f"{status}", request_id)
                    yield file_path, status
                    return

            elif "error" in status_data:
                raise NetworkToolsError(f"Error occurred: {status_data['error']}")

            # if not got_parts:
            #     time.sleep(0.5)
            # else:
            #     time.sleep(0.2)
        else:
            raise NetworkToolsTimeout(f"Timeout for request_id {request_id}")

    def _check_music_status(self, request_id, model, attempts=1200) -> Generator:
        url = f"{self.api_url}/api/v2/status/{request_id}"
        returned_link = False

        for _ in range(attempts):
            response = self.session.get(url)
            status_data = response.json()

            status = status_data.get("status")
            if status == "stream" and not returned_link:
                returned_link = True
                audio_files = status_data.get("response", {})
                stream_urls = audio_files.get(model, []) if isinstance(audio_files.get(model), list) else []
                yield stream_urls  # Для riffusion будет пустой список

            elif status == "success":
                audio_files = status_data.get("response", {})
                music_clips = []

                for model_name, results in audio_files.items():
                    for i, result_data in enumerate(results):
                        audio_path = self._save_base64(
                            result_data["audio_base64"],
                            model,
                            i,
                            request_id
                        )
                        image_path = None
                        if result_data.get("image_base64"):
                            image_path = self._save_base64(
                                result_data["image_base64"],
                                model,
                                i,
                                request_id
                            )
                        music_clips.append(MusicClip(audio_path=audio_path, image_path=image_path))

                if not returned_link:
                    yield []  # Пустой список stream_urls, если не было стрима
                yield music_clips
                return

            error_api = status_data.get("error")
            if error_api:
                if "RiffusionModerationError" in error_api:
                    raise RiffusionModerationError(error_api)
                elif "RiffusionCriticalError" in error_api:
                    raise RiffusionCriticalError(error_api)
                elif "FileTooLong" in error_api:
                    raise RiffusionFileTooLong(error_api)
                raise NetworkToolsCriticalError(f"Error occurred: {status_data['error']}")

            # time.sleep(5)
        else:
            raise NetworkToolsTimeout(f"Timeout for id {request_id}")

    def _check_status_stream_gpt(self, request_id) -> Generator[GptResponse, None, None]:
        status_url = f"{self.api_url}/api/v2/status/{request_id}"
        stream_response = self.session.get(status_url, stream=True)

        # Читаем строки из потока
        for line in stream_response.iter_lines():
            if line.strip():
                decoded_line = line.decode('utf-8').strip()
                # print("decoded_line", decoded_line)
                # Если достигли конца потока, прекращаем чтение
                if decoded_line == "data: [DONE]":
                    break
                # Если строка начинается с "data: ", отрезаем префикс
                if decoded_line.startswith("data: "):
                    sliced_line = decoded_line[len("data: "):]
                else:
                    sliced_line = decoded_line

                # print("sliced_line", sliced_line)
                json_data_chunk = json.loads(sliced_line)
                # print("json_data_chunk",json_data_chunk)
                yield GptResponse.from_json(json_data_chunk)

    def _save_base64(self, file_base64: str, model, index, request_id):
        """Сохраняет файлы из base64 в файл с соответствующим расширением."""
        if file_base64.startswith("https://"):  # При send_url = True вернутся ссылки
            return file_base64
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


class AsyncNetworkToolsAPI:
    def __init__(self, api_key, output_dir="images"):
        self.api_url = "https://sert.yellowfire.ru:444"
        self.api_key = api_key
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self._session = None

    def get_session(self):
        if self._session is None:
            timeout = ClientTimeout(total=300)
            connector = TCPConnector(limit=100, limit_per_host=30)
            self._session = ClientSession(
                timeout=timeout,
                connector=connector
            )
        return self._session

    @staticmethod
    async def _file_to_base64(file_path):
        """Конвертирует файл в строку base64"""
        async with aiofiles.open(file_path, "rb") as file:
            content = await file.read()
            encoded_string = base64.b64encode(content).decode("utf-8")
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

    async def chatgpt_api(self, prompt, model=GptModels.gpt_4o, chat_history=[], file_path=None,
                          internet_access=False, stream=False) -> Union[GptResponse, AsyncGenerator[GptResponse, None]]:
        url = f"{self.api_url}/api/v2/chatgpt"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        # Если указан файл — конвертируем его в base64
        file_base64 = None
        mime_type = None
        if file_path:
            file_base64 = await self._file_to_base64(file_path)
            mime_type = self._get_mime_type(file_path)

        payload = {
            "model": model,
            "prompt": prompt,
            "chat_history": chat_history,
            "file_base64": file_base64 or "",  # если нет base64, передаем пустую строку
            "internet_access": internet_access,
            "mime_type": mime_type,
            "stream": stream,
        }

        async with self.get_session().post(url, headers=headers, json=payload) as response:
            response_data = await response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise NetworkToolsError("Request ID not found in response")

        if stream:
            return self._check_status_stream_gpt(request_id)
        else:
            # Ждем время, указанное сервером
            await asyncio.sleep(response_data.get("wait", 1))
            # Не стримовый режим: опрашиваем статус до успешного завершения
            attempts = 300

            result = await self._check_status(request_id, attempts=attempts, delay=0.1)
            return GptResponse.from_json(result)

    async def get_usage(self) -> UserUsage:
        url = f"{self.api_url}/api/v2/user"

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        async with self.get_session().get(url, headers=headers, json="") as response:
            response_data = await response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        return UserUsage.from_dict(response_data)

    async def _check_status(self, request_id, attempts=1200, delay=2.0) -> dict:
        """Запрашивает статус запроса, пока он не станет 'success'."""
        url = f"{self.api_url}/api/v2/status/{request_id}"

        for i in range(attempts):
            async with self.get_session().get(url) as response:
                result = await response.json()

            if result.get("error"):
                raise NetworkToolsError(result.get("error"))
            if result["status"] == "success":
                # print(result.get("count_tokens"))
                return result

            await asyncio.sleep(delay)
        else:
            raise NetworkToolsTimeout(f"Timeout for id {request_id}")

    async def image_generate_api(self, models, prompt, aspect_ratio, send_url=False, return_minimal_images=True, width=None, height=None, allow_nsfw=True):
        """
        :param models: List[obj[ImageModels]]
        :param prompt: запрос
        :param aspect_ratio: obj[AspectRatio]
        :param send_url: отправить картинку ссылкой
        :param return_minimal_images: вернуть минимальное число картинок (1). False - вернуть 4 картинки
        :param width: Указать ширину (будет игнорироваться aspect_ratio)
        :param height: Указать высоту (будет игнорироваться aspect_ratio)
        :param allow_nsfw: фильтр NSFW (работает только на 'Flux')
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
            "prompt": prompt,
            "send_url": send_url,
            "return_minimal_images": return_minimal_images,
            "width": width,
            "height": height,
            "allow_nsfw": allow_nsfw,
        }

        async with self.get_session().post(url, headers=headers, json=data) as response:
            response_data = await response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            yield {"status": "error", "error": "Request ID not found in response"}
            return

        await asyncio.sleep(response_data.get("wait", 10))

        async for result in self._check_status_stream_images(request_id):
            yield result

    async def change_image_api(self, model, image_path, prompt="", prompt_2="", strength=None, inpaint_models=None,
                               send_url=False):
        """
        Отправляет изображение на обработку (удаление фона, апскейл и т. д.).

        :param model: str, тип обработки (использует ImageChangeModels)
        :param image_path: str, путь к файлу изображения
        :param prompt: str, основной текстовый запрос
        :param prompt_2: str, дополнительный текстовый запрос
        :param strength: float, сила изменения изображения для inpaint
        :return: список путей обработанных изображений
        """
        if strength and not model == ImageChangeModels.inpaint:
            print("strength supports only with ImageChangeModels.inpaint, so strength will be ignored")
        elif not strength:
            strength = 0.5

        if not inpaint_models:
            inpaint_models = []
        url = f"{self.api_url}/api/v2/image_change"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        file_base64 = await self._file_to_base64(image_path)
        mime_type = self._get_mime_type(image_path)

        data = {
            "model": model,
            "file_base64": file_base64,
            "mime_type": mime_type,
            "prompt": prompt,
            "prompt_2": prompt_2,
            "strength": strength,
            "inpaint_models": inpaint_models,
            "send_url": send_url
        }

        async with self.get_session().post(url, headers=headers, json=data) as response:
            response_data = await response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        await asyncio.sleep(response_data.get("wait", 5))

        async for result in self._check_status_stream_images(request_id):
            yield result

    async def music_generate_api(
            self,
            model,
            lyrics,
            file_path=None,
            music_style="piano",
            instrumental=False,
            mode=SunoMode.extend,
            send_url=False
    ) -> AsyncGenerator:
        url = f"{self.api_url}/api/v2/music_generate"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        data = {
            "model": model,
            "lyrics": lyrics,
            "music_style": music_style,
            "instrumental": instrumental,
            "return_images": True,
            "mode": mode,
            "send_url": send_url
        }

        if file_path:
            file_base64 = await self._file_to_base64(file_path)
            data["file_base64"] = file_base64

        async with self.get_session().post(url, headers=headers, json=data) as response:
            response_data = await response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        await asyncio.sleep(response_data.get("wait", 5))

        async for result in self._check_music_status(request_id, model):
            yield result

    async def video_generate_api(self, model, image_path=None, prompt="", send_url=False, aspect_ratio="16:9"):
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
            file_base64 = await self._file_to_base64(image_path)
        else:
            file_base64 = ""

        data = {
            "model": model,
            "file_base64": file_base64,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "send_url": send_url
        }

        async with self.get_session().post(url, headers=headers, json=data) as response:
            response_data = await response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        await asyncio.sleep(response_data.get("wait", 10))

        video_data = await self._check_status(request_id, attempts=6000, delay=10)
        video_base64 = video_data['response'][model][0]
        return await self._save_base64(video_base64, model, "0", request_id)

    async def tts_api(self, prompt: str, model: str, speed: float = 1, lang: str = "Auto", voice_id: str = None,
                      model_id: str = HailuoModelIds.speech_02_hd):
        """
        Отправляет запрос на генерацию аудио (TTS).

        :param prompt: str, текст для озвучки
        :param model: str, модель генерации голоса
        :param speed: float, скорость речи (по умолчанию 1)
        :param lang: str, язык (по умолчанию "Auto")
        :param voice_id: Optional[str], ID голоса (если None, выбирается по языку)
        :return: List[str], пути к аудиофайлам
        """
        url = f"{self.api_url}/api/v2/tts"
        headers = {"Content-Type": "application/json", "api-key": self.api_key}

        # голос по умолчанию
        if not voice_id:
            voice_id = "226893671006272"

        data = {
            "model": model,
            "prompt": prompt,
            "params": {
                "speed": speed,
                "lang": lang,
                "voice_id": voice_id,
                "model_id": model_id
            }
        }

        async with self.get_session().post(url, headers=headers, json=data) as response:
            response_data = await response.json()

        if "error" in response_data:
            raise NetworkToolsBadRequest(response_data["error"])

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        async for result in self._check_status_stream_tts(request_id):
            yield result

    async def audio_generate_api(
            self,
            prompt:str,
            model=AudioModels.stable_audio,
            audio_path:str=None,
            duration=90,
            steps=50,
            cfg_scale=7.0,
            strength=1.0,
            seed=0,
            send_url=False
    ):
        """
        Отправляет запрос на генерацию видео.

        :param prompt: str, текстовый запрос
        :param model: str, модель генерации аудио
        :param audio_path: str, путь к входному аудио
        :param duration: int, длительность аудио
        :param steps: int, шаги генерации
        :param cfg_scale: float, ?
        :param strength: float, сила изменения входного аудио
        :param seed: int, сид
        :param send_url: bool, отпрвить ссылку в результате
        :return: audio_path
        """

        url = f"{self.api_url}/api/v2/audio_generate"

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        if audio_path:
            file_base64 = await self._file_to_base64(audio_path)
        else:
            file_base64 = ""

        data = {
            "prompt": prompt,
            "model": model,
            "file_base64": file_base64,
            "duration": duration,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "strength": strength,
            "seed": seed,
            "send_url": send_url
        }

        async with self.get_session().post(url, headers=headers, json=data) as response:
            response_data = await response.json()

        if response_data.get("error"):
            raise NetworkToolsBadRequest(response_data.get("error"))

        request_id = response_data.get("request_id")
        if not request_id:
            raise Exception("Request ID not found in response")

        await asyncio.sleep(response_data.get("wait", 3))

        audio_data = await self._check_status(request_id, attempts=60, delay=1)

        audio_base64 = audio_data['response'][model][0]
        return await self._save_base64(audio_base64, model, "0", request_id)

    async def _check_status_stream_images(self, request_id, attempts=1200):
        """Проверяет статус запроса до получения 'success' и сохраняет изображения."""

        url = f"{self.api_url}/api/v2/status/{request_id}"
        model_was = []

        for _ in range(attempts):
            async with self.get_session().get(url) as response:
                status_data = await response.json()

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
                        file_path = await self._save_base64(file_base64, model, i, request_id)
                        image_paths_list.append(file_path)
                    yield image_paths_list
            if status == "success":
                return
            elif "error" in status_data:
                raise NetworkToolsError(f"Error occurred: {status_data['error']}")

        else:
            raise NetworkToolsTimeout(f"Timeout for id {request_id}")

    async def _check_status_stream_tts(self, request_id, attempts=300):
        """
        :return: str, путь к итоговому аудиофайлу
        """
        url = f"{self.api_url}/api/v2/status/{request_id}"
        got_parts = 0

        for _ in range(attempts):
            async with self.get_session().get(url) as response:
                status_data = await response.json()

            status = status_data.get("status")
            if status in ["stream", "success"]:
                for model_name, audio_paths in status_data.get("stream_parts", status_data.get("response")).items():
                    for i, file_base64 in enumerate(audio_paths):
                        if i < got_parts:
                            print("continue", i, got_parts)
                            continue
                        got_parts += 1
                        file_path = await self._save_base64(file_base64, model_name, f"{status}-{i}", request_id)
                        yield file_path, "stream"

            if status == "success":
                for model_name, audio_paths in status_data.get("response").items():
                    file_path = await self._save_base64(audio_paths[0], model_name, f"{status}", request_id)
                    yield file_path, status
                    return

            elif "error" in status_data:
                raise NetworkToolsError(f"Error occurred: {status_data['error']}")

        else:
            raise NetworkToolsTimeout(f"Timeout for request_id {request_id}")

    async def _check_music_status(self, request_id, model, attempts=1200) -> AsyncGenerator:
        url = f"{self.api_url}/api/v2/status/{request_id}"
        returned_link = False

        for _ in range(attempts):
            async with self.get_session().get(url) as response:
                status_data = await response.json()

            status = status_data.get("status")
            if status == "stream" and not returned_link:
                returned_link = True
                audio_files = status_data.get("response", {})
                stream_urls = audio_files.get(model, []) if isinstance(audio_files.get(model), list) else []
                yield stream_urls

            elif status == "success":
                audio_files = status_data.get("response", {})
                music_clips = []

                for model_name, results in audio_files.items():
                    for i, result_data in enumerate(results):
                        audio_path = await self._save_base64(
                            result_data["audio_base64"],
                            model,
                            i,
                            request_id
                        )
                        image_path = None
                        if result_data.get("image_base64"):
                            image_path = await self._save_base64(
                                result_data["image_base64"],
                                model,
                                i,
                                request_id
                            )
                        music_clips.append(MusicClip(audio_path=audio_path, image_path=image_path))

                if not returned_link:
                    yield []
                yield music_clips
                return

            error_api = status_data.get("error")
            if error_api:
                if "RiffusionModerationError" in error_api:
                    raise RiffusionModerationError(error_api)
                elif "RiffusionCriticalError" in error_api:
                    raise RiffusionCriticalError(error_api)
                elif "FileTooLong" in error_api:
                    raise RiffusionFileTooLong(error_api)
                raise NetworkToolsCriticalError(f"Error occurred: {status_data['error']}")

        else:
            raise NetworkToolsTimeout(f"Timeout for id {request_id}")

    async def _check_status_stream_gpt(self, request_id) -> AsyncGenerator[GptResponse, None]:
        status_url = f"{self.api_url}/api/v2/status/{request_id}"

        async with self.get_session().get(status_url) as response:
            async for line in response.content:
                if line.strip():
                    decoded_line = line.decode('utf-8').strip()

                    if decoded_line == "data: [DONE]":
                        break

                    if decoded_line.startswith("data: "):
                        sliced_line = decoded_line[len("data: "):]
                    else:
                        sliced_line = decoded_line

                    # print(f"sliced_line: '{line}'")
                    json_data_chunk = json.loads(sliced_line)
                    yield GptResponse.from_json(json_data_chunk)

    async def _save_base64(self, file_base64: str, model, index, request_id):
        """Сохраняет файлы из base64 в файл с соответствующим расширением."""
        if file_base64.startswith("https://"):
            return file_base64

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

        # Сохраняем файл асинхронно
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(img_data)

        return file_path
