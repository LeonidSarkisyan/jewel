from aiogram import Bot
from aiogram.types import Message


async def save_photo(message: Message, bot: Bot):
    document_id = message.photo[-1].file_id
    file_info = await bot.get_file(document_id)
    ext = file_info.file_path.split('.')[-1]
    filename = f"media/{message.photo[-1].file_id}.{ext}"
    await bot.download(message.photo[-1].file_id, destination=filename)
    return filename
