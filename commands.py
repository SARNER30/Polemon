from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import cursor, conn
from keyboards import get_main_menu
from config import ADMIN_IDS, POKEMONS

async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    user = cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if not user:
        cursor.execute("INSERT INTO users (user_id, username, is_admin) VALUES (?, ?, ?)", 
                      (user_id, username, user_id in ADMIN_IDS))
        conn.commit()

        starter_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔥 Чармандер", callback_data="starter_4")],
            [InlineKeyboardButton(text="🌱 Бульбазавр", callback_data="starter_1")],
            [InlineKeyboardButton(text="💧 Сквиртл", callback_data="starter_7")]
        ])
        await message.answer(
            f"🐲 Добро пожаловать в мир Покемонов, {username}!\n"
            "Выбери своего первого покемона:", 
            reply_markup=starter_kb
        )
    else:
        await message.answer(
            f"С возвращением, {username}!", 
            reply_markup=get_main_menu(user_id)
        )

async def starter_pokemon_callback(callback: CallbackQuery):
    pokemon_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    pokemon = next((p for league in POKEMONS.values() for p in league if p['id'] == pokemon_id), None)
    if pokemon:
        cursor.executescript(f"""
            INSERT INTO pokemons (owner_id, pokemon_id, name, image, hp, attack, defense)
            VALUES ({user_id}, {pokemon_id}, '{pokemon['name']}', '{pokemon['image']}', 
                    {pokemon['hp']}, {pokemon['attack']}, {pokemon['defense']});

            INSERT INTO pokemon_counts (user_id, pokemon_id, count) VALUES ({user_id}, {pokemon_id}, 1);

            UPDATE users SET total_pokemons = total_pokemons + 1 WHERE user_id = {user_id};

            INSERT INTO main_pokemon (user_id, pokemon_id) VALUES ({user_id}, {pokemon_id});

            INSERT INTO pokedex (user_id, pokemon_id, seen, caught) 
            VALUES ({user_id}, {pokemon_id}, TRUE, TRUE);
        """)
        conn.commit()

        await callback.message.edit_text(
            f"🎉 Поздравляем! {pokemon['name']} теперь твой первый покемон!"
        )
        await callback.message.answer(
            "Теперь ты можешь начать свое приключение!", 
            reply_markup=get_main_menu(user_id)
        )
    await callback.answer()

async def back_handler(message: Message):
    await message.answer("Главное меню:", reply_markup=get_main_menu(message.from_user.id))