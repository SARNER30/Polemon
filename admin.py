from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID  # Импортируем из вашего конфига
from database import add_pokemon_to_user, give_user_coins, get_user_by_username
from keyboards import (
    admin_kb,
    cancel_kb,
    back_to_admin_kb
)
from states import CreatePokemonState
from utils import save_pokemon_image, add_custom_pokemon_to_json

router = Router(name="admin")

# Универсальная проверка админских прав
def admin_required(handler):
    async def wrapper(event: types.Message | types.CallbackQuery, *args, **kwargs):
        if event.from_user.id != ADMIN_ID:
            if isinstance(event, types.CallbackQuery):
                await event.answer("⛔ Доступ запрещен", show_alert=True)
            else:
                await event.answer("⛔ Доступ запрещен")
            return
        return await handler(event, *args, **kwargs)
    return wrapper

# Основное меню админа
@router.message(Command("admin"))
@admin_required
async def admin_panel(message: Message):
    await message.answer(
        "🛠 Админ-панель:",
        reply_markup=admin_kb()
    )

# Раздел создания покемона
@router.callback_query(F.data == "create_pokemon"))
@admin_required
async def start_pokemon_creation(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🎮 Режим создания покемона:\n"
        "Пришлите изображение покемона",
        reply_markup=cancel_kb()
    )
    await state.set_state(CreatePokemonState.waiting_for_image)

@router.message(CreatePokemonState.waiting_for_image, F.photo)
@admin_required
async def process_pokemon_image(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(image=photo_id)
    
    await message.answer(
        "📝 Теперь введите название покемона:",
        reply_markup=cancel_kb()
    )
    await state.set_state(CreatePokemonState.waiting_for_name)

@router.message(CreatePokemonState.waiting_for_name)
@admin_required
async def process_pokemon_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    
    await message.answer(
        "⚔️ Введите характеристики через пробел (HP Атака Защита):\n"
        "Пример: 100 50 30",
        reply_markup=cancel_kb()
    )
    await state.set_state(CreatePokemonState.waiting_for_stats)

@router.message(CreatePokemonState.waiting_for_stats)
@admin_required
async def process_pokemon_stats(message: Message, state: FSMContext):
    try:
        hp, attack, defense = map(int, message.text.split())
        data = await state.get_data()
        
        pokemon_data = {
            "id": f"custom_{data['name'].lower()}",
            "name": data['name'],
            "hp": hp,
            "attack": attack,
            "defense": defense,
            "image": data['image']
        }
        
        add_custom_pokemon_to_json(pokemon_data)
        await save_pokemon_image(data['image'], f"{data['name']}.jpg")
        
        await message.answer(
            f"✅ Покемон {data['name']} создан!\n"
            f"HP: {hp} ⚔️ ATK: {attack} 🛡 DEF: {defense}",
            reply_markup=back_to_admin_kb()
        )
        await state.clear()
        
    except ValueError:
        await message.answer("❌ Неверный формат! Нужно 3 числа через пробел")

# Выдача покемона пользователю
@router.callback_query(F.data == "give_pokemon"))
@admin_required
async def ask_for_pokemon_data(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "👤 Введите @username и ID покемона через пробел:\n"
        "Пример: @username pikachu\n"
        "Для кастомных: @username custom_имя",
        reply_markup=cancel_kb()
    )
    await state.set_state("waiting_for_pokemon_gift")

@router.message(F.text.regexp(r'^@\w+\s.+$'), state="waiting_for_pokemon_gift")
@admin_required
async def process_pokemon_gift(message: Message, state: FSMContext):
    username = message.text.split()[0][1:]
    pokemon_id = message.text.split()[1]
    
    user = await get_user_by_username(username)
    if not user:
        return await message.answer("❌ Пользователь не найден")
    
    success = await add_pokemon_to_user(user['id'], pokemon_id)
    if success:
        await message.answer(
            f"✅ Покемон {pokemon_id} выдан @{username}",
            reply_markup=back_to_admin_kb()
        )
    else:
        await message.answer(
            "❌ Ошибка: возможно, такого покемона не существует",
            reply_markup=back_to_admin_kb()
        )
    await state.clear()

# Выдача монет
@router.callback_query(F.data == "give_coins"))
@admin_required
async def ask_for_coins_data(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "💰 Введите @username и сумму через пробел:\n"
        "Пример: @username 500",
        reply_markup=cancel_kb()
    )
    await state.set_state("waiting_for_coins_gift")

@router.message(F.text.regexp(r'^@\w+\s\d+$'), state="waiting_for_coins_gift")
@admin_required
async def process_coins_gift(message: Message, state: FSMContext):
    username = message.text.split()[0][1:]
    amount = int(message.text.split()[1])
    
    user = await get_user_by_username(username)
    if not user:
        return await message.answer("❌ Пользователь не найден")
    
    await give_user_coins(user['id'], amount)
    await message.answer(
        f"✅ @{username} получил {amount} монет",
        reply_markup=back_to_admin_kb()
    )
    await state.clear()

# Отмена действий
@router.callback_query(F.data == "cancel_action"))
@admin_required
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "❌ Действие отменено",
        reply_markup=admin_kb()
    )