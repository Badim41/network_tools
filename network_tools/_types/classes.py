import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


class AspectRatio:
    ratio_1x1 = "1:1"
    ratio_2x3 = "2:3"
    ratio_3x2 = "3:2"


class ImageModels:
    kandinsky = "kandinsky"
    dalle_light = "dalle_light"
    flux = "flux"
    sd_ultra = "sd_ultra"
    flux_dev = "flux_dev"
    sd_xl = "sd_xl"
    recraft = "recraft"
    dalle_3 = "dalle_3"


class GptModels:
    claude_models = "claude_models"
    gpt_4o = "gpt_4o"
    command_r = "command_r"
    o1 = "o1"


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

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "GptResponse":
        chat_history = data["chat_history"]
        response = ResponseDetails(**data["response"])
        return cls(
            chat_history=chat_history,
            cost=data["cost"],
            created=data["created"],
            response=response,
            status=data["status"]
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