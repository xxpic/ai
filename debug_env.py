import os
from dotenv import load_dotenv

print("🔍 Отладка переменных окружения")
print("=" * 50)

# Проверяем существование .env файла
env_file = ".env"
if os.path.exists(env_file):
    print(f"✅ Файл {env_file} найден")
    
    # Читаем содержимое файла
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"📄 Содержимое файла .env:")
        print("-" * 30)
        print(content)
        print("-" * 30)
else:
    print(f"❌ Файл {env_file} НЕ найден")
    print("💡 Создайте файл .env в корне проекта")

print("\n🔧 Загружаем переменные окружения...")
load_dotenv()

# Проверяем токен
bot_token = os.getenv("BOT_TOKEN")
author_id = os.getenv("AUTHOR_USER_ID")

print(f"🤖 BOT_TOKEN: {'✅ Установлен' if bot_token else '❌ НЕ установлен'}")
if bot_token:
    print(f"   Длина токена: {len(bot_token)} символов")
    print(f"   Начинается с: {bot_token[:10]}...")

print(f"👤 AUTHOR_USER_ID: {'✅ Установлен' if author_id else '❌ НЕ установлен'}")
if author_id:
    print(f"   Значение: {author_id}")

print("\n📁 Текущая директория:", os.getcwd())
print("📋 Файлы в директории:")
for file in os.listdir("."):
    print(f"   - {file}")

print("\n💡 Если токен установлен правильно, но ошибка остается:")
print("   1. Проверьте, что в .env нет пробелов вокруг знака =")
print("   2. Убедитесь, что файл .env в кодировке UTF-8")
print("   3. Проверьте, что токен не содержит лишних символов")
print("   4. Формат должен быть: BOT_TOKEN=1234567890:ABCD...")