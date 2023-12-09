from gigachat import GigaChat

from src.config import GIGA_CHAT_API_KEY


giga = GigaChat(credentials=GIGA_CHAT_API_KEY, verify_ssl_certs=False)
