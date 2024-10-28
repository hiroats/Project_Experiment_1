# Project_Experiment_1

## 概要

食材とカテゴリに基づいてレシピを提案する Flask アプリケーション

### 前提条件

- Python 3.7以上がインストールされていること

## セットアップ手順

# 1. リポジトリのクローン
git clone https://github.com/hiroats/Project_Experiment_1.git

# 2. ブランチ変更
git checkout <branch名>

# 2. プロジェクトのディレクトリに移動
cd Project_Experiment_1

# 3. 仮想環境の作成とアクティベート　(オプション(推奨))

# - Windowsの場合
python -m venv venv
venv\Scripts\activate

# - macOS / Linuxの場合
python -m venv venv
source venv/bin/activate

# 4. 必要なパッケージのインストール
pip install -r requirements.txt


# 5. `run.py` をエントリーポイントに指定　(今後変えるかも)

# - Linux / Macの人
export FLASK_APP=run.py

# - Windowsの人
set FLASK_APP=run.py

# 6. アプリケーション起動
flask run

# 7. 仮想環境の終了（オプション）
deactivate
