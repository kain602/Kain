import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# Получаем токен из настроек Koyeb (Environment Variables)
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
user_connections = {}

@dp.message(CommandStart())
async def start_command(message: types.Message):
    args = message.text.split()
    if len(args) > 1:
        owner_id = args[1]
        user_connections[message.from_user.id] = owner_id
        await message.answer("🤫 Ты в анонимном чате! Пришли фото, видео или голос.")
    else:
        # Ссылка на бота (динамически берем имя бота)
        bot_info = await bot.get_me()
        link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Мой Web App", web_app=WebAppInfo(url="https://твой-сайт.com"))],
            [InlineKeyboardButton(text="🔗 Поделиться ссылкой", url=f"https://t.me/share/url?url={link}")]
        ])
        
        await message.answer(f"Твоя анонимная ссылка:\n{link}", reply_markup=kb)

@dp.message()
async def forward_to_owner(message: types.Message):
    target_id = user_connections.get(message.from_user.id)
    if target_id:
        try:
            await bot.send_message(target_id, "📩 Новое анонимное сообщение:")
            await message.copy_to(chat_id=target_id)
            await message.answer("✅ Отправлено!")
        except Exception:
            await message.answer("❌ Ошибка отправки.")
    else:
        await message.answer("Создай свою ссылку через /start")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
