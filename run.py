from app import create_app, db
from app.models import Recipe

app = create_app()

# データベースの初期化
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
