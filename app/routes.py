from flask import render_template, jsonify, request, Blueprint, redirect, url_for, session
from app import db
from app.models import AddRecipe, Recipe, User
from app.ml.mlp_dep import recommend_category
from sqlalchemy import or_
import jaconv
from werkzeug.utils import secure_filename
import os
from flask import current_app
import MeCab

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

    # Recipeテーブル検索(AND検索)
    query_recipe = Recipe.query
    if ingredients:
        for ingredient in ingredients.split():
            query_recipe = query_recipe.filter(Recipe.ingredients_hiragana.contains(ingredient))
    if category and category.lower() != "all":
        query_recipe = query_recipe.filter(Recipe.category == category.lower())
    recipes = query_recipe.limit(10).all()

    # AddRecipeテーブル検索(AND検索)
    query_addrecipe = AddRecipe.query
    if ingredients:
        for ingredient in ingredients.split():
            query_addrecipe = query_addrecipe.filter(AddRecipe.ingredients_hiragana.contains(ingredient))
    if category and category.lower() != "all":
        query_addrecipe = query_addrecipe.filter(AddRecipe.category == category.lower())
    add_recipes = query_addrecipe.limit(10).all()

    combined = [
        {"type": "addrecipe", "data": r} for r in add_recipes
    ] + [
        {"type": "recipe", "data": r} for r in recipes
    ]

    # 検索結果が3件未満の場合、MeCabで名詞を抽出し、段階的採用ロジック実行
    if len(combined) < 3 and ingredients:
        
        tagger = MeCab.Tagger()
        node = tagger.parseToNode(ingredients)
        nouns = []
        while node:
            features = node.feature.split(',')
            # features[0]が品詞、'名詞'かどうかをチェック
            if features[0] == '名詞':
                nouns.append(node.surface)
            node = node.next

        if nouns:
            # nounsのOR検索をRecipeとAddRecipe双方で行う
            or_conditions_recipe = [Recipe.ingredients_hiragana.contains(n) for n in nouns]
            or_conditions_addrecipe = [AddRecipe.ingredients_hiragana.contains(n) for n in nouns]

            or_query_recipe = Recipe.query.filter(or_(*or_conditions_recipe))
            or_query_addrecipe = AddRecipe.query.filter(or_(*or_conditions_addrecipe))

            if category and category.lower() != "all":
                or_query_recipe = or_query_recipe.filter(Recipe.category == category.lower())
                or_query_addrecipe = or_query_addrecipe.filter(AddRecipe.category == category.lower())

            candidate_recipes = or_query_recipe.all()
            candidate_addrecipes = or_query_addrecipe.all()

            # レシピごとにnouns中何単語一致するかカウント
            ranked_results = []
            for r in candidate_recipes:
                count = sum(n in r.ingredients_hiragana for n in nouns)
                ranked_results.append((count, "recipe", r))
            for r in candidate_addrecipes:
                count = sum(n in r.ingredients_hiragana for n in nouns)
                ranked_results.append((count, "addrecipe", r))

            # 一致数で降順ソート
            ranked_results.sort(key=lambda x: x[0], reverse=True)

            # 全部一致から順に採用
            # 段階的に落としていくロジック
            def filter_by_match_count(results, nouns_count):
                # nouns_countから0まで減らしながら、3件以上になったら返す
                filtered = []
                for c in range(nouns_count, 0, -1):
                    matched = [r for (co, t, r) in results if co == c]
                    filtered += matched
                    if len(filtered) >= 3:
                        return filtered
                # 最後は1以上一致するもの全部
                if not filtered:
                    filtered = [r for (co, t, r) in results if co > 0]
                return filtered

            chosen = filter_by_match_count(ranked_results, len(nouns))


            # chosenにはtypeないので元のresultsから照合
            final_combined = []
            for r in chosen[:5]:  # 5件まで表示
                # typeを取得するためにranked_resultsを再度見る
                for (co, t, rec) in ranked_results:
                    if rec == r:
                        final_combined.append({"type": t, "data": r})
                        break

            combined = final_combined

    return render_template('index.html', recipes=combined, ingredients=ingredients_input, category=category)


@bp.route('/get_addRecipe', methods=['POST'])
def get_addRecipe():
    ingredients_input = request.form.get('ingredients', '')
    category = request.form.get('category', 'all')
    ingredients = jaconv.kata2hira(ingredients_input)

    query = AddRecipe.query
    if ingredients:
        for ingredient in ingredients.split():
            query = query.filter(AddRecipe.ingredients_hiragana.contains(ingredient))

    if category and category.lower() != "all":
        query = query.filter(AddRecipe.category == category.lower())
    recipes = query.all()

    # レシピが3件未満ならMeCabで名詞抽出して段階的採用ロジック
    if len(recipes) < 3 and ingredients:
        
        tagger = MeCab.Tagger()
        node = tagger.parseToNode(ingredients)
        nouns = []
        while node:
            features = node.feature.split(',')
            # features[0]が品詞、'名詞'かどうかをチェック
            if features[0] == '名詞':
                nouns.append(node.surface)
            node = node.next

        if nouns:
            # nounsでOR検索
            or_conditions = [Recipe.ingredients_hiragana.contains(n) for n in nouns]
            or_query = Recipe.query.filter(or_(*or_conditions))
            if category and category.lower() != "all":
                or_query = or_query.filter(Recipe.category == category.lower())
            candidate_recipes = or_query.all()

            # 一致数カウント
            ranked_results = []
            for r in candidate_recipes:
                count = sum(n in r.ingredients_hiragana for n in nouns)
                ranked_results.append((count, r))

            ranked_results.sort(key=lambda x: x[0], reverse=True)

            # 全部一致→(N-1)一致…と段階的にフィルタ
            def filter_by_match_count(results, nouns_count):
                filtered = []
                for c in range(nouns_count, 0, -1):
                    matched = [r for (co, r) in results if co == c]
                    filtered += matched
                    if len(filtered) >= 3:
                        return filtered
                if not filtered:
                    filtered = [r for (co, r) in results if co > 0]
                return filtered

            chosen = filter_by_match_count(ranked_results, len(nouns))
            recipes = chosen[:5]

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
