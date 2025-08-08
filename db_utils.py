import sqlite3
import os

DB_FILENAME = "Recipe_keeper.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_FILENAME)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_database():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
    ID            INTEGER PRIMARY KEY AUTOINCREMENT,
    RecipeName    TEXT    NOT NULL,
    Ingredients   TEXT    NOT NULL,
    Instructions  TEXT    NOT NULL,
    visible       INTEGER DEFAULT 1,
    deleted       INTEGER DEFAULT 0
);
    """)
    # On first run, file won’t exist
    new_db = not os.path.exists(DB_PATH)
    conn = get_connection()
    cursor = conn.cursor()

    

    # If you need initial seed data, do it here when new_db=True
    if new_db:
        # e.g. cursor.execute("INSERT INTO recipes(name) VALUES(?)", ("Example",))
        pass

    conn.commit()
    cursor.close()
    conn.close()

def soft_delete_recipe(recipe_id: int):
    """
    Mark a recipe as deleted instead of hard-deleting.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE recipes SET deleted = 1 WHERE id = ?",
        (recipe_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
