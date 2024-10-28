# Project_Experiment_1

## 概要

食材とカテゴリに基づいてレシピを提案する Flask アプリケーション

### 前提条件

- Python 3.7以上がインストールされていること

## セットアップ手順

# 1. リポジトリのクローン
git clone https://github.com/hiroats/Project_Experiment_1.git

# 2. プロジェクトのディレクトリに移動
cd Project_Experiment_1

# 3. 仮想環境の作成とアクティベート

# - Windowsの場合
python -m venv venv
venv\Scripts\activate

# - macOS / Linuxの場合
python3 -m venv venv
source venv/bin/activate

# 4. 必要なパッケージのインストール
pip install -r requirements.txt

# 5. flask のディレクトリに移動
cd app

# 6. `main.py` をエントリーポイントに指定　(今後変えるかも)

# - Linux / Macの人
export FLASK_APP=main.py

# - Windowsの人
set FLASK_APP=main.py

# 7. アプリケーション起動
flask run

# 8. 仮想環境の終了（オプション）
deactivate
