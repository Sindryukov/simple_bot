import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(os.getenv("ADMIN_ID", "0"))]

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден!")

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "🚆 **Привет! Я помощник по электропоезду ЭШ2**\n\n"
        "Я работаю с документацией и отвечаю на вопросы.\n\n"
        "📄 **Как пользоваться:**\n"
        "• Отправьте мне PDF-файл с инструкцией\n"
        "• Я сохраню её в базу знаний\n"
        "• Задавайте любые вопросы — я найду ответ!\n\n"
        "📖 /help — помощь\n"
        "📊 /stats — статистика",
        parse_mode="Markdown"
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "📖 **Помощь**\n\n"
        "1. Отправьте PDF с инструкцией по электропоезду\n"
        "2. Я обработаю и сохраню документ\n"
        "3. Задавайте вопросы — я ищу ответ в базе знаний\n\n"
        "Примеры:\n"
        "• Какое давление в тормозной системе ЭШ2?\n"
        "• Как проверить уровень масла?",
        parse_mode="Markdown"
    )

@dp.message(Command("stats"))
async def stats_command(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Только администратор.")
        return
    await message.answer("📊 База знаний активна. Можно задавать вопросы!")

@dp.message(lambda message: message.document)
async def handle_document(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Только администратор.")
        return
    
    if not message.document.file_name.endswith('.pdf'):
        await message.answer("❌ Поддерживаются только PDF.")
        return
    
    await message.answer(f"📥 Получен файл: {message.document.file_name}\n✅ Сохранён. Скоро добавлю обработку!")

@dp.message()
async def echo(message: types.Message):
    await message.answer(
        f"📚 **Ваш вопрос:**\n{message.text}\n\n"
        "⚠️ Полноценная работа с документами настраивается.\n"
        "Скоро я смогу искать ответы в ваших инструкциях!",
        parse_mode="Markdown"
    )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("🤖 Простой бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())