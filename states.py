from aiogram.fsm.state import State, StatesGroup

class CreatePokemonState(StatesGroup):
    name = State()
    image = State()
    hp = State()
    attack = State()
    defense = State()

class ChangeBalanceState(StatesGroup):
    user_id = State()
    amount = State()

class GivePokemonState(StatesGroup):
    user_id = State()

class PokedexState(StatesGroup):
    search = State()