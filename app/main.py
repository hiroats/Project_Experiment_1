from flask import render_template, jsonify, request
from . import app, db
import os
from sqlalchemy import or_

# Recipes モデルの定義
class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text)
    title = db.Column(db.Text)
    recipe_url = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    image_url = db.Column(db.Text)

# データベースの初期化
def initialize_database():
    db_path = os.path.join(os.path.dirname(__file__), 'sample.db')
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
        print("データベースが初期化されました")

# モデル定義の後で初期化関数を呼び出す
initialize_database()

@app.route('/')
def index():
    # 最初のページ表示時には空のリストを渡す
    return render_template('index.html', recipes=[])

@app.route('/get_recipe', methods=['POST'])
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
@app.route('/recipes', methods=['GET'])
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

@app.route('/test_db_connection')
def test_db_connection():
    recipes = Recipe.query.limit(5).all()
    return jsonify([recipe.title for recipe in recipes])

# アプリケーションの起動
if __name__ == '__main__':
    app.run()
