from flask import Flask, request, jsonify, send_from_directory
import os
import json
from dotenv import load_dotenv
import database
import recipe_parser

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')

# Initialize database
database.init_db()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/styles.css')
def serve_css():
    """Serve CSS file"""
    return send_from_directory('static', 'styles.css')

@app.route('/app.js')
def serve_js():
    """Serve JavaScript file"""
    return send_from_directory('static', 'app.js')

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes"""
    try:
        recipes = database.get_all_recipes()
        
        # Parse JSON fields
        for recipe in recipes:
            if recipe.get('ingredients') and isinstance(recipe['ingredients'], str):
                try:
                    recipe['ingredients'] = json.loads(recipe['ingredients'])
                except:
                    recipe['ingredients'] = [recipe['ingredients']]
            
            if recipe.get('instructions') and isinstance(recipe['instructions'], str):
                try:
                    recipe['instructions'] = json.loads(recipe['instructions'])
                except:
                    recipe['instructions'] = [recipe['instructions']]
            
            if recipe.get('tags') and isinstance(recipe['tags'], str):
                try:
                    recipe['tags'] = json.loads(recipe['tags'])
                except:
                    recipe['tags'] = []
        
        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """Get a specific recipe"""
    try:
        recipe = database.get_recipe(recipe_id)
        
        if not recipe:
            return jsonify({'error': 'Recipe not found'}), 404
        
        # Parse JSON fields
        if recipe.get('ingredients') and isinstance(recipe['ingredients'], str):
            try:
                recipe['ingredients'] = json.loads(recipe['ingredients'])
            except:
                recipe['ingredients'] = [recipe['ingredients']]
        
        if recipe.get('instructions') and isinstance(recipe['instructions'], str):
            try:
                recipe['instructions'] = json.loads(recipe['instructions'])
            except:
                recipe['instructions'] = [recipe['instructions']]
        
        if recipe.get('tags') and isinstance(recipe['tags'], str):
            try:
                recipe['tags'] = json.loads(recipe['tags'])
            except:
                recipe['tags'] = []
        
        return jsonify(recipe), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    """Create a new recipe"""
    try:
        data = request.json
        
        if not data.get('name') or not data.get('ingredients') or not data.get('instructions'):
            return jsonify({'error': 'Name, ingredients, and instructions are required'}), 400
        
        recipe_id = database.create_recipe(
            name=data['name'],
            description=data.get('description', ''),
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            prep_time=data.get('prep_time'),
            cook_time=data.get('cook_time'),
            servings=data.get('servings'),
            source_url=data.get('source_url'),
            image_url=data.get('image_url'),
            tags=data.get('tags', [])
        )
        
        return jsonify({'id': recipe_id, 'message': 'Recipe created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    """Update an existing recipe"""
    try:
        data = request.json
        
        success = database.update_recipe(
            recipe_id=recipe_id,
            name=data.get('name'),
            description=data.get('description'),
            ingredients=data.get('ingredients'),
            instructions=data.get('instructions'),
            prep_time=data.get('prep_time'),
            cook_time=data.get('cook_time'),
            servings=data.get('servings'),
            source_url=data.get('source_url'),
            image_url=data.get('image_url'),
            tags=data.get('tags')
        )
        
        if not success:
            return jsonify({'error': 'Recipe not found'}), 404
        
        return jsonify({'message': 'Recipe updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """Delete a recipe"""
    try:
        success = database.delete_recipe(recipe_id)
        
        if not success:
            return jsonify({'error': 'Recipe not found'}), 404
        
        return jsonify({'message': 'Recipe deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_recipes():
    """Search recipes by ingredients, name, description"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify([]), 200
        
        recipes = database.search_recipes(query)
        
        # Parse JSON fields
        for recipe in recipes:
            if recipe.get('ingredients') and isinstance(recipe['ingredients'], str):
                try:
                    recipe['ingredients'] = json.loads(recipe['ingredients'])
                except:
                    recipe['ingredients'] = [recipe['ingredients']]
            
            if recipe.get('instructions') and isinstance(recipe['instructions'], str):
                try:
                    recipe['instructions'] = json.loads(recipe['instructions'])
                except:
                    recipe['instructions'] = [recipe['instructions']]
            
            if recipe.get('tags') and isinstance(recipe['tags'], str):
                try:
                    recipe['tags'] = json.loads(recipe['tags'])
                except:
                    recipe['tags'] = []
        
        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/parse-url', methods=['POST'])
def parse_url():
    """Parse recipe from URL using Claude AI"""
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        recipe_data = recipe_parser.parse_recipe_with_claude(url)
        
        return jsonify(recipe_data), 200
    except Exception as e:
        app.logger.error(f"Error parsing URL: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'routes': [str(rule) for rule in app.url_map.iter_rules()],
        'anthropic_key_present': bool(os.getenv('ANTHROPIC_API_KEY'))
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
