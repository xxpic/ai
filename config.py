import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота (получить у @BotFather в Telegram)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверяем наличие токена
if not BOT_TOKEN:
    raise ValueError("❌ Пожалуйста, установите BOT_TOKEN в файле .env")

# URL для webhook
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Настройки бота
BOT_NAME = "🤖 AI Нейросети Гид"
BOT_DESCRIPTION = "Каталог лучших нейросетей 2025 года"

# Эмодзи для категорий
CATEGORY_EMOJIS = {
    "programming": "💻",
    "text": "✍️",
    "image": "🎨",
    "music": "🎵",
    "video": "🎬",
    "voice": "🎤",
    "data": "📊",
    "translation": "🌐",
    "search": "🔍",
    "other": "🔧"
}

# Настройки Telegram Stars
STARS_PACKAGES = {
    "small": {
        "stars": 50,
        "price": 50,
        "title": "☕ Кофе разработчику",
        "description": "Поддержите развитие бота покупкой кофе!"
    },
    "medium": {
        "stars": 150,
        "price": 150,
        "title": "🍕 Пицца для команды",
        "description": "Помогите команде разработки подкрепиться!"
    },
    "large": {
        "stars": 500,
        "price": 500,
        "title": "🚀 Ускоренное развитие",
        "description": "Ваш вклад в быстрое добавление новых функций!"
    },
    "premium": {
        "stars": 1000,
        "price": 1000,
        "title": "💎 VIP поддержка",
        "description": "Премиум поддержка проекта и приоритетные обновления!"
    }
}

# ID автора для получения Stars (замените на ваш)
AUTHOR_USER_ID = int(os.getenv("AUTHOR_USER_ID", "797749459"))