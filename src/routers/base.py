from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.utils.messages import MAIN_MESSAGE, CANCEL_MESSAGE
from src.keyboards.base import get_main_keyboard


router = Router()


@router.message(Command("start"))
async def start_core(message: Message):
    await message.answer(f"Привет, <b>{message.from_user.first_name}</b>!  👋")
    await message.answer(MAIN_MESSAGE, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "main_menu")
async def start_call(call: CallbackQuery):
    await call.message.edit_text(MAIN_MESSAGE, reply_markup=get_main_keyboard())


@router.message(Command("cancel"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(CANCEL_MESSAGE)
