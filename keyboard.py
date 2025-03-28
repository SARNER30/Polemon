from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    InlineKeyboardBuilder
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_IDS

# Главное меню
def get_main_menu(user_id: int) -> ReplyKeyboardMarkup:
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

# Админ-панель
def get_admin_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💰 Изменить баланс", callback_data="admin_balance"),
        InlineKeyboardButton(text="🎁 Выдать покемона", callback_data="admin_pokemon")
    )
    builder.row(
        InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
        InlineKeyboardButton(text="👥 Список игроков", callback_data="admin_users")
    )
    builder.row(
        InlineKeyboardButton(text="✨ Создать покемона", callback_data="admin_create_pokemon"),
        InlineKeyboardButton(text="🏪 Управление магазином", callback_data="admin_shop_management")
    )
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back"))
    return builder.as_markup()

# Магазин - основное меню
def get_shop_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍️ Товары")],
            [KeyboardButton(text="🏋️‍♂️ Тренеры")],
            [KeyboardButton(text="💼 Мой инвентарь")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )

# Магазин - товары
def get_shop_items_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎣 Покебол (100 монет)", callback_data="buy_pokeball"),
        InlineKeyboardButton(text="🎣 Улучш. покебол (250 монет)", callback_data="buy_greatball")
    )
    builder.row(
        InlineKeyboardButton(text="❤️ Зелье здоровья (50 монет)", callback_data="buy_potion"),
        InlineKeyboardButton(text="✨ Редкий камень (500 монет)", callback_data="buy_stone")
    )
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_shop"))
    return builder.as_markup()

# Магазин - тренеры
def get_shop_trainers_kb(available_trainers: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # Пример тренеров (можно вынести в конфиг)
    trainers = {
        "brock": {"name": "Брок", "price": 500},
        "misty": {"name": "Мисти", "price": 600},
        "oak": {"name": "Проф. Оук", "price": 1000}
    }
    
    for trainer_id in available_trainers:
        if trainer_id in trainers:
            trainer = trainers[trainer_id]
            builder.button(
                text=f"{trainer['name']} ({trainer['price']} монет)",
                callback_data=f"trainer_{trainer_id}"
            )
    
    builder.button(text="🔙 Назад", callback_data="back_to_shop")
    builder.adjust(1)
    return builder.as_markup()

# Подтверждение покупки тренера
def get_confirm_trainer_kb(trainer_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Купить", callback_data=f"buy_trainer_{trainer_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="shop_trainers")
    )
    return builder.as_markup()

# Кнопка "Назад в магазин"
def back_to_shop_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 В магазин", callback_data="back_to_shop")
    return builder.as_markup()

# Кнопка отмены
def cancel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Отмена", callback_data="cancel_action")
    return builder.as_markup()