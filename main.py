import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import TOKEN
from database import init_db
from handlers import commands, admin, battle, catching, pokedex, pokemons, shop
from keep_alive import keep_alive

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# Инициализация базы данных
init_db()

# Регистрация обработчиков
dp.include_router(commands.router)
dp.include_router(admin.router)
dp.include_router(battle.router)
dp.include_router(catching.router)
dp.include_router(pokedex.router)
dp.include_router(pokemons.router)
dp.include_router(shop.router)

async def main():
    keep_alive()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())