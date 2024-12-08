from app import db

# Recipeモデルの定義
class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text)
    title = db.Column(db.Text)
    recipe_url = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    ingredients_hiragana = db.Column(db.Text) 
    image_url = db.Column(db.Text)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class AddRecipe(db.Model):
    __tablename__ = 'addRecipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    category = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    ingredients_hiragana = db.Column(db.Text)
    recipe = db.Column(db.Text) # 手順
    image = db.Column(db.Text)
    created_by = db.Column(db.Text)
    is_public = db.Column(db.Text)