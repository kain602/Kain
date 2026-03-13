import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# Токен берем из настроек Koyeb
TOKEN = os.getenv("BOT_TOKEN")
# Твоя ссылка на GitHub Pages
WEB_APP_URL = "https://kain602.github.io/Kain/" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Временное хранилище связей (в идеале нужна база данных)
user_connections = {}

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    args = message.text.split()
    # Если зашли по анонимной ссылке
    if len(args) > 1:
        owner_id = args[1]
        user_connections[message.from_user.id] = owner_id
        await message.answer("🤫 Ты в анонимном чате! Пришли текст, фото или видео, и я передам их владельцу ссылки.")
    else:
        # Кнопка для открытия твоего сайта
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Открыть меню функций", web_app=WebAppInfo(url=WEB_APP_URL))]
        ])
        await message.answer("Привет! Я твой многофункциональный бот. Открой меню, чтобы выбрать нужную опцию:", reply_markup=kb)

# Обработка данных из Web App (когда нажал на карточку на сайте)
@dp.message(F.web_app_data)
async def web_app_handler(message: types.Message):
    data = message.web_app_data.data
    
    if data == "anon_link":
        bot_user = await bot.get_me()
        link = f"https://t.me/{bot_user.username}?start={message.from_user.id}"
        await message.answer(f"✅ Твоя личная ссылка для анонимных вопросов:\n\n`{link}`\n\nРазмести её в соцсетях!", parse_mode="Markdown")
        
    elif data == "group_chat":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="2 человека", callback_data="g_2")],
            [InlineKeyboardButton(text="3 человека", callback_data="g_3")],
            [InlineKeyboardButton(text="4 человека", callback_data="g_4")]
        ])
        await message.answer("Выбери количество участников для создания канала:", reply_markup=kb)

# Обработка выбора группы (заглушка)
@dp.callback_query(F.data.startswith("g_"))
async def group_callback(callback: types.CallbackQuery):
    count = callback.data.split("_")[1]
    await callback.message.answer(f"⚙️ Функция создания канала на {count} человек сейчас настраивается.")
    await callback.answer()

# Пересылка анонимных сообщений
@dp.message()
async def forward_logic(message: types.Message):
    target = user_connections.get(message.from_user.id)
    if target:
        try:
            await bot.send_message(target, "📩 Новое анонимное сообщение:")
            await message.copy_to(chat_id=target)
            await message.answer("✅ Отправлено анонимно!")
        except:
            await message.answer("❌ Ошибка: пользователь заблокировал бота.")
    else:
        await message.answer("Используй меню, чтобы сгенерировать ссылку или создать чат.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
