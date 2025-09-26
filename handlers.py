from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from data import NEURAL_NETWORKS
from keyboards import (
    get_main_menu_keyboard, 
    get_category_keyboard, 
    get_network_keyboard,
    get_help_keyboard,
    get_about_keyboard
)
from config import BOT_NAME, BOT_DESCRIPTION, AUTHOR_USER_ID
from stars import (
    get_support_info_text,
    get_support_keyboard,
    create_stars_invoice,
    get_payment_keyboard,
    handle_successful_payment,
    get_stars_statistics_text
)


# Создаем роутер для обработчиков
router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    """Обработчик команды /start"""
    welcome_text = f"""🤖 Добро пожаловать в {BOT_NAME}!

{BOT_DESCRIPTION}

🎯 **Что может этот бот:**
• 📂 Категории нейросетей по областям применения
• 🤖 Подробная информация о каждой ИИ
• 💰 Актуальные цены и бесплатные возможности  
• 🔗 Прямые ссылки на официальные сайты
• ⚡ Регулярные обновления базы данных

Выберите интересующую вас категорию:"""

    await message.answer(
        text=welcome_text,
        reply_markup=get_main_menu_keyboard()
    )

@router.message(Command("categories"))
async def categories_command(message: Message):
    """Обработчик команды /categories"""
    categories_text = "📂 **Доступные категории нейросетей:**\n\n"
    
    for category_id, category_data in NEURAL_NETWORKS.items():
        networks_count = len(category_data['networks'])
        categories_text += f"• {category_data['name']} ({networks_count} нейросетей)\n"
        categories_text += f"  _{category_data['description']}_\n\n"
    
    categories_text += "Выберите категорию для просмотра доступных нейросетей:"
    
    await message.answer(
        text=categories_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )

@router.message(Command("help"))
async def help_command(message: Message):
    """Обработчик команды /help"""
    help_text = """❓ **Помощь по использованию бота**

🔍 **Как пользоваться:**
1. Выберите категорию нейросетей
2. Просмотрите список доступных ИИ
3. Кликните на интересующую нейросеть
4. Изучите описание и возможности
5. Перейдите на официальный сайт

📋 **Доступные команды:**
• `/start` - Запустить бота заново
• `/categories` - Показать все категории
• `/help` - Показать эту справку

🆕 **Обновления:**
База данных нейросетей регулярно обновляется с актуальной информацией о ценах и возможностях.

⚠️ **Важно:**
Цены и условия могут изменяться. Всегда проверяйте актуальную информацию на официальных сайтах нейросетей."""

    await message.answer(
        text=help_text,
        reply_markup=get_help_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):
    """Обработчик возврата в главное меню"""
    main_menu_text = f"""🏠 **Главное меню - {BOT_NAME}**

📊 **Статистика бота:**
• {len(NEURAL_NETWORKS)} категорий нейросетей
• {sum(len(cat['networks']) for cat in NEURAL_NETWORKS.values())} ИИ в базе данных
• Актуальная информация на {callback.message.date.strftime('%B %Y')}

Выберите категорию для изучения доступных нейросетей:"""

    await callback.message.edit_text(
        text=main_menu_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("category:"))
async def category_callback(callback: CallbackQuery):
    """Обработчик выбора категории"""
    category_id = callback.data.split(":")[1]
    
    if category_id not in NEURAL_NETWORKS:
        await callback.answer("❌ Категория не найдена!", show_alert=True)
        return
    
    category_data = NEURAL_NETWORKS[category_id]
    networks_count = len(category_data['networks'])
    
    category_text = f"""📂 **{category_data['name']}**

📝 _{category_data['description']}_

🤖 **Доступно нейросетей:** {networks_count}

Выберите интересующую вас нейросеть для получения подробной информации:"""

    await callback.message.edit_text(
        text=category_text,
        reply_markup=get_category_keyboard(category_id),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("network:"))
async def network_callback(callback: CallbackQuery):
    """Обработчик выбора нейросети"""
    try:
        _, category_id, network_id = callback.data.split(":")
    except ValueError:
        await callback.answer("❌ Неверный формат данных!", show_alert=True)
        return
    
    if (category_id not in NEURAL_NETWORKS or 
        network_id not in NEURAL_NETWORKS[category_id]['networks']):
        await callback.answer("❌ Нейросеть не найдена!", show_alert=True)
        return
    
    network_data = NEURAL_NETWORKS[category_id]['networks'][network_id]
    
    network_text = f"""🤖 **{network_data['name']}**

📋 **Описание:**
{network_data['description']}

🆓 **Бесплатные возможности:**
{network_data['free_features']}

⚠️ **Ограничения бесплатной версии:**
{network_data['limitations']}

💰 **Стоимость подписки:**
{network_data['pricing']}

🔗 Нажмите кнопку ниже, чтобы перейти на официальный сайт."""

    await callback.message.edit_text(
        text=network_text,
        reply_markup=get_network_keyboard(category_id, network_id),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    """Обработчик кнопки помощи"""
    help_text = """❓ **Справка по боту**

🎯 **Назначение бота:**
Помочь вам найти подходящую нейросеть для ваших задач среди множества доступных вариантов.

🔍 **Как найти нужную нейросеть:**
• Определите тип задачи (программирование, тексты, изображения и т.д.)
• Выберите соответствующую категорию
• Изучите доступные варианты
• Сравните бесплатные возможности и цены
• Перейдите на сайт и начните использовать!

💡 **Советы по выбору:**
• Начинайте с бесплатных версий
• Обращайте внимание на ограничения
• Сравнивайте несколько вариантов
• Читайте отзывы пользователей

📱 **Контакты:**
Если у вас есть предложения по улучшению бота или вы хотите добавить новую нейросеть - свяжитесь с разработчиком."""

    await callback.message.edit_text(
        text=help_text,
        reply_markup=get_help_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "about")
async def about_callback(callback: CallbackQuery):
    """Обработчик кнопки 'О боте'"""
    about_text = f"""ℹ️ **О боте {BOT_NAME}**

🎯 **Миссия:** Упростить выбор подходящей нейросети для любых задач.

📊 **Актуальная статистика:**
• Категорий: {len(NEURAL_NETWORKS)}
• Нейросетей в базе: {sum(len(cat['networks']) for cat in NEURAL_NETWORKS.values())}
• Последнее обновление: Январь 2025

⚡ **Особенности:**
• Актуальные цены и возможности
• Подробные описания каждой ИИ
• Прямые ссылки на официальные сайты
• Регулярные обновления базы данных
• Простая навигация и поиск

🔄 **Обновления:**
Информация о нейросетях обновляется каждый месяц для поддержания актуальности данных о ценах и возможностях.

💝 **Поддержка проекта:**
Если бот полезен для вас, поделитесь им с друзьями и коллегами!"""

    await callback.message.edit_text(
        text=about_text,
        reply_markup=get_about_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "updates")
async def updates_callback(callback: CallbackQuery):
    """Обработчик информации об обновлениях"""
    updates_text = """🔄 **История обновлений**

📅 **Январь 2025:**
• Добавлено 50+ актуальных нейросетей
• Обновлены цены на все сервисы
• Добавлена категория генерации видео
• Улучшен интерфейс бота

📅 **Планируется в феврале 2025:**
• Добавление новых категорий
• Система уведомлений о скидках
• Сравнение нейросетей
• Рейтинги и отзывы пользователей

🆕 **Недавно добавленные нейросети:**
• Luma Dream Machine (видео)
• Claude Sonnet 4 (программирование)
• Suno v4 (музыка)
• Kling AI (видео)

🔔 **Следите за обновлениями** - база данных пополняется каждый месяц!"""

    await callback.message.edit_text(
        text=updates_text,
        reply_markup=get_about_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "support")
async def support_callback(callback: CallbackQuery):
    """Обработчик кнопки поддержки проекта"""
    support_text = get_support_info_text()
    
    await callback.message.edit_text(
        text=support_text,
        reply_markup=get_support_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("support:"))
async def support_package_callback(callback: CallbackQuery):
    """Обработчик выбора пакета поддержки"""
    package_id = callback.data.split(":")[1]
    
    # Создаем инвойс для оплаты
    invoice_link = await create_stars_invoice(
        bot=callback.bot,
        user_id=callback.from_user.id,
        package_id=package_id
    )
    
    if not invoice_link:
        await callback.answer("❌ Ошибка создания платежа. Попробуйте позже.", show_alert=True)
        return
    
    from config import STARS_PACKAGES
    package = STARS_PACKAGES[package_id]
    
    payment_text = f"""💫 **{package['title']}**

📝 **Описание:** {package['description']}
⭐ **Стоимость:** {package['stars']} Telegram Stars
💰 **Цена:** ~{package['stars'] * 0.013:.2f}$ (зависит от региона)

🌟 **Как оплатить:**
1. Нажмите кнопку "Оплатить Stars"
2. Подтвердите платеж в Telegram
3. Получите благодарность от разработчика!

⚡ **Мгновенная обработка** - платеж проходит через Telegram без комиссий для вас!"""

    await callback.message.edit_text(
        text=payment_text,
        reply_markup=get_payment_keyboard(invoice_link, package_id),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    """Обработчик pre-checkout запроса для Stars"""
    # Для Stars всегда подтверждаем платеж
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    """Обработчик успешного платежа"""
    payment = message.successful_payment
    
    success = await handle_successful_payment(
        bot=message.bot,
        user_id=message.from_user.id,
        payload=payment.invoice_payload,
        total_amount=payment.total_amount
    )
    
    if success:
        # Дополнительное сообщение с главным меню
        await message.answer(
            text="🏠 Возвращаемся в главное меню:",
            reply_markup=get_main_menu_keyboard()
        )

# Команда для админа для просмотра статистики (опционально)
@router.message(Command("admin"))
async def admin_command(message: Message):
    """Админ-команды (только для автора)"""
    if message.from_user.id != AUTHOR_USER_ID:
        return
    
    stats_text = get_stars_statistics_text()
    await message.answer(
        text=stats_text,
        parse_mode="Markdown"
    )

@router.message()
async def unknown_message(message: Message):
    """Обработчик неизвестных сообщений"""
    await message.answer(
        text="🤔 Не понимаю, что вы хотите. Используйте кнопки меню или команду /start",
        reply_markup=get_main_menu_keyboard()
    )

def register_handlers(dp):
    """Регистрация всех обработчиков"""
    dp.include_router(router)