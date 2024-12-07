from flask import render_template, jsonify, request, Blueprint, redirect, url_for, session
from app import db
from app.models import AddRecipe, Recipe, User
from app.ml.mlp_dep import recommend_category
from sqlalchemy import or_
import jaconv
from werkzeug.utils import secure_filename
import os
from flask import current_app

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', recipes=[], user_id=session['user_id'])
    else:    
        return redirect(url_for('main.login'))

@bp.route('/get_recipe', methods=['POST'])
def get_recipe():
    ingredients_input = request.form.get('ingredients', '')
    category = request.form.get('category', 'all')

    # 食材をひらがなに変換
    ingredients = jaconv.kata2hira(ingredients_input)

    # Recipe からデータを取得
    query_recipe = Recipe.query
    if ingredients:
        ingredient_filters_recipe = [Recipe.ingredients_hiragana.contains(ingredient) for ingredient in ingredients.split()]
        query_recipe = query_recipe.filter(or_(*ingredient_filters_recipe))
    if category and category.lower() != "all":
        query_recipe = query_recipe.filter(Recipe.category == category.lower())
    recipes = query_recipe.all()

    # AddRecipe からデータを取得
    query_addrecipe = AddRecipe.query
    if ingredients:
        ingredient_filters_addrecipe = [AddRecipe.ingredients_hiragana.contains(ingredient) for ingredient in ingredients.split()]
        query_addrecipe = query_addrecipe.filter(or_(*ingredient_filters_addrecipe))
    if category and category.lower() != "all":
        query_addrecipe = query_addrecipe.filter(AddRecipe.category == category.lower())
    add_recipes = query_addrecipe.all()

    # 結果をリストにまとめ、データの種類をフラグで追加
    combined_recipes = [
        {"type": "addrecipe", "data": add_recipe} for add_recipe in add_recipes
    ] + [
        {"type": "recipe", "data": recipe} for recipe in recipes
    ]

    return render_template(
        'index.html',
        recipes=combined_recipes[:10],  # 表示件数を制限
        ingredients=ingredients_input,
        category=category
    )



@bp.route('/get_addRecipe', methods=['POST'])
def get_addRecipe():
    ingredients_input = request.form.get('ingredients', '')
    category = request.form.get('category', 'all')
    ingredients = jaconv.kata2hira(ingredients_input)
    query = AddRecipe.query
    if ingredients:
        ingredient_filters = [AddRecipe.ingredients_hiragana.contains(ingredient) for ingredient in ingredients.split()]
        query = query.filter(or_(*ingredient_filters))
    if category and category.lower() != "all":
        query = query.filter(AddRecipe.category == category.lower())
    recipes = query.all()
    return render_template('index.html', recipes=recipes[:5], ingredients=ingredients_input, category=category)

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

@bp.route('/addRecipes', methods=['GET'])
def get_addRecipes():
    recipes = AddRecipe.query.all()
    recipes_list = [
        {
            "id": recipe.id,
            "title": recipe.title,
            "category": recipe.category,
            "ingredients": recipe.ingredients,
            "procedure": recipe.procedure,
            "image": recipe.image,
            "created_by": recipe.created_by,
            "is_public": recipe.created_by
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

@bp.route('/upload')
def upload():
    return render_template('upload.html')

@bp.route('/upload-recipe', methods=['POST'])
def upload_recipe():
    title = request.form['title']
    category = request.form['category']
    ingredients = request.form['ingredients']
    ingredients_hiragana = jaconv.kata2hira(ingredients)
    recipe = request.form['recipe']
    image_file = request.files['image']
    created_by = session.get('user_id', '匿名ユーザー')
    is_public = request.form.get('is_public', 'true')
    
    if image_file and image_file.filename:
        # ファイル名を安全にする
        filename = secure_filename(image_file.filename)
        # 保存先のパスを定義（UPLOAD_FOLDERはアプリの設定で指定）
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        print(f"Saving file to: {save_path}")
        # ファイルを保存
        image_file.save(save_path)

        # 画像のパスをデータベースに保存する
        image_path = os.path.join('uploads', filename)  # 'uploads'はアプリの静的ファイルとして設定されているディレクトリ
        image_path = image_path.replace('\\', '/')
    else:
        image_path = None
        
    new_recipe = AddRecipe(
        title=title,
        category=category.lower(),
        ingredients=ingredients,
        ingredients_hiragana=ingredients_hiragana,
        recipe=recipe,
        image=image_path,  # データベースに画像のパスを保存
        created_by=created_by,
        is_public=is_public
    )
    
    db.session.add(new_recipe)
    db.session.commit()
    return redirect(url_for('main.index'))


@bp.route('/predict_category', methods=['POST'])
def predict_category():
    data = request.get_json()
    ingredients_input = data.get('ingredients', '')
    if not ingredients_input:
        return jsonify({"error": "食材が入力されていません"}), 400
    category_predictions = recommend_category(ingredients_input)
    print("category_predictions:", category_predictions)
    if category_predictions is None:
        return jsonify({"error": "予測結果が無効です"}), 400
    category_translation = {
        'chinese': '中華',
        'ethnic': 'エスニック（中南米料理）',
        'french': 'フランス料理',
        'italian': 'イタリアン',
        'japanese': '日本食',
        'korean': '韓国料理'
    }
    category_predictions = {
        category_translation.get(str(key), str(key)): round(float(value), 2) 
        for key, value in category_predictions.items()
    }
    return jsonify(category_predictions)
