from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, URLInputFile, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from src.utils.files import save_photo
from src.utils.messages import MAIN_GEM_MESSAGE, ASK_GEM_PHOTO_MESSAGE
from src.keyboards.gem import get_main_gem_main_keyboard, get_list_links
from src.gem.service import gem_service


router = Router()


@router.callback_query(F.data == "search_stone")
async def send_gem_menu(call: CallbackQuery):
    await call.message.edit_text(MAIN_GEM_MESSAGE, reply_markup=get_main_gem_main_keyboard())


class GemPhotoStates(StatesGroup):
    get_photo = State()


@router.callback_query(F.data == "market_gem")
async def ask_gem_photo(call: CallbackQuery, state: FSMContext):
    await call.message.answer(ASK_GEM_PHOTO_MESSAGE)
    await state.set_state(GemPhotoStates.get_photo)
    await call.answer()


@router.message(GemPhotoStates.get_photo)
async def get_photo_and_send_links(message: Message, bot: Bot, state: FSMContext):
    if message.photo:
        await message.answer("Фото получено, начинаю поиск...  🔎")
        await state.clear()
        filename = await save_photo(message, bot)
        links = gem_service.get_links_by_photo(filename)
        media = []
        for link in links:
            photo = URLInputFile(url=link["image_link"])
            media.append(InputMediaPhoto(type="photo", media=photo))
        await message.answer_media_group(media)
        await message.answer("Полученные ссылки:", reply_markup=get_list_links(links))
    else:
        await message.answer("Отправьте фотографию!")
