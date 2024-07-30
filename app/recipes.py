from flask import Blueprint, render_template, request
import requests

recipes = Blueprint('recipes', __name__)
API_KEY = 'your_spoonacular_api_key'

@recipes.route('/recipes')
def recipe_search():
    query = request.args.get('query')
    if query:
        response = requests.get(f'https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={API_KEY}')
        data = response.json()
        return render_template('recipes.html', recipes=data['results'])
    return render_template('recipes.html', recipes=[])

@recipes.route('/recipes/<int:recipe_id>')
def recipe_detail(recipe_id):
    response = requests.get(f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}')
    recipe = response.json()
    return render_template('recipe_detail.html', recipe=recipe)
