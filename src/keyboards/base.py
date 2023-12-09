from aiogram.utils.keyboard import InlineKeyboardBuilder


#  main_menu
def get_main_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Задать вопрос ChatGPT  🤖", callback_data="chat_gpt")
    inline_keyboard_builder.button(text="Узнать погоду в регионе  🌤", callback_data="weather")
    inline_keyboard_builder.button(text="Поиск камня по фото  🔎  💎", callback_data="search_stone")

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()
