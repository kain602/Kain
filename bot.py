import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# ВСТАВЬ СВОЙ ТОКЕН В КАВЫЧКИ НИЖЕ
TOKEN = "ЗДЕСЬ_ТВОЙ_ТОКЕН_ОТ_BOTFATHER"
# Ссылка с новым хвостиком, чтобы Гитхаб проснулся
URL = "https://kain602.github.io/Kain/index.html?v=999"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ПРОВЕРКА МЕНЮ", web_app=WebAppInfo(url=URL))]
    ])
    await message.answer("Если кнопка ниже называется 'ПРОВЕРКА МЕНЮ', значит код обновился!", reply_markup=markup)

@dp.message(F.web_app_data)
async def wh(message: types.Message):
    await message.answer(f"Данные получены: {message.web_app_data.data}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
