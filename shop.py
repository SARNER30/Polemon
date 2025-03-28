from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database import (
    get_user_coins,
    add_item_to_user,
    reduce_user_coins,
    get_user_items,
    get_available_trainers
)
from keyboards import (
    shop_main_kb,
    shop_items_kb,
    shop_trainers_kb,
    back_to_shop_kb,
    confirm_purchase_kb
)
from states import ShopStates

router = Router(name="shop")

# Список тренеров и их характеристик
TRAINERS = {
    "brock": {
        "name": "Брок",
        "price": 500,
        "bonus": "Увеличивает защиту всех покемонов на 10%",
        "image": "brock.jpg"
    },
    "misty": {
        "name": "Мисти",
        "price": 600,
        "bonus": "Увеличивает атаку водных покемонов на 15%",
        "image": "misty.jpg"
    },
    "oak": {
        "name": "Профессор Оук",
        "price": 1000,
        "bonus": "Увеличивает шанс поимки покемонов на 20%",
        "image": "oak.jpg"
    }
}

@router.message(Command("shop"))
async def shop_main(message: Message):
    """Главное меню магазина"""
    coins = await get_user_coins(message.from_user.id)
    await message.answer(
        f"🏪 Магазин Покемаркет\n"
        f"💰 Ваш баланс: {coins} монет\n"
        "Выберите раздел:",
        reply_markup=shop_main_kb()
    )

@router.callback_query(F.data == "shop_trainers"))
async def show_trainers(callback: CallbackQuery, state: FSMContext):
    """Показать список доступных тренеров"""
    user_trainers = await get_user_items(callback.from_user.id, item_type="trainer")
    available_trainers = await get_available_trainers(callback.from_user.id)
    
    text = "🏋️‍♂️ Доступные тренеры:\n\n"
    for trainer_id, trainer in TRAINERS.items():
        owned = "✅" if trainer_id in user_trainers else "❌"
        text += (
            f"{owned} {trainer['name']} - {trainer['price']} монет\n"
            f"Бонус: {trainer['bonus']}\n\n"
        )
    
    await callback.message.edit_text(
        text,
        reply_markup=shop_trainers_kb(available_trainers)
    )

@router.callback_query(F.data.startswith("trainer_"))
async def select_trainer(callback: CallbackQuery, state: FSMContext):
    """Выбор конкретного тренера для покупки"""
    trainer_id = callback.data.split("_")[1]
    trainer = TRAINERS.get(trainer_id)
    
    if not trainer:
        return await callback.answer("Тренер не найден", show_alert=True)
    
    await state.update_data(selected_trainer=trainer_id)
    
    await callback.message.edit_text(
        f"🏋️‍♂️ Тренер: {trainer['name']}\n"
        f"💵 Цена: {trainer['price']} монет\n"
        f"✨ Бонус: {trainer['bonus']}\n\n"
        "Хотите приобрести этого тренера?",
        reply_markup=confirm_purchase_kb(trainer_id)
    )

@router.callback_query(F.data.startswith("confirm_trainer_"))
async def buy_trainer(callback: CallbackQuery, state: FSMContext):
    """Подтверждение покупки тренера"""
    trainer_id = callback.data.split("_")[2]
    trainer = TRAINERS.get(trainer_id)
    user_coins = await get_user_coins(callback.from_user.id)
    
    if not trainer:
        return await callback.answer("Тренер не найден", show_alert=True)
    
    if user_coins < trainer['price']:
        return await callback.answer("Недостаточно монет", show_alert=True)
    
    # Покупка тренера
    await reduce_user_coins(callback.from_user.id, trainer['price'])
    await add_item_to_user(callback.from_user.id, trainer_id, "trainer")
    
    await callback.message.edit_text(
        f"🎉 Поздравляем! Вы приобрели тренера {trainer['name']}!\n"
        f"Теперь ваш бонус: {trainer['bonus']}",
        reply_markup=back_to_shop_kb()
    )
    await state.clear()

@router.callback_query(F.data == "back_to_shop"))
async def back_to_shop(callback: CallbackQuery):
    """Возврат в главное меню магазина"""
    coins = await get_user_coins(callback.from_user.id)
    await callback.message.edit_text(
        f"🏪 Магазин Покемаркет\n"
        f"💰 Ваш баланс: {coins} монет",
        reply_markup=shop_main_kb()
    )