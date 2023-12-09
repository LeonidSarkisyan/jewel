
# main

MAIN_MESSAGE = """
Я бот, который умеет:\n
<b>1.</b> Отвечать на любые вопросы  ❔\n
<b>2.</b> Показывать погоду  🌤\n
<b>3.</b> Искать драгоценные камни по фото 💎
"""

CANCEL_MESSAGE = "Вы отменили действие!"


# chat

GREETING_CHAT_MESSAGE = "Что вы хотите сделать с нейросетью?\n\n"

ASK_PROMPT_MESSAGE = "Спросите меня о чём-нибудь  👇👇👇"

PLEASE_WAIT_MESSAGE = "Пожалуйста, подождите немного, пока я обработую ваш запрос..."

INCORRECT_PROMPT_MESSAGE = "Некорректный запрос! Напишите ещё раз!"


#  weather

def get_message_about_weather(weather_data: dict):
    return f"""        
{weather_data["type"]}, {with_sign(weather_data["temp"])}°C (ощущается как {with_sign(weather_data["temp_feels_like"])}°C)
    
Давление: {weather_data["pressure"]} гПа
Влажность: {weather_data["humidity"]}% 💧
"""


def with_sign(value: float):
    return f"+{value}" if value >= 0 else f"{value}"


MAIN_WEATHER_MESSAGE = "Что вам подсказать по погоде?"

ASK_GEOLOCATION_MESSAGE = "Чтобы я мог сказать вам погоду, пришлите геолокацию  👇👇👇"

GET_GEOLOCATION_MESSAGE = "Локация получена, узнаю погоду..."

INCORRECT_LOCATION_MESSAGE = "Вы прислали что-то другое, попробуйте ещё раз"

CHOOSE_CITY_MESSAGE = "Выберите город или воспользуйтесь поиском  🔎"


def get_city_weather_message(city: str):
    return f"Погода в городе: {city}"


ASK_SEARCH_CITY_MESSAGE = "Напишите запрос (поиск работает с начала названия города)  👇👇👇"

INCORRECT_SEARCH_MESSAGE = "Некорректный запрос (введите текст)"
