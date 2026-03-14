import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# Берем токен из переменных окружения (Koyeb)
TOKEN = os.getenv("BOT_TOKEN")
# ВАЖНО: Добавлен параметр ?v=FINAL_TEST для обхода кэша
WEB_APP_URL = "https://kain602.github.io/Kain/?v=FINAL_TEST"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# База данных в памяти (кто кому пишет)
anon_targets = {}

@dp.message(CommandStart())
async def start(message: types.Message):
    args = message.text.split()
    
    # Если зашли через анонимную ссылку (например, /start 12345)
    if len(args) > 1:
        target_id = args[1]
        anon_targets[message.from_user.id] = target_id
        await message.answer("🤫 Ты в анонимном режиме. Напиши что угодно, и я передам это владельцу ссылки!")
    else:
        # Главное меню с Web App
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Открыть меню функций", web_app=WebAppInfo(url=WEB_APP_URL))]
        ])
        await message.answer("Привет! Я бот Kain. Нажми на кнопку, чтобы открыть меню:", reply_markup=markup)

# Обработка выбора из Web App
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    data = message.web_app_data.data
    
    if data == "anon_link":
        me = await bot.get_me()
        link = f"https://t.me/{me.username}?start={message.from_user.id}"
        await message.answer(f"✅ Твоя личная анонимная ссылка:\n\n`{link}`\n\nРассылай её друзьям!", parse_mode="Markdown")
        
    elif data == "group_chat":
        # Мини-меню для выбора количества людей
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="2 чел", callback_data="g2"),
             InlineKeyboardButton(text="3 чел", callback_data="g3"),
             InlineKeyboardButton(text="4 чел", callback_data="g4")]
        ])
        await message.answer("Выберите количество участников для анонимного канала:", reply_markup=kb)

# Заглушка для группового чата
@dp.callback_query(F.data.startswith("g"))
async def group_callback(call: types.CallbackQuery):
    await call.message.answer(f"⚙️ Функция создания канала на {call.data[1]} чел. в разработке!")
    await call.answer()

# Пересылка анонимных сообщений
@dp.message()
async def forwarder(message: types.Message):
    target = anon_targets.get(message.from_user.id)
    if target:
        try:
            await bot.send_message(target, "📩 Новое анонимное сообщение:")
            await message.copy_to(target)
            await message.answer("✅ Сообщение доставлено!")
        except:
            await message.answer("❌ Ошибка доставки.")
    else:
        await message.answer("Используй /start для вызова меню.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
