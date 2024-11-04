from flask import render_template, jsonify, request, Blueprint, redirect, url_for, session
from app import db
from app.models import Recipe, User
from sqlalchemy import or_
import jaconv

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', recipes=[], user_id=session['user_id'])
    else:    
        return redirect(url_for('main.login'))

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

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        else:
            return "ユーザー名またはパスワードが間違っています。"
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.login'))

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"Attempting to sign up user: {username}")
        
        if User.query.filter_by(username=username).first() is not None:
            return "そのユーザー名はすでに使用されています。"
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('main.login'))
    
    return render_template('signup.html')

@bp.route('/test_db_connection')
def test_db_connection():
    recipes = Recipe.query.limit(5).all()
    return jsonify([recipe.title for recipe in recipes])
