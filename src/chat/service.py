from gigachat import GigaChat

from src.chat.base import giga


class GigaChatService:

    def __init__(self, giga_chat: GigaChat):
        self.giga = giga_chat

    def ask_question(self, messages: list[str]) -> str:
        message = self.giga.chat({"messages": messages})
        return message.choices[0].message.content


giga_chat_service = GigaChatService(giga)
