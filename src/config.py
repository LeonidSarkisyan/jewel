import os

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.environ.get("BOT_TOKEN")

ADMIN_ID = os.environ.get("ADMIN_ID")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GIGA_CHAT_API_KEY = os.environ.get("GIGA_CHAT_API_KEY")
WEATHER_API_KEY = os.environ.get("OPEN_WEATHER_KEY")
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

YANDEX_IMAGE_SEARCH_URL = "https://yandex.ru/images"

PHOTO_SERVICE_API_KEY = os.environ.get("PHOTO_SERVICE_API_KEY")
PHOTO_SERVICE_URL = os.environ.get("PHOTO_SERVICE_URL")
ALBUM_ID = os.environ.get("ALBUM_ID")


class Proxy:
    host = os.environ.get("PROXY_HOST")
    port = os.environ.get("PROXY_PORT")
    user = os.environ.get("PROXY_USER")
    password = os.environ.get("PROXY_PASSWORD")


print(Proxy.host)
print(Proxy.port)
