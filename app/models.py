from app import db

# Recipeモデルの定義
class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text)
    title = db.Column(db.Text)
    recipe_url = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    image_url = db.Column(db.Text)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)