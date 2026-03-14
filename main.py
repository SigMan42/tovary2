# bot.py
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
import urllib.parse
import asyncio

# ⚠️ ЗАМЕНИ ЭТО НА СВОЙ ТОКЕН БОТА (получи у @BotFather)
BOT_TOKEN = "8535980393:AAE2eh7I7U6o6vxUc8k8pUQfpHClGu50cKI"  # ← ТУТ ТВОЙ ТОКЕН!

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def generate_links(query):
    """Генерирует ссылки на магазины по поисковому запросу"""
    return {
        "Ozon": f"https://www.ozon.ru/search/?text={urllib.parse.quote(query)}",
        "Yandex.Market": f"https://market.yandex.ru/search?text={urllib.parse.quote(query)}"
    }

@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "👋 Привет! Я бот для поиска товаров.\n"
        "Напиши название вещи — например: «синяя кофта с рукавом»\n"
        "Я найду её на Ozon и Яндекс.Маркете."
    )

@dp.message()
async def handle_text(message: Message):
    if message.photo:
        await message.answer(
            "📸 Я пока не умею искать по фото.\n"
            "Пожалуйста, напиши название одежды текстом, например:\n"
            "«красная кофта с воротником»"
        )
        return

    query = message.text.strip()
    if not query:
        await message.answer("Пожалуйста, введите название товара.")
        return

    links = generate_links(query)
    response = "🔍 Вот ссылки по запросу «" + query + "»:\n\n"
    for site, url in links.items():
        response += f"🔹 [{site}]({url})\n"

    await message.answer(response, parse_mode="Markdown")

# Главная функция запуска
async def main():
    # Удаляем вебхуки (если были установлены ранее)
    await bot.delete_webhook(drop_pending_updates=True)
    print("🚀 Бот запущен и ожидает сообщений...")
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
