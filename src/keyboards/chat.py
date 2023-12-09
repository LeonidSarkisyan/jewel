from aiogram.utils.keyboard import InlineKeyboardBuilder


#  chat_gpt
def get_chat_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Задать вопрос  🤖", callback_data="ask_chat_gpt")
    inline_keyboard_builder.button(text="Назад  ⬅", callback_data="main_menu")

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


def get_more_question_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Спросить ещё  🤖", callback_data="ask_chat_gpt")

    return inline_keyboard_builder.as_markup()
