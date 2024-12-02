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

git checkout <branch名> #ブランチ変更

git pull origin <branch名>　#ブランチの最新情報をローカル環境に反映


# 4. Git LFSのインストール(初回のみ)
Windowsの場合 : Git LFSのインストーラーからダウンロードし、インストール

Linuxの場合 : sudo apt install git-lfs

# - Git LFSの初期化 (初回のみ)
git lfs install  #プロジェクトのディレクトリで行う

git lfs pull　#LFSファイルを明示的にダウンロード(省略可能な場合在り)

# 5. 仮想環境の作成とアクティベート　(省略可)

# - Windowsの場合

python -m venv (任意環境名)

(任意環境名)\Scripts\activate

# - macOS / Linuxの場合

python -m venv (任意環境名)

source (任意環境名)/bin/activate

# 6. 必要なパッケージのインストール

pip install -r requirements.txt


# 7. `run.py` をエントリーポイントに指定　(今後変えるかも)

# - Linux / Macの人

export FLASK_APP=run.py

# - Windowsの人

set FLASK_APP="run.py"

# 8. アプリケーション起動

flask run

# 9. 仮想環境の終了（オプション）

deactivate