import sqlite3
import json
from contextlib import contextmanager
from datetime import datetime

DATABASE_NAME = 'recipes.db'

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create recipes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                prep_time TEXT,
                cook_time TEXT,
                servings TEXT,
                source_url TEXT,
                image_url TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create full-text search virtual table
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS recipes_fts USING fts5(
                name,
                description,
                ingredients,
                instructions,
                tags,
                content=recipes,
                content_rowid=id
            )
        ''')
        
        # Create triggers to keep FTS index in sync
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS recipes_ai AFTER INSERT ON recipes BEGIN
                INSERT INTO recipes_fts(rowid, name, description, ingredients, instructions, tags)
                VALUES (new.id, new.name, new.description, new.ingredients, new.instructions, new.tags);
            END
        ''')
        
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS recipes_ad AFTER DELETE ON recipes BEGIN
                DELETE FROM recipes_fts WHERE rowid = old.id;
            END
        ''')
        
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS recipes_au AFTER UPDATE ON recipes BEGIN
                UPDATE recipes_fts SET 
                    name = new.name,
                    description = new.description,
                    ingredients = new.ingredients,
                    instructions = new.instructions,
                    tags = new.tags
                WHERE rowid = new.id;
            END
        ''')
        
        conn.commit()

def create_recipe(name, description, ingredients, instructions, prep_time=None, 
                 cook_time=None, servings=None, source_url=None, image_url=None, tags=None):
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Convert lists to JSON strings if needed
        if isinstance(ingredients, list):
            ingredients = json.dumps(ingredients)
        if isinstance(instructions, list):
            instructions = json.dumps(instructions)
        if isinstance(tags, list):
            tags = json.dumps(tags)
            
        cursor.execute('''
            INSERT INTO recipes (name, description, ingredients, instructions, prep_time, 
                               cook_time, servings, source_url, image_url, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, ingredients, instructions, prep_time, cook_time, 
              servings, source_url, image_url, tags))
        
        return cursor.lastrowid

def get_recipe(recipe_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_recipes():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM recipes ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]

def update_recipe(recipe_id, name=None, description=None, ingredients=None, 
                 instructions=None, prep_time=None, cook_time=None, servings=None,
                 source_url=None, image_url=None, tags=None):
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Get current recipe
        cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
        current = cursor.fetchone()
        if not current:
            return False
        
        # Convert lists to JSON strings if needed
        if isinstance(ingredients, list):
            ingredients = json.dumps(ingredients)
        if isinstance(instructions, list):
            instructions = json.dumps(instructions)
        if isinstance(tags, list):
            tags = json.dumps(tags)
        
        # Update only provided fields
        updates = {}
        if name is not None:
            updates['name'] = name
        if description is not None:
            updates['description'] = description
        if ingredients is not None:
            updates['ingredients'] = ingredients
        if instructions is not None:
            updates['instructions'] = instructions
        if prep_time is not None:
            updates['prep_time'] = prep_time
        if cook_time is not None:
            updates['cook_time'] = cook_time
        if servings is not None:
            updates['servings'] = servings
        if source_url is not None:
            updates['source_url'] = source_url
        if image_url is not None:
            updates['image_url'] = image_url
        if tags is not None:
            updates['tags'] = tags
        
        updates['updated_at'] = datetime.now().isoformat()
        
        set_clause = ', '.join([f'{k} = ?' for k in updates.keys()])
        values = list(updates.values()) + [recipe_id]
        
        cursor.execute(f'UPDATE recipes SET {set_clause} WHERE id = ?', values)
        return True

def delete_recipe(recipe_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        return cursor.rowcount > 0

def search_recipes(query):
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Use FTS5 for full-text search
        cursor.execute('''
            SELECT recipes.* FROM recipes
            JOIN recipes_fts ON recipes.id = recipes_fts.rowid
            WHERE recipes_fts MATCH ?
            ORDER BY rank
        ''', (query,))
        
        return [dict(row) for row in cursor.fetchall()]
