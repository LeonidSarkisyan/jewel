from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from src.weather.russian_cities import get_cities, search_cities_from_file


#  weather
def get_main_weather_menu_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(
        text="Узнать погоду по геолокации  🌤",
        callback_data="ask_weather"
    )
    inline_keyboard_builder.button(
        text="Узнать погоду в городе  🏙",
        callback_data="city_weather"
    )
    inline_keyboard_builder.button(text="Назад  ⬅", callback_data="main_menu")

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


#  ask_weather
def get_location_keyboard():
    reply_keyboard_builder = ReplyKeyboardBuilder()

    reply_keyboard_builder.button(text="Скинуть геолокацию  📍", request_location=True)

    return reply_keyboard_builder.as_markup(
        resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Скиньте геолокацию..."
    )


def get_cities_list_keyboard(search_string: str = None):
    inline_keyboard_builder = InlineKeyboardBuilder()

    if search_string:
        cities = search_cities_from_file(search_string)
    else:
        cities = get_cities()

    for city in cities:
        inline_keyboard_builder.button(
            text=city,
            callback_data=f"weather_city__{city}"
        )

    inline_keyboard_builder.button(
        text="Найти город  🔎", callback_data="search_city"
    )

    inline_keyboard_builder.button(text="Назад  ⬅", callback_data="main_menu")

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()
