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
    # dalle_3 = "dalle_3"
    # gemini = "gemini"
    chat_gpt_images = "chat_gpt_images"
    flux_pro_ultra_raw = "flux_pro_ultra_raw"
    nano_banana = "nano_banana"
    nano_banana_pro = "nano_banana_pro"


class GptModels:
    # OPENAI
    gpt_5_2_pro = "gpt-5-2-pro"
    gpt_5_2_high = "gpt-5-2-high"
    gpt_5_2 = "gpt-5-2"

    gpt_5_1_high = "gpt-5-1-high"
    chatgpt_5_1 = "chatgpt-5-1"
    gpt_5_1 = "gpt-5-1"

    gpt_5_high = "gpt-5-high"
    chatgpt_5 = "chatgpt-5"
    gpt_5 = "gpt-5"
    gpt_5_mini = "gpt-5-mini"
    gpt_5_nano = "gpt-5-nano"

    gpt_oss = "gpt-oss"

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
    claude_4_5_opus_thinking = "claude-4-5-opus-thinking"  # thinking
    claude_4_5_opus = "claude-4-5-opus"
    claude_4_5_sonnet_thinking = "claude-4-5-sonnet-thinking"  # thinking
    claude_4_5_sonnet = "claude-4-5-sonnet"
    claude_4_1_opus = "claude-4-1-opus"
    claude_4_1_opus_thinking = "claude-4-1-opus-thinking"
    claude_4_opus = "claude-4-opus"
    claude_4_sonnet = "claude-4-sonnet"
    claude_4_opus_thinking = "claude-4-opus-thinking"  # thinking
    claude_4_sonnet_thinking = "claude-4-sonnet-thinking"  # thinking

    # Claude legacy
    claude_3_7_sonnet_thinking = "claude-3-7-sonnet-thinking"  # thinking
    claude_3_7_sonnet = "claude-3-7-sonnet"
    claude_3_5_sonnet = "claude-3-5-sonnet"
    claude_3_opus = "claude-3-opus"
    claude_3_sonnet = "claude-3-sonnet"
    claude_3_haiku = "claude-3-haiku"

    # DEEPSEEK
    deepseek_r1 = "deepseek-r1"  # thinking
    deepseek_v3 = "deepseek-v3"
    deepseek_r1_0528 = "deepseek-r1-0528-qwen3-8b"
    deepseek_v3_2 = "deepseek-v3.2"
    deepseek_v3_2_thinking = "deepseek-v3.2-thinking"  # thinking

    # command
    command_r_plus = "command-r-plus"
    command_a = "command-a"
    command_a_vision = "command-a-vision"
    c4ai_aya_vision_32b = "c4ai-aya-vision-32b"

    # X-ai
    grok_4 = "grok-4"  # thinking
    grok_3 = "grok-3"  # thinking

    kimi_k2_thinking = "kimi-k2-thinking"  # thinking

    gemini_3_0_pro = "gemini-3-0-pro"  # thinking
    gemini_3_0_flash = "gemini-3-0-flash"  # thinking
    gemini_2_5_pro = "gemini-2-5-pro"  # thinking
    gemini_2_5_flash = "gemini-2.5-flash"
    gemini_2_5_flash_lite = "gemini-2.5-flash-lite"  # quick
    gemini_2_0_flash_lite = "gemini-2.0-flash-lite"  # very quick

    reka_flash = "reka-flash"
    # minimax_01 = "minimax-01"
    # minimax_02 = "minimax-02"  # thinking
    glm_4_6 = "glm-4.6"  # thinking

    available_models = [
        claude_4_opus, claude_4_opus_thinking, claude_4_sonnet, claude_4_sonnet_thinking, claude_4_1_opus, claude_4_1_opus_thinking,
        gpt_4_5, o3_mini, o1, gpt_4o, gpt_4o_mini, chatgpt_4o, gpt_4_1, gpt_4_1_mini, gpt_4_1_nano, gpt_3_5,
        claude_3_7_sonnet_thinking, claude_3_7_sonnet, claude_3_5_sonnet,
        claude_3_opus, claude_3_sonnet, claude_3_haiku,
        deepseek_r1, deepseek_v3, deepseek_r1_0528, deepseek_v3_2, deepseek_v3_2_thinking,
        command_r_plus, command_a, c4ai_aya_vision_32b,
        reka_flash, grok_3, grok_4, kimi_k2_thinking, gemini_3_0_pro, gemini_2_5_pro, gemini_2_5_flash, gemini_2_5_flash_lite, gemini_2_0_flash_lite, o3_high, o4_mini,
        gpt_5_high, chatgpt_5, gpt_5, gpt_5_mini, gpt_5_nano, glm_4_6, gpt_oss, gpt_5_1, gpt_5_1_high, chatgpt_5_1, gpt_5_2, gpt_5_2_pro, gemini_3_0_flash, gpt_5_2_high
    ]


AVAILABLE_MODELS = GptModels.available_models

CLAUDE_MODELS = [
    GptModels.claude_4_5_opus,
    GptModels.claude_4_5_opus_thinking,
    GptModels.claude_4_5_sonnet,
    GptModels.claude_4_5_sonnet_thinking,
    GptModels.claude_4_1_opus,
    GptModels.claude_4_1_opus_thinking,
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
GPT_5_MODELS = [
    GptModels.gpt_5_2_pro,
    GptModels.gpt_5_2_high,
    GptModels.gpt_5_2,
    GptModels.gpt_5_1_high,
    GptModels.chatgpt_5_1,
    GptModels.gpt_5_1,
    GptModels.gpt_5_high,
    GptModels.chatgpt_5,
    GptModels.gpt_5,
    GptModels.gpt_5_mini,
    GptModels.gpt_5_nano
]
ALL_VISION_MODELS = ([GptModels.reka_flash, GptModels.c4ai_aya_vision_32b] + GPT_4O_MODELS +
                     [GptModels.gemini_3_0_pro,
                      GptModels.gemini_3_0_flash,
                      GptModels.gemini_2_5_pro,
                      GptModels.gemini_2_5_flash,
                      GptModels.gemini_2_5_flash_lite,
                      GptModels.gemini_2_0_flash_lite
                      ] + [
                         GptModels.o4_mini,
                         GptModels.o3_high
                     ] + GPT_5_MODELS + [
                         GptModels.claude_4_5_opus,
                         GptModels.claude_4_5_opus_thinking,
                         GptModels.claude_4_5_sonnet,
                         GptModels.claude_4_5_sonnet_thinking,
                         GptModels.claude_4_sonnet,
                         GptModels.claude_4_sonnet_thinking,
                         GptModels.claude_4_1_opus,
                         GptModels.claude_4_1_opus_thinking,
                         GptModels.claude_4_opus,
                         GptModels.claude_4_opus_thinking,
                         GptModels.claude_4_sonnet,
                         GptModels.claude_4_sonnet_thinking
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
    suno_v5 = "suno_v5"

class SunoMode:
    extend = "extend"
    cover = "cover"


class VideoModels:
    stable_video_diffusion = "stable_video_diffusion"
    # veo_3 = "veo-3"
    # kling_1_6 = "kling-1.6"
    sora_2 = "sora-2"


class TtsModels:
    # hailuo = "hailuo"
    # elevenlabs = "elevenlabs"
    voice_model_v3 = "voice_model_v3"

class AudioModels:
    stable_audio = "stable_audio"

class ModelV3Languages:
    English_US = "en-US"
    Spanish_LatinAmerica = "es-XL"
    Arabic_Egypt = "ar-EG"
    Arabic_Syria = "ar-SY"
    Arabic_Lebanese = "ar-LB"
    Arabic_Qatar = "ar-QA"
    Arabic_SaudiArabia = "ar-SA"
    Croatian_Croatia = "hr-HR"
    Czech_CzechRepublic = "cs-CZ"
    Danish_Denmark = "da-DK"
    Dutch_Netherlands = "nl-Nl"
    English_Australia = "en-AU"
    English_Canada = "en-CA"
    English_Ireland = "en-IE"
    English_UK = "en-GB"
    Finnish_Finland = "fi-FI"
    French_Canada = "fr-CA"
    French_France = "fr-FR"
    German_Germany = "de-DE"
    Hebrew_Israel = "he-IL"
    Hindi_India = "hi-IN"
    Hungarian_Hungary = "hu-HU"
    Indonesian_Indonesia = "id-ID"
    Italian_Italy = "it-IT"
    Japanese_Japan = "ja-JP"
    Korean_SouthKorea = "ko-KR"
    Lithuanian_Lithuania = "lt-LT"
    Norwegian_Norway = "no-NO"
    Polish_Poland = "pl-PL"
    Portuguese_Brazil = "pt-BR"
    Portuguese_Portugal = "pt-PT"
    Romanian_Romania = "ro-RO"
    Russian_Russia = "ru-RU"
    Slovak_Slovakia = "sk-SK"
    Spanish_Argentina = "es-AR"
    Spanish_Chile = "es-CL"
    Spanish_Colombia = "es-CO"
    Spanish_Mexico = "es-MX"
    Spanish_Peru = "es-PE"
    Spanish_Spain = "es-ES"
    Swedish_Sweden = "sv-SE"
    Tamil_India = "ta-IN"
    Thai_Thailand = "th-TH"
    Turkish_Turkey = "tr-TR"
    German_Switzerland = "de-CH"
    Greek_Greece = "el-GR"
    Auto = "Auto"

class ModelV3Voices:
    en_US_MALE = "en_US_MALE"
    en_US_FEMALE = "en_US_FEMALE"
    pt_BR_MALE = "pt_BR_MALE"
    pt_BR_FEMALE = "pt_BR_FEMALE"
    hi_IN_MALE = "hi_IN_MALE"
    hi_IN_FEMALE = "hi_IN_FEMALE"
    ru_RU_MALE = "ru_RU_MALE"
    ru_RU_FEMALE = "ru_RU_FEMALE"
    de_CH_MALE = "de_CH_MALE"
    de_CH_FEMALE = "de_CH_FEMALE"
    he_IL_MALE = "he_IL_MALE"
    he_IL_FEMALE = "he_IL_FEMALE"
    cs_CZ_MALE = "cs_CZ_MALE"
    cs_CZ_FEMALE = "cs_CZ_FEMALE"
    sl_SI_MALE = "sl_SI_MALE"
    sl_SI_FEMALE = "sl_SI_FEMALE"
    es_MX_MALE = "es_MX_MALE"
    es_MX_FEMALE = "es_MX_FEMALE"
    es_XL_MALE = "es_XL_MALE"
    es_XL_FEMALE = "es_XL_FEMALE"
    de_DE_MALE = "de_DE_MALE"
    de_DE_FEMALE = "de_DE_FEMALE"
    de_AT_MALE = "de_AT_MALE"
    de_AT_FEMALE = "de_AT_FEMALE"
    ro_RO_MALE = "ro_RO_MALE"
    ro_RO_FEMALE = "ro_RO_FEMALE"
    es_ES_MALE = "es_ES_MALE"
    es_ES_FEMALE = "es_ES_FEMALE"
    fr_FR_MALE = "fr_FR_MALE"
    fr_FR_FEMALE = "fr_FR_FEMALE"
    en_KE_MALE = "en_KE_MALE"
    en_KE_FEMALE = "en_KE_FEMALE"
    uz_UZ_MALE = "uz_UZ_MALE"
    uz_UZ_FEMALE = "uz_UZ_FEMALE"
    zh_CN_MALE = "zh_CN_MALE"
    zh_CN_FEMALE = "zh_CN_FEMALE"
    de_BE_FEMALE = "de_BE_FEMALE"
    lo_LA_MALE = "lo_LA_MALE"
    lo_LA_FEMALE = "lo_LA_FEMALE"
    es_HN_MALE = "es_HN_MALE"
    es_HN_FEMALE = "es_HN_FEMALE"
    en_AU_MALE = "en_AU_MALE"
    en_AU_FEMALE = "en_AU_FEMALE"
    ja_JP_MALE = "ja_JP_MALE"
    ja_JP_FEMALE = "ja_JP_FEMALE"
    cy_GB_MALE = "cy_GB_MALE"
    cy_GB_FEMALE = "cy_GB_FEMALE"
    it_IT_MALE = "it_IT_MALE"
    it_IT_FEMALE = "it_IT_FEMALE"
    nl_NL_MALE = "nl_NL_MALE"
    nl_NL_FEMALE = "nl_NL_FEMALE"
    ar_QA_MALE = "ar_QA_MALE"
    ar_QA_FEMALE = "ar_QA_FEMALE"
    en_GB_MALE = "en_GB_MALE"
    en_GB_FEMALE = "en_GB_FEMALE"
    hu_HU_MALE = "hu_HU_MALE"
    hu_HU_FEMALE = "hu_HU_FEMALE"
    fi_FI_MALE = "fi_FI_MALE"
    fi_FI_FEMALE = "fi_FI_FEMALE"
    en_IN_MALE = "en_IN_MALE"
    en_IN_FEMALE = "en_IN_FEMALE"
    ar_LB_MALE = "ar_LB_MALE"
    ar_LB_FEMALE = "ar_LB_FEMALE"
    sk_SK_MALE = "sk_SK_MALE"
    sk_SK_FEMALE = "sk_SK_FEMALE"
    ta_SG_MALE = "ta_SG_MALE"
    ta_SG_FEMALE = "ta_SG_FEMALE"
    id_ID_MALE = "id_ID_MALE"
    id_ID_FEMALE = "id_ID_FEMALE"
    ar_MA_MALE = "ar_MA_MALE"
    ar_MA_FEMALE = "ar_MA_FEMALE"
    fa_IR_MALE = "fa_IR_MALE"
    fa_IR_FEMALE = "fa_IR_FEMALE"
    pl_PL_MALE = "pl_PL_MALE"
    pl_PL_FEMALE = "pl_PL_FEMALE"
    ar_IQ_MALE = "ar_IQ_MALE"
    ar_IQ_FEMALE = "ar_IQ_FEMALE"
    sr_RS_MALE = "sr_RS_MALE"
    sr_RS_FEMALE = "sr_RS_FEMALE"
    ca_ES_MALE = "ca_ES_MALE"
    ca_ES_FEMALE = "ca_ES_FEMALE"
    ko_KR_MALE = "ko_KR_MALE"
    ko_KR_FEMALE = "ko_KR_FEMALE"
    ar_SA_MALE = "ar_SA_MALE"
    ar_SA_FEMALE = "ar_SA_FEMALE"
    es_CR_MALE = "es_CR_MALE"
    es_CR_FEMALE = "es_CR_FEMALE"
    bn_BD_MALE = "bn_BD_MALE"
    bn_BD_FEMALE = "bn_BD_FEMALE"
    wuu_CN_MALE = "wuu_CN_MALE"
    wuu_CN_FEMALE = "wuu_CN_FEMALE"
    es_DO_MALE = "es_DO_MALE"
    es_DO_FEMALE = "es_DO_FEMALE"
    ar_TN_MALE = "ar_TN_MALE"
    ar_TN_FEMALE = "ar_TN_FEMALE"
    ml_IN_MALE = "ml_IN_MALE"
    ml_IN_FEMALE = "ml_IN_FEMALE"
    es_BO_MALE = "es_BO_MALE"
    es_BO_FEMALE = "es_BO_FEMALE"
    ar_LY_MALE = "ar_LY_MALE"
    ar_LY_FEMALE = "ar_LY_FEMALE"
    fr_CA_MALE = "fr_CA_MALE"
    fr_CA_FEMALE = "fr_CA_FEMALE"
    mr_IN_MALE = "mr_IN_MALE"
    mr_IN_FEMALE = "mr_IN_FEMALE"
    el_GR_MALE = "el_GR_MALE"
    el_GR_FEMALE = "el_GR_FEMALE"
    ta_IN_MALE = "ta_IN_MALE"
    ta_IN_FEMALE = "ta_IN_FEMALE"
    so_SO_MALE = "so_SO_MALE"
    so_SO_FEMALE = "so_SO_FEMALE"
    mn_MN_MALE = "mn_MN_MALE"
    mn_MN_FEMALE = "mn_MN_FEMALE"
    es_GT_MALE = "es_GT_MALE"
    es_GT_FEMALE = "es_GT_FEMALE"
    su_ID_MALE = "su_ID_MALE"
    su_ID_FEMALE = "su_ID_FEMALE"
    es_EC_MALE = "es_EC_MALE"
    es_EC_FEMALE = "es_EC_FEMALE"
    ar_EG_MALE = "ar_EG_MALE"
    ar_EG_FEMALE = "ar_EG_FEMALE"
    is_IS_MALE = "is_IS_MALE"
    is_IS_FEMALE = "is_IS_FEMALE"
    af_ZA_MALE = "af_ZA_MALE"
    af_ZA_FEMALE = "af_ZA_FEMALE"
    es_PY_MALE = "es_PY_MALE"
    es_PY_FEMALE = "es_PY_FEMALE"
    am_ET_MALE = "am_ET_MALE"
    am_ET_FEMALE = "am_ET_FEMALE"
    bn_IN_MALE = "bn_IN_MALE"
    bn_IN_FEMALE = "bn_IN_FEMALE"
    en_CA_MALE = "en_CA_MALE"
    en_CA_FEMALE = "en_CA_FEMALE"
    ar_YE_MALE = "ar_YE_MALE"
    ar_YE_FEMALE = "ar_YE_FEMALE"
    en_ZA_MALE = "en_ZA_MALE"
    en_ZA_FEMALE = "en_ZA_FEMALE"
    kn_IN_MALE = "kn_IN_MALE"
    kn_IN_FEMALE = "kn_IN_FEMALE"
    ar_AE_MALE = "ar_AE_MALE"
    ar_AE_FEMALE = "ar_AE_FEMALE"
    pa_IN_MALE = "pa_IN_MALE"
    pa_IN_FEMALE = "pa_IN_FEMALE"
    nb_NO_MALE = "nb_NO_MALE"
    nb_NO_FEMALE = "nb_NO_FEMALE"
    et_EE_MALE = "et_EE_MALE"
    et_EE_FEMALE = "et_EE_FEMALE"
    yue_CN_MALE = "yue_CN_MALE"
    yue_CN_FEMALE = "yue_CN_FEMALE"
    uk_UA_MALE = "uk_UA_MALE"
    uk_UA_FEMALE = "uk_UA_FEMALE"
    fr_BE_MALE = "fr_BE_MALE"
    fr_BE_FEMALE = "fr_BE_FEMALE"
    en_NG_MALE = "en_NG_MALE"
    en_NG_FEMALE = "en_NG_FEMALE"
    gu_IN_MALE = "gu_IN_MALE"
    gu_IN_FEMALE = "gu_IN_FEMALE"
    hy_AM_MALE = "hy_AM_MALE"
    hy_AM_FEMALE = "hy_AM_FEMALE"
    pt_PT_MALE = "pt_PT_MALE"
    pt_PT_FEMALE = "pt_PT_FEMALE"
    jv_ID_MALE = "jv_ID_MALE"
    jv_ID_FEMALE = "jv_ID_FEMALE"
    te_IN_MALE = "te_IN_MALE"
    te_IN_FEMALE = "te_IN_FEMALE"
    zh_TW_MALE = "zh_TW_MALE"
    zh_TW_FEMALE = "zh_TW_FEMALE"
    ne_NP_MALE = "ne_NP_MALE"
    ne_NP_FEMALE = "ne_NP_FEMALE"
    mt_MT_MALE = "mt_MT_MALE"
    mt_MT_FEMALE = "mt_MT_FEMALE"
    gl_ES_MALE = "gl_ES_MALE"
    gl_ES_FEMALE = "gl_ES_FEMALE"
    ar_DZ_MALE = "ar_DZ_MALE"
    ar_DZ_FEMALE = "ar_DZ_FEMALE"
    ta_MY_MALE = "ta_MY_MALE"
    ta_MY_FEMALE = "ta_MY_FEMALE"
    es_PE_MALE = "es_PE_MALE"
    es_PE_FEMALE = "es_PE_FEMALE"
    es_UY_MALE = "es_UY_MALE"
    es_UY_FEMALE = "es_UY_FEMALE"
    en_PH_MALE = "en_PH_MALE"
    en_PH_FEMALE = "en_PH_FEMALE"
    en_NZ_MALE = "en_NZ_MALE"
    en_NZ_FEMALE = "en_NZ_FEMALE"
    ka_GE_MALE = "ka_GE_MALE"
    ka_GE_FEMALE = "ka_GE_FEMALE"
    zh_HK_MALE = "zh_HK_MALE"
    zh_HK_FEMALE = "zh_HK_FEMALE"
    es_US_MALE = "es_US_MALE"
    es_US_FEMALE = "es_US_FEMALE"
    es_NI_MALE = "es_NI_MALE"
    es_NI_FEMALE = "es_NI_FEMALE"
    en_SG_MALE = "en_SG_MALE"
    en_SG_FEMALE = "en_SG_FEMALE"
    lv_LV_MALE = "lv_LV_MALE"
    lv_LV_FEMALE = "lv_LV_FEMALE"
    es_GQ_MALE = "es_GQ_MALE"
    es_GQ_FEMALE = "es_GQ_FEMALE"
    ar_KW_MALE = "ar_KW_MALE"
    ar_KW_FEMALE = "ar_KW_FEMALE"
    az_AZ_MALE = "az_AZ_MALE"
    az_AZ_FEMALE = "az_AZ_FEMALE"
    es_CO_MALE = "es_CO_MALE"
    es_CO_FEMALE = "es_CO_FEMALE"
    es_AR_MALE = "es_AR_MALE"
    es_AR_FEMALE = "es_AR_FEMALE"
    lt_LT_MALE = "lt_LT_MALE"
    lt_LT_FEMALE = "lt_LT_FEMALE"
    kk_KZ_MALE = "kk_KZ_MALE"
    kk_KZ_FEMALE = "kk_KZ_FEMALE"
    hr_HR_MALE = "hr_HR_MALE"
    hr_HR_FEMALE = "hr_HR_FEMALE"
    zh_CN_shandong_MALE = "zh_CN_shandong_MALE"
    ta_LK_MALE = "ta_LK_MALE"
    ta_LK_FEMALE = "ta_LK_FEMALE"
    da_DK_MALE = "da_DK_MALE"
    da_DK_FEMALE = "da_DK_FEMALE"
    ar_SY_MALE = "ar_SY_MALE"
    ar_SY_FEMALE = "ar_SY_FEMALE"
    bs_BA_MALE = "bs_BA_MALE"
    bs_BA_FEMALE = "bs_BA_FEMALE"
    mk_MK_MALE = "mk_MK_MALE"
    mk_MK_FEMALE = "mk_MK_FEMALE"
    ar_OM_MALE = "ar_OM_MALE"
    ar_OM_FEMALE = "ar_OM_FEMALE"
    th_TH_MALE = "th_TH_MALE"
    th_TH_FEMALE = "th_TH_FEMALE"
    ur_PK_MALE = "ur_PK_MALE"
    ur_PK_FEMALE = "ur_PK_FEMALE"
    en_TZ_MALE = "en_TZ_MALE"
    en_TZ_FEMALE = "en_TZ_FEMALE"
    en_HK_MALE = "en_HK_MALE"
    en_HK_FEMALE = "en_HK_FEMALE"
    ur_IN_MALE = "ur_IN_MALE"
    ur_IN_FEMALE = "ur_IN_FEMALE"
    es_PA_MALE = "es_PA_MALE"
    es_PA_FEMALE = "es_PA_FEMALE"
    sq_AL_MALE = "sq_AL_MALE"
    sq_AL_FEMALE = "sq_AL_FEMALE"
    es_SV_MALE = "es_SV_MALE"
    es_SV_FEMALE = "es_SV_FEMALE"
    ar_BH_MALE = "ar_BH_MALE"
    ar_BH_FEMALE = "ar_BH_FEMALE"
    fr_CH_MALE = "fr_CH_MALE"
    fr_CH_FEMALE = "fr_CH_FEMALE"
    sw_TZ_MALE = "sw_TZ_MALE"
    sw_TZ_FEMALE = "sw_TZ_FEMALE"
    es_VE_MALE = "es_VE_MALE"
    es_VE_FEMALE = "es_VE_FEMALE"
    es_CL_MALE = "es_CL_MALE"
    es_CL_FEMALE = "es_CL_FEMALE"
    ar_JO_MALE = "ar_JO_MALE"
    ar_JO_FEMALE = "ar_JO_FEMALE"
    eu_ES_MALE = "eu_ES_MALE"
    eu_ES_FEMALE = "eu_ES_FEMALE"
    sv_SE_MALE = "sv_SE_MALE"
    sv_SE_FEMALE = "sv_SE_FEMALE"
    ga_IE_MALE = "ga_IE_MALE"
    ga_IE_FEMALE = "ga_IE_FEMALE"
    km_KH_MALE = "km_KH_MALE"
    km_KH_FEMALE = "km_KH_FEMALE"
    zu_ZA_MALE = "zu_ZA_MALE"
    zu_ZA_FEMALE = "zu_ZA_FEMALE"
    es_CU_MALE = "es_CU_MALE"
    es_CU_FEMALE = "es_CU_FEMALE"
    si_LK_MALE = "si_LK_MALE"
    si_LK_FEMALE = "si_LK_FEMALE"
    my_MM_MALE = "my_MM_MALE"
    my_MM_FEMALE = "my_MM_FEMALE"
    nl_BE_MALE = "nl_BE_MALE"
    nl_BE_FEMALE = "nl_BE_FEMALE"
    bg_BG_MALE = "bg_BG_MALE"
    bg_BG_FEMALE = "bg_BG_FEMALE"
    ps_AF_MALE = "ps_AF_MALE"
    ps_AF_FEMALE = "ps_AF_FEMALE"
    vi_VN_MALE = "vi_VN_MALE"
    vi_VN_FEMALE = "vi_VN_FEMALE"
    sw_KE_MALE = "sw_KE_MALE"
    sw_KE_FEMALE = "sw_KE_FEMALE"
    zh_CN_henan_MALE = "zh_CN_henan_MALE"
    ms_MY_MALE = "ms_MY_MALE"
    ms_MY_FEMALE = "ms_MY_FEMALE"
    tr_TR_MALE = "tr_TR_MALE"
    tr_TR_FEMALE = "tr_TR_FEMALE"
    en_IE_MALE = "en_IE_MALE"
    en_IE_FEMALE = "en_IE_FEMALE"
    fil_PH_MALE = "fil_PH_MALE"
    fil_PH_FEMALE = "fil_PH_FEMALE"
    es_PR_MALE = "es_PR_MALE"
    es_PR_FEMALE = "es_PR_FEMALE"

# class HailuoModelIds:
#     speech_01_hd = "speech-01-hd"
#     speech_01_turbo = "speech-01-turbo"
#     speech_02_hd = "speech-02-hd"
#     speech_02_turbo = "speech-02-turbo"


# class HailuoLanguages:
#     eng = "English"
#     arb = "Arabic"
#     hk = "Cantonese"
#     cmn = "Chinese (Mandarin)"
#     nld = "Dutch"
#     fra = "French"
#     deu = "German"
#     ind = "Indonesian"
#     ita = "Italian"
#     jpn = "Japanese"
#     kor = "Korean"
#     por = "Portuguese"
#     rus = "Russian"
#     spa = "Spanish"
#     tur = "Turkish"
#     ukr = "Ukrainian"
#     vie = "Vietnamese"
#     auto = "Auto"

# class ElevenlabsVoices:
#     Will = "Will (US male)"
#     Liam = "Liam (US male)"
#     Mark = "Mark (US male)"
#     Bill = "Bill (US male)"
#     Matilda = "Matilda (US female)"
#     Jessica = "Jessica (US female)"
#     Hope = "Hope (US female)"
#     Cassidy = "Cassidy (US female)"
#     George = "George (UK male)"
#     Archer = "Archer (UK male)"
#     AdamUK = "Adam (UK male)"
#     Lily = "Lily (UK female)"
#     Amelia = "Amelia (UK female)"
#     AnaRita = "Ana-Rita (UK female)"
#     Wahab = "Wahab (Arabic male)"
#     Haytham = "Haytham (Arabic male)"
#     Sana = "Sana (Arabic female)"
#     Martin = "Martin (Chinese male)"
#     Guillaume = "Guillaume (French male)"
#     Hugo = "Hugo (French male)"
#     Darine = "Darine (French female)"
#     Jessy = "Jessy (French female)"
#     Kurt = "Kurt (German male)"
#     Otto = "Otto (German male)"
#     Leonie = "Leonie (German female)"
#     Mila = "Mila (German female)"
#     Niraj = "Niraj (Hindi male)"
#     LeoDeprecated = "Leo (Hindi male)"
#     Leo = "Leo (Hindustani male)"
#     Monika = "Monika (Hindi female)"
#     ShakuntalaDeprecated = "Shakuntala (Hindi female)"
#     Shakuntala = "Shakuntala (Hindustani female)"
#     Maciej = "Maciej (Polish male)"
#     AdamPolish = "Adam (Polish male)"
#     Aneta = "Aneta (Polish female)"
#     Bea = "Bea (Polish female)"
#     Juan = "Juan (Spanish male)"
#     David = "David (Spanish male)"
#     Dan = "Dan (Spanish male)"
#     Gabriela = "Gabriela (Spanish female)"
#     Sara = "Sara (Spanish female)"
