import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# Настройка логирования
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
# Мы добавили ?v=999 в конец, чтобы сбросить кэш Телеграма
WEB_APP_URL = "https://kain602.github.io/Kain/?v=999"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище связей: кто кому пишет анонимно
user_connections = {}

@dp.message(CommandStart())
async def start_command(message: types.Message):
    args = message.text.split()
    
    # Если зашли по ссылке /start 12345
    if len(args) > 1:
        target_id = args[1]
        user_connections[message.from_user.id] = target_id
        await message.answer("🤫 Теперь ты можешь написать анонимное сообщение этому человеку.\nПросто отправь текст, фото или видео!")
    else:
        # Обычный старт
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Открыть меню", web_app=WebAppInfo(url=WEB_APP_URL))]
        ])
        await message.answer("Добро пожаловать! Нажми на кнопку ниже, чтобы начать работу:", reply_markup=kb)

# Обработка выбора из Web App
@dp.message(F.web_app_data)
async def web_app_handler(message: types.Message):
    choice = message.web_app_data.data
    
    if choice == "anon_link":
        bot_info = await bot.get_me()
        link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"
        await message.answer(f"✅ Твоя личная ссылка для анонимных вопросов:\n\n`{link}`", parse_mode="Markdown")
        
    elif choice == "group_chat":
        await message.answer("👥 Функция создания групповых чатов сейчас находится в разработке!")

# Пересылка сообщений
@dp.message()
async def forward_messages(message: types.Message):
    target = user_connections.get(message.from_user.id)
    if target:
        try:
            await bot.send_message(target, "📩 Пришло анонимное сообщение:")
            await message.copy_to(chat_id=target)
            await message.answer("✅ Отправлено!")
        except Exception:
            await message.answer("❌ Не удалось отправить. Возможно, пользователь заблокировал бота.")
    else:
        await message.answer("Чтобы получить свою ссылку, нажми на кнопку 'Открыть меню' в /start")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
