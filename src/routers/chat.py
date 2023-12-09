from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.keyboards.chat import get_chat_keyboard, get_more_question_keyboard
from src.chat.service import giga_chat_service
from src.utils.messages import (
    GREETING_CHAT_MESSAGE, ASK_PROMPT_MESSAGE, PLEASE_WAIT_MESSAGE, INCORRECT_PROMPT_MESSAGE
)
from src.chat.context import compare_messages, RoleEnum


router = Router()


class ChatStates(StatesGroup):
    get_prompt = State()
    get_prompt_with_context = State()


@router.callback_query(F.data == "chat_gpt")
async def get_started_chat(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        GREETING_CHAT_MESSAGE,
        reply_markup=get_chat_keyboard()
    )


@router.callback_query(F.data == "ask_chat_gpt")
async def get_prompt(call: CallbackQuery, state: FSMContext):
    await call.message.answer(ASK_PROMPT_MESSAGE)
    await state.set_state(ChatStates.get_prompt)
    await call.answer()


@router.message(ChatStates.get_prompt)
async def answer_to_prompt(message: Message, state: FSMContext):
    data = await state.get_data()
    messages_context = data.get("messages_context")
    if not messages_context:
        messages_context = []
    if message.text and not message.sticker:
        please_wait_message = await message.answer(PLEASE_WAIT_MESSAGE)
        messages_context = compare_messages(message.text, RoleEnum.user, messages_context)
        message_from_giga_chat = giga_chat_service.ask_question(messages_context)
        messages_context = compare_messages(message_from_giga_chat, RoleEnum.assistant, messages_context)
        await please_wait_message.delete()
        await message.answer(message_from_giga_chat)
        await state.update_data(messages_context=messages_context)
    else:
        await message.answer(INCORRECT_PROMPT_MESSAGE)
