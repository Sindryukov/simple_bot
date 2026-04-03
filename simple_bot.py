import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GIGA_KEY = os.getenv("GIGACHAT_API_KEY")  # Ваш новый ключ

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден!")

# ПРАВИЛЬНАЯ инициализация GigaChat
giga = GigaChat(
    credentials=GIGA_KEY,          # Ваш ключ авторизации
    verify_ssl_certs=False,        # Отключаем проверку SSL (для Bothost)
    scope="GIGACHAT_API_PERS",     # Явно указываем версию API для физлиц
)

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "🚆 **Привет! Я помощник по электропоезду ЭШ2**\n\n"
        "Я работаю с документацией и отвечаю на вопросы с помощью GigaChat.\n\n"
        "📄 **Как пользоваться:**\n"
        "• Отправьте мне PDF-файл с инструкцией\n"
        "• Я сохраню её в базу знаний\n"
        "• Задавайте любые вопросы — я найду ответ!\n\n"
        "📖 /help — помощь",
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

@dp.message()
async def answer_with_giga(message: types.Message):
    await message.answer("🤔 Думаю над ответом...")
    
    try:
        # Отправляем запрос к GigaChat
        response = giga.chat(message.text)
        answer = response.choices[0].message.content
        
        await message.answer(f"**Ответ:**\n{answer}", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка GigaChat: {e}\n\nПроверьте API-ключ в настройках.")
        # Выводим подробную ошибку в логи
        logging.error(f"GigaChat error: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("🤖 Бот с GigaChat запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
