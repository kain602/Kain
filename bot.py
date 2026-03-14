import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

TOKEN = os.getenv("BOT_TOKEN")
# Мы меняем версию ссылки на v100, чтобы Telegram скачал сайт заново
URL = "https://kain602.github.io/Kain/?v=100"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    # Создаем кнопку с ПРЯМОЙ ссылкой на GitHub Pages
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 ОТКРЫТЬ МЕНЮ (V100)", web_app=WebAppInfo(url=URL))]
    ])
    await message.answer("Бот обновлен! Нажми на кнопку ниже:", reply_markup=kb)

@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    # Логика обработки нажатий на карточки
    res = message.web_app_data.data
    if res == "anon_link":
        user_id = message.from_user.id
        bot_user = await bot.get_me()
        await message.answer(f"Твоя ссылка: t.me/{bot_user.username}?start={user_id}")
    else:
        await message.answer(f"Выбрано: {res}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
