import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

TOKEN = os.getenv("BOT_TOKEN")
# ВСТАВЬ СЮДА СВОЮ ССЫЛКУ ИЗ GITHUB PAGES
WEB_APP_URL = "https://твой-ник.github.io/название-репозитория/" 

bot = Bot(token=TOKEN)
dp = Dispatcher()
user_connections = {}

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    args = message.text.split()
    if len(args) > 1:
        user_connections[message.from_user.id] = args[1]
        await message.answer("🤫 Ты в анонимном чате! Пиши сообщение.")
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Меню функций", web_app=WebAppInfo(url=WEB_APP_URL))]
        ])
        await message.answer("Привет! Открой меню, чтобы выбрать действие:", reply_markup=kb)

# ОБРАБОТКА НАЖАТИЙ В WEB APP
@dp.message(F.web_app_data)
async def web_app_handler(message: types.Message):
    action = message.web_app_data.data
    
    if action == "anon_link":
        link = f"https://t.me/{(await bot.get_me()).username}?start={message.from_user.id}"
        await message.answer(f"✅ Твоя ссылка создана:\n{link}")
        
    elif action == "group_chat":
        # Кнопки выбора количества людей
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="2 человека", callback_data="group_2")],
            [InlineKeyboardButton(text="3 человека", callback_data="group_3")],
            [InlineKeyboardButton(text="4 человека", callback_data="group_4")]
        ])
        await message.answer("Выберите количество участников для канала:", reply_markup=kb)

# Обработка выбора группы (заглушка)
@dp.callback_query(F.data.startswith("group_"))
async def group_choice(callback: types.CallbackQuery):
    count = callback.data.split("_")[1]
    await callback.message.answer(f"Создаю канал на {count} чел... (функция в разработке)")
    await callback.answer()

@dp.message()
async def forward(message: types.Message):
    target = user_connections.get(message.from_user.id)
    if target:
        try:
            await message.copy_to(target)
            await message.answer("✅ Отправлено!")
        except:
            await message.answer("❌ Ошибка.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
            
