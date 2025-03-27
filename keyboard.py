from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_IDS

def get_main_menu(user_id):
    buttons = [
        [KeyboardButton(text="🎣 Ловить покемона")],
        [KeyboardButton(text="📊 Моя статистика")],
        [KeyboardButton(text="📦 Мои покемоны")],
        [KeyboardButton(text="🛒 Магазин")],
        [KeyboardButton(text="📘 Покедекс")]
    ]
    if user_id in ADMIN_IDS:
        buttons.append([KeyboardButton(text="👑 Админ-панель")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Изменить баланс", callback_data="admin_balance"),
         InlineKeyboardButton(text="🎁 Выдать покемона", callback_data="admin_pokemon")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
         InlineKeyboardButton(text="👥 Список игроков", callback_data="admin_users")],
        [InlineKeyboardButton(text="✨ Создать покемона", callback_data="admin_create_pokemon")],
        [InlineKeyboardButton(text="🏪 Управление магазином", callback_data="admin_shop_management")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
    ])

def get_shop_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎣 Купить покебал (500)")],
            [KeyboardButton(text="👨‍🏫 Нанять тренера")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )