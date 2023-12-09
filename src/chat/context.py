from enum import Enum


class RoleEnum(Enum):
    user = "user"
    assistant = "assistant"


def compare_messages(message_text: str, role: RoleEnum, old_messages: list):
    message = {
        "role": role.value,
        "content": message_text
    }
    return [*old_messages, message]

