import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional


class AspectRatio:
    ratio_1x1 = "1:1"
    ratio_2x3 = "2:3"
    ratio_3x2 = "3:2"

class VideoAspectRatio:
    ratio_1x1 = "1:1"
    ratio_16x9 = "16:9"
    ratio_9x16 = "9:16"

class ImageModels:
    kandinsky = "kandinsky"
    flux = "flux"
    sd_ultra = "sd_ultra"
    # flux_dev = "flux_dev"
    sd_xl = "sd_xl"
    recraft = "recraft"
    dalle_3 = "dalle_3"
    gemini = "gemini"
    chat_gpt_images = "chat_gpt_images"
    flux_pro_ultra_raw = "flux_pro_ultra_raw"


class GptModels:
    # OPENAI
    o3_high = "o3-high"  # thinking
    o4_mini = "o4-mini"  # thinking

    gpt_4_1 = "gpt-4-1"
    gpt_4_1_mini = "gpt-4-1-mini"
    gpt_4_1_nano = "gpt-4-1-nano"

    gpt_4_5 = "gpt-4-5"
    o3_mini = "o3-mini"  # thinking
    o1 = "o1"  # thinking
    gpt_4o = "gpt-4o"
    chatgpt_4o = "chatgpt-4o"
    gpt_4o_mini = "gpt-4o-mini"
    gpt_3_5 = "gpt-3-5"

    # CLAUDE
    claude_4_opus = "claude-4-opus"
    claude_4_sonnet = "claude-4-sonnet"
    claude_4_opus_thinking = "claude-4-opus-thinking"  # thinking
    claude_4_sonnet_thinking = "claude-4-sonnet-thinking"  # thinking

    claude_3_7_sonnet_thinking = "claude-3-7-sonnet-thinking"  # thinking
    claude_3_7_sonnet = "claude-3-7-sonnet"
    claude_3_5_sonnet = "claude-3-5-sonnet"
    claude_3_opus = "claude-3-opus"
    claude_3_sonnet = "claude-3-sonnet"
    claude_3_haiku = "claude-3-haiku"

    # DEEPSEEK
    deepseek_r1 = "deepseek-r1"  # thinking
    deepseek_v3 = "deepseek-v3"

    # command
    command_r_plus = "command-r-plus"
    command_a = "command-a"
    c4ai_aya_vision_32b = "c4ai-aya-vision-32b"

    # X-ai
    grok_3 = "grok-3"  # thinking

    gemini_2_5_pro = "gemini-2-5-pro"  # thinking
    gemini_2_5_flash = "gemini-2.5-flash"  # ?thinking
    gemini_2_5_flash_lite = "gemini-2.5-flash-lite"  # quick
    gemini_2_0_flash_lite = "gemini-2.0-flash-lite"  # very quick

    reka_flash = "reka-flash"
    minimax_01 = "minimax-01"

    available_models = [
        claude_4_opus, claude_4_opus_thinking, claude_4_sonnet, claude_4_sonnet_thinking,
        gpt_4_5, o3_mini, o1, gpt_4o, gpt_4o_mini, chatgpt_4o, gpt_4_1_mini, gpt_4_1_nano, gpt_3_5,
        claude_3_7_sonnet_thinking, claude_3_7_sonnet, claude_3_5_sonnet,
        claude_3_opus, claude_3_sonnet, claude_3_haiku,
        deepseek_r1, deepseek_v3,
        command_r_plus, command_a, c4ai_aya_vision_32b,
        reka_flash, minimax_01, grok_3, gemini_2_5_pro, gemini_2_5_flash, gemini_2_5_flash_lite, gemini_2_0_flash_lite, o3_high, o4_mini
    ]


AVAILABLE_MODELS = GptModels.available_models

CLAUDE_MODELS = [
    GptModels.claude_4_opus,
    GptModels.claude_4_opus_thinking,
    GptModels.claude_4_sonnet,
    GptModels.claude_4_sonnet_thinking,

    GptModels.claude_3_7_sonnet_thinking,
    GptModels.claude_3_7_sonnet,
    GptModels.claude_3_5_sonnet,
    GptModels.claude_3_opus,
    GptModels.claude_3_sonnet,
    GptModels.claude_3_haiku
]
GPT_4O_MODELS = [
    GptModels.chatgpt_4o,
    GptModels.gpt_4o,
    GptModels.gpt_4o_mini
]
ALL_VISION_MODELS = ([GptModels.reka_flash, GptModels.c4ai_aya_vision_32b] + GPT_4O_MODELS +
                     [GptModels.gemini_2_5_pro,
                      GptModels.gemini_2_5_flash,
                      GptModels.gemini_2_5_flash_lite,
                      GptModels.gemini_2_0_flash_lite
                      ] + [
                         GptModels.o4_mini,
                         GptModels.o3_high
                     ])


@dataclass
class MusicClip:
    audio_path: str
    image_path: Optional[str] = None


@dataclass
class ResponseDetails:
    model: str
    provider: str
    text: str


@dataclass
class GptResponse:
    chat_history: list
    cost: float
    created: float
    response: ResponseDetails
    status: str
    count_tokens: dict
    full_response: dict
    extra_info: dict
    plugins: dict
    internet_query: str
    image_description: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "GptResponse":
        # print("data", data)
        chat_history = data.get("chat_history", [])
        data["response"]["provider"] = data["response"].get("provider", "Unknown")
        response = ResponseDetails(**data["response"])
        full_response = data.get("full_response", {})
        extra_info = full_response.get("extra_info", {})
        plugins = extra_info.get("plugins", {})
        internet_query = extra_info.get("internet_query", "")
        image_description = extra_info.get("image_description", "")
        return cls(
            chat_history=chat_history,
            cost=data["cost"],
            created=data["created"],
            response=response,
            status=data["status"],
            count_tokens=data.get("count_tokens", {}),
            full_response=full_response,
            extra_info=extra_info,
            plugins=plugins,
            internet_query=internet_query,
            image_description=image_description
        )

    def get_formatted_created_time(self) -> str:
        return datetime.fromtimestamp(self.created).strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self) -> str:
        return (
            f"Status: {self.status}\n"
            f"Cost: {self.cost}\n"
            f"Created: {self.get_formatted_created_time()}\n"
            f"Response: {self.response.text}\n"
            f"Chat History:\n{self.chat_history}"
        )


@dataclass
class UsageEntry:
    timestamp: float
    balance_change: float
    comment: str
    new_balance: float


@dataclass
class ResponseData:
    balance: float
    usage: List[UsageEntry] = field(default_factory=list)


@dataclass
class UserUsage:
    created: float
    status: str
    response: ResponseData

    @classmethod
    def from_dict(cls, data: dict):
        """Создает экземпляр класса UserUsage из строки JSON"""

        usage_entries = [
            UsageEntry(**entry) for entry in data["response"].get("usage", [])
        ]
        response_data = ResponseData(
            balance=data["response"].get("balance"),
            usage=usage_entries,
        )

        return cls(
            created=data.get("created"),
            status=data.get("status"),
            response=response_data,
        )

    def to_json(self) -> str:
        """Сериализует объект обратно в JSON"""
        return json.dumps({
            "created": self.created,
            "status": self.status,
            "response": {
                "balance": self.response.balance,
                "usage": [entry.__dict__ for entry in self.response.usage],
            }
        }, indent=4)


class ImageChangeModels:
    remove_background = "remove_background"
    change_background = "change_background"
    outpaint = "outpaint"
    inpaint = "inpaint"
    upscale = "upscale"
    add_text = "add_text"
    style = "style"
    vectorise = "vectorise"
    search_and_replace = "search_and_replace"
    model_3d = "model_3d"


class Upscale_Mode:
    quality_8K = "8K"
    quality_4K = "4K"
    quality_HD = "HD"


class MusicModels:
    suno_v3 = "suno_v3"
    suno_v4 = "suno_v4"
    suno_v4_5 = "suno_v4_5"

class SunoMode:
    extend = "extend"
    cover = "cover"


class VideoModels:
    stable_video_diffusion = "stable_video_diffusion"
    veo_3 = "veo-3"
    kling_1_6 = "kling-1.6"


class TtsModels:
    hailuo = "hailuo"
    elevenlabs = "elevenlabs"

class AudioModels:
    stable_audio = "stable_audio"


class HailuoModelIds:
    speech_01_hd = "speech-01-hd"
    speech_01_turbo = "speech-01-turbo"
    speech_02_hd = "speech-02-hd"
    speech_02_turbo = "speech-02-turbo"


class HailuoLanguages:
    eng = "English"
    arb = "Arabic"
    hk = "Cantonese"
    cmn = "Chinese (Mandarin)"
    nld = "Dutch"
    fra = "French"
    deu = "German"
    ind = "Indonesian"
    ita = "Italian"
    jpn = "Japanese"
    kor = "Korean"
    por = "Portuguese"
    rus = "Russian"
    spa = "Spanish"
    tur = "Turkish"
    ukr = "Ukrainian"
    vie = "Vietnamese"
    auto = "Auto"

class ElevenlabsVoices:
    Will = "Will (US male)"
    Liam = "Liam (US male)"
    Mark = "Mark (US male)"
    Bill = "Bill (US male)"
    Matilda = "Matilda (US female)"
    Jessica = "Jessica (US female)"
    Hope = "Hope (US female)"
    Cassidy = "Cassidy (US female)"
    George = "George (UK male)"
    Archer = "Archer (UK male)"
    AdamUK = "Adam (UK male)"
    Lily = "Lily (UK female)"
    Amelia = "Amelia (UK female)"
    AnaRita = "Ana-Rita (UK female)"
    Wahab = "Wahab (Arabic male)"
    Haytham = "Haytham (Arabic male)"
    Sana = "Sana (Arabic female)"
    Martin = "Martin (Chinese male)"
    Guillaume = "Guillaume (French male)"
    Hugo = "Hugo (French male)"
    Darine = "Darine (French female)"
    Jessy = "Jessy (French female)"
    Kurt = "Kurt (German male)"
    Otto = "Otto (German male)"
    Leonie = "Leonie (German female)"
    Mila = "Mila (German female)"
    Niraj = "Niraj (Hindi male)"
    LeoDeprecated = "Leo (Hindi male)"
    Leo = "Leo (Hindustani male)"
    Monika = "Monika (Hindi female)"
    ShakuntalaDeprecated = "Shakuntala (Hindi female)"
    Shakuntala = "Shakuntala (Hindustani female)"
    Maciej = "Maciej (Polish male)"
    AdamPolish = "Adam (Polish male)"
    Aneta = "Aneta (Polish female)"
    Bea = "Bea (Polish female)"
    Juan = "Juan (Spanish male)"
    David = "David (Spanish male)"
    Dan = "Dan (Spanish male)"
    Gabriela = "Gabriela (Spanish female)"
    Sara = "Sara (Spanish female)"
