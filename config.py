import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # データベースのパスを設定（プロジェクトディレクトリ内の sample.db を使用）
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sample.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False