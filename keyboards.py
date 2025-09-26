from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from data import NEURAL_NETWORKS
from config import CATEGORY_EMOJIS

def get_main_menu_keyboard():
    """Создает главную клавиатуру с категориями"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    # Добавляем кнопки для каждой категории
    for category_id, category_data in NEURAL_NETWORKS.items():
        emoji = CATEGORY_EMOJIS.get(category_id, "🔧")
        button_text = f"{emoji} {category_data['name'].replace(emoji + ' ', '')}"
        
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"category:{category_id}"
            )
        ])
    
    # Добавляем кнопки помощи и информации
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="❓ Помощь", callback_data="help"),
        InlineKeyboardButton(text="ℹ️ О боте", callback_data="about")
    ])
    
    return keyboard

def get_category_keyboard(category_id):
    """Создает клавиатуру для конкретной категории"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    if category_id not in NEURAL_NETWORKS:
        return get_main_menu_keyboard()
    
    category_data = NEURAL_NETWORKS[category_id]
    
    # Добавляем кнопки для каждой нейросети в категории
    for network_id, network_data in category_data['networks'].items():
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🤖 {network_data['name']}",
                callback_data=f"network:{category_id}:{network_id}"
            )
        ])
    
    # Кнопка "Назад"
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="⬅️ Назад к категориям", callback_data="main_menu")
    ])
    
    return keyboard

def get_network_keyboard(category_id, network_id):
    """Создает клавиатуру для конкретной нейросети"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    if (category_id not in NEURAL_NETWORKS or 
        network_id not in NEURAL_NETWORKS[category_id]['networks']):
        return get_main_menu_keyboard()
    
    network_data = NEURAL_NETWORKS[category_id]['networks'][network_id]
    
    # Кнопка перехода на сайт нейросети
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text=f"🌐 Перейти на {network_data['name']}",
            url=network_data['url']
        )
    ])
    
    # Кнопки навигации
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="⬅️ К нейросетям категории", 
            callback_data=f"category:{category_id}"
        )
    ])
    
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="🏠 Главное меню", 
            callback_data="main_menu"
        )
    ])
    
    return keyboard

def get_help_keyboard():
    """Создает клавиатуру для раздела помощи"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📂 Категории", callback_data="main_menu")],
        [InlineKeyboardButton(text="👨‍💻 Связь с автором", url="https://t.me/yanparker")],
        [InlineKeyboardButton(text="⭐ Оценить бота", url="https://t.me/neirowiki_bot")]
    ])
    
    return keyboard

def get_about_keyboard():
    """Создает клавиатуру для раздела 'О боте'"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Обновления", callback_data="updates")],
        [InlineKeyboardButton(text="💝 Поддержать проект", callback_data="support")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ])
    
    return keyboard