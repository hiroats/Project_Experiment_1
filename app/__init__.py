from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ベースディレクトリの取得
basedir = os.path.abspath(os.path.dirname(__file__))

# データベースのパスを設定（プロジェクトディレクトリ内の sample.db を使用）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sample.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from . import main
