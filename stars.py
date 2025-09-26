import logging
from aiogram import Bot
from aiogram.types import LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from config import STARS_PACKAGES, AUTHOR_USER_ID

logger = logging.getLogger(__name__)

def get_support_keyboard():
    """Создает клавиатуру с вариантами поддержки проекта"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    # Добавляем кнопки для каждого пакета Stars
    for package_id, package_data in STARS_PACKAGES.items():
        stars_count = package_data['stars']
        title = package_data['title']
        
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"⭐ {title} ({stars_count} Stars)",
                callback_data=f"support:{package_id}"
            )
        ])
    
    # Добавляем кнопку "Назад"
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="⬅️ Назад", callback_data="about")
    ])
    
    return keyboard

async def create_stars_invoice(bot: Bot, user_id: int, package_id: str):
    """Создает инвойс для оплаты Stars"""
    
    if package_id not in STARS_PACKAGES:
        logger.error(f"Неизвестный пакет: {package_id}")
        return None
    
    package = STARS_PACKAGES[package_id]
    
    try:
        # Создаем инвойс для Telegram Stars
        invoice_link = await bot.create_invoice_link(
            title=package['title'],
            description=package['description'],
            payload=f"support_{package_id}_{user_id}",
            currency="XTR",  # XTR - валюта для Telegram Stars
            prices=[
                LabeledPrice(
                    label=f"{package['stars']} Telegram Stars",
                    amount=package['price']
                )
            ],
            provider_token=""  # Для Stars токен не нужен
        )
        
        return invoice_link
        
    except Exception as e:
        logger.error(f"Ошибка создания инвойса: {e}")
        return None

def get_payment_keyboard(invoice_link: str, package_id: str):
    """Создает клавиатуру с кнопкой оплаты"""
    package = STARS_PACKAGES[package_id]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"⭐ Оплатить {package['stars']} Stars",
                url=invoice_link
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Выбрать другой пакет",
                callback_data="support"
            )
        ],
        [
            InlineKeyboardButton(
                text="🏠 Главное меню",
                callback_data="main_menu"
            )
        ]
    ])
    
    return keyboard

def get_support_info_text():
    """Возвращает текст с информацией о поддержке"""
    text = """💝 **Поддержка проекта через Telegram Stars**

🌟 **Зачем поддерживать проект?**
• Регулярные обновления базы данных нейросетей
• Добавление новых функций и возможностей
• Поддержание актуальности цен и информации
• Развитие дополнительных сервисов

⭐ **Что такое Telegram Stars?**
Telegram Stars - встроенная валюта Telegram для поддержки создателей контента. Звезды можно купить прямо в приложении и использовать для донатов.

💎 **Преимущества Stars:**
• Безопасные платежи через Telegram
• Мгновенные переводы
• Низкие комиссии
• Поддержка от Telegram

Выберите подходящий пакет поддержки:"""
    
    return text

async def handle_successful_payment(bot: Bot, user_id: int, payload: str, total_amount: int):
    """Обработчик успешного платежа"""
    try:
        # Парсим payload
        parts = payload.split("_")
        if len(parts) >= 3 and parts[0] == "support":
            package_id = parts[1]
            payer_id = int(parts[2])
            
            if package_id in STARS_PACKAGES:
                package = STARS_PACKAGES[package_id]
                
                # Отправляем благодарность пользователю
                thank_you_text = f"""🙏 **Огромное спасибо за поддержку!**

✅ **Платеж успешно обработан:**
• Пакет: {package['title']}
• Сумма: {package['stars']} Stars
• Статус: Подтвержден

🚀 **Что дальше:**
• Ваша поддержка поможет развивать проект
• В ближайших обновлениях появятся новые функции
• Следите за новостями в боте

💝 Спасибо, что помогаете делать бот лучше!"""

                await bot.send_message(
                    chat_id=payer_id,
                    text=thank_you_text,
                    parse_mode="Markdown"
                )
                
                # Уведомляем автора о поддержке
                if AUTHOR_USER_ID and AUTHOR_USER_ID != payer_id:
                    author_notification = f"""💝 **Новая поддержка проекта!**

👤 **Пользователь:** {payer_id}
💰 **Пакет:** {package['title']}
⭐ **Сумма:** {package['stars']} Stars

Время: {total_amount}"""

                    try:
                        await bot.send_message(
                            chat_id=AUTHOR_USER_ID,
                            text=author_notification,
                            parse_mode="Markdown"
                        )
                    except Exception as e:
                        logger.error(f"Не удалось уведомить автора: {e}")
                
                logger.info(f"Успешный платеж: {package_id} от пользователя {payer_id}")
                return True
    
    except Exception as e:
        logger.error(f"Ошибка обработки платежа: {e}")
    
    return False

def get_stars_statistics_text(payments_count: int = 0, total_stars: int = 0):
    """Возвращает статистику по Stars для админ-панели"""
    text = f"""📊 **Статистика поддержки проекта**

💫 **Всего получено Stars:** {total_stars}
🤝 **Количество поддержавших:** {payments_count}
💝 **Средний донат:** {total_stars // payments_count if payments_count > 0 else 0} Stars

📈 **Доступные пакеты:**"""
    
    for package_id, package_data in STARS_PACKAGES.items():
        text += f"\n• {package_data['title']}: {package_data['stars']} ⭐"
    
    text += f"""

🎯 **Цели проекта:**
• Еженедельные обновления базы ИИ
• Добавление новых категорий
• Разработка мобильного приложения
• API для разработчиков

Спасибо всем за поддержку! 🙏"""
    
    return text