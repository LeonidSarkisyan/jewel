from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


#  search_stone
def get_main_gem_main_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(
        text="Найти камень на маркетплейсах  🔎  💎  🛒",
        callback_data="market_gem"
    )
    inline_keyboard_builder.button(text="Назад  ⬅", callback_data="main_menu")

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


def get_list_links(links: list[dict[str, str]]):
    inline_keyboard_builder = InlineKeyboardBuilder()

    index = 1
    for link in links:
        inline_keyboard_builder.button(
            text=f"{index}",
            url=link["link"]
        )
        index += 1
    inline_keyboard_builder.button(text="Назад  ⬅", callback_data="search_stone")

    inline_keyboard_builder.adjust(5, 1)

    return inline_keyboard_builder.as_markup()
