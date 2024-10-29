# Project_Experiment_1

## 概要

食材とカテゴリに基づいてレシピを提案する Flask アプリケーション

### 前提条件

- Python 3.7以上がインストールされていること

## セットアップ手順

# 1. リポジトリのクローン (初回のみ)

git clone https://github.com/hiroats/Project_Experiment_1.git

# 2. プロジェクトのディレクトリに移動

cd Project_Experiment_1

# 3. ブランチ変更
git fetch origin <branch名>  #ブランチを最新情報に更新

git checkout <branch名>

# 4. 仮想環境の作成とアクティベート　(省略可)

# - Windowsの場合

python -m venv (任意環境名)

(任意環境名)\Scripts\activate

# - macOS / Linuxの場合

python -m venv (任意環境名)

source (任意環境名)/bin/activate

# 4. 必要なパッケージのインストール

pip install -r requirements.txt


# 5. `run.py` をエントリーポイントに指定　(今後変えるかも)

# - Linux / Macの人

export FLASK_APP=run.py

# - Windowsの人

set FLASK_APP="run.py"

# 6. アプリケーション起動

flask run

# 7. 仮想環境の終了（オプション）

deactivate
