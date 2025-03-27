import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_IDS = [5953677116]

with open('pokemons.json', 'r') as f:
    POKEMONS = json.load(f)