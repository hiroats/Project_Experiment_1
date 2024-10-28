from flask import render_template, jsonify, request, Blueprint
from app import db
from app.models import Recipe
from sqlalchemy import or_

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # 最初のページ表示時には空のリストを渡す
    return render_template('index.html', recipes=[])

@bp.route('/get_recipe', methods=['POST'])
def get_recipe():
    ingredients = request.form.get('ingredients', '')
    category = request.form.get('category', 'all')

    # クエリのフィルタリング: 類似食材とカテゴリ一致
    query = Recipe.query
    if ingredients:
        ingredient_filters = [Recipe.ingredients.contains(ingredient) for ingredient in ingredients.split()]
        query = query.filter(or_(*ingredient_filters))

    # カテゴリが「全て」以外の場合のみカテゴリフィルタを適用
    if category and category.lower() != "all":
        query = query.filter(Recipe.category == category.lower())

    recipes = query.all()
    return render_template('index.html', recipes=recipes, ingredients=ingredients, category=category)

# レシピ一覧を取得するエンドポイント
@bp.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    recipes_list = [
        {
            "id": recipe.id,
            "category": recipe.category,
            "title": recipe.title,
            "recipe_url": recipe.recipe_url,
            "ingredients": recipe.ingredients,
            "image_url": recipe.image_url
        }
        for recipe in recipes
    ]
    return jsonify(recipes_list)

@bp.route('/test_db_connection')
def test_db_connection():
    recipes = Recipe.query.limit(5).all()
    return jsonify([recipe.title for recipe in recipes])
