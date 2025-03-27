import sqlite3
from config import POKEMONS

conn = sqlite3.connect('pokemon.db', check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 3000,
        pokeballs INTEGER DEFAULT 5,
        total_pokemons INTEGER DEFAULT 0,
        is_admin BOOLEAN DEFAULT FALSE,
        trainer_id INTEGER DEFAULT NULL,
        trainer_level INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS pokemons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER,
        pokemon_id INTEGER,
        name TEXT,
        image TEXT,
        hp INTEGER,
        attack INTEGER,
        defense INTEGER,
        is_custom BOOLEAN DEFAULT FALSE,
        FOREIGN KEY(owner_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS pokemon_counts (
        user_id INTEGER,
        pokemon_id INTEGER,
        count INTEGER DEFAULT 0,
        PRIMARY KEY (user_id, pokemon_id)
    );

    CREATE TABLE IF NOT EXISTS custom_pokemons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        image TEXT,
        hp INTEGER,
        attack INTEGER,
        defense INTEGER
    );

    CREATE TABLE IF NOT EXISTS trainers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        income INTEGER,
        image TEXT
    );

    CREATE TABLE IF NOT EXISTS pokedex (
        user_id INTEGER,
        pokemon_id INTEGER,
        seen BOOLEAN DEFAULT FALSE,
        caught BOOLEAN DEFAULT FALSE,
        PRIMARY KEY (user_id, pokemon_id)
    );

    CREATE TABLE IF NOT EXISTS main_pokemon (
        user_id INTEGER PRIMARY KEY,
        pokemon_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    ''')

    # Заполняем тренеров
    if not cursor.execute("SELECT COUNT(*) FROM trainers").fetchone()[0]:
        cursor.executemany(
            "INSERT INTO trainers VALUES (?, ?, ?, ?, ?)",
            [
                (1, "Брок", 10000, 100, "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/trainer/1.png"),
                (2, "Мсти", 25000, 250, "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/trainer/2.png"),
                (3, "Эш", 50000, 500, "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/trainer/3.png")
            ]
        )
        conn.commit()