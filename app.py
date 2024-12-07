from flask import Flask, render_template, request
import os

app = Flask(__name__)

# アップロードされたファイルを保存するディレクトリ
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
app.config['UPLOAD_FOLDER'] = 'static/uploads'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    # フォームからのデータを取得
    ingredients = request.form.get('ingredients')
    cuisine = request.form.get('cuisine')

    # 仮のレシピ応答を生成
    recipe = f"{cuisine}料理のレシピ提案：{ingredients}を使った料理のアイデア。"

    # 結果を含むHTMLを返す
    return render_template('index.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)
