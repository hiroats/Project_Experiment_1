import os
import pickle
import re
import MeCab
import torch
import torch.nn as nn
import unidic_lite

# ベースディレクトリを取得（このファイルが存在するディレクトリ）
base_dir = os.path.dirname(os.path.abspath(__file__))

# 辞書パスをプロジェクト内の辞書ディレクトリに設定
mecab_dict_path = unidic_lite.DICDIR

# 保存したベクトライザ、ラベルエンコーダ、モデルの読み込み
with open(os.path.join(base_dir, 'mlp_vectorizer.pkl'), 'rb') as f:
    vectorizer = pickle.load(f)

with open(os.path.join(base_dir, 'mlp_label_encoder.pkl'), 'rb') as f:
    label_encoder = pickle.load(f)

# MLPモデルの定義（学習時と同じクラス定義が必要）
class MLPModel(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim, dropout_rate=0.6):
        super(MLPModel, self).__init__()
        layers = []
        prev_dim = input_dim
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))  # バッチ正規化を追加
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            prev_dim = hidden_dim
        layers.append(nn.Linear(prev_dim, output_dim))
        self.net = nn.Sequential(*layers)
        
    def forward(self, x):
        return self.net(x)

# デバイスの設定
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# モデルの初期化
input_dim = vectorizer.max_features  # またはX_train.shape[1]と同じ次元数
hidden_dims = [256, 128, 64]
num_classes = len(label_encoder.classes_)
model = MLPModel(input_dim, hidden_dims, num_classes, dropout_rate=0.6).to(device)

# モデルの重みをロード
model_path = os.path.join(base_dir, 'best_mlp_model.pth')
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

# MeCabの辞書パスを指定（学習時と同じ辞書を使用）
mecab = MeCab.Tagger(f"-d {mecab_dict_path}")  # プロジェクト内の辞書パスを使用

# 正規表現パターンを事前にコンパイル（学習時と同じパターンを使用）
pattern = re.compile(r'\(.*?\)|[◎☆※・;]|^[A-Za-z]$|[^ぁ-んァ-ンー一-龥]+')

def clean_ingredients(text):
    # 不要な文字やパターンを除去
    text = pattern.sub(' ', text)
    # 連続する空白を一つの空白に置換
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_ingredients(ingredients_input):
    # 入力された材料を前処理
    cleaned_ingredients = clean_ingredients(ingredients_input)
    
    # ストップワードと抽出する品詞（学習時と同じ設定）
    stop_words = set(['の', 'と', 'に', 'を', 'は', 'が', 'で', 'て', 'から', 'まで', 'です', 'ます', 'する', 'いる', 'ある'])
    desired_pos = {'名詞', '動詞'}
    
    words = []
    node = mecab.parseToNode(cleaned_ingredients)
    while node:
        surface = node.surface
        features = node.feature.split(',')
        # 品詞を取得
        if len(features) >= 1:
            pos = features[0]
        else:
            pos = ''
        # 基本形ではなく表層形を使用
        base_form = surface
        # 不要なトークンを除外
        if pos in desired_pos and base_form not in stop_words and base_form != '*':
            # 一文字のアルファベットを除外
            if not re.match(r'^[A-Za-z]$', base_form):
                words.append(base_form)
        node = node.next
    
    processed_ingredients = ' '.join(words)
    return processed_ingredients


def recommend_category(ingredients_input):
    # 前処理
    processed_input = preprocess_ingredients(ingredients_input)
    # ベクトル化
    X_input = vectorizer.transform([processed_input])
    # テンソルに変換
    X_input_tensor = torch.tensor(X_input.toarray(), dtype=torch.float32).to(device)
    # モデルで予測
    with torch.no_grad():
        outputs = model(X_input_tensor)
        probabilities = torch.softmax(outputs, dim=1).cpu().numpy()[0]

    # カテゴリ名の取得
    categories = label_encoder.classes_

    # カテゴリと確率を対応付け
    category_probabilities = dict(zip(categories, probabilities))

    if not category_probabilities:
        return None

    # 確率の高い順にソート
    sorted_categories = sorted(category_probabilities.items(), key=lambda x: x[1], reverse=True)

    # 最終的な予測結果
    result = {category: prob * 100 for category, prob in sorted_categories}
    return result


if __name__ == '__main__':
    try:
        # コマンドラインから材料の入力を受け付ける
        ingredients_input = input("材料を入力してください: ")
        recommend_category(ingredients_input)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
