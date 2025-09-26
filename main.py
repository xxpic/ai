import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiohttp.web import AppRunner, TCPSite
from handlers import register_handlers
from config import BOT_TOKEN, BOT_NAME, WEBHOOK_URL

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Команды для меню
COMMANDS = [
    BotCommand(command="start", description="🚀 Запустить бота"),
    BotCommand(command="categories", description="📂 Показать категории"),
    BotCommand(command="help", description="❓ Помощь"),
]

async def set_commands(bot: Bot):
    """Установка команд бота"""
    await bot.set_my_commands(COMMANDS)

async def on_startup(bot: Bot):
    """Действия при запуске"""
    bot_info = await bot.get_me()
    logger.info(f"✅ Подключение к Telegram API успешно")
    logger.info(f"👤 Имя бота: @{bot_info.username}")
    logger.info(f"🆔 ID бота: {bot_info.id}")
    
    await set_commands(bot)
    logger.info("⌨️ Команды бота установлены")
    
    # Удаляем старый webhook если есть
    await bot.delete_webhook()
    logger.info("🗑️ Старый webhook удален")
    
    # Установка webhook
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"🔗 Webhook установлен: {WEBHOOK_URL}")

async def main():
    """Основная функция запуска бота"""
    try:
        # Проверяем токен еще раз
        if not BOT_TOKEN:
            raise ValueError("BOT_TOKEN не может быть пустым")
        
        if not WEBHOOK_URL:
            raise ValueError("WEBHOOK_URL не может быть пустым для webhook режима")
        
        logger.info(f"🚀 Запуск бота {BOT_NAME} в webhook режиме...")
        logger.info(f"🔑 Токен: {BOT_TOKEN[:10]}...{BOT_TOKEN[-10:]}")
        logger.info(f"🔗 Webhook URL: {WEBHOOK_URL}")
        
        # Создаем экземпляры бота и диспетчера
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        
        # Регистрируем обработчики
        register_handlers(dp)
        logger.info("📝 Обработчики зарегистрированы")
        
        # Вызов startup
        await on_startup(bot)
        
        # Настройка webhook
        app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
        setup_application(app, dp, bot=bot)
        
        # Асинхронный запуск сервера
        runner = AppRunner(app)
        await runner.setup()
        site = TCPSite(runner, "0.0.0.0", 8080)
        await site.start()
        
        logger.info("🤖 Бот успешно запущен в webhook режиме!")
        logger.info("🌐 Сервер запущен на http://0.0.0.0:8080")
        logger.info("📱 Отправьте /start боту в Telegram для тестирования")
        
        # Держим сервер живым
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"💥 Критическая ошибка при запуске бота: {e}")
        logger.error("🔧 Проверьте конфигурацию и попробуйте снова")
    finally:
        if 'runner' in locals():
            await runner.cleanup()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())